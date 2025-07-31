import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Grid,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import {
  Fingerprint,
  Face,
  CameraAlt,
  CheckCircle,
  Warning,
  Schedule,
} from '@mui/icons-material';

interface BiometricDetailsProps {
  biometricData: any[];
}

const BiometricDetails: React.FC<BiometricDetailsProps> = ({ biometricData }) => {
  const getBiometricIcon = (type: string) => {
    switch (type) {
      case 'fingerprint': return <Fingerprint />;
      case 'face': return <Face />;
      case 'palmprint': return <CameraAlt />;
      default: return <Fingerprint />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle color="success" />;
      case 'inactive': return <Warning color="error" />;
      case 'pending': return <Schedule color="warning" />;
      default: return <Warning color="error" />;
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Biometric Authentication Details
      </Typography>
      
      <Grid container spacing={3}>
        {biometricData.map((bio) => (
          <Grid item xs={12} md={6} key={bio.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  {getBiometricIcon(bio.type)}
                  <Typography variant="h6">
                    {bio.type.charAt(0).toUpperCase() + bio.type.slice(1)} Recognition
                  </Typography>
                  {getStatusIcon(bio.status)}
                </Box>
                
                <List dense>
                  <ListItem>
                    <ListItemText
                      primary="Confidence Score"
                      secondary={bio.confidence != null && !isNaN(bio.confidence) 
                        ? `${Math.round(bio.confidence * 100)}%` 
                        : 'N/A'}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Registered"
                      secondary={bio.registeredAt 
                        ? new Date(bio.registeredAt).toLocaleDateString() 
                        : 'Invalid Date'}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Last Used"
                      secondary={bio.lastUsed 
                        ? new Date(bio.lastUsed).toLocaleDateString() 
                        : 'Invalid Date'}
                    />
                  </ListItem>
                </List>
                
                <Box sx={{ mt: 2 }}>
                  <Chip
                    label={bio.status}
                    color={bio.status === 'active' ? 'success' : 'error'}
                    size="small"
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default BiometricDetails; 