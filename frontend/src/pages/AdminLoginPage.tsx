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
  CircularProgress,
  Paper,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  AdminPanelSettings,
  Security,
  Lock,
  Visibility,
  VisibilityOff,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const AdminLoginPage: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { adminLogin } = useAuth();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const handleInputChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.username || !formData.password) {
      setError('Please fill in all fields');
      return;
    }

    try {
      setLoading(true);
      setError('');
      await adminLogin(formData.username, formData.password);
      navigate('/admin/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid admin credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
        p: { xs: 1, sm: 2 },
      }}
    >
      <Card sx={{ 
        maxWidth: { xs: '100%', sm: 450 }, 
        width: '100%', 
        boxShadow: 3,
        mx: { xs: 1, sm: 0 }
      }}>
        <CardContent sx={{ p: { xs: 2, sm: 3, md: 4 } }}>
          <Box sx={{ textAlign: 'center', mb: { xs: 3, sm: 4 } }}>
            <Paper
              sx={{
                width: { xs: 60, sm: 80 },
                height: { xs: 60, sm: 80 },
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mx: 'auto',
                mb: 2,
                bgcolor: 'primary.main',
                color: 'white',
              }}
            >
              <AdminPanelSettings sx={{ fontSize: { xs: 30, sm: 40 } }} />
            </Paper>
            <Typography 
              variant={isMobile ? 'h5' : 'h4'}
              component="h1" 
              gutterBottom 
              sx={{ fontWeight: 600 }}
            >
              Admin Portal
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Secure administrative access to biometric authentication system
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Admin Username"
              value={formData.username}
              onChange={handleInputChange('username')}
              margin="normal"
              required
              autoFocus
              size={isMobile ? 'small' : 'medium'}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Security color="action" />
                  </InputAdornment>
                ),
              }}
            />
            
            <TextField
              fullWidth
              label="Admin Password"
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={handleInputChange('password')}
              margin="normal"
              required
              size={isMobile ? 'small' : 'medium'}
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
                      size={isMobile ? 'small' : 'medium'}
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
              size={isMobile ? 'medium' : 'large'}
              disabled={loading || !formData.username || !formData.password}
              sx={{ mt: { xs: 3, sm: 4 }, mb: 2, py: { xs: 1.2, sm: 1.5 } }}
            >
              {loading ? <CircularProgress size={24} /> : 'Access Admin Portal'}
            </Button>
          </Box>

          <Box sx={{ textAlign: 'center', mt: { xs: 2, sm: 3 } }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              For security reasons, this portal is restricted to authorized administrators only.
            </Typography>
            <Button
              variant="text"
              size="small"
              onClick={() => navigate('/login')}
              sx={{ mt: 1 }}
            >
              Back to User Login
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default AdminLoginPage; 