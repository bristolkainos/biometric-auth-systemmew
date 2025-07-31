import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  IconButton,
  Tooltip,
  List,
  ListItem,
  ListItemText,
  LinearProgress,
  Tabs,
  Tab,
  Stack,
  Divider,
} from '@mui/material';
import {
  Face as FaceIcon,
  Fingerprint as FingerprintIcon,
  RemoveRedEye as EyeIcon,
  VoiceChat as VoiceIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Download as DownloadIcon,
  Visibility as VisibilityIcon,
  History as HistoryIcon,
  Analytics as AnalyticsIcon,
  Schedule as ScheduleIcon,
  Security as SecurityIcon,
  GetApp as GetAppIcon,
  Assessment as AssessmentIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';
import { authService } from '../services/authService';
import VisualizationModal from './VisualizationModal';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  ChartTooltip,
  Legend
);

interface BackendVisualization {
  title?: string;
  description?: string;
  data?: string;
}

interface BiometricAnalysisResponse {
  biometric_id: number;
  biometric_type: string;
  created_at: string;
  analysis: any;
  features: any;
  processing_steps: any[];
  visualizations: { [key: string]: BackendVisualization };
  hash: string;
}

interface DashboardData {
  overview: {
    total_users: number;
    total_login_attempts: number;
    successful_logins: number;
    failed_logins: number;
    success_rate: number;
    registered_biometrics: number;
  };
  user_activity: { [date: string]: { successful: number; failed: number } };
  biometric_distribution: { [type: string]: number };
  success_rates: { [type: string]: number };
  recent_activity: {
    timestamp: string;
    user: string;
    type: string;
    success: boolean;
    ip_address: string;
  }[];
}

interface PersonalAnalytics {
  temporal_patterns: {
    hourly_usage: { [hour: string]: number };
    daily_usage: { [day: string]: number };
  };
  quality_metrics: Array<{
    type: string;
    quality_score: number;
    enrollment_date: string | null;
    last_used: string | null;
  }>;
  biometric_entries: Array<{
    id: number;
    type: string;
    created_at: string | null;
    features_count: number;
    processing_steps: number;
    processing_steps_details: any[];
    visualizations_count: number;
    quality_score: number;
    processing_time: string;
    analysis_data: any;
    has_analysis: boolean;
  }>;
  security_insights: {
    total_attempts: number;
    successful_attempts: number;
    failed_attempts: number;
    success_rate: number;
    success_rate_by_type: { [type: string]: number };
    recent_failed_attempts: Array<{
      timestamp: string;
      type: string;
      ip_address: string;
    }>;
    common_locations: Array<{
      ip: string;
      count: number;
    }>;
    risk_level: string;
  };
}

const BiometricAnalysisDashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  
  // New state variables for enhanced features
  const [personalAnalytics, setPersonalAnalytics] = useState<PersonalAnalytics | null>(null);
  const [selectedTab, setSelectedTab] = useState(0);
  const [downloadLoading, setDownloadLoading] = useState(false);
  const [regenerateLoading, setRegenerateLoading] = useState(false);
  
  // Visualization modal state
  const [visualizationModalOpen, setVisualizationModalOpen] = useState(false);
  const [selectedEntry, setSelectedEntry] = useState<any>(null);

  useEffect(() => {
    const loadInitialData = async () => {
      await fetchDashboardData();
      // Personal analytics will be set from the dashboard data transformation
      // But if we need separate personal analytics, uncomment the line below
      // await fetchPersonalAnalytics();
    };
    
    loadInitialData();
  }, []);

  const fetchDashboardData = async (forceRefresh = false) => {
    try {
      if (forceRefresh) {
        // Clear cache to force fresh data
        authService.clearUserCache();
      } else {
        setLoading(true);
      }
      setError(null);
      
      console.log('🔍 Fetching biometric dashboard data...');
      // Prefer local backend for development; fallback to env or online only if not set
      const localApiUrl = process.env.REACT_APP_API_URL;
      console.log('📡 API URL:', process.env.REACT_APP_API_URL || localApiUrl);
      
      // Check if user is authenticated
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.error('❌ No access token found');
        setError('Authentication required. Please login again.');
        return;
      }
      
      console.log('✅ Access token found, making request...');
      
      // For personal analytics dashboard, we should use personal analytics instead of global dashboard
      // The global dashboard is for admin use and may timeout with large datasets
      const response = await authService.getPersonalAnalytics();
      console.log('✅ Personal analytics data received:', response);
      
      // Transform personal analytics response to match expected dashboard format
      const dashboardResponse = {
        overview: {
          total_users: 1, // Personal view, so just this user
          total_login_attempts: response.security_insights?.total_attempts || 0,
          successful_logins: response.security_insights?.successful_attempts || 0,
          failed_logins: response.security_insights?.failed_attempts || 0,
          success_rate: response.security_insights?.success_rate || 0,
          registered_biometrics: response.biometric_entries?.length || 0
        },
        user_activity: response.temporal_patterns || {},
        biometric_distribution: response.biometric_entries?.reduce((acc: any, entry: any) => {
          acc[entry.type] = (acc[entry.type] || 0) + 1;
          return acc;
        }, {}) || {},
        success_rates: response.security_insights?.success_rate_by_type || {},
        recent_activity: response.security_insights?.recent_failed_attempts?.map((attempt: any) => ({
          timestamp: attempt.timestamp,
          user: 'You',
          type: attempt.type,
          success: false,
          ip_address: attempt.ip_address
        })) || []
      };
      
      setDashboardData(dashboardResponse);
      setPersonalAnalytics(response); // Also set the personal analytics data
    } catch (err: any) {
      console.error('❌ Error fetching dashboard data:', err);
      console.error('Error details:', {
        message: err.message,
        status: err.response?.status,
        statusText: err.response?.statusText,
        data: err.response?.data
      });
      
      if (err.response?.status === 401) {
        setError('Authentication failed. Please login again.');
      } else if (err.response?.status === 403) {
        setError('Access denied. You do not have permission to view this data.');
      } else if (err.code === 'ERR_NETWORK') {
        setError('Network error. Please check your connection and try again.');
      } else {
        setError(err.response?.data?.detail || 'Failed to fetch dashboard data');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchPersonalAnalytics = async (forceRefresh = false) => {
    try {
      if (forceRefresh) {
        setAnalysisLoading(true);
        // Clear cache to force fresh data
        authService.clearUserCache();
      }
      
      // If we already have personal analytics from the dashboard fetch, don't duplicate the call
      if (personalAnalytics && !forceRefresh) {
        return;
      }
      
      const response = await authService.getPersonalAnalytics();
      console.log('Personal analytics response:', response);
      setPersonalAnalytics(response);
    } catch (err: any) {
      console.error('Error fetching personal analytics:', err);
      // Don't set error state since this is secondary data
    } finally {
      setAnalysisLoading(false);
    }
  };


  const downloadDashboardReport = async (format: 'json' | 'zip') => {
    try {
      setDownloadLoading(true);
      const response = await authService.get(`/biometric/dashboard/download?format=${format}`, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `my_biometric_report.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      console.error('Error downloading report:', err);
      setError('Failed to download report');
    } finally {
      setDownloadLoading(false);
    }
  };

  const handleRegenerateAnalysis = async () => {
    try {
      setRegenerateLoading(true);
      setError(null);
      console.log('🔄 Starting biometric analysis regeneration...');
      const response = await authService.post('/biometric/regenerate-analysis');
      console.log('Regeneration response:', response.data);
      if (response.data.success) {
        // Show success message
        const summary = response.data.summary;
        const successMsg = `Analysis regenerated successfully! ` +
          `${summary.regenerated} entries updated, ${summary.skipped} entries skipped.`;
        // You could also show this in a snackbar or alert
        console.log('✅ ' + successMsg);
        // Refresh the dashboard data to show updated analysis
        await fetchDashboardData();
        await fetchPersonalAnalytics();
      } else {
        // Show as much error info as possible
        let backendMsg = response.data.message || response.data.detail || JSON.stringify(response.data);
        setError('Failed to regenerate analysis: ' + backendMsg);
      }
    } catch (err: any) {
      console.error('Error regenerating analysis:', err);
      // Show as much error info as possible from backend
      let backendMsg = err.response?.data?.detail || err.response?.data?.message || JSON.stringify(err.response?.data) || err.message;
      setError('Failed to regenerate biometric analysis: ' + backendMsg);
    } finally {
      setRegenerateLoading(false);
    }
  };

  const getBiometricIcon = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'face':
        return <FaceIcon />;
      case 'fingerprint':
        return <FingerprintIcon />;
      case 'iris':
        return <EyeIcon />;
      case 'voice':
        return <VoiceIcon />;
      default:
        return <FaceIcon />;
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

    const handleViewVisualization = async (entry: any) => {
    console.log('🔍 handleViewVisualization called with entry:', entry);
    try {
      // If entry doesn't have full analysis data, fetch it from the API
      if (!entry.analysis_data || !entry.analysis_data.generated_visualizations) {
        console.log('📡 Fetching detailed analysis for biometric ID:', entry.id);
        const analysisResponse: BiometricAnalysisResponse = await authService.getBiometricAnalysis(entry.id);
        
        console.log('📊 Raw API response:', analysisResponse);
        
        // Convert backend visualizations format to frontend expected format
        const generatedVisualizations = [];
        if (analysisResponse.visualizations) {
          for (const [key, viz] of Object.entries(analysisResponse.visualizations)) {
            generatedVisualizations.push({
              id: key,
              type: key,
              title: viz.title || key,
              description: viz.description || `${key} visualization`,
              data: viz.data, // This should be the base64 data URL
              format: 'image/png'
            });
          }
        }
        
        console.log('🎨 Converted visualizations:', generatedVisualizations);
        
        // Update the entry with the properly formatted analysis data
        const enhancedEntry = {
          ...entry,
          analysis_data: {
            ...analysisResponse.analysis,
            generated_visualizations: generatedVisualizations
          }
        };
        setSelectedEntry(enhancedEntry);
      } else {
        console.log('📋 Using existing analysis data for entry:', entry.id);
        setSelectedEntry(entry);
      }
      console.log('🖼️ Opening visualization modal');
      setVisualizationModalOpen(true);
    } catch (error) {
      console.error('❌ Error fetching biometric analysis:', error);
      // Show the modal anyway with whatever data we have
      setSelectedEntry(entry);
      setVisualizationModalOpen(true);
    }
  };

  const renderTimePatterns = () => {
    if (!personalAnalytics || !personalAnalytics.temporal_patterns) {
      return (
        <Typography variant="body2" color="text.secondary">
          No time pattern data available.
        </Typography>
      );
    }

    const { hourly_usage, daily_usage } = personalAnalytics.temporal_patterns;

    return (
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <ScheduleIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
                Hourly Usage Patterns
              </Typography>
              <Box sx={{ height: 300, p: 2 }}>
                <Bar
                  data={{
                    labels: Object.keys(hourly_usage).map(hour => `${hour}:00`),
                    datasets: [{
                      label: 'Login Count',
                      data: Object.values(hourly_usage),
                      backgroundColor: 'rgba(76, 175, 80, 0.6)',
                      borderColor: '#4caf50',
                      borderWidth: 1
                    }]
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'top' as const,
                      }
                    },
                    scales: {
                      y: {
                        beginAtZero: true,
                        ticks: {
                          stepSize: 1
                        }
                      }
                    }
                  }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <TimelineIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
                Daily Usage Patterns
              </Typography>
              <Box sx={{ height: 300, p: 2 }}>
                <Bar
                  data={{
                    labels: Object.keys(daily_usage),
                    datasets: [{
                      label: 'Login Count',
                      data: Object.values(daily_usage),
                      backgroundColor: 'rgba(33, 150, 243, 0.6)',
                      borderColor: '#2196f3',
                      borderWidth: 1
                    }]
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'top' as const,
                      }
                    },
                    scales: {
                      y: {
                        beginAtZero: true,
                        ticks: {
                          stepSize: 1
                        }
                      }
                    }
                  }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  const renderQualityMetrics = () => {
    if (!personalAnalytics || !Array.isArray(personalAnalytics.quality_metrics) || personalAnalytics.quality_metrics.length === 0) {
      return (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              <AssessmentIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
              Biometric Quality Metrics
            </Typography>
            <Typography variant="body2" color="text.secondary">
              No quality metrics data available.
            </Typography>
          </CardContent>
        </Card>
      );
    }

    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            <AssessmentIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
            Biometric Quality Metrics
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Biometric Type</TableCell>
                  <TableCell>Quality Score</TableCell>
                  <TableCell>Enrollment Date</TableCell>
                  <TableCell>Last Used</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {personalAnalytics.quality_metrics.map((metric, index) => (
                  <TableRow key={index}>
                    <TableCell>
                      <Chip
                        icon={getBiometricIcon(metric.type)}
                        label={metric.type}
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>{Math.round(metric.quality_score)}%</TableCell>
                    <TableCell>{metric.enrollment_date ? formatTimestamp(metric.enrollment_date) : 'N/A'}</TableCell>
                    <TableCell>{metric.last_used ? formatTimestamp(metric.last_used) : 'N/A'}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    );
  };

  const renderSecurityInsights = () => {
    if (!personalAnalytics || !personalAnalytics.security_insights) {
      return (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              <SecurityIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
              Security Insights
            </Typography>
            <Typography variant="body2" color="text.secondary">
              No security insights data available.
            </Typography>
          </CardContent>
        </Card>
      );
    }

    const { security_insights } = personalAnalytics;

    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            <SecurityIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
            Security Insights
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="primary">
                  {security_insights.total_attempts}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Total Attempts
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="success.main">
                  {Math.round(security_insights.success_rate)}%
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Success Rate
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Chip
                  label={security_insights.risk_level}
                  color={
                    security_insights.risk_level === 'Low' ? 'success' :
                    security_insights.risk_level === 'Medium' ? 'warning' : 'error'
                  }
                  size="medium"
                />
                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
                  Risk Level
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    );
  };

  const renderOverview = () => {
    return (
      <Box>
        {/* Welcome Section */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Biometric Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Here's your biometric security overview
            </Typography>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <FingerprintIcon color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    Active Biometrics
                  </Typography>
                </Box>
                <Typography variant="h4" color="primary">
                  {dashboardData?.overview?.registered_biometrics || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Registered methods
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <CheckCircleIcon color="success" />
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    Success Rate
                  </Typography>
                </Box>
                <Typography variant="h4" color="success.main">
                  {Math.round(dashboardData?.overview?.success_rate || 0)}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Overall success rate
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <HistoryIcon color="info" />
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    Total Logins
                  </Typography>
                </Box>
                <Typography variant="h4" color="info.main">
                  {dashboardData?.overview?.total_login_attempts || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  All time attempts
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <SecurityIcon color="warning" />
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    Total Users
                  </Typography>
                </Box>
                <Typography variant="h4" color="warning.main">
                  {dashboardData?.overview?.total_users || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Registered users
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Dashboard Charts */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  User Activity Over Time
                </Typography>
                <Box sx={{ height: 400, p: 2 }}>
                  <Line
                    data={{
                      labels: Object.keys(dashboardData?.user_activity || {}),
                      datasets: [
                        {
                          label: 'Successful Logins',
                          data: Object.values(dashboardData?.user_activity || {}).map((day: any) => day.successful || 0),
                          borderColor: '#4caf50',
                          backgroundColor: 'rgba(76, 175, 80, 0.1)',
                          tension: 0.4,
                        },
                        {
                          label: 'Failed Logins',
                          data: Object.values(dashboardData?.user_activity || {}).map((day: any) => day.failed || 0),
                          borderColor: '#f44336',
                          backgroundColor: 'rgba(244, 67, 54, 0.1)',
                          tension: 0.4,
                        }
                      ]
                    }}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'top' as const,
                        },
                        title: {
                          display: true,
                          text: 'Login Activity Trends'
                        }
                      },
                      scales: {
                        y: {
                          beginAtZero: true,
                          ticks: {
                            stepSize: 1
                          }
                        }
                      }
                    }}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Biometric Type Distribution
                </Typography>
                <Box sx={{ height: 400, p: 2 }}>
                  <Doughnut
                    data={{
                      labels: Object.keys(dashboardData?.biometric_distribution || {}),
                      datasets: [{
                        data: Object.values(dashboardData?.biometric_distribution || {}),
                        backgroundColor: [
                          '#4caf50',
                          '#2196f3',
                          '#ff9800',
                          '#f44336',
                          '#9c27b0'
                        ]
                      }]
                    }}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom' as const,
                        }
                      }
                    }}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Recent Activity */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <List>
              {dashboardData?.recent_activity?.slice(0, 5).map((activity, index) => (
                <ListItem key={index} divider>
                  <ListItemText
                    primary={`${activity.type} Login`}
                    secondary={`${formatTimestamp(activity.timestamp)} - ${activity.success ? 'Success' : 'Failed'} - ${activity.user}`}
                  />
                  <Chip
                    label={activity.success ? 'Success' : 'Failed'}
                    color={activity.success ? 'success' : 'error'}
                    size="small"
                  />
                </ListItem>
              )) || (
                <ListItem>
                  <ListItemText
                    primary="No recent activity"
                    secondary="Recent login attempts will appear here"
                  />
                </ListItem>
              )}
            </List>
          </CardContent>
        </Card>
      </Box>
    );
  };

  const renderBiometricDetails = () => {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          Registered Biometric Types
        </Typography>
        <Grid container spacing={3}>
          {Object.entries(dashboardData?.biometric_distribution || {}).map(([type, count]) => (
            <Grid item xs={12} md={6} key={type}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      {getBiometricIcon(type)}
                      <Box sx={{ ml: 1 }}>
                        <Typography variant="h6">
                          {type.charAt(0).toUpperCase() + type.slice(1)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {count} registered
                        </Typography>
                      </Box>
                    </Box>
                    <Chip
                      label={`${Math.round(dashboardData?.success_rates?.[type] || 0)}%`}
                      color={
                        (dashboardData?.success_rates?.[type] || 0) > 70 ? 'success' : 
                        (dashboardData?.success_rates?.[type] || 0) > 40 ? 'warning' : 'error'
                      }
                    />
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Success Rate: {Math.round(dashboardData?.success_rates?.[type] || 0)}%
                  </Typography>
                  
                  <LinearProgress
                    variant="determinate"
                    value={dashboardData?.success_rates?.[type] || 0}
                    sx={{ mb: 2, height: 8, borderRadius: 4 }}
                  />
                </CardContent>
              </Card>
            </Grid>
          ))}
          {Object.keys(dashboardData?.biometric_distribution || {}).length === 0 && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" align="center" color="text.secondary">
                    No biometric data registered
                  </Typography>
                  <Typography variant="body2" align="center" color="text.secondary">
                    Register your first biometric method to get started
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </Box>
    );
  };

  const renderFeatureAnalysis = () => {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          Feature Analysis
        </Typography>
        <Grid container spacing={3}>
          {/* Quality Metrics */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quality Metrics
                </Typography>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Biometric Type</TableCell>
                        <TableCell>Quality Score</TableCell>
                        <TableCell>Feature Count</TableCell>
                        <TableCell>Processing Time</TableCell>
                        <TableCell>Created</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {Object.keys(dashboardData?.biometric_distribution || {}).length > 0 ? 
                        Object.entries(dashboardData?.biometric_distribution || {}).map(([type, count]) => (
                        <TableRow key={type}>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              {getBiometricIcon(type)}
                              <Typography sx={{ ml: 1 }}>
                                {type.charAt(0).toUpperCase() + type.slice(1)}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={`${Math.round(dashboardData?.success_rates?.[type] || 0)}%`}
                              color={
                                (dashboardData?.success_rates?.[type] || 0) > 70 ? 'success' : 
                                (dashboardData?.success_rates?.[type] || 0) > 40 ? 'warning' : 'error'
                              }
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            {count} registered
                          </TableCell>
                          <TableCell>
                            N/A
                          </TableCell>
                          <TableCell>
                            {new Date().toLocaleString()}
                          </TableCell>
                        </TableRow>
                      )) : (
                        <TableRow>
                          <TableCell colSpan={5} align="center">
                            <Typography variant="body2" color="text.secondary">
                              No biometric data available
                            </Typography>
                          </TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
          
          {/* Feature Analysis Chart */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quality Score Distribution
                </Typography>
                <Box sx={{ height: 300, p: 2 }}>
                  <Doughnut
                    data={{
                      labels: Object.keys(personalAnalytics?.quality_metrics ? 
                        personalAnalytics.quality_metrics.reduce((acc: any, metric) => {
                          acc[metric.type] = (acc[metric.type] || 0) + 1;
                          return acc;
                        }, {}) : {}),
                      datasets: [{
                        data: Object.values(personalAnalytics?.quality_metrics ? 
                          personalAnalytics.quality_metrics.reduce((acc: any, metric) => {
                            acc[metric.type] = (acc[metric.type] || 0) + 1;
                            return acc;
                          }, {}) : {}),
                        backgroundColor: [
                          '#4caf50',
                          '#2196f3',
                          '#ff9800',
                          '#f44336',
                          '#9c27b0'
                        ]
                      }]
                    }}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom' as const,
                        }
                      }
                    }}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Feature Dimensions
                </Typography>
                <Box sx={{ height: 300, p: 2 }}>
                  <Bar
                    data={{
                      labels: personalAnalytics?.quality_metrics?.map(metric => metric.type) || [],
                      datasets: [{
                        label: 'Quality Score',
                        data: personalAnalytics?.quality_metrics?.map(metric => metric.quality_score) || [],
                        backgroundColor: 'rgba(33, 150, 243, 0.6)',
                        borderColor: '#2196f3',
                        borderWidth: 1
                      }]
                    }}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'top' as const,
                        },
                        title: {
                          display: true,
                          text: 'Biometric Quality Scores'
                        }
                      },
                      scales: {
                        y: {
                          beginAtZero: true,
                          max: 100,
                          ticks: {
                            callback: function(value) {
                              return value + '%';
                            }
                          }
                        }
                      }
                    }}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  const renderLoginHistory = () => {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          Login History
        </Typography>
        <Card>
          <CardContent>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Date & Time</TableCell>
                    <TableCell>Method</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>IP Address</TableCell>
                    <TableCell>User</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {dashboardData?.recent_activity?.map((activity, index) => (
                    <TableRow key={index}>
                      <TableCell>{formatTimestamp(activity.timestamp)}</TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          {getBiometricIcon(activity.type)}
                          <Typography sx={{ ml: 1 }}>
                            {activity.type || 'Unknown'}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={activity.success ? 'Success' : 'Failed'}
                          color={activity.success ? 'success' : 'error'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{activity.ip_address || 'N/A'}</TableCell>
                      <TableCell>
                        <Typography variant="body2" sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                          {activity.user || 'N/A'}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  )) || (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        <Typography variant="body2" color="text.secondary">
                          No login history available
                        </Typography>
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </Box>
    );
  };

  const renderSecuritySettings = () => {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          Security Settings
        </Typography>
        <Grid container spacing={3}>
          {/* Account Security */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Account Security
                </Typography>
                <List>
                  <ListItem>
                    <ListItemText
                      primary="Two-Factor Authentication"
                      secondary="Enhance your account security"
                    />
                    <Chip label="Enabled" color="success" size="small" />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Login Notifications"
                      secondary="Get notified of login attempts"
                    />
                    <Chip label="Enabled" color="success" size="small" />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Session Timeout"
                      secondary="Automatic logout after inactivity"
                    />
                    <Chip label="30 minutes" color="default" size="small" />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>
          
          {/* Biometric Settings */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Biometric Settings
                </Typography>
                <List>
                  <ListItem>
                    <ListItemText
                      primary="Quality Threshold"
                      secondary="Minimum quality score required"
                    />
                    <Chip label="70%" color="primary" size="small" />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Fallback Authentication"
                      secondary="Use password if biometric fails"
                    />
                    <Chip label="Enabled" color="success" size="small" />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Auto-regenerate Analysis"
                      secondary="Update analysis on each login"
                    />
                    <Chip label="Enabled" color="success" size="small" />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>
          
          {/* Privacy Settings */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Privacy & Data Management
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={<DownloadIcon />}
                      onClick={() => downloadDashboardReport('zip')}
                    >
                      Export Data
                    </Button>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={<SecurityIcon />}
                      onClick={handleRegenerateAnalysis}
                      disabled={regenerateLoading}
                    >
                      Regenerate Analysis
                    </Button>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Button
                      variant="outlined"
                      color="warning"
                      fullWidth
                    >
                      Clear History
                    </Button>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Button
                      variant="outlined"
                      color="error"
                      fullWidth
                    >
                      Delete Account
                    </Button>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!dashboardData) {
    return (
      <Alert severity="warning" sx={{ m: 2 }}>
        No dashboard data available
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
      <Typography variant="h4" gutterBottom>
          My Biometric Dashboard
      </Typography>
        <Stack direction="row" spacing={2}>
          <Button
            variant="outlined"
            startIcon={<GetAppIcon />}
            onClick={() => downloadDashboardReport('json')}
            disabled={downloadLoading}
          >
            Download JSON
          </Button>
          <Button
            variant="contained"
            startIcon={<GetAppIcon />}
            onClick={() => downloadDashboardReport('zip')}
            disabled={downloadLoading}
          >
            Download Full Report
          </Button>
        </Stack>
      </Box>

      {/* Main Navigation Tabs */}
      <Box sx={{ mb: 3 }}>
        <Tabs value={selectedTab} onChange={handleTabChange} centered>
          <Tab label="Overview" icon={<AnalyticsIcon />} />
          <Tab label="Biometric Details" icon={<FingerprintIcon />} />
          <Tab label="Feature Analysis" icon={<AssessmentIcon />} />
          <Tab label="Login History" icon={<HistoryIcon />} />
          <Tab label="Security Settings" icon={<SecurityIcon />} />
        </Tabs>
      </Box>

      {/* Tab Content */}
      {selectedTab === 0 && renderOverview()}
      {selectedTab === 1 && renderBiometricDetails()}
      {selectedTab === 2 && renderFeatureAnalysis()}
      {selectedTab === 3 && renderLoginHistory()}
      {selectedTab === 4 && renderSecuritySettings()}

      {/* User Account Status */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Account Status
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="body1">
                <strong>Total Users:</strong> {dashboardData.overview?.total_users || 0}
              </Typography>
              <Typography variant="body1">
                <strong>Success Rate:</strong> {Math.round(dashboardData.overview?.success_rate || 0)}%
              </Typography>
              <Typography variant="body1">
                <strong>Total Login Attempts:</strong> {dashboardData.overview?.total_login_attempts || 0}
              </Typography>
              <Typography variant="body1">
                <strong>Successful Logins:</strong> {dashboardData.overview?.successful_logins || 0}
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="body1" gutterBottom>
                <strong>Registered Biometric Methods:</strong>
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {Object.keys(dashboardData.biometric_distribution || {}).map((type) => (
                  <Chip
                    key={type}
                    icon={getBiometricIcon(type)}
                    label={type}
                    color="primary"
                    variant="outlined"
                  />
                )) || <Typography variant="body2" color="text.secondary">No biometric methods registered</Typography>}
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Success Rates */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Success Sign-in Rates
          </Typography>
          <Grid container spacing={2}>
            {dashboardData.success_rates && Object.keys(dashboardData.success_rates).length > 0 ? (
              Object.entries(dashboardData.success_rates).map(([type, rate]) => (
              <Grid item xs={12} sm={6} md={3} key={type}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      {getBiometricIcon(type)}
                      <Typography variant="h6" sx={{ ml: 1 }}>
                        {type}
                      </Typography>
                    </Box>
                    <Typography variant="h4" color="primary">
                      {Math.round(rate)}%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Success Rate
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={rate}
                      sx={{ mt: 1 }}
                    />
                  </CardContent>
                </Card>
              </Grid>
              ))
            ) : (
              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary" align="center">
                  No success rate data available yet
                </Typography>
              </Grid>
            )}
          </Grid>
        </CardContent>
      </Card>

      {/* Biometric Summary */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Biometric Data Overview
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <FaceIcon />
                    <Typography variant="h6" sx={{ ml: 1 }}>
                      Face Data
                    </Typography>
                  </Box>
                  <Typography variant="h4" color="primary">
                                            {dashboardData.biometric_distribution?.face || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <FingerprintIcon />
                    <Typography variant="h6" sx={{ ml: 1 }}>
                      Fingerprint Data
                    </Typography>
                  </Box>
                  <Typography variant="h4" color="primary">
                                            {dashboardData.biometric_distribution?.fingerprint || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <EyeIcon />
                    <Typography variant="h6" sx={{ ml: 1 }}>
                      Iris Data
                    </Typography>
                  </Box>
                  <Typography variant="h4" color="primary">
                                            {dashboardData.biometric_distribution?.iris || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <VoiceIcon />
                    <Typography variant="h6" sx={{ ml: 1 }}>
                      Voice Data
                    </Typography>
                  </Box>
                  <Typography variant="h4" color="primary">
                                            {dashboardData.biometric_distribution?.voice || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Last updated: {new Date().toLocaleString()}
          </Typography>
        </CardContent>
      </Card>

      {/* Login History Section */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            <HistoryIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
            Login History
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Timestamp</TableCell>
                  <TableCell>Biometric Type</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>IP Address</TableCell>
                  <TableCell>User Agent</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {dashboardData.recent_activity?.map((entry, index) => (
                  <TableRow key={index}>
                    <TableCell>{formatTimestamp(entry.timestamp)}</TableCell>
                    <TableCell>
                      <Chip
                        icon={getBiometricIcon(entry.type)}
                        label={entry.type}
                        size="small"
                        color="primary"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        icon={entry.success ? <CheckCircleIcon /> : <ErrorIcon />}
                        label={entry.success ? 'Success' : 'Failed'}
                        size="small"
                        color={entry.success ? 'success' : 'error'}
                      />
                    </TableCell>
                    <TableCell>
                            <Typography variant="body2" sx={{ fontSize: '0.75rem' }}>
                        {entry.ip_address || 'N/A'}
                            </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" sx={{ fontSize: '0.75rem' }}>
                        {entry.user || 'N/A'}
                      </Typography>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          {dashboardData.recent_activity?.length === 0 && (
            <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
              No login history available
            </Typography>
          )}
        </CardContent>
      </Card>

      {/* Detailed Biometric Entries Section */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
            Detailed Biometric Entries
          </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={handleRegenerateAnalysis}
              disabled={regenerateLoading}
              startIcon={regenerateLoading ? <CircularProgress size={20} /> : <AssessmentIcon />}
              size="small"
            >
              {regenerateLoading ? 'Regenerating...' : 'Regenerate Analysis'}
            </Button>
          </Box>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Features</TableCell>
                  <TableCell>Processing Steps</TableCell>
                  <TableCell>Visualizations</TableCell>
                  <TableCell>Quality Score</TableCell>
                  <TableCell>Processing Time</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {personalAnalytics?.biometric_entries && personalAnalytics.biometric_entries.length > 0 ? 
                  personalAnalytics.biometric_entries.map((entry) => (
                  <TableRow key={entry.id}>
                    <TableCell>{entry.id}</TableCell>
                    <TableCell>
                      <Chip
                        icon={getBiometricIcon(entry.type)}
                        label={entry.type}
                        size="small"
                        color="primary"
                      />
                    </TableCell>
                    <TableCell>
                      {entry.created_at ? new Date(entry.created_at).toLocaleString() : 'N/A'}
                    </TableCell>
                    <TableCell>{entry.features_count}</TableCell>
                    <TableCell>
                      <Chip
                        label={entry.processing_steps}
                        size="small"
                        color={entry.processing_steps > 0 ? 'success' : 'default'}
                        variant={entry.processing_steps > 0 ? 'filled' : 'outlined'}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={entry.visualizations_count}
                        size="small"
                        color={entry.visualizations_count > 0 ? 'success' : 'default'}
                        variant={entry.visualizations_count > 0 ? 'filled' : 'outlined'}
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {entry.quality_score ? entry.quality_score.toFixed(1) + '%' : 'N/A'}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" color={entry.processing_time !== 'N/A' ? 'text.primary' : 'text.secondary'}>
                        {entry.processing_time}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Tooltip title="View Analysis Visualizations">
                        <IconButton
                          onClick={() => {
                            console.log('👁️ Eye icon clicked for entry:', entry);
                            handleViewVisualization(entry);
                          }}
                          disabled={analysisLoading}
                        >
                          <VisibilityIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                )) : (
                  <TableRow>
                    <TableCell colSpan={9} align="center">
                      <Typography variant="body2" color="text.secondary">
                        No biometric entries available
                      </Typography>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Enhanced Analytics Section */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            <AnalyticsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
            Personal Analytics
          </Typography>
          <Tabs value={selectedTab} onChange={handleTabChange} centered>
            <Tab label="Time Patterns" icon={<ScheduleIcon />} />
            <Tab label="Quality Metrics" icon={<AssessmentIcon />} />
            <Tab label="Security Insights" icon={<SecurityIcon />} />
          </Tabs>
          <Divider sx={{ my: 2 }} />
          {selectedTab === 0 && renderTimePatterns()}
          {selectedTab === 1 && renderQualityMetrics()}
          {selectedTab === 2 && renderSecurityInsights()}
        </CardContent>
      </Card>

      {/* Visualization Modal */}
      <VisualizationModal
        open={visualizationModalOpen}
        onClose={() => setVisualizationModalOpen(false)}
        entry={selectedEntry}
      />
    </Box>
  );
};

export default BiometricAnalysisDashboard;