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
  Card,
  CardContent,
  Grid,
  Chip,
  CircularProgress,
  Fade,
  Stepper,
  Step,
  StepLabel,
  Paper,
  Avatar,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Email,
  Lock,
  Person,
  Visibility,
  VisibilityOff,
  Fingerprint,
  Face,
  Security,
  CheckCircle,
  ArrowBack,
  ArrowForward,
  PersonAdd,
  Login,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import BiometricCapture from '../components/BiometricCapture';
import { ensureValidBase64, debugBase64 } from '../utils/base64Utils';

interface BiometricData {
  type: 'fingerprint' | 'face' | 'palmprint';
  imageData: string;
}

const steps = ['Account Information', 'Biometric Registration', 'Review & Submit'];

const RegisterPage: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [registrationProgress, setRegistrationProgress] = useState('');
  const [error, setError] = useState<string>('');
  const [biometricData, setBiometricData] = useState<BiometricData[]>([]);
  const [currentBiometricType, setCurrentBiometricType] = useState<'fingerprint' | 'face' | 'palmprint' | null>(null);
  const [showBiometricCapture, setShowBiometricCapture] = useState(false);
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    confirmPassword: '',
  });

  const { register } = useAuth();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const validateStep = (step: number) => {
    switch (step) {
      case 0:
        return formData.username && 
               formData.email && 
               formData.firstName && 
               formData.lastName && 
               formData.password && 
               formData.confirmPassword &&
               formData.password === formData.confirmPassword;
      case 1:
        return biometricData.length >= 1; // At least 1 biometric type required
      case 2:
        return true;
      default:
        return false;
    }
  };

  const handleNext = () => {
    if (validateStep(activeStep)) {
      setActiveStep(prev => prev + 1);
      setError('');
    } else {
      if (activeStep === 0) {
        setError('Please fill in all fields and ensure passwords match');
      } else if (activeStep === 1) {
        setError('Please register at least one biometric method');
      }
    }
  };

  const handleBack = () => {
    setActiveStep(prev => prev - 1);
    setError('');
  };

  const handleBiometricCapture = async (type: 'fingerprint' | 'face' | 'palmprint') => {
    setCurrentBiometricType(type);
    setShowBiometricCapture(true);
    setError('');
  };

  const handleBiometricData = (imageData: string) => {
    if (!currentBiometricType) return;

    try {
      // Debug the incoming data
      debugBase64(imageData, `${currentBiometricType} capture`);
      
      // Ensure the data is properly formatted base64
      const cleanedData = ensureValidBase64(imageData);

    setBiometricData(prev => {
      const filtered = prev.filter(data => data.type !== currentBiometricType);
        return [...filtered, { type: currentBiometricType, imageData: cleanedData }];
    });

    setShowBiometricCapture(false);
    setCurrentBiometricType(null);
    } catch (error) {
      console.error('Error processing biometric data:', error);
      setError(`Failed to process ${currentBiometricType} data. Please try again.`);
      setShowBiometricCapture(false);
      setCurrentBiometricType(null);
    }
  };

  const handleBiometricCancel = () => {
    setShowBiometricCapture(false);
    setCurrentBiometricType(null);
    setError('');
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError('');
      setRegistrationProgress('Preparing registration data...');
      
      // Validate biometric data
      if (biometricData.length === 0) {
        setError('Please register at least one biometric method');
        return;
      }
      
      setRegistrationProgress(`Processing ${biometricData.length} biometric samples...`);
      
      // Format data to match RegisterRequest interface
      const registerData = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        first_name: formData.firstName,
        last_name: formData.lastName,
        biometric_data: biometricData.map(data => ({
          biometric_type: data.type,
          image_data: data.imageData, // Already cleaned in handleBiometricData
        })),
      };
      
      console.log('Submitting registration data:', {
        ...registerData,
        biometric_data: registerData.biometric_data.map(bio => ({
          biometric_type: bio.biometric_type,
          image_data: bio.image_data.substring(0, 50) + '... (length: ' + bio.image_data.length + ')'
        }))
      });
      
      setRegistrationProgress('Sending data to server (this may take up to 10 minutes)...');
      
      await register(registerData);
      
      setRegistrationProgress('Registration successful! Redirecting...');
      setTimeout(() => navigate('/login'), 1000);
      
    } catch (err: any) {
      console.error('Registration error:', err);
      
      // Handle different error response structures
      let errorMessage = 'Registration failed. Please try again.';
      
      // Check if it's a timeout error
      if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
        errorMessage = 'Registration timed out. The server may be processing your biometric data. Please wait a few moments and try logging in, or try again with different biometric samples.';
      } else if (err.response?.data) {
        const errorData = err.response.data;
        
        if (typeof errorData === 'string') {
          errorMessage = errorData;
        } else if (errorData.detail) {
          if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail;
          } else if (Array.isArray(errorData.detail)) {
            // Handle Pydantic validation errors
            const validationErrors = errorData.detail.map((error: any) => {
              if (error.msg) {
                return `${error.loc?.join('.') || 'Field'}: ${error.msg}`;
              }
              return JSON.stringify(error);
            });
            errorMessage = validationErrors.join(', ');
          }
        } else if (errorData.message) {
          errorMessage = errorData.message;
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(typeof errorMessage === 'string' ? errorMessage : 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const biometricOptions = [
    {
      type: 'fingerprint' as const,
      icon: <Fingerprint />,
      label: 'Fingerprint',
      description: 'Scan your fingerprint',
      color: '#4caf50',
    },
    {
      type: 'face' as const,
      icon: <Face />,
      label: 'Face Recognition',
      description: 'Capture your face',
      color: '#2196f3',
    },
    {
      type: 'palmprint' as const,
      icon: <Security />,
      label: 'Palmprint',
      description: 'Scan your palm',
      color: '#ff9800',
    },
  ];

  if (showBiometricCapture && currentBiometricType) {
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
              Biometric Registration
            </Typography>
            
            <BiometricCapture
              type={currentBiometricType}
              onCapture={handleBiometricData}
              onCancel={handleBiometricCancel}
            />
          </Box>
        </Fade>
      </Container>
    );
  }

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Fade in={true} timeout={500}>
            <Box>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                Account Information
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="username"
                    label="Username"
                    value={formData.username}
                    onChange={handleInputChange}
                    required
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Person color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="email"
                    label="Email Address"
                    type="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Email color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="firstName"
                    label="First Name"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    required
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Person color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="lastName"
                    label="Last Name"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    required
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Person color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="password"
                    label="Password"
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={handleInputChange}
                    required
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
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="confirmPassword"
                    label="Confirm Password"
                    type={showPassword ? 'text' : 'password'}
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    required
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Lock color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>
              </Grid>
            </Box>
          </Fade>
        );
      
      case 1:
        return (
          <Fade in={true} timeout={500}>
            <Box>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                Biometric Registration
              </Typography>
              
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Register your biometric data for secure authentication. You can register multiple methods.
              </Typography>
              
              <Grid container spacing={3}>
                {biometricOptions.map((option) => {
                  const isRegistered = biometricData.some(data => data.type === option.type);
                  
                  return (
                    <Grid item xs={12} sm={6} md={4} key={option.type}>
                      <Paper
                        sx={{
                          p: { xs: 2, sm: 3 },
                          border: isRegistered ? `2px solid ${option.color}` : '1px solid #e0e0e0',
                          backgroundColor: isRegistered ? `${option.color}11` : 'white',
                          transition: 'all 0.3s ease',
                          cursor: 'pointer',
                          '&:hover': {
                            transform: 'translateY(-2px)',
                            boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                          }
                        }}
                        onClick={() => !isRegistered && handleBiometricCapture(option.type)}
                      >
                        <Box sx={{ 
                          display: 'flex', 
                          flexDirection: { xs: 'row', sm: 'column' },
                          alignItems: 'center', 
                          justifyContent: { xs: 'flex-start', sm: 'center' },
                          textAlign: { xs: 'left', sm: 'center' },
                          gap: { xs: 2, sm: 1 }
                        }}>
                          <Avatar sx={{ 
                            bgcolor: option.color, 
                            width: { xs: 40, sm: 48 },
                            height: { xs: 40, sm: 48 },
                            mb: { xs: 0, sm: 1 }
                          }}>
                              {option.icon}
                            </Avatar>
                          <Box sx={{ flex: { xs: 1, sm: 'none' } }}>
                            <Typography variant="subtitle1" sx={{ fontWeight: 600, fontSize: { xs: '0.875rem', sm: '1rem' } }}>
                                {option.label}
                              </Typography>
                            <Typography variant="body2" color="text.secondary" sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}>
                                {option.description}
                              </Typography>
                            {isRegistered && (
                              <Chip
                                icon={<CheckCircle />}
                                label="Registered"
                                color="success"
                                size="small"
                                sx={{ mt: 1 }}
                              />
                            )}
                          </Box>
                        </Box>
                      </Paper>
                    </Grid>
                  );
                })}
              </Grid>
            </Box>
          </Fade>
        );
      
      case 2:
        return (
          <Fade in={true} timeout={500}>
            <Box>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                Review & Submit
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 3, mb: 2 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                      Account Details
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                      <Typography variant="body2">
                        <strong>Username:</strong> {formData.username}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Name:</strong> {formData.firstName} {formData.lastName}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Email:</strong> {formData.email}
                      </Typography>
                    </Box>
                  </Paper>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 3, mb: 2 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                      Biometric Methods
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                      {biometricData.map((data) => {
                        const option = biometricOptions.find(opt => opt.type === data.type);
                        return (
                          <Box key={data.type} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <CheckCircle sx={{ color: option?.color, fontSize: 20 }} />
                            <Typography variant="body2">{option?.label}</Typography>
                          </Box>
                        );
                      })}
                    </Box>
                  </Paper>
                </Grid>
              </Grid>
            </Box>
          </Fade>
        );
      
      default:
        return null;
    }
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
      <Container maxWidth={activeStep === 1 ? "lg" : "md"}>
        <Fade in={true} timeout={500}>
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)', 
            backdropFilter: 'blur(10px)',
            boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
          }}>
            <CardContent sx={{ p: { xs: 2, sm: 3, md: 4 } }}>
              <Typography variant={isMobile ? 'h5' : 'h4'} align="center" gutterBottom sx={{ 
                fontWeight: 700, 
                background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 1,
              }}>
                Create Account
              </Typography>
              
              <Typography variant="body1" align="center" color="text.secondary" sx={{ mb: { xs: 2, sm: 4 } }}>
                Join our secure biometric authentication platform
              </Typography>

              <Box sx={{ mb: { xs: 2, sm: 4 } }}>
                <Stepper activeStep={activeStep} alternativeLabel>
                  {steps.map((label) => (
                    <Step key={label}>
                      <StepLabel sx={{
                        '& .MuiStepLabel-label': {
                          fontSize: { xs: '0.75rem', sm: '0.875rem' }
                        }
                      }}>{label}</StepLabel>
                    </Step>
                  ))}
                </Stepper>
              </Box>

              {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  {typeof error === 'string' ? error : JSON.stringify(error)}
                </Alert>
              )}

              <Box sx={{ minHeight: { xs: 300, sm: 400 } }}>
                {renderStepContent(activeStep)}
              </Box>

              <Box sx={{ 
                display: 'flex', 
                flexDirection: { xs: 'column', sm: 'row' },
                justifyContent: 'space-between', 
                gap: { xs: 2, sm: 0 },
                mt: { xs: 3, sm: 4 }
              }}>
                <Button
                  onClick={handleBack}
                  disabled={activeStep === 0}
                  startIcon={<ArrowBack />}
                  variant="outlined"
                  fullWidth={isMobile}
                >
                  Back
                </Button>

                {activeStep === steps.length - 1 ? (
                  <Button
                    onClick={handleSubmit}
                    disabled={loading}
                    startIcon={loading ? <CircularProgress size={20} /> : <PersonAdd />}
                    variant="contained"
                    sx={{
                      background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #5a6fd8 30%, #6a4190 90%)',
                      }
                    }}
                  >
                    {loading ? (registrationProgress || 'Creating Account...') : 'Create Account'}
                  </Button>
                ) : (
                  <Button
                    onClick={handleNext}
                    disabled={!validateStep(activeStep)}
                    endIcon={<ArrowForward />}
                    variant="contained"
                    sx={{
                      background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #5a6fd8 30%, #6a4190 90%)',
                      }
                    }}
                  >
                    Next
                  </Button>
                )}
                
                {/* Progress feedback during registration */}
                {loading && activeStep === steps.length - 1 && (
                  <Box sx={{ mt: 2, textAlign: 'center' }}>
                    <Typography variant="body2" color="text.secondary">
                      {registrationProgress || 'Processing your biometric data...'}
                    </Typography>
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                      This process may take up to 10 minutes due to biometric processing.
                    </Typography>
                  </Box>
                )}
              </Box>

              <Box sx={{ mt: 4, textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  Already have an account?{' '}
                  <Button
                    variant="text"
                    startIcon={<Login />}
                    onClick={() => navigate('/login')}
                    sx={{ textTransform: 'none' }}
                  >
                    Sign In
                  </Button>
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Fade>
      </Container>
    </Box>
  );
};

export default RegisterPage;
