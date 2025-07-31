import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Avatar,
  Button,
  Tabs,
  Tab,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Paper,
  IconButton,
  Alert,
  CircularProgress,
  useTheme as useMuiTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Person,
  Fingerprint,
  Face,
  CameraAlt,
  Security,
  Timeline,
  Settings,
  Logout,
  Refresh,
  Visibility,
  VisibilityOff,
  CheckCircle,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import BiometricDetails from '../components/BiometricDetails';
import FeatureExtractionChart from '../components/FeatureExtractionChart';
import LoginHistory from '../components/LoginHistory';
import BiometricAnalysisDashboard from '../components/BiometricAnalysisDashboard';
import BlockchainAnalytics from '../components/BlockchainAnalytics';
import ThemeToggle from '../components/ThemeToggle';
import { authService } from '../services/authService';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`dashboard-tabpanel-${index}`}
      aria-labelledby={`dashboard-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

const DashboardPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [userData, setUserData] = useState<any>(null);
  const [biometricData, setBiometricData] = useState<any[]>([]);
  const [loginHistory, setLoginHistory] = useState<any[]>([]);
  
  const { user, logout } = useAuth();
  const { getGradient } = useTheme();
  const navigate = useNavigate();
  const theme = useMuiTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const fetchUserData = React.useCallback(async (forceRefresh = false) => {
    try {
      setError(null); // Clear any previous errors
      if (forceRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      
      if (!user) return;

      // Fetch real user data from backend - this should now be much faster!
      console.log('Fetching user dashboard data for user ID:', user.id);
      const response = await authService.getUserDashboardData(user.id);
      console.log('Fetched user data:', response);
      
      // Transform backend data to match frontend expectations
      const { user_details, biometric_data, login_history } = response;
      
      // Transform biometric data to match BiometricDetails component expectations
      const transformedBiometricData = (biometric_data || []).map((bio: any) => {
        // Ensure quality_score is properly converted to confidence (0-1 scale)
        let confidence = 0.85; // Default fallback
        if (typeof bio.quality_score === 'number') {
          confidence = Math.max(0, Math.min(1, bio.quality_score)); // Clamp between 0-1
        }
        
        return {
          id: bio.id,
          type: bio.type,
          confidence: confidence,
          registeredAt: bio.created_at || new Date().toISOString(),
          lastUsed: bio.updated_at || bio.created_at || new Date().toISOString(),
          status: 'active' // All returned biometric data should be active
        };
      });
      
      setUserData(user_details || user); // Fallback to user context if no detailed data
      setBiometricData(transformedBiometricData);
      setLoginHistory(login_history || []);

    } catch (error: any) {
      console.error("Failed to fetch user data:", error);
      console.error("Error details:", {
        message: error?.message,
        status: error?.response?.status,
        statusText: error?.response?.statusText,
        data: error?.response?.data,
        config: error?.config?.url
      });
      
      // Temporary fallback: provide some basic data structure
      console.log("Using fallback data structure");
      setUserData(user);
      setBiometricData([
        {
          id: 1,
          type: 'fingerprint',
          confidence: 0.92,
          registeredAt: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          status: 'active'
        },
        {
          id: 2,
          type: 'face',
          confidence: 0.88,
          registeredAt: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          status: 'active'
        },
        {
          id: 3,
          type: 'palmprint',
          confidence: 0.85,
          registeredAt: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          status: 'active'
        }
      ]);
      setLoginHistory([]);
      
      setError(error?.response?.data?.detail || error?.message || "Failed to load dashboard data");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [user]);

  const handleRetry = () => {
    fetchUserData(true);
  };

  useEffect(() => {
    if (user) {
      console.log('Current user:', user);
      fetchUserData();
    }
  }, [user, fetchUserData]);  const handleRefresh = () => {
    fetchUserData(true);
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleLogout = () => {
    // Clear all cache when logging out
    authService.clearAllCache();
    logout();
    navigate('/login');
  };

  const getBiometricIcon = (type: string) => {
    switch (type) {
      case 'fingerprint':
        return <Fingerprint />;
      case 'face':
        return <Face />;
      case 'palmprint':
        return <CameraAlt />;
      default:
        return <Security />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'inactive':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          gap: 2,
        }}
      >
        <CircularProgress size={60} />
        <Typography variant="h6" color="text.secondary">
          Loading your dashboard...
        </Typography>
        <Typography variant="body2" color="text.secondary">
          This should be much faster now!
        </Typography>
      </Box>
    );
  }

  // Show error state with retry option
  if (error && !refreshing) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          gap: 2,
          p: 3,
        }}
      >
        <Alert severity="error" sx={{ maxWidth: 500 }}>
          <Typography variant="h6">Failed to load dashboard</Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            {error}
          </Typography>
        </Alert>
        <Button 
          variant="contained" 
          onClick={handleRetry}
          startIcon={<Refresh />}
        >
          Try Again
        </Button>
        <Button 
          variant="outlined" 
          onClick={handleLogout}
          startIcon={<Logout />}
        >
          Logout
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
      {/* Header */}
      <Paper sx={{ p: { xs: 1, sm: 2 }, mb: 3, boxShadow: 1 }}>
        <Container maxWidth="xl">
          <Box sx={{ 
            display: 'flex', 
            flexDirection: { xs: 'column', sm: 'row' },
            justifyContent: 'space-between', 
            alignItems: { xs: 'flex-start', sm: 'center' },
            gap: { xs: 2, sm: 0 }
          }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Avatar sx={{ bgcolor: 'primary.main' }}>
                <Person />
              </Avatar>
              <Box>
                <Typography variant={isMobile ? 'subtitle1' : 'h6'}>
                  Welcome, {userData?.first_name} {userData?.last_name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {userData?.email}
                </Typography>
              </Box>
            </Box>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <ThemeToggle size="small" />
              <IconButton onClick={handleRefresh} size="small" disabled={refreshing}>
                {refreshing ? <CircularProgress size={20} /> : <Refresh />}
              </IconButton>
              <Button
                variant="outlined"
                startIcon={<Logout />}
                onClick={handleLogout}
                size={isMobile ? 'small' : 'medium'}
              >
                <Box component="span" sx={{ display: { xs: 'none', sm: 'inline' } }}>
                  Logout
                </Box>
              </Button>
            </Box>
          </Box>
        </Container>
      </Paper>

      <Container maxWidth="xl">
        <Grid container spacing={{ xs: 2, md: 3 }}>
          {/* Sidebar */}
          <Grid item xs={12} lg={3}>
            <Card sx={{ mb: 3 }}>
              <CardContent sx={{ p: { xs: 2, sm: 3 } }}>
                <Typography variant="h6" gutterBottom>
                  Account Status
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <Security color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Account Active"
                      secondary="Your account is secure and active"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Timeline color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary={`${biometricData.length} Biometric Methods`}
                      secondary="Registered for authentication"
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>

            <Card sx={{ display: { xs: 'block', lg: 'block' } }}>
              <CardContent sx={{ p: { xs: 2, sm: 3 } }}>
                <Typography variant="h6" gutterBottom>
                  Biometric Methods
                </Typography>
                <Box sx={{ 
                  display: 'flex', 
                  flexDirection: { xs: 'row', lg: 'column' }, 
                  flexWrap: { xs: 'wrap', lg: 'nowrap' },
                  gap: 1 
                }}>
                  {biometricData.map((bio) => (
                    <Chip
                      key={bio.id}
                      icon={getBiometricIcon(bio.type)}
                      label={`${bio.type.charAt(0).toUpperCase() + bio.type.slice(1)} (${Math.round(bio.confidence * 100)}%)`}
                      color={getStatusColor(bio.status) as any}
                      variant="outlined"
                      size="small"
                    />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Main Content */}
          <Grid item xs={12} lg={9}>
            <Card>
              <CardContent sx={{ p: { xs: 1, sm: 2, md: 3 } }}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
                  <Tabs 
                    value={tabValue} 
                    onChange={handleTabChange}
                    variant="scrollable"
                    scrollButtons="auto"
                    allowScrollButtonsMobile
                    sx={{
                      '& .MuiTab-root': {
                        minWidth: { xs: 'auto', sm: 120 },
                        fontSize: { xs: '0.75rem', sm: '0.875rem' },
                        padding: { xs: '6px 8px', sm: '12px 16px' }
                      }
                    }}
                  >
                    <Tab label="Overview" />
                    <Tab label="Biometric Data" />
                    <Tab label="Login History" />
                    <Tab label="Analytics" />
                    <Tab label="Blockchain" />
                  </Tabs>
                </Box>

                <TabPanel value={tabValue} index={0}>
                  {/* Overview */}
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Security Overview
                          </Typography>
                          <List dense>
                            <ListItem>
                              <ListItemIcon>
                                <CheckCircle color={user?.is_verified ? "success" : "warning"} />
                              </ListItemIcon>
                              <ListItemText 
                                primary={user?.is_verified ? "Account Verified" : "Account Pending Verification"} 
                                secondary={user?.is_verified ? "Your account is verified and secure" : "Please verify your account"}
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemIcon>
                                <Security color="primary" />
                              </ListItemIcon>
                              <ListItemText 
                                primary="Multi-Factor Authentication" 
                                secondary={`${biometricData.length} biometric method${biometricData.length !== 1 ? 's' : ''} registered`}
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemIcon>
                                <Timeline color="primary" />
                              </ListItemIcon>
                              <ListItemText 
                                primary="Account Status" 
                                secondary={user?.is_active ? "Active" : "Inactive"}
                              />
                            </ListItem>
                          </List>
                        </CardContent>
                      </Card>
                    </Grid>
                    
                    <Grid item xs={12} md={6}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Recent Activity
                          </Typography>
                          {loginHistory.length > 0 ? (
                            <>
                              <Typography variant="body2" color="text.secondary">
                                Last login: {new Date(loginHistory[0].timestamp).toLocaleString()}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                Login method: {loginHistory[0].biometricType || 'Password'}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                Status: {loginHistory[0].success ? 'Successful' : 'Failed'}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                IP Address: {loginHistory[0].ipAddress}
                              </Typography>
                            </>
                          ) : (
                            <Typography variant="body2" color="text.secondary">
                              No login history available
                            </Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </TabPanel>

                <TabPanel value={tabValue} index={1}>
                  <BiometricDetails biometricData={biometricData} />
                </TabPanel>

                <TabPanel value={tabValue} index={2}>
                  <LoginHistory loginHistory={loginHistory} />
                </TabPanel>

                <TabPanel value={tabValue} index={3}>
                  <BiometricAnalysisDashboard />
                </TabPanel>

                <TabPanel value={tabValue} index={4}>
                  <BlockchainAnalytics userData={userData} />
                </TabPanel>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default DashboardPage; 