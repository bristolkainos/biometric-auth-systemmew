import React, { useState, useEffect } from 'react';
import {
  Container,
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider,
  CircularProgress,
} from '@mui/material';
import {
  Fingerprint,
  Computer,
  CheckCircle,
  Warning,
  Error as ErrorIcon,
  Info,
} from '@mui/icons-material';
import { 
  detectMobileBiometrics, 
  isLaptopDevice, 
  getLaptopBiometricName,
  getBiometricDeviceName 
} from '../types/webauthn';

const BiometricTestPage: React.FC = () => {
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<string>('');
  const [deviceCapabilities, setDeviceCapabilities] = useState<any>(null);
  const [webAuthnSupport, setWebAuthnSupport] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    checkDeviceCapabilities();
  }, []);

  const checkDeviceCapabilities = async () => {
    try {
      // Check WebAuthn support
      const webAuthnAvailable = !!window.PublicKeyCredential;
      setWebAuthnSupport(webAuthnAvailable);

      if (webAuthnAvailable) {
        // Check platform authenticator
        const platformAvailable = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
        
        // Get device capabilities
        const capabilities = await detectMobileBiometrics();
        setDeviceCapabilities(capabilities);

        console.log('Device capabilities:', {
          webAuthn: webAuthnAvailable,
          platform: platformAvailable,
          capabilities
        });
      }
    } catch (err) {
      console.error('Error checking device capabilities:', err);
      setError('Failed to check device capabilities');
    }
  };

  const testLaptopFingerprint = async () => {
    try {
      setTesting(true);
      setError('');
      setTestResult('');

      console.log('🧪 Testing laptop fingerprint sensor...');

      const challenge = new Uint8Array(32);
      window.crypto.getRandomValues(challenge);

      const options: PublicKeyCredentialCreationOptions = {
        challenge,
        rp: {
          name: "Biometric Test",
          id: window.location.hostname,
        },
        user: {
          id: new TextEncoder().encode("test@example.com"),
          name: "test@example.com",
          displayName: "Test User",
        },
        pubKeyCredParams: [
          { alg: -7, type: "public-key" }, // ES256
          { alg: -257, type: "public-key" } // RS256
        ],
        authenticatorSelection: {
          authenticatorAttachment: "platform",
          userVerification: "required",
          requireResidentKey: false,
        },
        timeout: 60000,
        attestation: "none"
      };

      const credential = await navigator.credentials.create({
        publicKey: options
      }) as PublicKeyCredential;

      if (credential) {
        setTestResult('✅ SUCCESS: Laptop fingerprint sensor is working perfectly!');
        console.log('✅ Laptop fingerprint test successful:', credential);
      }
    } catch (err: any) {
      console.error('❌ Laptop fingerprint test failed:', err);
      
      let errorMessage = '';
      switch (err.name) {
        case 'NotSupportedError':
          errorMessage = '❌ Laptop fingerprint sensor not supported. Check if Windows Hello/Touch ID is enabled.';
          break;
        case 'NotAllowedError':
          errorMessage = '⚠️ Test cancelled or permission denied. Please try again and follow the prompts.';
          break;
        case 'InvalidStateError':
          errorMessage = '⚠️ Fingerprint sensor is busy. Close other apps using it and try again.';
          break;
        case 'SecurityError':
          errorMessage = '🔒 Security error. Ensure you\'re using HTTPS and try again.';
          break;
        case 'AbortError':
          errorMessage = '⏱️ Test timed out. Your sensor may need more time - try again.';
          break;
        default:
          errorMessage = `❌ Test failed: ${err.message}`;
      }
      
      setError(errorMessage);
    } finally {
      setTesting(false);
    }
  };

  const getDeviceInfo = () => {
    return {
      userAgent: navigator.userAgent,
      platform: navigator.platform,
      isLaptop: isLaptopDevice(),
      biometricName: getBiometricDeviceName(),
      webAuthnSupported: webAuthnSupport,
    };
  };

  const deviceInfo = getDeviceInfo();

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Card>
        <CardContent>
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Computer sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" gutterBottom>
              Laptop Fingerprint Test
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Test your laptop's fingerprint sensor compatibility
            </Typography>
          </Box>

          {/* Device Detection */}
          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Device Detection
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  {deviceInfo.isLaptop ? <CheckCircle color="success" /> : <Warning color="warning" />}
                </ListItemIcon>
                <ListItemText
                  primary="Device Type"
                  secondary={deviceInfo.isLaptop ? 'Laptop/Desktop' : 'Mobile Device'}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  {deviceInfo.webAuthnSupported ? <CheckCircle color="success" /> : <ErrorIcon color="error" />}
                </ListItemIcon>
                <ListItemText
                  primary="WebAuthn Support"
                  secondary={deviceInfo.webAuthnSupported ? 'Supported' : 'Not Supported'}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Fingerprint color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Detected Biometric"
                  secondary={deviceInfo.biometricName}
                />
              </ListItem>
            </List>
          </Box>

          <Divider sx={{ my: 3 }} />

          {/* Capabilities */}
          {deviceCapabilities && (
            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom>
                Biometric Capabilities
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {deviceCapabilities.windowsHello && (
                  <Chip icon={<CheckCircle />} label="Windows Hello" color="success" />
                )}
                {deviceCapabilities.touchId && (
                  <Chip icon={<CheckCircle />} label="Touch ID" color="success" />
                )}
                {deviceCapabilities.linuxFingerprint && (
                  <Chip icon={<CheckCircle />} label="Linux Fingerprint" color="success" />
                )}
                {deviceCapabilities.laptopBiometric && (
                  <Chip icon={<CheckCircle />} label="Laptop Biometric" color="success" />
                )}
                {deviceCapabilities.fingerprint && (
                  <Chip icon={<CheckCircle />} label="Fingerprint" color="primary" />
                )}
              </Box>
            </Box>
          )}

          <Divider sx={{ my: 3 }} />

          {/* Test Section */}
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Fingerprint Sensor Test
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Click the button below to test your laptop's fingerprint sensor
            </Typography>

            <Button
              variant="contained"
              size="large"
              onClick={testLaptopFingerprint}
              disabled={testing || !deviceInfo.webAuthnSupported}
              startIcon={testing ? <CircularProgress size={20} /> : <Fingerprint />}
              sx={{ mb: 2 }}
            >
              {testing ? 'Testing Fingerprint Sensor...' : 'Test Laptop Fingerprint'}
            </Button>

            {!deviceInfo.webAuthnSupported && (
              <Alert severity="error" sx={{ mt: 2 }}>
                WebAuthn is not supported in this browser. Please use a modern browser like Chrome, Firefox, or Edge.
              </Alert>
            )}
          </Box>

          {/* Results */}
          {testResult && (
            <Alert severity="success" sx={{ mb: 2 }}>
              {testResult}
            </Alert>
          )}

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* Instructions */}
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Setup Instructions
            </Typography>
            
            {deviceInfo.platform.toLowerCase().includes('win') && (
              <Alert severity="info" sx={{ mb: 2 }}>
                <strong>Windows Setup:</strong>
                <br />• Go to Settings → Accounts → Sign-in options
                <br />• Set up Windows Hello Fingerprint
                <br />• Ensure your browser supports WebAuthn (Chrome, Edge, Firefox)
              </Alert>
            )}

            {deviceInfo.platform.toLowerCase().includes('mac') && (
              <Alert severity="info" sx={{ mb: 2 }}>
                <strong>macOS Setup:</strong>
                <br />• Go to System Preferences → Touch ID & Password
                <br />• Add your fingerprints
                <br />• Use Safari or Chrome for best compatibility
              </Alert>
            )}

            {deviceInfo.platform.toLowerCase().includes('linux') && (
              <Alert severity="info" sx={{ mb: 2 }}>
                <strong>Linux Setup:</strong>
                <br />• Install fprintd package: <code>sudo apt install fprintd</code>
                <br />• Enroll fingerprints: <code>fprintd-enroll</code>
                <br />• Use Firefox or Chrome with WebAuthn support
              </Alert>
            )}
          </Box>

          {/* Technical Details */}
          <details>
            <summary style={{ cursor: 'pointer', marginTop: '16px' }}>
              <Typography variant="subtitle2" component="span">
                Technical Details
              </Typography>
            </summary>
            <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
              <Typography variant="caption" component="pre" sx={{ fontSize: '0.75rem' }}>
                {JSON.stringify(deviceInfo, null, 2)}
              </Typography>
            </Box>
          </details>
        </CardContent>
      </Card>
    </Container>
  );
};

export default BiometricTestPage; 