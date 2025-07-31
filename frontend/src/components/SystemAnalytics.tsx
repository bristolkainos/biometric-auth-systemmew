import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Paper,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  People,
  Security,
  Timeline,
  CheckCircle,
  Warning,
  Error,
} from '@mui/icons-material';

interface SystemAnalyticsProps {
  systemStats: any;
}

const SystemAnalytics: React.FC<SystemAnalyticsProps> = ({ systemStats }) => {
  const getMetricColor = (value: number, threshold: number = 80) => {
    if (value >= threshold) return 'success';
    if (value >= threshold * 0.7) return 'warning';
    return 'error';
  };

  const getTrendIcon = (trend: string) => {
    return trend === 'up' ? <TrendingUp color="success" /> : <TrendingDown color="error" />;
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        System Analytics & Performance Metrics
      </Typography>
      
      <Grid container spacing={3}>
        {/* Key Metrics */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <People color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  {systemStats?.totalUsers || 0}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Total Users
              </Typography>
              <Typography variant="caption" color="success.main">
                +{systemStats?.activeUsers || 0} active
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Security color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  {systemStats?.successRate || 0}%
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Success Rate
              </Typography>
              <Typography variant="caption" color="success.main">
                {systemStats?.totalLogins || 0} total logins
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Warning color="warning" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  {systemStats?.failedAttempts || 0}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Failed Attempts
              </Typography>
              <Typography variant="caption" color="warning.main">
                Last 24 hours
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Timeline color="info" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  {systemStats?.biometricMethods?.fingerprint + 
                   systemStats?.biometricMethods?.face + 
                   systemStats?.biometricMethods?.palmprint || 0}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Total Biometric Methods
              </Typography>
              <Typography variant="caption" color="info.main">
                Across all users
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Biometric Usage Breakdown */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Biometric Method Usage
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Fingerprint</Typography>
                  <Typography variant="body2">
                    {systemStats?.biometricMethods?.fingerprint || 0} users
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={(systemStats?.biometricMethods?.fingerprint / systemStats?.totalUsers) * 100 || 0}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Face Recognition</Typography>
                  <Typography variant="body2">
                    {systemStats?.biometricMethods?.face || 0} users
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={(systemStats?.biometricMethods?.face / systemStats?.totalUsers) * 100 || 0}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Palmprint</Typography>
                  <Typography variant="body2">
                    {systemStats?.biometricMethods?.palmprint || 0} users
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={(systemStats?.biometricMethods?.palmprint / systemStats?.totalUsers) * 100 || 0}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent System Activity
              </Typography>
              
              <List dense>
                {systemStats?.recentActivity?.map((activity: any, index: number) => (
                  <ListItem key={index} divider>
                    <ListItemIcon>
                      {getTrendIcon(activity.trend)}
                    </ListItemIcon>
                    <ListItemText
                      primary={activity.type.replace('_', ' ').toUpperCase()}
                      secondary={`${activity.count} events in last 24 hours`}
                    />
                    <Typography
                      variant="body2"
                      color={activity.trend === 'up' ? 'success.main' : 'error.main'}
                    >
                      {activity.trend === 'up' ? '+' : '-'}{activity.count}
                    </Typography>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Performance Metrics */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Performance Metrics
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="primary.main">
                      {systemStats?.successRate || 0}%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Authentication Success Rate
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={systemStats?.successRate || 0}
                      color={getMetricColor(systemStats?.successRate || 0) as any}
                      sx={{ mt: 1, height: 6 }}
                    />
                  </Paper>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="success.main">
                      {systemStats?.activeUsers || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Active Users
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={(systemStats?.activeUsers / systemStats?.totalUsers) * 100 || 0}
                      color="success"
                      sx={{ mt: 1, height: 6 }}
                    />
                  </Paper>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="warning.main">
                      {systemStats?.failedAttempts || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Failed Login Attempts
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={Math.min((systemStats?.failedAttempts / systemStats?.totalLogins) * 100 || 0, 100)}
                      color="warning"
                      sx={{ mt: 1, height: 6 }}
                    />
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SystemAnalytics; 