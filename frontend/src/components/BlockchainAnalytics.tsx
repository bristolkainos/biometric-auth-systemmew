import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  CircularProgress,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
} from '@mui/material';
import {
  AccountBalance,
  Security,
  Timeline,
  CheckCircle,
  Error,
  Warning,
  Refresh,
  Fingerprint,
  Face,
  CameraAlt,
  VerifiedUser,
  Key,
  Lock,
  Download,
  GetApp,
  PictureAsPdf,
  Image as ImageIcon,
} from '@mui/icons-material';

// Chart.js imports for visualizations
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
  RadialLinearScale,
  LineController,
  BarController,
  DoughnutController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  BubbleController,
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
  Filler,
  RadialLinearScale,
  LineController,
  BarController,
  DoughnutController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  BubbleController
);

interface BlockchainAnalyticsProps {
  userData?: any;
}

interface Transaction {
  id: string;
  type: 'biometric_mint' | 'verification' | 'access_grant' | 'security_update';
  timestamp: string;
  status: 'success' | 'pending' | 'failed';
  hash: string;
  biometricType?: string;
  description: string;
  gasUsed?: number;
  blockNumber?: number;
}

interface SecurityMetrics {
  totalTransactions: number;
  successfulTransactions: number;
  failedTransactions: number;
  averageGasUsed: number;
  lastBlockNumber: number;
  encryptionStrength: number;
  biometricTokens: number;
  securityScore: number;
}

