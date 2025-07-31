import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Paper,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Security,
  Lock,
  Key,
  Timeline,
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Warning,
  Error,
  AccountBalance,
  VerifiedUser,
  Fingerprint,
  Face,
  CameraAlt,
  LockOpen,
  VpnKey,
  Shield,
} from '@mui/icons-material';

interface BlockchainVisualizationProps {
  metrics?: any;
  transactions?: any[];
}

const BlockchainVisualization: React.FC<BlockchainVisualizationProps> = ({ 
  metrics, 
  transactions = [] 
}) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const [encryptionSteps, setEncryptionSteps] = useState([
    { step: 1, name: 'Biometric Capture', status: 'completed', icon: <Fingerprint /> },
    { step: 2, name: 'Feature Extraction', status: 'completed', icon: <Key /> },
    { step: 3, name: 'AES-256 Encryption', status: 'completed', icon: <Lock /> },
    { step: 4, name: 'Hash Generation', status: 'completed', icon: <Shield /> },
    { step: 5, name: 'Blockchain Minting', status: 'completed', icon: <AccountBalance /> },
    { step: 6, name: 'Token Verification', status: 'completed', icon: <VerifiedUser /> }
  ]);

  const [securityLayers, setSecurityLayers] = useState([
    { layer: 'Application Layer', strength: 95, color: 'success' as const },
    { layer: 'Transport Layer', strength: 98, color: 'primary' as const },
    { layer: 'Encryption Layer', strength: 99, color: 'secondary' as const },
    { layer: 'Blockchain Layer', strength: 100, color: 'info' as const }
  ]);

  const getStepColor = (status: string) => {
    switch (status) {
      case 'completed': return theme.palette.success.main;
      case 'in_progress': return theme.palette.warning.main;
      case 'pending': return theme.palette.info.main;
      case 'failed': return theme.palette.error.main;
      default: return theme.palette.grey[500];
    }
  };

  const getStepIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle color="success" />;
      case 'in_progress': return <Warning color="warning" />;
      case 'pending': return <Timeline color="info" />;
      case 'failed': return <Error color="error" />;
      default: return <Timeline />;
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Blockchain Security Visualization
      </Typography>

      {/* Encryption Process Flow */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Biometric Encryption Process
          </Typography>
          <Grid container spacing={2}>
            {encryptionSteps.map((step, index) => (
              <Grid item xs={12} sm={6} md={4} key={step.step}>
                <Paper
                  sx={{
                    p: 2,
                    textAlign: 'center',
                    border: `2px solid ${getStepColor(step.status)}`,
                    borderRadius: 2,
                    position: 'relative',
                    '&::after': index < encryptionSteps.length - 1 ? {
                      content: '""',
                      position: 'absolute',
                      top: '50%',
                      right: '-20px',
                      width: '20px',
                      height: '2px',
                      backgroundColor: getStepColor(step.status),
                      transform: 'translateY(-50%)',
                      [theme.breakpoints.down('md')]: {
                        display: 'none'
                      }
                    } : {}
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'center', mb: 1 }}>
                    {step.icon}
                  </Box>
                  <Typography variant="subtitle2" fontWeight="bold">
                    Step {step.step}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {step.name}
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    {getStepIcon(step.status)}
                  </Box>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Security Layers */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Security Layer Strength
              </Typography>
              <List>
                {securityLayers.map((layer, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Shield color={layer.color as 'success' | 'primary' | 'secondary' | 'info'} />
                    </ListItemIcon>
                    <ListItemText
                      primary={layer.layer}
                      secondary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Box
                            sx={{
                              width: '100%',
                              height: 8,
                              backgroundColor: theme.palette.grey[200],
                              borderRadius: 4,
                              overflow: 'hidden'
                            }}
                          >
                            <Box
                              sx={{
                                width: `${layer.strength}%`,
                                height: '100%',
                                backgroundColor: theme.palette[layer.color as 'success' | 'primary' | 'secondary' | 'info'].main,
                                transition: 'width 0.3s ease'
                              }}
                            />
                          </Box>
                          <Typography variant="body2" color="text.secondary">
                            {layer.strength}%
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Blockchain Network Status
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2">Network Status</Typography>
                  <Chip label="Active" color="success" size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2">Consensus</Typography>
                  <Chip label="Proof of Stake" color="primary" size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2">Block Time</Typography>
                  <Typography variant="body2">~12 seconds</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2">Gas Price</Typography>
                  <Typography variant="body2">20 Gwei</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2">Contract Address</Typography>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.75rem' }}>
                    0x1234...5678
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Transaction Flow Diagram */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Transaction Flow
          </Typography>
          <Box sx={{ 
            display: 'flex', 
            flexDirection: isMobile ? 'column' : 'row',
            alignItems: 'center',
            gap: 2,
            flexWrap: 'wrap'
          }}>
            {/* User */}
            <Paper sx={{ p: 2, textAlign: 'center', minWidth: 120 }}>
              <VerifiedUser color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="body2" fontWeight="bold">User</Typography>
              <Typography variant="caption" color="text.secondary">Biometric Input</Typography>
            </Paper>

            {/* Arrow */}
            <Box sx={{ 
              display: isMobile ? 'none' : 'block',
              fontSize: 24,
              color: theme.palette.primary.main 
            }}>
              →
            </Box>

            {/* Encryption */}
            <Paper sx={{ p: 2, textAlign: 'center', minWidth: 120 }}>
              <Lock color="secondary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="body2" fontWeight="bold">Encryption</Typography>
              <Typography variant="caption" color="text.secondary">AES-256</Typography>
            </Paper>

            {/* Arrow */}
            <Box sx={{ 
              display: isMobile ? 'none' : 'block',
              fontSize: 24,
              color: theme.palette.primary.main 
            }}>
              →
            </Box>

            {/* Blockchain */}
            <Paper sx={{ p: 2, textAlign: 'center', minWidth: 120 }}>
              <AccountBalance color="success" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="body2" fontWeight="bold">Blockchain</Typography>
              <Typography variant="caption" color="text.secondary">NFT Minting</Typography>
            </Paper>

            {/* Arrow */}
            <Box sx={{ 
              display: isMobile ? 'none' : 'block',
              fontSize: 24,
              color: theme.palette.primary.main 
            }}>
              →
            </Box>

            {/* Verification */}
            <Paper sx={{ p: 2, textAlign: 'center', minWidth: 120 }}>
              <CheckCircle color="info" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="body2" fontWeight="bold">Verification</Typography>
              <Typography variant="caption" color="text.secondary">Smart Contract</Typography>
            </Paper>
          </Box>
        </CardContent>
      </Card>

      {/* Security Features */}
      <Grid container spacing={2} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <LockOpen color="primary" sx={{ fontSize: 32, mb: 1 }} />
            <Typography variant="body2" fontWeight="bold">Immutable</Typography>
            <Typography variant="caption" color="text.secondary">
              Data cannot be altered once stored
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <VpnKey color="secondary" sx={{ fontSize: 32, mb: 1 }} />
            <Typography variant="body2" fontWeight="bold">Decentralized</Typography>
            <Typography variant="caption" color="text.secondary">
              No single point of failure
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Shield color="success" sx={{ fontSize: 32, mb: 1 }} />
            <Typography variant="body2" fontWeight="bold">Tamper-Proof</Typography>
            <Typography variant="caption" color="text.secondary">
              Cryptographic verification
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Timeline color="info" sx={{ fontSize: 32, mb: 1 }} />
            <Typography variant="body2" fontWeight="bold">Auditable</Typography>
            <Typography variant="caption" color="text.secondary">
              Complete transaction history
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default BlockchainVisualization; 