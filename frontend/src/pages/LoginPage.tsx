import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  InputAdornment,
  IconButton,
  Divider,
  Card,
  CardContent,
  Grid,
  Chip,
  CircularProgress,
  Fade,
  Zoom,
  useTheme as useMuiTheme,
} from '@mui/material';
import {
  Email,
  Lock,
  Visibility,
  VisibilityOff,
  Fingerprint,
  Face,
  Security,
  Login,
  PersonAdd,
  AdminPanelSettings,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import BiometricCapture from '../components/BiometricCapture';
import ThemeToggle from '../components/ThemeToggle';
import { API_BASE_URL } from '../services/authService';

const LoginPage: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [biometricType, setBiometricType] = useState<'fingerprint' | 'face' | 'palmprint' | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [showBiometricCapture, setShowBiometricCapture] = useState(false);
  
  const { login, adminLogin } = useAuth();
  const { getGradient } = useTheme();
  const theme = useMuiTheme();
  const navigate = useNavigate();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleTraditionalLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.username || !formData.password) {
      setError('Please fill in all fields');
      return;
    }

    // For traditional login, we still need biometric data
    // Set a default biometric type and show capture
    setBiometricType('fingerprint');
    setShowBiometricCapture(true);
    setError('Please complete biometric authentication to proceed');
  };

  const handleBiometricLogin = async (type: 'fingerprint' | 'face' | 'palmprint') => {
    setBiometricType(type);
    setShowBiometricCapture(true);
    setError('');
  };

  const handleBiometricCapture = async (imageData: string) => {
    if (!biometricType) return;
    try {
      setLoading(true);
      setError('');
      console.log('🔍 Starting biometric login process at:', `${API_BASE_URL}/auth/login-fast`);
      await login(formData.username, formData.password, { type: biometricType, data: imageData });
      console.log('✅ Login successful, navigating to dashboard...');
      navigate('/dashboard');
    } catch (err: any) {
      console.error('❌ Login error:', err);
      const msg = err.response?.data?.detail || err.message || 'Authentication failed. Please try again.';
      setError(msg);
    } finally {
      setLoading(false);
      setShowBiometricCapture(false);
      setBiometricType(null);
    }
  };

  const handleBiometricCancel = () => {
    setShowBiometricCapture(false);
    setBiometricType(null);
    setError('');
  };

  const biometricOptions = [
    {
      type: 'fingerprint' as const,
      icon: <Fingerprint />,
      label: 'Fingerprint',
      description: 'Quick and secure access',
      color: '#4caf50',
    },
    {
      type: 'face' as const,
      icon: <Face />,
      label: 'Face Recognition',
      description: 'Contactless authentication',
      color: '#2196f3',
    },
    {
      type: 'palmprint' as const,
      icon: <Security />,
      label: 'Palmprint',
      description: 'Advanced biometric security',
      color: '#ff9800',
    },
  ];

  if (showBiometricCapture && biometricType) {
    return (
      <Container maxWidth="sm" sx={{ py: 4 }}>
        <Fade in={true} timeout={500}>
          <Box>
            <Typography variant="h4" align="center" gutterBottom sx={{ 
              fontWeight: 700, 
              background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 3,
            }}>
              Biometric Authentication
            </Typography>
            
            <BiometricCapture
              type={biometricType}
              onCapture={handleBiometricCapture}
              onCancel={handleBiometricCancel}
            />
          </Box>
        </Fade>
      </Container>
    );
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: getGradient(),
        p: { xs: 1, sm: 2 },
        position: 'relative',
      }}
    >
      <Box sx={{ position: 'absolute', top: 16, right: 16, zIndex: 1 }}>
        <ThemeToggle />
      </Box>

      <Container maxWidth="lg">
        <Fade in={true} timeout={800}>
          <Box>
            {/* Header */}
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography 
                variant="h3" 
                sx={{ 
                  fontWeight: 700, 
                  color: 'white',
                  textShadow: '0 2px 4px rgba(0,0,0,0.3)',
                  mb: 1,
                }}
              >
                Biometric Authentication
              </Typography>
              <Typography 
                variant="h6" 
                sx={{ 
                  color: 'rgba(255,255,255,0.9)',
                  fontWeight: 400,
                }}
              >
                Secure, Fast, and Reliable
              </Typography>
            </Box>
            
            <Typography variant="h6" align="center" sx={{ 
              color: 'rgba(255,255,255,0.9)', 
              mb: 4,
              textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
            }}>
              Choose your preferred authentication method
            </Typography>

            <Grid container spacing={4}>
              {/* Traditional Login */}
              <Grid item xs={12} md={6}>
                <Zoom in={true} timeout={600}>
                  <Card sx={{ 
                    height: '100%',
                    background: 'rgba(255,255,255,0.95)',
                    backdropFilter: 'blur(10px)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 12px 24px rgba(0,0,0,0.2)',
                    }
                  }}>
                    <CardContent sx={{ p: 3 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                        <Login sx={{ mr: 2, color: '#667eea' }} />
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                          Traditional Login
                        </Typography>
                      </Box>

                      <Box component="form" onSubmit={handleTraditionalLogin}>
                        <TextField
                          fullWidth
                          name="username"
                          label="Username or Email"
                          value={formData.username}
                          onChange={handleInputChange}
                          margin="normal"
                          required
                          disabled={loading}
                          InputProps={{
                            startAdornment: (
                              <InputAdornment position="start">
                                <Email color="action" />
                              </InputAdornment>
                            ),
                          }}
                        />
                        
                        <TextField
                          fullWidth
                          name="password"
                          label="Password"
                          type={showPassword ? 'text' : 'password'}
                          value={formData.password}
                          onChange={handleInputChange}
                          margin="normal"
                          required
                          disabled={loading}
                          InputProps={{
                            startAdornment: (
                              <InputAdornment position="start">
                                <Lock color="action" />
                              </InputAdornment>
                            ),
                            endAdornment: (
                              <InputAdornment position="end">
                                <IconButton
                                  onClick={() => setShowPassword(!showPassword)}
                                  edge="end"
                                >
                                  {showPassword ? <VisibilityOff /> : <Visibility />}
                                </IconButton>
                              </InputAdornment>
                            ),
                          }}
                        />

                        <Button
                          type="submit"
                          fullWidth
                          variant="contained"
                          disabled={loading}
                          sx={{ 
                            mt: 3, 
                            py: 1.5,
                            background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                            '&:hover': {
                              background: 'linear-gradient(45deg, #5a6fd8 30%, #6a4190 90%)',
                            }
                          }}
                        >
                          {loading ? (
                            <CircularProgress size={24} color="inherit" />
                          ) : (
                            'Sign In'
                          )}
                        </Button>
                      </Box>
                    </CardContent>
                  </Card>
                </Zoom>
              </Grid>

              {/* Biometric Login */}
              <Grid item xs={12} md={6}>
                <Zoom in={true} timeout={800}>
                  <Card sx={{ 
                    height: '100%',
                    background: 'rgba(255,255,255,0.1)',
                    backdropFilter: 'blur(10px)',
                    color: 'white',
                    border: '1px solid rgba(255,255,255,0.3)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 12px 24px rgba(255,255,255,0.1)',
                    }
                  }}>
                    <CardContent sx={{ p: 3 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                        <Security sx={{ mr: 2 }} />
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                          Biometric Login
                        </Typography>
                        <Chip 
                          label="Secure" 
                          size="small" 
                          sx={{ 
                            ml: 'auto', 
                            backgroundColor: 'rgba(255, 255, 255, 0.2)',
                            color: 'white',
                          }} 
                        />
                      </Box>

                      <Typography variant="body2" sx={{ mb: 3, opacity: 0.9 }}>
                        Use your unique biometric features for secure, passwordless access
                      </Typography>

                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                        {biometricOptions.map((option) => (
                          <Button
                            key={option.type}
                            variant="outlined"
                            fullWidth
                            startIcon={option.icon}
                            onClick={() => handleBiometricLogin(option.type)}
                            disabled={loading}
                            sx={{
                              py: 1.5,
                              color: 'white',
                              borderColor: 'rgba(255, 255, 255, 0.3)',
                              backgroundColor: 'rgba(255, 255, 255, 0.1)',
                              '&:hover': {
                                borderColor: 'white',
                                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                              },
                            }}
                          >
                            <Box sx={{ textAlign: 'left', width: '100%' }}>
                              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                                {option.label}
                              </Typography>
                              <Typography variant="caption" sx={{ opacity: 0.8 }}>
                                {option.description}
                              </Typography>
                            </Box>
                          </Button>
                        ))}
                      </Box>
                    </CardContent>
                  </Card>
                </Zoom>
              </Grid>
            </Grid>

            {error && (
              <Fade in={true} timeout={300}>
                <Alert severity="error" sx={{ mt: 3, backgroundColor: 'rgba(255,255,255,0.9)' }}>
                  {typeof error === 'string' ? error : JSON.stringify(error)}
                </Alert>
              </Fade>
            )}

            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Divider sx={{ borderColor: 'rgba(255,255,255,0.3)', mb: 3 }} />
              
              <Box sx={{ display: 'flex', justifyContent: 'center', gap: 3, flexWrap: 'wrap' }}>
                <Button
                  variant="outlined"
                  startIcon={<PersonAdd />}
                  onClick={() => navigate('/register')}
                  sx={{ 
                    px: 3,
                    color: 'white',
                    borderColor: 'rgba(255,255,255,0.5)',
                    '&:hover': {
                      borderColor: 'white',
                      backgroundColor: 'rgba(255,255,255,0.1)',
                    }
                  }}
                >
                  Create Account
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<AdminPanelSettings />}
                  onClick={() => navigate('/admin/login')}
                  sx={{ 
                    px: 3,
                    color: 'white',
                    borderColor: 'rgba(255,255,255,0.5)',
                    '&:hover': {
                      borderColor: 'white',
                      backgroundColor: 'rgba(255,255,255,0.1)',
                    }
                  }}
                >
                  Admin Portal
                </Button>
              </Box>
            </Box>
          </Box>
        </Fade>
      </Container>
    </Box>
  );
};

export default LoginPage;
