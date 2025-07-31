import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Box,
  Chip,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Download as DownloadIcon,
  Close as CloseIcon,
  Fullscreen as FullscreenIcon
} from '@mui/icons-material';

interface VisualizationData {
  id: string;
  type: string;
  title?: string;
  description?: string;
  data?: string; // Base64 encoded image or data URL
  format?: string; // 'image/png', 'image/jpeg', etc.
  metadata?: any;
}

interface BiometricEntry {
  id: number;
  type: string;
  analysis_data: {
    generated_visualizations?: VisualizationData[];
    processing_steps?: any[];
    quality_score?: number;
    [key: string]: any;
  };
}

interface VisualizationModalProps {
  open: boolean;
  onClose: () => void;
  entry: BiometricEntry | null;
}

const VisualizationModal: React.FC<VisualizationModalProps> = ({
  open,
  onClose,
  entry
}) => {
  const [selectedVisualization, setSelectedVisualization] = useState<VisualizationData | null>(null);

  const handleDownload = (visualization: VisualizationData) => {
    if (!visualization.data) return;

    try {
      // Create a temporary link element for download
      const link = document.createElement('a');
      link.href = visualization.data;
      
      // Generate filename
      const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
      const filename = `${entry?.type || 'biometric'}_${entry?.id || 'unknown'}_${visualization.type}_${timestamp}.png`;
      
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading visualization:', error);
    }
  };

  const handleFullscreen = (visualization: VisualizationData) => {
    setSelectedVisualization(visualization);
  };

  const visualizations = React.useMemo(() => 
    entry?.analysis_data?.generated_visualizations || [], 
    [entry?.analysis_data?.generated_visualizations]
  );
  
  // Debug logging
  React.useEffect(() => {
    if (open && entry) {
      console.log('VisualizationModal - Entry data:', entry);
      console.log('VisualizationModal - Analysis data:', entry.analysis_data);
      console.log('VisualizationModal - Visualizations:', visualizations);
      visualizations.forEach((viz, index) => {
        console.log(`Visualization ${index}:`, {
          id: viz.id,
          type: viz.type,
          title: viz.title,
          hasData: !!viz.data,
          dataPrefix: viz.data ? viz.data.substring(0, 50) + '...' : 'No data'
        });
      });
    }
  }, [open, entry, visualizations]);

  return (
    <>
      <Dialog
        open={open}
        onClose={onClose}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: { minHeight: '80vh' }
        }}
      >
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">
              Biometric Analysis Visualizations - {entry?.type} (ID: {entry?.id})
            </Typography>
            <IconButton onClick={onClose} size="small">
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>

        <DialogContent dividers>
          {visualizations.length === 0 ? (
            <Box textAlign="center" py={4}>
              <Typography variant="body1" color="text.secondary">
                No visualizations available for this biometric entry.
              </Typography>
            </Box>
          ) : (
            <Grid container spacing={3}>
              {visualizations.map((viz, index) => (
                <Grid item xs={12} sm={6} md={4} key={viz.id || index}>
                  <Card elevation={2}>
                    {viz.data ? (
                      <Box
                        sx={{
                          height: 200,
                          backgroundColor: '#f5f5f5',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          cursor: 'pointer',
                          overflow: 'hidden'
                        }}
                        onClick={() => handleFullscreen(viz)}
                      >
                        <img
                          src={viz.data}
                          alt={viz.title || `Visualization ${index + 1}`}
                          style={{
                            maxWidth: '100%',
                            maxHeight: '100%',
                            objectFit: 'contain'
                          }}
                          onError={(e) => {
                            console.error('Image loading error for visualization:', viz.id, e);
                            e.currentTarget.style.display = 'none';
                            e.currentTarget.parentElement!.innerHTML = `
                              <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:#666;">
                                <div>Image Loading Error</div>
                                <div style="font-size:12px;margin-top:8px;">Check console for details</div>
                              </div>
                            `;
                          }}
                          onLoad={() => {
                            console.log('Image loaded successfully for visualization:', viz.id);
                          }}
                        />
                      </Box>
                    ) : (
                      <Box
                        sx={{
                          height: 200,
                          backgroundColor: '#f5f5f5',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: '#666'
                        }}
                      >
                        <Typography variant="body2">No image data available</Typography>
                      </Box>
                    )}
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {viz.title || `Visualization ${index + 1}`}
                      </Typography>
                      <Chip 
                        label={viz.type || 'Unknown'} 
                        size="small" 
                        color="primary" 
                        sx={{ mb: 1 }}
                      />
                      {viz.description && (
                        <Typography variant="body2" color="text.secondary">
                          {viz.description}
                        </Typography>
                      )}
                    </CardContent>
                    <CardActions>
                      <Tooltip title="View Fullscreen">
                        <IconButton
                          size="small"
                          onClick={() => handleFullscreen(viz)}
                          disabled={!viz.data}
                        >
                          <FullscreenIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Download">
                        <IconButton
                          size="small"
                          onClick={() => handleDownload(viz)}
                          disabled={!viz.data}
                        >
                          <DownloadIcon />
                        </IconButton>
                      </Tooltip>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}

          {/* Analysis Summary */}
          {entry?.analysis_data && (
            <Box mt={4}>
              <Typography variant="h6" gutterBottom>
                Analysis Summary
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <Card variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="primary">
                      {entry.analysis_data.processing_steps?.length || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Processing Steps
                    </Typography>
                  </Card>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Card variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="primary">
                      {visualizations.length}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Visualizations
                    </Typography>
                  </Card>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Card variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="primary">
                      {entry.analysis_data.quality_score ? `${entry.analysis_data.quality_score}%` : 'N/A'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Quality Score
                    </Typography>
                  </Card>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Card variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="primary">
                      {entry.analysis_data.processing_time || 'N/A'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Processing Time
                    </Typography>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose} variant="outlined">
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Fullscreen Visualization Dialog */}
      <Dialog
        open={selectedVisualization !== null}
        onClose={() => setSelectedVisualization(null)}
        maxWidth="xl"
        fullWidth
        PaperProps={{
          sx: { 
            height: '90vh',
            backgroundColor: 'rgba(0, 0, 0, 0.9)'
          }
        }}
      >
        <DialogTitle sx={{ color: 'white' }}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">
              {selectedVisualization?.title || 'Visualization'}
            </Typography>
            <Box>
              <IconButton
                onClick={() => selectedVisualization && handleDownload(selectedVisualization)}
                sx={{ color: 'white', mr: 1 }}
              >
                <DownloadIcon />
              </IconButton>
              <IconButton
                onClick={() => setSelectedVisualization(null)}
                sx={{ color: 'white' }}
              >
                <CloseIcon />
              </IconButton>
            </Box>
          </Box>
        </DialogTitle>
        <DialogContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', p: 2 }}>
          {selectedVisualization?.data && (
            <Box
              component="img"
              src={selectedVisualization.data}
              alt={selectedVisualization.title || 'Visualization'}
              sx={{
                maxWidth: '100%',
                maxHeight: '100%',
                objectFit: 'contain'
              }}
            />
          )}
        </DialogContent>
      </Dialog>
    </>
  );
};

export default VisualizationModal;
