import React, { useState, useEffect, useCallback } from 'react';
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
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Paper,
  IconButton,
  CircularProgress,
  useTheme,
  useMediaQuery,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  LinearProgress,
} from '@mui/material';
import {
  AdminPanelSettings,
  People,
  Security,
  Logout,
  Refresh,
  Visibility,
  CheckCircle,
  Warning,
  DataUsage,
  Fingerprint,
  Face,
  CameraAlt,
  Schedule,
  FileDownload,
  Person,
  TrendingUp,
  GetApp,
  AccountTree,
  Delete,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
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
      id={`admin-dashboard-tabpanel-${index}`}
      aria-labelledby={`admin-dashboard-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

const AdminDashboardPage: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  // const isTablet = useMediaQuery(theme.breakpoints.down('md'));
  
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [adminData, setAdminData] = useState<any>(null);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<any>(null);
  const [userDetailsDialogOpen, setUserDetailsDialogOpen] = useState(false);
  const [selectedUserDetails, setSelectedUserDetails] = useState<any>(null);
  
  // System Performance Analytics State
  // const [modalityPerformance, setModalityPerformance] = useState<any>(null);
  // const [pipelineAnalysis, setPipelineAnalysis] = useState<any>(null);
  const [errorAnalysis, setErrorAnalysis] = useState<any>(null);
  const [systemHealth, setSystemHealth] = useState<any>(null);
  
  // Plot URLs State
  const [modalityPlotUrl, setModalityPlotUrl] = useState<string | null>(null);
  const [systemHealthPlotUrl, setSystemHealthPlotUrl] = useState<string | null>(null);
  const [errorAnalysisPlotUrl, setErrorAnalysisPlotUrl] = useState<string | null>(null);
  const [pipelineAnalysisPlotUrl, setPipelineAnalysisPlotUrl] = useState<string | null>(null);
  
  // Advanced Analytics Plot URLs
  const [ablationStudyPlotUrl, setAblationStudyPlotUrl] = useState<string | null>(null);
  const [modelArchitecturePlotUrl, setModelArchitecturePlotUrl] = useState<string | null>(null);
  const [similarityPlotsUrl, setSimilarityPlotsUrl] = useState<string | null>(null);
  const [crossDatasetValidationPlotUrl, setCrossDatasetValidationPlotUrl] = useState<string | null>(null);
  const [dataAugmentationComparisonPlotUrl, setDataAugmentationComparisonPlotUrl] = useState<string | null>(null);
  const [falsePositiveNegativeExamplesPlotUrl, setFalsePositiveNegativeExamplesPlotUrl] = useState<string | null>(null);
  const [featureDistributionTimePlotUrl, setFeatureDistributionTimePlotUrl] = useState<string | null>(null);
  const [modelPerformanceByClassPlotUrl, setModelPerformanceByClassPlotUrl] = useState<string | null>(null);
  const [lossLandscapePlotUrl, setLossLandscapePlotUrl] = useState<string | null>(null);
  const [errorRateThresholdCurvesPlotUrl, setErrorRateThresholdCurvesPlotUrl] = useState<string | null>(null);
  const [embeddingCorrelationHeatmapPlotUrl, setEmbeddingCorrelationHeatmapPlotUrl] = useState<string | null>(null);
  const [modelInferenceSpeedPlotUrl, setModelInferenceSpeedPlotUrl] = useState<string | null>(null);
  const [learningRateSchedulesPlotUrl, setLearningRateSchedulesPlotUrl] = useState<string | null>(null);
  const [classActivationMappingPlotUrl, setClassActivationMappingPlotUrl] = useState<string | null>(null);
  const [sensitivityAnalysisPlotUrl, setSensitivityAnalysisPlotUrl] = useState<string | null>(null);
  const [classWisePrecisionRecallF1PlotUrl, setClassWisePrecisionRecallF1PlotUrl] = useState<string | null>(null);
  
  const { adminUser, logout } = useAuth();
  const navigate = useNavigate();

  console.log('AdminDashboardPage render:', { adminUser: !!adminUser, loading, refreshing });

  const fetchAdminData = useCallback(async (forceRefresh = false) => {
    console.log('fetchAdminData called:', { forceRefresh, adminUser: !!adminUser });
    try {
      if (forceRefresh) {
        setRefreshing(true);
        // Clear cache to force fresh data
        authService.clearAllCache();
      } else {
      setLoading(true);
      }
      
      // Fetch dashboard data (will use cache if available)
      const dashboardResponse = await authService.getAdminDashboard();
      setDashboardData(dashboardResponse);
      
      // Fetch users (will use cache if available)
      const usersResponse = await authService.getUsers();
      setUsers(usersResponse);
      
      // Fetch system performance analytics (will use cache if available)
      const [errorData, healthData] = await Promise.all([
        authService.getErrorAnalysis(),
        authService.getSystemHealth()
      ]);
      setErrorAnalysis(errorData);
      setSystemHealth(healthData);
      
      setAdminData(adminUser);
    } catch (error) {
      console.error('Error fetching admin data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [adminUser]);

  useEffect(() => {
    console.log('AdminDashboardPage useEffect triggered:', { adminUser: !!adminUser });
    if (adminUser) {
      fetchAdminData();
    }
  }, [adminUser, fetchAdminData]);

  const handleRefresh = useCallback(() => {
    fetchAdminData(true);
  }, [fetchAdminData]);

  // Fetch all plot images
  useEffect(() => {
    const fetchPlots = async () => {
      // Don't fetch plots if admin user is not authenticated
      if (!adminUser) {
        console.log('Admin user not authenticated, skipping plot fetch');
        return;
      }

      const token = localStorage.getItem('access_token');
      if (!token) {
        console.error('No access token found for plots');
        return;
      }

      console.log('Starting to fetch plots...');
      console.log('Admin user:', adminUser);
      console.log('Token exists:', !!token);
      
      // Use the same base URL as authService
      const baseUrl = process.env.REACT_APP_API_URL;
      console.log('Using base URL:', baseUrl);

      // First test if the admin endpoint is accessible
      try {
        console.log('Testing admin dashboard endpoint...');
        const testResponse = await fetch(`${baseUrl}/admin/dashboard`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        console.log('Admin dashboard test response:', testResponse.status);
        
        if (!testResponse.ok) {
          const errorText = await testResponse.text();
          console.error('Admin dashboard test failed:', errorText);
          return;
        } else {
          console.log('✅ Admin authentication working');
        }
      } catch (error) {
        console.error('❌ Admin authentication test failed:', error);
        return;
      }

      // Plot endpoints and their corresponding setters
      const plotConfigs = [
        { endpoint: '/admin/analytics/modality-performance/plot', setter: setModalityPlotUrl },
        { endpoint: '/admin/analytics/system-health/plot', setter: setSystemHealthPlotUrl },
        { endpoint: '/admin/analytics/error-analysis/plot', setter: setErrorAnalysisPlotUrl },
        { endpoint: '/admin/analytics/pipeline-analysis/plot', setter: setPipelineAnalysisPlotUrl },
        { endpoint: '/admin/analytics/ablation-study/plot', setter: setAblationStudyPlotUrl },
        { endpoint: '/admin/analytics/model-architecture/plot', setter: setModelArchitecturePlotUrl },
        { endpoint: '/admin/analytics/similarity-plots/plot', setter: setSimilarityPlotsUrl },
        { endpoint: '/admin/analytics/cross-dataset-validation/plot', setter: setCrossDatasetValidationPlotUrl },
        { endpoint: '/admin/analytics/data-augmentation-comparison/plot', setter: setDataAugmentationComparisonPlotUrl },
        { endpoint: '/admin/analytics/false-positive-negative-examples/plot', setter: setFalsePositiveNegativeExamplesPlotUrl },
        { endpoint: '/admin/analytics/feature-distribution-time/plot', setter: setFeatureDistributionTimePlotUrl },
        { endpoint: '/admin/analytics/model-performance-by-class/plot', setter: setModelPerformanceByClassPlotUrl },
        { endpoint: '/admin/analytics/loss-landscape/plot', setter: setLossLandscapePlotUrl },
        { endpoint: '/admin/analytics/error-rate-threshold-curves/plot', setter: setErrorRateThresholdCurvesPlotUrl },
        { endpoint: '/admin/analytics/embedding-correlation-heatmap/plot', setter: setEmbeddingCorrelationHeatmapPlotUrl },
        { endpoint: '/admin/analytics/model-inference-speed/plot', setter: setModelInferenceSpeedPlotUrl },
        { endpoint: '/admin/analytics/learning-rate-schedules/plot', setter: setLearningRateSchedulesPlotUrl },
        { endpoint: '/admin/analytics/class-activation-mapping/plot', setter: setClassActivationMappingPlotUrl },
        { endpoint: '/admin/analytics/sensitivity-analysis/plot', setter: setSensitivityAnalysisPlotUrl },
        { endpoint: '/admin/analytics/class-wise-precision-recall-f1/plot', setter: setClassWisePrecisionRecallF1PlotUrl }
      ];

      // Fetch plots sequentially to avoid overwhelming the server
      for (const config of plotConfigs) {
        try {
          console.log(`Fetching plot: ${config.endpoint}`);
          console.log(`Full URL: ${baseUrl}${config.endpoint}`);
          console.log(`Using token: ${token ? 'Token present' : 'No token'}`);
          
          const response = await fetch(`${baseUrl}${config.endpoint}`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          console.log(`Response status for ${config.endpoint}: ${response.status}`);
          console.log(`Response headers:`, Object.fromEntries(response.headers.entries()));

          if (response.ok && response.headers.get('content-type')?.includes('image')) {
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            config.setter(imageUrl);
            console.log(`✅ Successfully loaded plot: ${config.endpoint}`);
          } else {
            console.error(`❌ Failed to fetch plot ${config.endpoint}: ${response.status} ${response.statusText}`);
            const errorText = await response.text().catch(() => 'Unknown error');
            console.error(`Error details: ${errorText}`);
            
            // Try to parse JSON error if available
            try {
              const errorJson = JSON.parse(errorText);
              console.error(`JSON Error:`, errorJson);
            } catch (e) {
              console.error(`Raw error text: ${errorText}`);
            }
          }
        } catch (error) {
          console.error(`❌ Network error fetching plot ${config.endpoint}:`, error);
        }
        
        // Small delay between requests to avoid overwhelming the server
        await new Promise(resolve => setTimeout(resolve, 200));
      }
      
      console.log('Finished fetching all plots');
    };

    fetchPlots();
  }, [adminUser]); // Only depend on adminUser

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  const handleDeleteUser = (user: any) => {
    setSelectedUser(user);
    setDeleteDialogOpen(true);
  };

  const confirmDeleteUser = async () => {
    try {
      await authService.deleteUser(selectedUser.id);
      setUsers(users.filter(u => u.id !== selectedUser.id));
      setDeleteDialogOpen(false);
      setSelectedUser(null);
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const handleViewUserDetails = async (user: any) => {
    try {
      const userDetails = await authService.getUserDetails(user.id);
      setSelectedUserDetails(userDetails);
      setUserDetailsDialogOpen(true);
    } catch (error) {
      console.error('Error fetching user details:', error);
    }
  };

  const handleViewUserDashboard = (user: any) => {
    navigate(`/admin/user/${user.id}`);
  };

  const handleExportReport = async () => {
    try {
      const report = await authService.exportSystemReport();
      const blob = new Blob([JSON.stringify(report, null, 2)], {
        type: 'application/json'
      });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `system-report-${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting report:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'inactive': return 'error';
      case 'pending': return 'warning';
      default: return 'default';
    }
  };

  const getBiometricIcon = (type: string) => {
    switch (type) {
      case 'fingerprint': return <Fingerprint />;
      case 'face': return <Face />;
      case 'palmprint': return <CameraAlt />;
      default: return <Security />;
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  console.log('AdminDashboardPage about to render main content:', { 
    loading, 
    refreshing, 
    adminUser: !!adminUser,
    dashboardData: !!dashboardData,
    users: users?.length || 0
  });

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
                <AdminPanelSettings />
              </Avatar>
              <Box>
                <Typography variant={isMobile ? 'subtitle1' : 'h6'}>
                  Admin Dashboard - {adminData?.first_name} {adminData?.last_name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {adminData?.email} • {adminData?.is_super_admin ? 'Super Admin' : 'Administrator'}
                </Typography>
              </Box>
            </Box>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <ThemeToggle />
              <IconButton onClick={handleRefresh} size="small" disabled={refreshing}>
                {refreshing ? <CircularProgress size={20} /> : <Refresh />}
              </IconButton>
              <Button
                variant="outlined"
                startIcon={<Logout />}
                onClick={handleLogout}
                size="small"
                sx={{ minWidth: 'auto' }}
              >
                <Box component="span" sx={{ display: { xs: 'none', sm: 'inline' } }}>
                Logout
                </Box>
              </Button>
            </Box>
          </Box>
        </Container>
      </Paper>

      {/* Main Content */}
      <Container maxWidth="xl">
        <Grid container spacing={{ xs: 2, md: 3 }}>
          {/* Sidebar */}
          <Grid item xs={12} lg={3}>
            <Box sx={{ position: 'sticky', top: 20 }}>
              {/* Quick Stats */}
            <Card sx={{ mb: 3 }}>
                <CardContent sx={{ p: { xs: 2, sm: 3 } }}>
                <Typography variant="h6" gutterBottom>
                  System Overview
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <People color="primary" />
                    </ListItemIcon>
                    <ListItemText
                        primary={`${dashboardData?.statistics?.total_users || 0} Users`}
                        secondary={`${dashboardData?.statistics?.active_users || 0} active`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Security color="success" />
                    </ListItemIcon>
                    <ListItemText
                        primary={`${dashboardData?.statistics?.success_rate || 0}% Success Rate`}
                        secondary={`${dashboardData?.statistics?.total_logins || 0} total logins`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Warning color="warning" />
                    </ListItemIcon>
                    <ListItemText
                        primary={`${dashboardData?.statistics?.failed_logins || 0} Failed Attempts`}
                        secondary="All time"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon>
                        <DataUsage color="info" />
                      </ListItemIcon>
                      <ListItemText
                        primary={`${dashboardData?.statistics?.total_biometric_data || 0} Biometric Records`}
                        secondary={`${dashboardData?.statistics?.active_biometric_data || 0} active`}
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>

              {/* System Health (Responsive sidebar) */}
              <Card sx={{ mb: 3, display: { xs: 'none', lg: 'block' } }}>
                <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                    System Health
                </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body2">Response Time</Typography>
                      <Chip 
                        label={`${systemHealth?.avg_response_time || 0}s`} 
                        color={systemHealth?.avg_response_time < 0.5 ? 'success' : 'warning'} 
                    size="small"
                      />
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body2">Uptime</Typography>
                      <Chip 
                        label={`${Math.floor((systemHealth?.uptime_seconds || 0) / 3600)}h`} 
                        color="info" 
                    size="small"
                      />
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body2">Status</Typography>
                      <Chip 
                        label={systemHealth?.status || "Unknown"} 
                        color={systemHealth?.status === 'healthy' ? 'success' : 'error'} 
                    size="small"
                      />
                    </Box>
                </Box>
              </CardContent>
            </Card>

              {/* Error Summary (Responsive sidebar) */}
              <Card sx={{ display: { xs: 'none', lg: 'block' } }}>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Error Summary
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body2">Success Rate</Typography>
                      <Typography variant="body2" fontWeight="bold" color="success.main">
                        {errorAnalysis?.success_rate || 0}%
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body2">Failure Rate</Typography>
                      <Typography variant="body2" fontWeight="bold" color="error.main">
                        {errorAnalysis?.failure_rate || 0}%
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body2">Total Attempts</Typography>
                      <Typography variant="body2" fontWeight="bold">
                        {errorAnalysis?.total || 0}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Box>
          </Grid>

          {/* Main Content Area */}
          <Grid item xs={12} lg={9}>
            <Card sx={{ mb: 3 }}>
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
                    <Tab label="User Management" />
                    <Tab label="System Analytics" />
                    <Tab label="System Performance" />
                    <Tab label="Error Analysis" />
                    <Tab label="Security Monitoring" />
                    <Tab label="Login History" />
                    <Tab label="Reports" />
                    <Tab label="Advanced Analytics" />
                    <Tab label="Model Analysis" />
                  </Tabs>
                </Box>

                <TabPanel value={tabValue} index={0}>
                  <Typography variant="h6" gutterBottom>
                    System Overview & Analytics
                  </Typography>
                  
                  <Grid container spacing={{ xs: 2, md: 3 }}>
                    {/* 2. Biometric Method Usage */}
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                      <Typography variant="h6" gutterBottom>
                            Biometric Usage
                          </Typography>
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            {dashboardData?.biometric_methods && Object.entries(dashboardData.biometric_methods).map(([type, count]: [string, any]) => (
                              <Paper key={type} sx={{ p: 2 }}>
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                  {getBiometricIcon(type)}
                                  <Typography variant="subtitle2" color="text.secondary">
                                    {type.charAt(0).toUpperCase() + type.slice(1)}
                                  </Typography>
                                </Box>
                                <Typography variant="h6">
                                  {count}
                                </Typography>
                              </Paper>
                            ))}
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>

                    {/* 3. Recent System Activity */}
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Recent Activity
                          </Typography>
                          <List dense>
                            <ListItem>
                              <ListItemIcon>
                                <Person color="primary" />
                              </ListItemIcon>
                              <ListItemText
                                primary={`${dashboardData?.recent_activity?.registrations || 0} New Registrations`}
                                secondary="Last 24 hours"
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemIcon>
                                <Security color="success" />
                              </ListItemIcon>
                              <ListItemText
                                primary={`${dashboardData?.recent_activity?.logins || 0} Login Attempts`}
                                secondary="Last 24 hours"
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemIcon>
                                <Warning color="error" />
                              </ListItemIcon>
                              <ListItemText
                                primary={`${dashboardData?.recent_activity?.failed_attempts || 0} Failed Attempts`}
                                secondary="Last 24 hours"
                              />
                            </ListItem>
                          </List>
                        </CardContent>
                      </Card>
                    </Grid>

                    {/* 4. Performance & Quality Metrics */}
                    <Grid item xs={12} sm={6} md={4}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Performance Metrics
                          </Typography>
                          <Box sx={{ mb: 2 }}>
                            <Typography variant="body2" color="text.secondary">
                              Avg Processing Time
                            </Typography>
                            <Typography variant="h6">
                              {dashboardData?.performance_metrics?.avg_processing_time || 0}s
                            </Typography>
                            <LinearProgress 
                              variant="determinate" 
                              value={Math.min((dashboardData?.performance_metrics?.avg_processing_time || 0) / 5 * 100, 100)} 
                              sx={{ mt: 1 }}
                            />
                          </Box>
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              Avg Quality Score
                            </Typography>
                            <Typography variant="h6">
                              {Math.round((dashboardData?.performance_metrics?.avg_quality_score || 0) * 100)}%
                            </Typography>
                            <LinearProgress 
                              variant="determinate" 
                              value={(dashboardData?.performance_metrics?.avg_quality_score || 0) * 100} 
                              sx={{ mt: 1 }}
                            />
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>

                    {/* 5. Security Insights */}
                    <Grid item xs={12} sm={6} md={4}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Security Insights
                          </Typography>
                          <List dense>
                            <ListItem>
                              <ListItemIcon>
                                <TrendingUp color="primary" />
                              </ListItemIcon>
                              <ListItemText
                                primary="Most Used Biometric"
                                secondary={dashboardData?.security_insights?.most_used_biometric || "None"}
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemIcon>
                                <Schedule color="info" />
                              </ListItemIcon>
                              <ListItemText
                                primary="Peak Usage Hour"
                                secondary={dashboardData?.security_insights?.peak_usage_hour || "Unknown"}
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemIcon>
                                <CheckCircle color="success" />
                              </ListItemIcon>
                              <ListItemText
                                primary="Most Successful Day"
                                secondary={dashboardData?.security_insights?.most_successful_day || "Unknown"}
                              />
                            </ListItem>
                          </List>
                        </CardContent>
                      </Card>
                    </Grid>

                    {/* Mobile-only System Health */}
                    <Grid item xs={12} sm={6} md={4} sx={{ display: { xs: 'block', lg: 'none' } }}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            System Health
                          </Typography>
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <Typography variant="body2">Response Time</Typography>
                              <Chip 
                                label={`${systemHealth?.avg_response_time || 0}s`} 
                                color={systemHealth?.avg_response_time < 0.5 ? 'success' : 'warning'} 
                                size="small" 
                              />
                            </Box>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <Typography variant="body2">Uptime</Typography>
                              <Chip 
                                label={`${Math.floor((systemHealth?.uptime_seconds || 0) / 3600)}h`} 
                                color="info" 
                                size="small" 
                              />
                            </Box>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <Typography variant="body2">Status</Typography>
                              <Chip 
                                label={systemHealth?.status || "Unknown"} 
                                color={systemHealth?.status === 'healthy' ? 'success' : 'error'} 
                                size="small" 
                              />
                            </Box>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>

                    {/* 6. Login History & Audit */}
                    <Grid item xs={12}>
                      <Typography variant="h6" gutterBottom>
                        Recent Login Activity
                      </Typography>
                      <List>
                        {dashboardData?.recent_login_attempts?.slice(0, 5).map((attempt: any, index: number) => (
                          <ListItem key={index} divider>
                            <ListItemIcon>
                              {attempt.success ? (
                                <CheckCircle color="success" />
                              ) : (
                                <Warning color="error" />
                              )}
                            </ListItemIcon>
                            <ListItemText
                              primary={attempt.username || 'Unknown'}
                              secondary={`${attempt.attempt_type} • ${new Date(attempt.timestamp).toLocaleString()}`}
                            />
                            <Chip
                              label={attempt.success ? 'Success' : 'Failed'}
                              color={attempt.success ? 'success' : 'error'}
                              size="small"
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Grid>
                    
                    {/* 7. Biometric Data Quality & Analysis */}
                    <Grid item xs={12} md={6}>
                      <Typography variant="h6" gutterBottom>
                        Biometric Quality Distribution
                      </Typography>
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="subtitle2" color="text.secondary">
                            Active Biometric Records
                          </Typography>
                          <Typography variant="h6">
                            {dashboardData?.statistics?.active_biometric_data || 0}
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={
                              dashboardData?.statistics?.total_biometric_data > 0 
                                ? (dashboardData.statistics.active_biometric_data / dashboardData.statistics.total_biometric_data) * 100 
                                : 0
                            } 
                            sx={{ mt: 1 }}
                          />
                        </Paper>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="subtitle2" color="text.secondary">
                            Failed Attempts by Type
                          </Typography>
                          {dashboardData?.security_insights?.failed_attempts_by_type && 
                            Object.entries(dashboardData.security_insights.failed_attempts_by_type).map(([type, count]: [string, any]) => (
                              <Box key={type} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 1 }}>
                                <Typography variant="body2">{type}</Typography>
                                <Chip label={count} size="small" color="error" />
                              </Box>
                            ))
                          }
                        </Paper>
                      </Box>
                    </Grid>

                    {/* 8. Export Section */}
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            System Reports
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            Download comprehensive system reports and analytics data.
                          </Typography>
                          <Button
                            variant="contained"
                            startIcon={<GetApp />}
                            onClick={handleExportReport}
                            fullWidth
                          >
                            Export System Report
                          </Button>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </TabPanel>

                <TabPanel value={tabValue} index={1}>
                  {/* User Management */}
                  <Typography variant="h6" gutterBottom>
                    User Management
                  </Typography>
                  <TableContainer component={Paper} sx={{ 
                    overflowX: 'auto',
                    '& .MuiTable-root': {
                      minWidth: { xs: 650, sm: 'auto' }
                    }
                  }}>
                    <Table size={isMobile ? 'small' : 'medium'}>
                      <TableHead>
                        <TableRow>
                          <TableCell>User</TableCell>
                          <TableCell>Email</TableCell>
                          <TableCell sx={{ display: { xs: 'none', sm: 'table-cell' } }}>Status</TableCell>
                          <TableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>Biometric Methods</TableCell>
                          <TableCell sx={{ display: { xs: 'none', lg: 'table-cell' } }}>Last Login</TableCell>
                          <TableCell>Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {dashboardData?.users_overview?.map((user: any) => (
                          <TableRow key={user.id}>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                <Avatar sx={{ width: { xs: 24, sm: 32 }, height: { xs: 24, sm: 32 } }}>
                                  <Person />
                                </Avatar>
                                <Box>
                                  <Typography variant="body2" sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}>
                                    {user.first_name} {user.last_name}
                                  </Typography>
                                  <Typography variant="caption" color="text.secondary" sx={{ display: { xs: 'none', sm: 'block' } }}>
                                    @{user.username}
                                  </Typography>
                                </Box>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Typography variant="body2" sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}>
                                {user.email}
                              </Typography>
                            </TableCell>
                            <TableCell sx={{ display: { xs: 'none', sm: 'table-cell' } }}>
                              <Chip
                                label={user.status || 'active'}
                                color={getStatusColor(user.status || 'active')}
                                size="small"
                              />
                            </TableCell>
                            <TableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>
                              <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                                {user.biometric_methods?.map((method: string) => (
                                  <Chip key={method} label={method} size="small" variant="outlined" />
                                ))}
                              </Box>
                            </TableCell>
                            <TableCell sx={{ display: { xs: 'none', lg: 'table-cell' } }}>
                              <Typography variant="body2">
                                {user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', gap: 0.5 }}>
                                <Tooltip title="View Dashboard">
                                  <IconButton 
                                    size="small" 
                                    color="primary"
                                    onClick={() => handleViewUserDashboard(user)}
                                  >
                                    <AccountTree />
                                  </IconButton>
                                </Tooltip>
                                <Tooltip title="View Details">
                                  <IconButton size="small" onClick={() => handleViewUserDetails(user)}>
                                    <Visibility />
                                  </IconButton>
                                </Tooltip>
                                <Tooltip title="Delete User">
                                  <IconButton size="small" color="error" onClick={() => handleDeleteUser(user)}>
                                    <Delete />
                                  </IconButton>
                                </Tooltip>
                              </Box>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </TabPanel>

                <TabPanel value={tabValue} index={2}>
                  <Typography variant="h6" gutterBottom>
                    System Analytics
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Biometric Method Distribution
                          </Typography>
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            {dashboardData?.biometric_methods && Object.entries(dashboardData.biometric_methods).map(([type, count]: [string, any]) => (
                              <Box key={type}>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                  <Typography variant="body2">{type.charAt(0).toUpperCase() + type.slice(1)}</Typography>
                                  <Typography variant="body2">{count}</Typography>
                                </Box>
                                <LinearProgress 
                                  variant="determinate" 
                                  value={
                                    dashboardData.statistics.total_biometric_data > 0 
                                      ? (count / dashboardData.statistics.total_biometric_data) * 100 
                                      : 0
                                  } 
                                />
                              </Box>
                            ))}
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Performance Metrics
                          </Typography>
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                Authentication Success Rate
                              </Typography>
                              <Typography variant="h4" color="success.main">
                                {dashboardData?.statistics?.success_rate || 0}%
                              </Typography>
                            </Box>
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                Average Processing Time
                              </Typography>
                              <Typography variant="h4" color="primary.main">
                                {dashboardData?.performance_metrics?.avg_processing_time || 0}s
                              </Typography>
                            </Box>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </TabPanel>

                <TabPanel value={tabValue} index={3}>
                  <Typography variant="h6" gutterBottom>
                    System Performance
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Modality Performance Comparison
                          </Typography>
                          {modalityPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={modalityPlotUrl} alt="Modality Performance Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = modalityPlotUrl;
                                  a.download = 'modality_performance.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                  </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Processing Pipeline Analysis
                          </Typography>
                          {pipelineAnalysisPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={pipelineAnalysisPlotUrl} alt="Pipeline Analysis Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = pipelineAnalysisPlotUrl;
                                  a.download = 'pipeline_analysis.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </TabPanel>

                <TabPanel value={tabValue} index={4}>
                  <Typography variant="h6" gutterBottom>
                    Error Analysis
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Authentication Success/Failure Overview
                          </Typography>
                          {errorAnalysisPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={errorAnalysisPlotUrl} alt="Error Analysis Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = errorAnalysisPlotUrl;
                                  a.download = 'error_analysis.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                  </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            System Health Status
                          </Typography>
                          {systemHealthPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={systemHealthPlotUrl} alt="System Health Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = systemHealthPlotUrl;
                                  a.download = 'system_health.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </TabPanel>

                <TabPanel value={tabValue} index={5}>
                  <Typography variant="h6" gutterBottom>
                    Security Monitoring
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Failed Login Attempts
                          </Typography>
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            {dashboardData?.security_insights?.failed_attempts_by_type && 
                              Object.entries(dashboardData.security_insights.failed_attempts_by_type).map(([type, count]: [string, any]) => (
                                <Box key={type} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                  <Typography variant="body2">{type}</Typography>
                                  <Chip label={count} color="error" size="small" />
                                </Box>
                              ))
                            }
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Security Insights
                          </Typography>
                          <List dense>
                            <ListItem>
                              <ListItemIcon>
                                <TrendingUp color="primary" />
                              </ListItemIcon>
                              <ListItemText
                                primary="Most Used Biometric"
                                secondary={dashboardData?.security_insights?.most_used_biometric || "None"}
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemIcon>
                                <Schedule color="info" />
                              </ListItemIcon>
                              <ListItemText
                                primary="Peak Usage Hour"
                                secondary={dashboardData?.security_insights?.peak_usage_hour || "Unknown"}
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemIcon>
                                <CheckCircle color="success" />
                              </ListItemIcon>
                              <ListItemText
                                primary="Most Successful Day"
                                secondary={dashboardData?.security_insights?.most_successful_day || "Unknown"}
                              />
                            </ListItem>
                          </List>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </TabPanel>

                <TabPanel value={tabValue} index={6}>
                  <Typography variant="h6" gutterBottom>
                    Login History & Audit
                  </Typography>
                  <TableContainer component={Paper}>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>User</TableCell>
                          <TableCell>Type</TableCell>
                          <TableCell>Status</TableCell>
                          <TableCell>IP Address</TableCell>
                          <TableCell>Timestamp</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {dashboardData?.recent_login_attempts?.map((attempt: any, index: number) => (
                          <TableRow key={index}>
                            <TableCell>{attempt.username || 'Unknown'}</TableCell>
                            <TableCell>
                              <Chip 
                                label={attempt.attempt_type} 
                                size="small" 
                                variant="outlined"
                              />
                            </TableCell>
                            <TableCell>
                              <Chip
                                label={attempt.success ? 'Success' : 'Failed'}
                                color={attempt.success ? 'success' : 'error'}
                                size="small"
                              />
                            </TableCell>
                            <TableCell>{attempt.ip_address || 'Unknown'}</TableCell>
                            <TableCell>
                              {new Date(attempt.timestamp).toLocaleString()}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </TabPanel>

                <TabPanel value={tabValue} index={7}>
                  {/* 9. Downloadable Reports */}
                  <Typography variant="h6" gutterBottom>
                    Reports & Exports
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            System Report
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            Export comprehensive system data including users, biometric data, and login history.
                          </Typography>
                          <Button
                            variant="contained"
                            startIcon={<FileDownload />}
                            onClick={handleExportReport}
                            fullWidth
                          >
                            Export System Report
                          </Button>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Quick Stats
                          </Typography>
                          <List dense>
                            <ListItem>
                              <ListItemText
                                primary="Total Users"
                                secondary={dashboardData?.statistics?.total_users || 0}
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemText
                                primary="Active Users"
                                secondary={dashboardData?.statistics?.active_users || 0}
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemText
                                primary="Total Logins"
                                secondary={dashboardData?.statistics?.total_logins || 0}
                              />
                            </ListItem>
                            <ListItem>
                              <ListItemText
                                primary="Success Rate"
                                secondary={`${dashboardData?.statistics?.success_rate || 0}%`}
                              />
                            </ListItem>
                          </List>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </TabPanel>

                <TabPanel value={tabValue} index={8}>
                  <Typography variant="h6" gutterBottom>
                    Advanced Analytics
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Ablation Study
                          </Typography>
                          {ablationStudyPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={ablationStudyPlotUrl} alt="Ablation Study Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = ablationStudyPlotUrl;
                                  a.download = 'ablation_study.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Model Architecture
                          </Typography>
                          {modelArchitecturePlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={modelArchitecturePlotUrl} alt="Model Architecture Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = modelArchitecturePlotUrl;
                                  a.download = 'model_architecture.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Similarity Plots
                          </Typography>
                          {similarityPlotsUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={similarityPlotsUrl} alt="Similarity Plots" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = similarityPlotsUrl;
                                  a.download = 'similarity_plots.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Cross-Dataset Validation
                          </Typography>
                          {crossDatasetValidationPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={crossDatasetValidationPlotUrl} alt="Cross-Dataset Validation Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = crossDatasetValidationPlotUrl;
                                  a.download = 'cross_dataset_validation.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Data Augmentation Comparison
                          </Typography>
                          {dataAugmentationComparisonPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={dataAugmentationComparisonPlotUrl} alt="Data Augmentation Comparison Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = dataAugmentationComparisonPlotUrl;
                                  a.download = 'data_augmentation_comparison.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            False Positive/Negative Examples
                          </Typography>
                          {falsePositiveNegativeExamplesPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={falsePositiveNegativeExamplesPlotUrl} alt="False Positive/Negative Examples Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = falsePositiveNegativeExamplesPlotUrl;
                                  a.download = 'false_positive_negative_examples.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Feature Distribution Over Time
                          </Typography>
                          {featureDistributionTimePlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={featureDistributionTimePlotUrl} alt="Feature Distribution Over Time Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = featureDistributionTimePlotUrl;
                                  a.download = 'feature_distribution_time.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Model Performance by Class
                          </Typography>
                          {modelPerformanceByClassPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={modelPerformanceByClassPlotUrl} alt="Model Performance by Class Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = modelPerformanceByClassPlotUrl;
                                  a.download = 'model_performance_by_class.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Loss Landscape
                          </Typography>
                          {lossLandscapePlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={lossLandscapePlotUrl} alt="Loss Landscape Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = lossLandscapePlotUrl;
                                  a.download = 'loss_landscape.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Error Rate Threshold Curves
                          </Typography>
                          {errorRateThresholdCurvesPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={errorRateThresholdCurvesPlotUrl} alt="Error Rate Threshold Curves Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = errorRateThresholdCurvesPlotUrl;
                                  a.download = 'error_rate_threshold_curves.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Embedding Correlation Heatmap
                          </Typography>
                          {embeddingCorrelationHeatmapPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={embeddingCorrelationHeatmapPlotUrl} alt="Embedding Correlation Heatmap Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = embeddingCorrelationHeatmapPlotUrl;
                                  a.download = 'embedding_correlation_heatmap.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Model Inference Speed
                          </Typography>
                          {modelInferenceSpeedPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={modelInferenceSpeedPlotUrl} alt="Model Inference Speed Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = modelInferenceSpeedPlotUrl;
                                  a.download = 'model_inference_speed.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Learning Rate Schedules
                          </Typography>
                          {learningRateSchedulesPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={learningRateSchedulesPlotUrl} alt="Learning Rate Schedules Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = learningRateSchedulesPlotUrl;
                                  a.download = 'learning_rate_schedules.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Class Activation Mapping
                          </Typography>
                          {classActivationMappingPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={classActivationMappingPlotUrl} alt="Class Activation Mapping Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = classActivationMappingPlotUrl;
                                  a.download = 'class_activation_mapping.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Sensitivity Analysis
                          </Typography>
                          {sensitivityAnalysisPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={sensitivityAnalysisPlotUrl} alt="Sensitivity Analysis Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = sensitivityAnalysisPlotUrl;
                                  a.download = 'sensitivity_analysis.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Class-wise Precision, Recall, F1
                          </Typography>
                          {classWisePrecisionRecallF1PlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={classWisePrecisionRecallF1PlotUrl} alt="Class-wise Precision, Recall, F1 Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = classWisePrecisionRecallF1PlotUrl;
                                  a.download = 'class_wise_precision_recall_f1.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </TabPanel>

                <TabPanel value={tabValue} index={9}>
                  <Typography variant="h6" gutterBottom>
                    Model Analysis
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Model Architecture
                          </Typography>
                          {modelArchitecturePlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={modelArchitecturePlotUrl} alt="Model Architecture Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = modelArchitecturePlotUrl;
                                  a.download = 'model_architecture.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Similarity Plots
                          </Typography>
                          {similarityPlotsUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={similarityPlotsUrl} alt="Similarity Plots" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = similarityPlotsUrl;
                                  a.download = 'similarity_plots.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Cross-Dataset Validation
                          </Typography>
                          {crossDatasetValidationPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={crossDatasetValidationPlotUrl} alt="Cross-Dataset Validation Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = crossDatasetValidationPlotUrl;
                                  a.download = 'cross_dataset_validation.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Data Augmentation Comparison
                          </Typography>
                          {dataAugmentationComparisonPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={dataAugmentationComparisonPlotUrl} alt="Data Augmentation Comparison Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = dataAugmentationComparisonPlotUrl;
                                  a.download = 'data_augmentation_comparison.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            False Positive/Negative Examples
                          </Typography>
                          {falsePositiveNegativeExamplesPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={falsePositiveNegativeExamplesPlotUrl} alt="False Positive/Negative Examples Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = falsePositiveNegativeExamplesPlotUrl;
                                  a.download = 'false_positive_negative_examples.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Feature Distribution Over Time
                          </Typography>
                          {featureDistributionTimePlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={featureDistributionTimePlotUrl} alt="Feature Distribution Over Time Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = featureDistributionTimePlotUrl;
                                  a.download = 'feature_distribution_time.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Model Performance by Class
                          </Typography>
                          {modelPerformanceByClassPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={modelPerformanceByClassPlotUrl} alt="Model Performance by Class Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = modelPerformanceByClassPlotUrl;
                                  a.download = 'model_performance_by_class.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Loss Landscape
                          </Typography>
                          {lossLandscapePlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={lossLandscapePlotUrl} alt="Loss Landscape Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = lossLandscapePlotUrl;
                                  a.download = 'loss_landscape.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Error Rate Threshold Curves
                          </Typography>
                          {errorRateThresholdCurvesPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={errorRateThresholdCurvesPlotUrl} alt="Error Rate Threshold Curves Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = errorRateThresholdCurvesPlotUrl;
                                  a.download = 'error_rate_threshold_curves.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Embedding Correlation Heatmap
                          </Typography>
                          {embeddingCorrelationHeatmapPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={embeddingCorrelationHeatmapPlotUrl} alt="Embedding Correlation Heatmap Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = embeddingCorrelationHeatmapPlotUrl;
                                  a.download = 'embedding_correlation_heatmap.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Model Inference Speed
                          </Typography>
                          {modelInferenceSpeedPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={modelInferenceSpeedPlotUrl} alt="Model Inference Speed Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = modelInferenceSpeedPlotUrl;
                                  a.download = 'model_inference_speed.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Learning Rate Schedules
                          </Typography>
                          {learningRateSchedulesPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={learningRateSchedulesPlotUrl} alt="Learning Rate Schedules Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = learningRateSchedulesPlotUrl;
                                  a.download = 'learning_rate_schedules.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Class Activation Mapping
                          </Typography>
                          {classActivationMappingPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={classActivationMappingPlotUrl} alt="Class Activation Mapping Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = classActivationMappingPlotUrl;
                                  a.download = 'class_activation_mapping.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Sensitivity Analysis
                          </Typography>
                          {sensitivityAnalysisPlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={sensitivityAnalysisPlotUrl} alt="Sensitivity Analysis Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = sensitivityAnalysisPlotUrl;
                                  a.download = 'sensitivity_analysis.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            Class-wise Precision, Recall, F1
                          </Typography>
                          {classWisePrecisionRecallF1PlotUrl ? (
                            <Box sx={{ textAlign: 'center' }}>
                              <img src={classWisePrecisionRecallF1PlotUrl} alt="Class-wise Precision, Recall, F1 Plot" className="dashboard-img" />
                              <Button
                                variant="outlined"
                                sx={{ mt: 2 }}
                                onClick={() => {
                                  const a = document.createElement('a');
                                  a.href = classWisePrecisionRecallF1PlotUrl;
                                  a.download = 'class_wise_precision_recall_f1.png';
                                  a.click();
                                }}
                              >
                                Download Chart
                              </Button>
                            </Box>
                          ) : (
                            <Typography color="text.secondary">No plot available</Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </TabPanel>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>

      {/* Delete User Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Confirm User Deletion</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete user "{selectedUser?.username}"? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={confirmDeleteUser} color="error" variant="contained">
            Delete User
          </Button>
        </DialogActions>
      </Dialog>

      {/* User Details Dialog */}
      <Dialog 
        open={userDetailsDialogOpen} 
        onClose={() => setUserDetailsDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>User Details</DialogTitle>
        <DialogContent>
          {selectedUserDetails && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>User Information</Typography>
                <List dense>
                  <ListItem>
                    <ListItemText
                      primary="Name"
                      secondary={`${selectedUserDetails.user.first_name} ${selectedUserDetails.user.last_name}`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Username"
                      secondary={selectedUserDetails.user.username}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Email"
                      secondary={selectedUserDetails.user.email}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Status"
                      secondary={selectedUserDetails.user.is_active ? 'Active' : 'Inactive'}
                    />
                  </ListItem>
                </List>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>Statistics</Typography>
                <List dense>
                  <ListItem>
                    <ListItemText
                      primary="Total Logins"
                      secondary={selectedUserDetails.statistics.total_logins}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Success Rate"
                      secondary={`${selectedUserDetails.statistics.success_rate}%`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Biometric Methods"
                      secondary={selectedUserDetails.statistics.biometric_methods}
                    />
                  </ListItem>
                </List>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>Biometric Data</Typography>
                <TableContainer component={Paper}>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Type</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Created</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {selectedUserDetails.biometric_data.map((bio: any) => (
                        <TableRow key={bio.id}>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              {getBiometricIcon(bio.type)}
                              {bio.type}
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={bio.is_active ? 'Active' : 'Inactive'}
                              color={bio.is_active ? 'success' : 'error'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            {new Date(bio.created_at).toLocaleDateString()}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUserDetailsDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AdminDashboardPage; 