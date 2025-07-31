import React from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Visibility,
  LocationOn,
  AccessTime,
  Security,
} from '@mui/icons-material';

interface LoginHistoryProps {
  loginHistory: any[];
}

const LoginHistory: React.FC<LoginHistoryProps> = ({ loginHistory }) => {
  const getMethodIcon = (method: string | undefined) => {
    if (!method) return <Security />;
    if (method.includes('fingerprint')) return <Security />;
    if (method.includes('face')) return <Security />;
    if (method.includes('palmprint')) return <Security />;
    return <Security />;
  };

  const getMethodName = (login: any) => {
    return login.method || login.biometricType || 'Unknown';
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Login History
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Date & Time</TableCell>
              <TableCell>Authentication Method</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>IP Address</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loginHistory.map((login) => {
              const methodName = getMethodName(login);
              return (
              <TableRow key={login.id}>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <AccessTime fontSize="small" />
                    {new Date(login.timestamp).toLocaleString()}
                  </Box>
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getMethodIcon(methodName)}
                      {methodName}
                  </Box>
                </TableCell>
                <TableCell>
                  <Chip
                    label={login.success ? 'Success' : 'Failed'}
                    color={login.success ? 'success' : 'error'}
                    size="small"
                  />
                </TableCell>
                <TableCell>{login.ipAddress}</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LocationOn fontSize="small" />
                    {login.location}
                  </Box>
                </TableCell>
                <TableCell>
                  <Tooltip title="View Details">
                    <IconButton size="small">
                      <Visibility />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default LoginHistory; 