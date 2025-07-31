import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Button,
  Typography,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Container,
  useTheme,
  useMediaQuery,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import {
  Fingerprint,
  Face,
  CameraAlt,
  PhoneAndroid,
  TouchApp,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import BiometricCapture from '../components/BiometricCapture';
import { authService } from '../services/authService';

const BiometricLoginPage: React.FC = () => {
  const [biometricType, setBiometricType] = useState<'face' | 'fingerprint' | 'palmprint'>('fingerprint');
  const [biometricData, setBiometricData] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [captureMode, setCaptureMode] = useState(false);
  const [username, setUsername] = useState('');
  const [showUsernameInput, setShowUsernameInput] = useState(false);
  
  const navigate = useNavigate();
  const { setTokens } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  useEffect(() => {
    // Auto-select fingerprint for mobile devices
    if (isMobile && window.PublicKeyCredential) {
      setBiometricType('fingerprint');
      checkWebAuthnSupport();
    }
  }, [isMobile]);

  const checkWebAuthnSupport = async () => {
    try {
      if (window.PublicKeyCredential) {
        const available = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
        if (available) {
          console.log('Mobile biometric authentication is supported');
        }
      }
    } catch (err) {
      console.log('WebAuthn check failed:', err);
    }
  };

  const handleBiometricCapture = (data: string) => {
    setBiometricData(data);
    setCaptureMode(false);
    
    // If it's WebAuthn data and no username provided, ask for username
    try {
      const parsed = JSON.parse(atob(data.split(',')[1]));
      if (parsed.type === 'public-key' || parsed.rawId) {
        if (!username) {
          setShowUsernameInput(true);
          return;
        }
      }
    } catch (err) {
      // Not WebAuthn data, continue with normal flow
    }
  };

  const handleUsernameSubmit = () => {
    if (username.trim()) {
      setShowUsernameInput(false);
      handleBiometricLogin();
    } else {
      setError('Please enter your username');
    }
  };

  const handleBiometricLogin = async () => {
    if (!biometricData) {
      setError('Please capture biometric data');
      return;
    }

    try {
      setLoading(true);
      setError('');

      // Parse the biometric data
      let parsedData;
      try {
        const dataContent = biometricData.includes('base64,') 
          ? biometricData.split(',')[1] 
          : biometricData;
        parsedData = JSON.parse(atob(dataContent));
      } catch (parseErr) {
        // If parsing fails, treat as blob data
        const response = await fetch(biometricData);
        const blob = await response.blob();
        const result = await authService.biometricLogin(biometricType, blob);
        setTokens(result.access_token, result.refresh_token);
        navigate('/dashboard');
        return;
      }

      // Handle WebAuthn credentials
      if (parsedData.type === 'public-key' || parsedData.rawId) {
        if (!username) {
          setError('Username required for biometric authentication');
          setShowUsernameInput(true);
          return;
        }
        
        const result = await authService.mobileBiometricLogin(biometricType, parsedData, username);
        setTokens(result.access_token, result.refresh_token);
        navigate('/dashboard');
      } else {
        // Handle traditional biometric data
        const result = await authService.mobileBiometricLogin(biometricType, parsedData);
        setTokens(result.access_token, result.refresh_token);
      navigate('/dashboard');
      }
    } catch (err: any) {
      console.error('Biometric login error:', err);
      if (err.message.includes('Username required')) {
        setShowUsernameInput(true);
      } else {
        setError(err.message || 'Biometric authentication failed');
      }
    } finally {
      setLoading(false);
    }
  };

  const getRecommendedMethod = () => {
    if (isMobile && biometricType === 'fingerprint') {
      return (
        <Alert severity="info" sx={{ mb: 2 }}>
          <strong>Mobile Device Detected!</strong><br />
          Use your device's fingerprint sensor for secure authentication.
        </Alert>
      );
    }
    return null;
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        p: { xs: 1, sm: 2 },
      }}
    >
      <Container maxWidth="sm">
        <Card sx={{ 
          background: 'rgba(255,255,255,0.95)', 
          backdropFilter: 'blur(10px)',
          mx: { xs: 1, sm: 0 }
        }}>
          <CardContent sx={{ p: { xs: 2, sm: 3, md: 4 } }}>
            <Typography 
              variant={isMobile ? 'h5' : 'h4'}
              align="center" 
              gutterBottom 
              sx={{ 
                fontWeight: 700, 
                background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: { xs: 2, sm: 3 }
              }}
            >
              Biometric Login
            </Typography>

            {getRecommendedMethod()}

            {!captureMode ? (
              <Box>
                <FormControl 
                  fullWidth 
                  sx={{ mb: { xs: 2, sm: 3 } }}
                  size={isMobile ? 'small' : 'medium'}
                >
                  <InputLabel>Authentication Method</InputLabel>
              <Select
                value={biometricType}
                    label="Authentication Method"
                onChange={(e) => setBiometricType(e.target.value as any)}
              >
                    {isMobile && (
                      <MenuItem value="fingerprint">
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <PhoneAndroid />
                          Mobile Fingerprint Sensor
                        </Box>
                      </MenuItem>
                    )}
                <MenuItem value="face">
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Face />
                        Face Recognition
                      </Box>
                </MenuItem>
                <MenuItem value="fingerprint">
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Fingerprint />
                        {isMobile ? 'Fingerprint Scanner' : 'Fingerprint'}
                      </Box>
                </MenuItem>
                <MenuItem value="palmprint">
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <CameraAlt />
                        Palmprint
                      </Box>
                </MenuItem>
              </Select>
            </FormControl>

                {error && (
                  <Alert severity="error" sx={{ mb: { xs: 2, sm: 3 } }}>
                    {error}
                  </Alert>
                )}

                <Box sx={{ 
                  display: 'flex', 
                  flexDirection: { xs: 'column', sm: 'row' },
                  gap: { xs: 2, sm: 1 },
                  justifyContent: 'center' 
                }}>
                  <Button
                    variant="contained"
                    onClick={() => setCaptureMode(true)}
                    disabled={loading}
                    fullWidth={isMobile}
                    size={isMobile ? 'medium' : 'large'}
                    startIcon={<TouchApp />}
                    sx={{
                      background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                      minWidth: { sm: 180 },
                      py: { xs: 1.5, sm: 2 }
                    }}
                  >
                    {isMobile && biometricType === 'fingerprint' 
                      ? 'Use Fingerprint' 
                      : `Capture ${biometricType}`}
                  </Button>

                  <Button
                    variant="outlined"
                    onClick={() => navigate('/login')}
                    fullWidth={isMobile}
                    size={isMobile ? 'medium' : 'large'}
                    sx={{ minWidth: { sm: 120 } }}
                  >
                    Back to Login
                  </Button>
          </Box>

                {biometricData && (
                  <Box sx={{ mt: { xs: 2, sm: 3 }, textAlign: 'center' }}>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {isMobile ? 'Biometric data captured from device sensor' : 'Biometric data captured successfully'}
                    </Typography>
                    <Button
                      variant="contained"
                      onClick={handleBiometricLogin}
                      disabled={loading}
                      fullWidth
                      size={isMobile ? 'medium' : 'large'}
                      startIcon={loading ? <CircularProgress size={20} /> : <Fingerprint />}
                      sx={{
                        background: 'linear-gradient(45deg, #4caf50 30%, #45a049 90%)',
                      }}
                    >
                      {loading ? 'Authenticating...' : 'Authenticate'}
                    </Button>
                  </Box>
                )}
              </Box>
            ) : (
              <BiometricCapture
                type={biometricType}
                onCapture={handleBiometricCapture}
                onCancel={() => setCaptureMode(false)}
              />
            )}
          </CardContent>
        </Card>
      </Container>

      {/* Username Input Dialog for WebAuthn */}
      <Dialog open={showUsernameInput} onClose={() => setShowUsernameInput(false)}>
        <DialogTitle>Username Required</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Please enter your username to complete biometric authentication.
          </Typography>
          <TextField
            autoFocus
            fullWidth
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleUsernameSubmit()}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowUsernameInput(false)}>Cancel</Button>
          <Button 
            onClick={handleUsernameSubmit} 
            variant="contained"
            disabled={!username.trim()}
          >
            Continue
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default BiometricLoginPage;
