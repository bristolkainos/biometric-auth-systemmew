import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  Grid,
  Chip,
  Divider,
  Link,
  IconButton,
  InputAdornment,
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Fingerprint,
  Face,
  CameraAlt,
  CheckCircle,
  ArrowBack,
  ArrowForward,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import BiometricCapture from '../components/BiometricCapture';

interface BiometricData {
  type: 'fingerprint' | 'face' | 'palmprint';
  imageData: string;
}

const steps = ['Account Information', 'Biometric Registration', 'Review & Submit'];

const RegisterPage: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [biometricData, setBiometricData] = useState<BiometricData[]>([]);
  const [currentBiometricType, setCurrentBiometricType] = useState<'fingerprint' | 'face' | 'palmprint'>('fingerprint');
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
  });

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleInputChange = (field: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleNext = () => {
    if (activeStep === 0) {
      // Validate account information
      if (!formData.username || !formData.email || !formData.password || !formData.confirmPassword || !formData.firstName || !formData.lastName) {
        setError('Please fill in all fields');
        return;
      }
      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match');
        return;
      }
      if (formData.password.length < 8) {
        setError('Password must be at least 8 characters long');
        return;
      }
      setError('');
    }
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const handleBiometricCapture = async (imageData: string): Promise<void> => {
    const newBiometric: BiometricData = {
      type: currentBiometricType,
      imageData,
    };
    
    // Replace if type already exists, otherwise add
    const existingIndex = biometricData.findIndex(bio => bio.type === currentBiometricType);
    if (existingIndex >= 0) {
      const updated = [...biometricData];
      updated[existingIndex] = newBiometric;
      setBiometricData(updated);
    } else {
      setBiometricData([...biometricData, newBiometric]);
    }
  };

  const handleRemoveBiometric = (type: string) => {
    setBiometricData(biometricData.filter(bio => bio.type !== type));
  };

  const handleSubmit = async () => {
    if (biometricData.length < 1) {
      setError('Please register at least 1 biometric method');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        first_name: formData.firstName,
        last_name: formData.lastName,
        biometric_data: biometricData.map(bio => ({
          biometric_type: bio.type,
          image_data: bio.imageData,
        })),
      });
      
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getBiometricIcon = (type: string) => {
    switch (type) {
      case 'fingerprint': return <Fingerprint />;
      case 'face': return <Face />;
      case 'palmprint': return <CameraAlt />;
      default: return <CameraAlt />;
    }
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box component="form">
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="First Name"
                  value={formData.firstName}
                  onChange={handleInputChange('firstName')}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Last Name"
                  value={formData.lastName}
                  onChange={handleInputChange('lastName')}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Username"
                  value={formData.username}
                  onChange={handleInputChange('username')}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange('email')}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Password"
                  type={showPassword ? 'text' : 'password'}
                  value={formData.password}
                  onChange={handleInputChange('password')}
                  required
                  InputProps={{
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
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Confirm Password"
                  type={showPassword ? 'text' : 'password'}
                  value={formData.confirmPassword}
                  onChange={handleInputChange('confirmPassword')}
                  required
                />
              </Grid>
            </Grid>
          </Box>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Register Biometric Data
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Please register at least 2 biometric methods for enhanced security.
            </Typography>

            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Select Biometric Type:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                <Button
                  variant={currentBiometricType === 'fingerprint' ? 'contained' : 'outlined'}
                  startIcon={<Fingerprint />}
                  onClick={() => setCurrentBiometricType('fingerprint')}
                  size="small"
                >
                  Fingerprint
                </Button>
                <Button
                  variant={currentBiometricType === 'face' ? 'contained' : 'outlined'}
                  startIcon={<Face />}
                  onClick={() => setCurrentBiometricType('face')}
                  size="small"
                >
                  Face ID
                </Button>
                <Button
                  variant={currentBiometricType === 'palmprint' ? 'contained' : 'outlined'}
                  startIcon={<CameraAlt />}
                  onClick={() => setCurrentBiometricType('palmprint')}
                  size="small"
                >
                  Palmprint
                </Button>
              </Box>
            </Box>

            <BiometricCapture
              type={currentBiometricType}
              onCapture={handleBiometricCapture}
              onCancel={() => {}}
            />

            {biometricData.length > 0 && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Registered Biometrics:
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  {biometricData.map((bio, index) => (
                    <Chip
                      key={index}
                      icon={getBiometricIcon(bio.type)}
                      label={bio.type.charAt(0).toUpperCase() + bio.type.slice(1)}
                      onDelete={() => handleRemoveBiometric(bio.type)}
                      color="primary"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Box>
            )}
          </Box>
        );

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Review Your Information
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Name
                </Typography>
                <Typography variant="body1">
                  {formData.firstName} {formData.lastName}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Username
                </Typography>
                <Typography variant="body1">
                  {formData.username}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle2" color="text.secondary">
                  Email
                </Typography>
                <Typography variant="body1">
                  {formData.email}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle2" color="text.secondary">
                  Biometric Methods ({biometricData.length}/3)
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 1 }}>
                  {biometricData.map((bio, index) => (
                    <Chip
                      key={index}
                      icon={getBiometricIcon(bio.type)}
                      label={bio.type.charAt(0).toUpperCase() + bio.type.slice(1)}
                      color="success"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Grid>
            </Grid>
          </Box>
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
        p: 2,
      }}
    >
      <Card sx={{ maxWidth: 800, width: '100%', boxShadow: 3 }}>
        <CardContent sx={{ p: 4 }}>
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
              Create Account
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Register with biometric authentication for enhanced security
            </Typography>
          </Box>

          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {renderStepContent(activeStep)}

          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Button
              disabled={activeStep === 0}
              onClick={handleBack}
              startIcon={<ArrowBack />}
            >
              Back
            </Button>
            
            <Box>
              {activeStep === steps.length - 1 ? (
                <Button
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={loading || biometricData.length < 2}
                  startIcon={loading ? <CircularProgress size={20} /> : <CheckCircle />}
                >
                  {loading ? 'Creating Account...' : 'Create Account'}
                </Button>
              ) : (
                <Button
                  variant="contained"
                  onClick={handleNext}
                  endIcon={<ArrowForward />}
                >
                  Next
                </Button>
              )}
            </Box>
          </Box>

          <Divider sx={{ my: 3 }}>
            <Typography variant="body2" color="text.secondary">
              OR
            </Typography>
          </Divider>

          <Box sx={{ textAlign: 'center' }}>
            <Link href="/login" variant="body2" sx={{ cursor: 'pointer' }}>
              Already have an account? Login here
            </Link>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default RegisterPage; 