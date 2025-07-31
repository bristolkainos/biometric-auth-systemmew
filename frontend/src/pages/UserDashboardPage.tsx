import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  CircularProgress,
  Alert,
  Chip,
  Avatar,
  IconButton,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Paper,
} from '@mui/material';
import {
  Person,
  Security,
  Email,
  CalendarToday,
  AccessTime,
  Fingerprint,
  Face,
  Download,
  ArrowBack,
  GetApp,
  Analytics,
  Timeline,
} from '@mui/icons-material';
import { authService } from '../services/authService';

// Chart.js imports
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Tooltip as ChartTooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Doughnut } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  ChartTooltip,
  Legend,
  Filler
);

interface UserDashboardPageProps {}

interface UserData {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
  biometric_methods?: string[];
  login_attempts?: any[];
  analytics?: any;
}

interface LoginTrendItem {
  date: string;
  logins: number;
}

const UserDashboardPage: React.FC<UserDashboardPageProps> = () => {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [user, setUser] = useState<UserData | null>(null);
  const [analytics, setAnalytics] = useState<any>(null);
  const [loginAttempts, setLoginAttempts] = useState<any[]>([]);
  const [biometricMethods, setBiometricMethods] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);



  useEffect(() => {
    const fetchUserData = async () => {
      try {
        setLoading(true);
        const response = await authService.getUserDashboardData(parseInt(userId || '1'));
        setUser(response.user);
        setAnalytics(response.analytics);
        setLoginAttempts(response.login_attempts);
        setBiometricMethods(response.biometric_methods);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching user data:', err);
        setError('Failed to load user data');
        setLoading(false);
      }
    };

    if (userId) {
      fetchUserData();
    }
  }, [userId]);

  const handleDownloadUserData = () => {
    if (!user) return;

    const userData = {
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
        is_active: user.is_active,
        is_verified: user.is_verified,
        created_at: user.created_at,
        last_login: user.last_login,
      },
      analytics: user.analytics,
      login_attempts: user.login_attempts,
    };

    const blob = new Blob([JSON.stringify(userData, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `user_${user.username}_data.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadAnalytics = () => {
    if (!user?.analytics) return;

    const analyticsData = {
      user_id: user.id,
      username: user.username,
      analytics: user.analytics,
      generated_at: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(analyticsData, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `user_${user.username}_analytics.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !user) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">{error || 'User not found'}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <IconButton onClick={() => navigate('/admin/dashboard')} sx={{ mr: 2 }}>
          <ArrowBack />
        </IconButton>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h4" gutterBottom>
            User Dashboard
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Viewing data for {user.first_name} {user.last_name}
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<GetApp />}
            onClick={handleDownloadAnalytics}
          >
            Download Analytics
          </Button>
          <Button
            variant="contained"
            startIcon={<Download />}
            onClick={handleDownloadUserData}
          >
            Download All Data
          </Button>
        </Box>
      </Box>

      {/* User Info Card */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Avatar sx={{ width: 64, height: 64, mr: 2 }}>
              {user.first_name.charAt(0)}
            </Avatar>
            <Box sx={{ flexGrow: 1 }}>
              <Typography variant="h5">
                {user.first_name} {user.last_name}
              </Typography>
              <Typography variant="body1" color="text.secondary">
                @{user.username}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Chip
                label={user.is_active ? 'Active' : 'Inactive'}
                color={user.is_active ? 'success' : 'error'}
                icon={<Person />}
              />
              <Chip
                label={user.is_verified ? 'Verified' : 'Unverified'}
                color={user.is_verified ? 'success' : 'warning'}
                icon={<Security />}
              />
            </Box>
          </Box>
          
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Email sx={{ mr: 1, color: 'text.secondary' }} />
                <Typography variant="body2">{user.email}</Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <CalendarToday sx={{ mr: 1, color: 'text.secondary' }} />
                <Typography variant="body2">
                  Member since {new Date(user.created_at).toLocaleDateString()}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <AccessTime sx={{ mr: 1, color: 'text.secondary' }} />
                <Typography variant="body2">
                  Last login: {user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Fingerprint sx={{ mr: 1, color: 'text.secondary' }} />
                <Typography variant="body2">
                  Biometric methods: {user.biometric_methods?.join(', ') || 'None'}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
          <Tab label="Analytics" icon={<Analytics />} />
          <Tab label="Login History" icon={<Timeline />} />
          <Tab label="Biometric Data" icon={<Fingerprint />} />
        </Tabs>
      </Paper>

      {/* Tab Content */}
      {activeTab === 0 && (
        <Grid container spacing={3}>
          {/* Analytics Overview */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Login Statistics
                </Typography>
                <Box sx={{ textAlign: 'center', py: 2 }}>
                  <Typography variant="h3" color="primary">
                    {analytics?.successRate || 0}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Success Rate
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Total Logins:</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {analytics?.totalLogins || 0}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Successful:</Typography>
                  <Typography variant="body2" color="success.main" fontWeight="bold">
                    {analytics?.successfulLogins || 0}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2">Failed:</Typography>
                  <Typography variant="body2" color="error.main" fontWeight="bold">
                    {analytics?.failedLogins || 0}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Biometric Usage Chart */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Biometric Usage
                </Typography>
                <Doughnut
                  data={{
                    labels: Object.keys(analytics?.biometricUsage || {}),
                    datasets: [
                      {
                        data: Object.values(analytics?.biometricUsage || {}),
                        backgroundColor: COLORS,
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    plugins: {
                      legend: {
                        position: 'top',
                      },
                      tooltip: {
                        callbacks: {
                          label: function(context: any) {
                            let label = context.dataset.label || '';
                            if (label) {
                              label += ': ';
                            }
                            if (context.parsed !== null) {
                              label += context.parsed;
                            }
                            return label;
                          }
                        }
                      }
                    }
                  }}
                />
              </CardContent>
            </Card>
          </Grid>

          {/* Login Trend */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Login Trend (Last 6 Days)
                </Typography>
                <Line
                  data={{
                    labels: analytics?.loginTrend?.map((item: LoginTrendItem) => new Date(item.date).toLocaleDateString()) || [],
                    datasets: [
                      {
                        label: 'Logins',
                        data: analytics?.loginTrend?.map((item: LoginTrendItem) => item.logins) || [],
                        borderColor: '#8884d8',
                        backgroundColor: 'rgba(136, 132, 216, 0.5)',
                        fill: true,
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    plugins: {
                      legend: {
                        position: 'top',
                      },
                      tooltip: {
                        callbacks: {
                          label: function(context: any) {
                            let label = context.dataset.label || '';
                            if (label) {
                              label += ': ';
                            }
                            if (context.parsed && context.parsed.y !== null) {
                              label += context.parsed.y;
                            }
                            return label;
                          }
                        }
                      }
                    }
                  }}
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Recent Login Attempts
            </Typography>
            <List>
              {loginAttempts.map((attempt, index) => (
                <React.Fragment key={attempt.id || index}>
                  <ListItem>
                    <ListItemIcon>
                      {attempt.success ? (
                        <Chip label="Success" color="success" size="small" />
                      ) : (
                        <Chip label="Failed" color="error" size="small" />
                      )}
                    </ListItemIcon>
                    <ListItemText
                      primary={`${attempt.biometric_type} authentication`}
                      secondary={new Date(attempt.created_at).toLocaleString()}
                    />
                  </ListItem>
                  {index < loginAttempts.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </CardContent>
        </Card>
      )}

      {activeTab === 2 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Biometric Methods
            </Typography>
            <Grid container spacing={2}>
              {biometricMethods.map((method) => (
                <Grid item xs={12} md={6} key={method.id}>
                  <Card variant="outlined">
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        {method.type === 'face' ? (
                          <Face sx={{ mr: 1, color: 'primary.main' }} />
                        ) : (
                          <Fingerprint sx={{ mr: 1, color: 'primary.main' }} />
                        )}
                        <Typography variant="h6" sx={{ textTransform: 'capitalize' }}>
                          {method.type} Recognition
                        </Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        {method.type === 'face' ? 'Facial recognition enabled' : 'Fingerprint scanning enabled'}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Created: {new Date(method.created_at).toLocaleDateString()}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default UserDashboardPage; 