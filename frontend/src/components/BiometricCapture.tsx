import React, { useState, useRef, useCallback, useEffect } from 'react';
import {
  Box,
  Button,
  Typography,
  Paper,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Chip,
  Grid,
  useTheme,
  useMediaQuery,
  Card,
  CardContent,
  CardActions,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  CameraAlt,
  Fingerprint,
  Face,
  Security,
  Close,
  CheckCircle,
  Error,
  Info,
  Upload,
  PhotoCamera,
  Smartphone,
  Laptop,
  Warning,
  TouchApp,
  PhoneAndroid,
} from '@mui/icons-material';


interface BiometricCaptureProps {
  type: 'fingerprint' | 'face' | 'palmprint';
  onCapture: (data: string) => void;
  onCancel: () => void;
}

interface BiometricDevice {
  type: 'webauthn' | 'camera' | 'native' | 'upload';
  name: string;
  available: boolean;
}

const BiometricCapture: React.FC<BiometricCaptureProps> = ({ type, onCapture, onCancel }) => {
  const [capturing, setCapturing] = useState(false);
  const [error, setError] = useState('');
  const [devices, setDevices] = useState<BiometricDevice[]>([]);
  const [selectedDevice, setSelectedDevice] = useState<BiometricDevice | null>(null);
  const [showDeviceDialog, setShowDeviceDialog] = useState(false);
  const [showNativePrompt, setShowNativePrompt] = useState(false);
  const [showUploadDialog, setShowUploadDialog] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadPreview, setUploadPreview] = useState<string>('');
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const detectAvailableDevices = useCallback(async () => {
    const detectedDevices: BiometricDevice[] = [];

    // Check for WebAuthn support (laptop/desktop fingerprint sensors)
    if (type === 'fingerprint' && window.PublicKeyCredential) {
      try {
        const available = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
        if (available) {
          const userAgent = navigator.userAgent.toLowerCase();
          
          // Detect specific laptop/desktop biometric systems
          let deviceName = 'Platform Authenticator';
          if (userAgent.includes('windows')) {
            deviceName = 'Windows Hello Fingerprint';
          } else if (userAgent.includes('mac')) {
            deviceName = 'MacBook Touch ID';
          } else if (userAgent.includes('linux')) {
            deviceName = 'Linux Fingerprint Reader';
          } else if (isMobile) {
            deviceName = 'Mobile Fingerprint Sensor';
          }
          
          detectedDevices.push({
            type: 'webauthn',
            name: deviceName,
            available: true
          });
        }
      } catch (err) {
        console.log('WebAuthn not available:', err);
      }
    }

    // Check for additional credential management API support
    if (type === 'fingerprint' && 'credentials' in navigator) {
      try {
        // Check if Credential Management API is available (enhanced laptop support)
        const credentialSupport = await navigator.credentials.create({
          publicKey: {
            challenge: new Uint8Array(32),
            rp: { name: "Test", id: window.location.hostname },
            user: { id: new Uint8Array(16), name: "test", displayName: "Test" },
            pubKeyCredParams: [{ alg: -7, type: "public-key" }],
            authenticatorSelection: {
              authenticatorAttachment: "platform",
              userVerification: "required"
            },
            timeout: 5000,
            attestation: "none"
          }
        }).then(() => true).catch(() => false);

        if (credentialSupport && !detectedDevices.some(d => d.type === 'webauthn')) {
          detectedDevices.push({
            type: 'webauthn',
            name: 'Laptop Biometric Sensor',
            available: true
          });
        }
      } catch (err) {
        console.log('Credential Management API check failed:', err);
      }
    }

    // Check for camera access (face/palmprint)
    if (type === 'face' || type === 'palmprint') {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        stream.getTracks().forEach(track => track.stop());
        detectedDevices.push({
          type: 'camera',
          name: 'Camera',
          available: true
        });
      } catch (err) {
        console.log('Camera not available:', err);
      }
    }

    // Check for native mobile integration (fallback)
    if (isMobile && 'navigator' in window && 'credentials' in navigator) {
      if (!detectedDevices.some(d => d.type === 'webauthn')) {
        detectedDevices.push({
          type: 'native',
          name: 'Native Mobile Biometrics',
          available: true
        });
      }
    }

    // Add image upload as a fallback option for fingerprint
    if (type === 'fingerprint') {
      detectedDevices.push({
        type: 'upload',
        name: 'Upload Fingerprint Image',
        available: true
      });
    }

    setDevices(detectedDevices);

    // Auto-select the best available device (prioritize laptop sensors for fingerprint)
    if (detectedDevices.length > 0) {
      // Prefer WebAuthn for any fingerprint sensor (laptop or mobile)
      const webauthnDevice = detectedDevices.find(d => d.type === 'webauthn');
      const nativeDevice = detectedDevices.find(d => d.type === 'native');
      const cameraDevice = detectedDevices.find(d => d.type === 'camera');

      if (type === 'fingerprint' && webauthnDevice) {
        setSelectedDevice(webauthnDevice);
      } else if (cameraDevice && (type === 'face' || type === 'palmprint')) {
        setSelectedDevice(cameraDevice);
      } else if (nativeDevice) {
        setSelectedDevice(nativeDevice);
      } else {
        setSelectedDevice(detectedDevices[0]);
      }
    }
  }, [type, isMobile]);

  useEffect(() => {
    detectAvailableDevices();
  }, [detectAvailableDevices]);

  const handleWebAuthnCapture = async () => {
    try {
      setCapturing(true);
      setError('');

      // Create credential for registration or get assertion for verification
      const challenge = new Uint8Array(32);
      window.crypto.getRandomValues(challenge);

      const publicKeyCredentialCreationOptions: PublicKeyCredentialCreationOptions = {
        challenge: challenge,
        rp: {
          name: "Biometric Auth App",
          id: window.location.hostname,
        },
        user: {
          id: new TextEncoder().encode("user@example.com"),
          name: "user@example.com",
          displayName: "User",
        },
        pubKeyCredParams: [
          {alg: -7, type: "public-key"}, // ES256
          {alg: -257, type: "public-key"} // RS256 (better Windows Hello support)
        ],
        authenticatorSelection: {
          authenticatorAttachment: "platform", // Ensures laptop/built-in sensors
          userVerification: "required", // Forces biometric verification
          requireResidentKey: false
        },
        timeout: 120000, // Increased timeout for laptop sensors
        attestation: "direct"
      };

      console.log('🔐 Attempting WebAuthn credential creation for laptop fingerprint...');
      
      const credential = await navigator.credentials.create({
        publicKey: publicKeyCredentialCreationOptions
      }) as PublicKeyCredential;

      if (credential) {
        console.log('✅ Laptop fingerprint credential created successfully');
        
        // Convert credential to base64 for backend processing
        const credentialData = {
          id: credential.id,
          rawId: Array.from(new Uint8Array(credential.rawId)),
          response: {
            attestationObject: Array.from(new Uint8Array((credential.response as AuthenticatorAttestationResponse).attestationObject)),
            clientDataJSON: Array.from(new Uint8Array(credential.response.clientDataJSON)),
          },
          type: credential.type,
          deviceInfo: {
            platform: navigator.platform,
            userAgent: navigator.userAgent,
            timestamp: Date.now()
          }
        };

        // Ensure proper base64 encoding
        const base64Data = ensureBase64Format(credentialData);
        onCapture(base64Data);
      }
    } catch (err: any) {
      console.error('💥 Laptop fingerprint capture failed:', err);
      
      // Enhanced error handling for laptop-specific issues
      if (err.name === 'NotSupportedError') {
        setError('Laptop fingerprint sensor is not supported on this device. Please check if Windows Hello, Touch ID, or equivalent is enabled.');
      } else if (err.name === 'NotAllowedError') {
        setError('Fingerprint authentication was cancelled. Please try again and follow the prompts on your laptop.');
      } else if (err.name === 'InvalidStateError') {
        setError('Laptop fingerprint sensor is busy or not available. Please ensure no other applications are using it.');
      } else if (err.name === 'SecurityError') {
        setError('Security error: Please ensure you are accessing this site over HTTPS for laptop fingerprint authentication.');
      } else if (err.name === 'AbortError') {
        setError('Fingerprint authentication timed out. Laptop sensors may need more time - please try again.');
      } else {
        setError(`Laptop fingerprint capture failed: ${err.message}. Please ensure your fingerprint sensor is working properly.`);
      }
    } finally {
      setCapturing(false);
    }
  };

  const handleNativeMobileCapture = async () => {
    try {
      setCapturing(true);
      setError('');
      setShowNativePrompt(true);
    } catch (err: any) {
      setError('Native biometric capture failed: ' + err.message);
      setCapturing(false);
    }
  };

  const handleNativePromptConfirm = async () => {
    try {
      setShowNativePrompt(false);
      
      // Try to trigger native mobile biometric prompt
      if ('credentials' in navigator) {
        // This is a simplified approach - in real implementation,
        // you might use a native mobile app bridge or PWA capabilities
        
        // Simulate successful capture with mock data after 2 seconds
        await new Promise((resolve) => setTimeout(resolve, 2000));
        
        // In real implementation, this would be actual biometric data
        const mockData = `data:application/json;base64,${btoa(JSON.stringify({
          type: type,
          timestamp: Date.now(),
          deviceInfo: navigator.userAgent,
          mockData: true
        }))}`;
        
        // Ensure proper base64 encoding
        const base64Data = ensureBase64Format(mockData);
        onCapture(base64Data);
      }
    } catch (err: any) {
      setError('Native biometric capture failed: ' + err.message);
    } finally {
      setCapturing(false);
    }
  };

  const handleNativePromptCancel = () => {
    setShowNativePrompt(false);
    setCapturing(false);
    setError('');
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file');
        return;
      }
      
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError('Image file size must be less than 5MB');
        return;
      }

      setUploadedFile(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result as string;
        setUploadPreview(result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUploadConfirm = () => {
    if (uploadedFile && uploadPreview) {
      try {
        // Convert the uploaded image to base64
        const base64Data = uploadPreview.split(',')[1]; // Remove data URL prefix
        onCapture(base64Data);
        setShowUploadDialog(false);
        setUploadedFile(null);
        setUploadPreview('');
      } catch (error) {
        setError('Failed to process uploaded image');
      }
    }
  };

  const handleUploadCancel = () => {
    setShowUploadDialog(false);
    setUploadedFile(null);
    setUploadPreview('');
    setError('');
  };

  const handleCameraCapture = async () => {
    try {
      setCapturing(true);
      setError('');
      
      // Get camera stream
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: type === 'face' ? 'user' : 'environment',
          width: { ideal: 640 },
          height: { ideal: 480 }
        }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();

        // Auto-capture after 3 seconds
        setTimeout(() => {
          captureFrame(stream);
        }, 3000);
      }
    } catch (err: any) {
      setError('Camera access denied or not available');
      setCapturing(false);
    }
  };

  const captureFrame = (stream: MediaStream) => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');

      if (ctx) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0);

        // Get the data URL and extract just the base64 part
        const dataUrl = canvas.toDataURL('image/png');
        
        // Stop the stream
        stream.getTracks().forEach(track => track.stop());
        
        // Ensure we return only the base64 data, not the data URL
        const base64Data = dataUrl.split(',')[1];
        onCapture(base64Data);
      }
    }
    setCapturing(false);
  };

  const ensureBase64Format = (data: any): string => {
    try {
      if (typeof data === 'string') {
        // If it's already a data URL, extract the base64 part
        if (data.startsWith('data:')) {
          const base64Part = data.split(',')[1];
          if (base64Part) {
            return base64Part;
          }
        }
        
        // If it contains base64 indicator, extract it
        if (data.includes('base64,')) {
          const base64Part = data.split('base64,')[1];
          if (base64Part) {
            return base64Part;
          }
        }
        
        // Test if it's already valid base64
        try {
          atob(data);
          return data;
        } catch {
          // If not valid base64, encode it
          return btoa(data);
        }
      } else {
        // If it's an object (like WebAuthn credential), stringify and encode
        return btoa(JSON.stringify(data));
      }
    } catch (error) {
      console.error('Error ensuring base64 format:', error);
      throw 'Failed to format biometric data';
    }
  };

  const handleCapture = () => {
    if (!selectedDevice) {
      setError('No device selected');
      return;
    }

    setError('');
    setCapturing(true);

    switch (selectedDevice.type) {
      case 'webauthn':
        handleWebAuthnCapture();
        break;
      case 'camera':
        handleCameraCapture();
        break;
      case 'native':
        handleNativeMobileCapture();
        break;
      case 'upload':
        setShowUploadDialog(true);
        setCapturing(false);
        break;
      default:
        setError('Unsupported device type');
        setCapturing(false);
    }
  };

  const getBiometricIcon = () => {
    switch (type) {
      case 'fingerprint':
        return <Fingerprint sx={{ fontSize: 60 }} />;
      case 'face':
        return <Face sx={{ fontSize: 60 }} />;
      case 'palmprint':
        return <CameraAlt sx={{ fontSize: 60 }} />;
    }
  };

  const getInstructions = () => {
    if (!selectedDevice) return 'No biometric device available';

    switch (selectedDevice.type) {
      case 'webauthn':
        const userAgent = navigator.userAgent.toLowerCase();
        
        if (userAgent.includes('windows')) {
          return 'Use Windows Hello: Follow the on-screen prompt and place your finger on the laptop fingerprint sensor';
        } else if (userAgent.includes('mac')) {
          return 'Use Touch ID: Place your finger on the MacBook Touch ID sensor when prompted';
        } else if (userAgent.includes('linux')) {
          return 'Use your laptop fingerprint reader: Follow the system prompt to scan your finger';
        } else if (isMobile) {
          return 'Place your finger on the mobile fingerprint sensor when prompted';
        } else {
          return 'Use your device\'s built-in fingerprint sensor when prompted';
        }
      case 'native':
        return `Use your device's built-in biometric authentication`;
      case 'camera':
        return type === 'face' 
          ? `Position your face in front of the camera`
          : `Place your ${type} in front of the camera`;
      case 'upload':
        return 'Upload a clear image of your fingerprint for registration';
      default:
        return 'Follow the prompts to capture your biometric data';
    }
  };

    return (
    <Box sx={{ textAlign: 'center', p: 2 }}>
      <Card sx={{ 
        maxWidth: 400, 
        mx: 'auto',
        background: isMobile ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'white',
        color: isMobile ? 'white' : 'inherit'
      }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              {type.charAt(0).toUpperCase() + type.slice(1)} Capture
            </Typography>
            <IconButton onClick={onCancel} sx={{ color: isMobile ? 'white' : 'inherit' }}>
              <Close />
            </IconButton>
          </Box>
          
          <Box sx={{ my: 3 }}>
            {getBiometricIcon()}
          </Box>

          {devices.length > 1 && (
            <Button
              variant="outlined"
              onClick={() => setShowDeviceDialog(true)}
              sx={{ mb: 2, color: isMobile ? 'white' : 'inherit', borderColor: isMobile ? 'white' : 'inherit' }}
              startIcon={<PhoneAndroid />}
            >
              Device: {selectedDevice?.name || 'Select Device'}
            </Button>
          )}

          <Typography variant="body2" sx={{ mb: 3, opacity: 0.8 }}>
            {getInstructions()}
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* Camera view for face/palmprint */}
          {selectedDevice?.type === 'camera' && capturing && (
            <Box sx={{ mb: 2 }}>
              <video
                ref={videoRef}
                style={{
                  width: '100%',
                  maxWidth: 300,
                  height: 'auto',
                  borderRadius: 8,
                }}
                autoPlay
                muted
              />
              <canvas ref={canvasRef} style={{ display: 'none' }} />
              </Box>
            )}

          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              variant="contained"
              onClick={handleCapture}
              disabled={capturing || !selectedDevice}
              startIcon={capturing ? <CircularProgress size={20} /> : <TouchApp />}
              sx={{ 
                background: isMobile ? 'rgba(255,255,255,0.2)' : undefined,
                '&:hover': {
                  background: isMobile ? 'rgba(255,255,255,0.3)' : undefined,
                }
              }}
            >
              {capturing ? 'Capturing...' : 'Start Capture'}
            </Button>

            <Button
              variant="outlined"
              onClick={onCancel}
              sx={{ 
                color: isMobile ? 'white' : 'inherit', 
                borderColor: isMobile ? 'white' : 'inherit' 
              }}
            >
              Cancel
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* Device Selection Dialog */}
      <Dialog open={showDeviceDialog} onClose={() => setShowDeviceDialog(false)}>
        <DialogTitle>Select Biometric Device</DialogTitle>
        <DialogContent>
          {devices.map((device, index) => (
            <Button
              key={index}
              fullWidth
              variant={selectedDevice?.name === device.name ? "contained" : "outlined"}
              onClick={() => {
                setSelectedDevice(device);
                setShowDeviceDialog(false);
              }}
              sx={{ mb: 1 }}
              startIcon={
                device.type === 'webauthn' ? <Fingerprint /> :
                device.type === 'native' ? <PhoneAndroid /> :
                device.type === 'upload' ? <Upload /> :
                <CameraAlt />
              }
            >
              {device.name}
            </Button>
          ))}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDeviceDialog(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Native Mobile Prompt Dialog */}
      <Dialog
        open={showNativePrompt}
        onClose={handleNativePromptCancel}
        aria-labelledby="native-prompt-dialog-title"
        aria-describedby="native-prompt-dialog-description"
      >
        <DialogTitle id="native-prompt-dialog-title">
          {type === 'fingerprint' ? 'Fingerprint Sensor' : 'Biometric Sensor'}
        </DialogTitle>
        <DialogContent>
          <Typography id="native-prompt-dialog-description">
            {type === 'fingerprint' ? 'Please place your finger on the fingerprint sensor.' : 'Please position your biometric sensor.'}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleNativePromptConfirm} color="primary">
            Confirm
          </Button>
          <Button onClick={handleNativePromptCancel} color="primary">
            Cancel
          </Button>
        </DialogActions>
      </Dialog>

      {/* Image Upload Dialog */}
      <Dialog
        open={showUploadDialog}
        onClose={handleUploadCancel}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Upload Fingerprint Image
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Please upload a clear image of your fingerprint. The image should be:
          </Typography>
          <List dense>
            <ListItem>
              <ListItemIcon>
                <CheckCircle color="primary" />
              </ListItemIcon>
              <ListItemText primary="High quality and well-lit" />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CheckCircle color="primary" />
              </ListItemIcon>
              <ListItemText primary="Shows the complete fingerprint pattern" />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CheckCircle color="primary" />
              </ListItemIcon>
              <ListItemText primary="Less than 5MB in size" />
            </ListItem>
          </List>

          <Box sx={{ mt: 2 }}>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              style={{ display: 'none' }}
            />
            <Button
              variant="outlined"
              onClick={() => fileInputRef.current?.click()}
              startIcon={<Upload />}
              fullWidth
              sx={{ mb: 2 }}
            >
              Select Image File
            </Button>

            {uploadPreview && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                  Preview:
                </Typography>
                <img
                  src={uploadPreview}
                  alt="Fingerprint preview"
                  style={{
                    width: '100%',
                    maxHeight: 200,
                    objectFit: 'contain',
                    borderRadius: 8,
                    border: '1px solid #ddd'
                  }}
                />
              </Box>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleUploadCancel}>
            Cancel
          </Button>
          <Button
            onClick={handleUploadConfirm}
            variant="contained"
            disabled={!uploadedFile}
          >
            Use This Image
          </Button>
        </DialogActions>
      </Dialog>
        </Box>
  );
};

export default BiometricCapture;