const BlockchainAnalytics: React.FC<BlockchainAnalyticsProps> = ({ userData }) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [metrics, setMetrics] = useState<SecurityMetrics | null>(null);
  const [loading, setLoading] = useState(false);
  const [downloadLoading, setDownloadLoading] = useState(false);
  const [exportDialogOpen, setExportDialogOpen] = useState(false);
  // Removed unused selectedExportType variables

  // Chart refs for download functionality
  const transactionChartRef = useRef<any>(null);
  const statusChartRef = useRef<any>(null);
  const gasChartRef = useRef<any>(null);

  // Mock data for demonstration
  useEffect(() => {
    const mockTransactions: Transaction[] = [
      {
        id: 'tx_001',
        type: 'biometric_mint',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        status: 'success',
        hash: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
        biometricType: 'fingerprint',
        description: 'Fingerprint biometric token minted',
        gasUsed: 21000,
        blockNumber: 12345678
      },
      {
        id: 'tx_002',
        type: 'biometric_mint',
        timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
        status: 'success',
        hash: '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        biometricType: 'face',
        description: 'Face recognition biometric token minted',
        gasUsed: 25000,
        blockNumber: 12345675
      },
      {
        id: 'tx_003',
        type: 'verification',
        timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        status: 'success',
        hash: '0x9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba',
        biometricType: 'fingerprint',
        description: 'Biometric verification completed',
        gasUsed: 15000,
        blockNumber: 12345680
      },
      {
        id: 'tx_004',
        type: 'access_grant',
        timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
        status: 'pending',
        hash: '0xfedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210',
        description: 'Access permissions updated',
        gasUsed: 18000,
        blockNumber: 12345682
      },
      {
        id: 'tx_005',
        type: 'security_update',
        timestamp: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
        status: 'success',
        hash: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
        description: 'Security protocol updated',
        gasUsed: 30000,
        blockNumber: 12345670
      }
    ];

    const mockMetrics: SecurityMetrics = {
      totalTransactions: 156,
      successfulTransactions: 152,
      failedTransactions: 4,
      averageGasUsed: 22000,
      lastBlockNumber: 12345682,
      encryptionStrength: 95,
      biometricTokens: 3,
      securityScore: 92
    };

    setTransactions(mockTransactions);
    setMetrics(mockMetrics);
  }, []);

  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'biometric_mint': return <Fingerprint />;
      case 'verification': return <VerifiedUser />;
      case 'access_grant': return <Key />;
      case 'security_update': return <Security />;
      default: return <Timeline />;
    }
  };

  const getBiometricIcon = (type?: string) => {
    switch (type) {
      case 'fingerprint': return <Fingerprint />;
      case 'face': return <Face />;
      case 'palmprint': return <CameraAlt />;
      default: return <Security />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'success';
      case 'pending': return 'warning';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success': return <CheckCircle />;
      case 'pending': return <Warning />;
      case 'failed': return <Error />;
      default: return <Timeline />;
    }
  };

  const formatHash = (hash: string) => {
    return `${hash.substring(0, 8)}...${hash.substring(hash.length - 8)}`;
  };

  // Chart data preparation
  const getTransactionChartData = () => {
    const transactionTypes = transactions.reduce((acc, tx) => {
      acc[tx.type] = (acc[tx.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return {
      labels: Object.keys(transactionTypes),
      datasets: [{
        label: 'Transaction Count',
        data: Object.values(transactionTypes),
        backgroundColor: [
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(255, 205, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(255, 205, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 2,
      }]
    };
  };

  const getSecurityMetricsChartData = () => {
    if (!metrics) return null;

    return {
      labels: ['Successful', 'Failed', 'Pending'],
      datasets: [{
        label: 'Transactions',
        data: [
          metrics.successfulTransactions,
          metrics.failedTransactions,
          metrics.totalTransactions - metrics.successfulTransactions - metrics.failedTransactions
        ],
        backgroundColor: [
          'rgba(75, 192, 192, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(255, 205, 86, 0.8)',
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(255, 205, 86, 1)',
        ],
        borderWidth: 2,
      }]
    };
  };

  const getGasUsageChartData = () => {
    const gasData = transactions
      .filter(tx => tx.gasUsed)
      .slice(-10)
      .map((tx, index) => ({
        x: `Block ${tx.blockNumber}`,
        y: tx.gasUsed || 0
      }));

    return {
      labels: gasData.map(d => d.x),
      datasets: [{
        label: 'Gas Used',
        data: gasData.map(d => d.y),
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.1)',
        fill: true,
        tension: 0.4,
      }]
    };
  };

  // Download functions
  const downloadChartAsImage = async (chartRef: any, filename: string) => {
    if (chartRef && chartRef.current) {
      const canvas = chartRef.current.canvas;
      const link = document.createElement('a');
      link.download = `${filename}.png`;
      link.href = canvas.toDataURL();
      link.click();
    }
  };

  const downloadReport = async () => {
    setDownloadLoading(true);
    try {
      const reportData = {
        timestamp: new Date().toISOString(),
        metrics,
        transactions,
        summary: {
          totalTransactions: metrics?.totalTransactions || 0,
          securityScore: metrics?.securityScore || 0,
          encryptionStrength: metrics?.encryptionStrength || 0
        }
      };

      const blob = new Blob([JSON.stringify(reportData, null, 2)], {
        type: 'application/json'
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'blockchain_analytics_report.json';
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading report:', error);
    } finally {
      setDownloadLoading(false);
    }
  };

  const handleRefresh = () => {
    setLoading(true);
    // Simulate refresh
    setTimeout(() => {
      console.log('Data refreshed');
      setLoading(false);
    }, 1000);
  };

  if (!metrics) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Blockchain Security Analytics
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            startIcon={<Refresh />}
            onClick={handleRefresh}
            variant="outlined"
            size="small"
            disabled={loading}
          >
            {loading ? <CircularProgress size={16} /> : 'Refresh'}
          </Button>
          <Button
            startIcon={<GetApp />}
            onClick={() => setExportDialogOpen(true)}
            variant="contained"
            size="small"
            disabled={downloadLoading}
          >
            Export Data
          </Button>
        </Box>
      </Box>

      {/* Security Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <AccountBalance color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="primary">
                {metrics?.totalTransactions || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Transactions
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Security color="success" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="success.main">
                {metrics?.securityScore || 0}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Security Score
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Lock color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="primary">
                {metrics?.encryptionStrength || 0}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Encryption Strength
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Fingerprint color="secondary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="secondary.main">
                {metrics?.biometricTokens || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Biometric Tokens
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Blockchain Visualizations */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Transaction Types Distribution
                </Typography>
                <Tooltip title="Download Chart">
                  <IconButton 
                    size="small" 
                    onClick={() => downloadChartAsImage(transactionChartRef, 'transaction-types')}
                  >
                    <Download />
                  </IconButton>
                </Tooltip>
              </Box>
              <Box sx={{ height: 300, position: 'relative' }}>
                <Doughnut 
                  ref={transactionChartRef}
                  data={getTransactionChartData()}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                    },
                  }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Transaction Status
                </Typography>
                <Tooltip title="Download Chart">
                  <IconButton 
                    size="small" 
                    onClick={() => downloadChartAsImage(statusChartRef, 'transaction-status')}
                  >
                    <Download />
                  </IconButton>
                </Tooltip>
              </Box>
              <Box sx={{ height: 300, position: 'relative' }}>
                {getSecurityMetricsChartData() && (
                  <Doughnut 
                    ref={statusChartRef}
                    data={getSecurityMetricsChartData()!}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom',
                        },
                      },
                    }}
                  />
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Gas Usage Over Time
                </Typography>
                <Tooltip title="Download Chart">
                  <IconButton 
                    size="small" 
                    onClick={() => downloadChartAsImage(gasChartRef, 'gas-usage')}
                  >
                    <Download />
                  </IconButton>
                </Tooltip>
              </Box>
              <Box sx={{ height: 300, position: 'relative' }}>
                <Line 
                  ref={gasChartRef}
                  data={getGasUsageChartData()}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        display: false,
                      },
                    },
                    scales: {
                      y: {
                        beginAtZero: true,
                        title: {
                          display: true,
                          text: 'Gas Used'
                        }
                      },
                      x: {
                        title: {
                          display: true,
                          text: 'Block Number'
                        }
                      }
                    },
                  }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Export Options */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              Export Blockchain Data
            </Typography>
          </Box>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<ImageIcon />}
                onClick={() => downloadChartAsImage(transactionChartRef, 'blockchain-transactions')}
                disabled={downloadLoading}
              >
                Download Charts
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<PictureAsPdf />}
                onClick={() => setExportDialogOpen(true)}
                disabled={downloadLoading}
              >
                Export Report
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<GetApp />}
                onClick={downloadReport}
                disabled={downloadLoading}
              >
                JSON Report
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<Refresh />}
                onClick={handleRefresh}
                disabled={loading}
              >
                {loading ? <CircularProgress size={20} /> : 'Refresh Data'}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Security Alerts */}
      <Alert severity="info" sx={{ mt: 3 }}>
        <Typography variant="body2">
          <strong>Blockchain Security:</strong> All biometric data is encrypted and stored as non-fungible tokens (NFTs) 
          on the blockchain, ensuring immutability and tamper-proof verification. Each transaction is cryptographically 
          signed and verified by the network.
        </Typography>
      </Alert>

      {/* Export Dialog */}
      <Dialog open={exportDialogOpen} onClose={() => setExportDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Export Blockchain Report</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Choose what you want to export:
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<ImageIcon />}
                onClick={() => {
                  downloadChartAsImage(transactionChartRef, 'blockchain-transaction-types');
                  downloadChartAsImage(statusChartRef, 'blockchain-transaction-status');
                  downloadChartAsImage(gasChartRef, 'blockchain-gas-usage');
                  setExportDialogOpen(false);
                }}
                disabled={downloadLoading}
              >
                Download All Charts (PNG)
              </Button>
            </Grid>
            <Grid item xs={12}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<GetApp />}
                onClick={() => {
                  downloadReport();
                  setExportDialogOpen(false);
                }}
                disabled={downloadLoading}
              >
                Download JSON Report
              </Button>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setExportDialogOpen(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Recent Transactions */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recent Blockchain Transactions
          </Typography>
          
          <List>
            {transactions.map((tx, index) => (
              <React.Fragment key={tx.id}>
                <ListItem>
                  <ListItemIcon>
                    {getTransactionIcon(tx.type)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                        <Typography variant="body1" fontWeight="medium">
                          {tx.description}
                        </Typography>
                        {tx.biometricType && (
                          <Tooltip title={tx.biometricType}>
                            <IconButton size="small">
                              {getBiometricIcon(tx.biometricType)}
                            </IconButton>
                          </Tooltip>
                        )}
                        <Chip
                          icon={getStatusIcon(tx.status)}
                          label={tx.status}
                          color={getStatusColor(tx.status) as any}
                          size="small"
                        />
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          {new Date(tx.timestamp).toLocaleString()}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ fontFamily: 'monospace' }}>
                          Hash: {formatHash(tx.hash)}
                        </Typography>
                        {tx.blockNumber && (
                          <Typography variant="body2" color="text.secondary">
                            Block: #{tx.blockNumber.toLocaleString()} | Gas: {tx.gasUsed?.toLocaleString()}
                          </Typography>
                        )}
                      </Box>
                    }
                  />
                </ListItem>
                {index < transactions.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </CardContent>
      </Card>
    </Box>
  );
};

export default BlockchainAnalytics; 