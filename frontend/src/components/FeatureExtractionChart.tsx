import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Paper,
  LinearProgress,
} from '@mui/material';

interface FeatureExtractionChartProps {
  biometricData: any[];
}

const FeatureExtractionChart: React.FC<FeatureExtractionChartProps> = ({ biometricData }) => {
  const getFeatureData = (type: string) => {
    const mockFeatures = {
      fingerprint: {
        minutiae: 45,
        ridgeCount: 12,
        quality: 'High',
        processingTime: '0.8s',
      },
      face: {
        landmarks: 68,
        faceQuality: 'Excellent',
        lighting: 'Good',
        processingTime: '1.2s',
      },
      palmprint: {
        principalLines: 3,
        wrinkles: 8,
        quality: 'Medium',
        processingTime: '1.0s',
      },
    };
    return mockFeatures[type as keyof typeof mockFeatures] || {};
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Feature Extraction Analysis
      </Typography>
      
      <Grid container spacing={3}>
        {biometricData.map((bio) => {
          const features = getFeatureData(bio.type);
          
          return (
            <Grid item xs={12} md={6} key={bio.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {bio.type.charAt(0).toUpperCase() + bio.type.slice(1)} Features
                  </Typography>
                  
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Confidence Score
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={bio.confidence * 100}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {Math.round(bio.confidence * 100)}%
                    </Typography>
                  </Box>
                  
                  <Grid container spacing={2}>
                    {bio.type === 'fingerprint' && (
                      <>
                        <Grid item xs={6}>
                          <Paper sx={{ p: 2, textAlign: 'center' }}>
                            <Typography variant="h6" color="primary">
                              {(features as any).minutiae}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Minutiae Points
                            </Typography>
                          </Paper>
                        </Grid>
                        <Grid item xs={6}>
                          <Paper sx={{ p: 2, textAlign: 'center' }}>
                            <Typography variant="h6" color="primary">
                              {(features as any).ridgeCount}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Ridge Count
                            </Typography>
                          </Paper>
                        </Grid>
                      </>
                    )}
                    
                    {bio.type === 'face' && (
                      <>
                        <Grid item xs={6}>
                          <Paper sx={{ p: 2, textAlign: 'center' }}>
                            <Typography variant="h6" color="primary">
                              {(features as any).landmarks}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Facial Landmarks
                            </Typography>
                          </Paper>
                        </Grid>
                        <Grid item xs={6}>
                          <Paper sx={{ p: 2, textAlign: 'center' }}>
                            <Typography variant="h6" color="primary">
                              {(features as any).faceQuality}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Face Quality
                            </Typography>
                          </Paper>
                        </Grid>
                      </>
                    )}
                    
                    {bio.type === 'palmprint' && (
                      <>
                        <Grid item xs={6}>
                          <Paper sx={{ p: 2, textAlign: 'center' }}>
                            <Typography variant="h6" color="primary">
                              {(features as any).principalLines}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Principal Lines
                            </Typography>
                          </Paper>
                        </Grid>
                        <Grid item xs={6}>
                          <Paper sx={{ p: 2, textAlign: 'center' }}>
                            <Typography variant="h6" color="primary">
                              {(features as any).wrinkles}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Wrinkles
                            </Typography>
                          </Paper>
                        </Grid>
                      </>
                    )}
                  </Grid>
                  
                  <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Processing Information
                    </Typography>
                    <Typography variant="body2">
                      Quality: {(features as any).quality}
                    </Typography>
                    <Typography variant="body2">
                      Processing Time: {(features as any).processingTime}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>
    </Box>
  );
};

export default FeatureExtractionChart; 