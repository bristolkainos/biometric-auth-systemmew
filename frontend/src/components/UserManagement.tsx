import React, { useState } from 'react';
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
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Avatar,
  Tooltip,
  Grid,
} from '@mui/material';
import {
  Edit,
  Delete,
  Visibility,
  Person,
  Security,
  CheckCircle,
  Cancel,
  Dashboard,
} from '@mui/icons-material';

interface UserManagementProps {
  users: any[];
  onDeleteUser: (user: any) => void;
  onViewUserDashboard?: (user: any) => void;
}

const UserManagement: React.FC<UserManagementProps> = ({ users, onDeleteUser, onViewUserDashboard }) => {
  const [selectedUser, setSelectedUser] = useState<any>(null);
  const [viewDialogOpen, setViewDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);

  const handleViewUser = (user: any) => {
    setSelectedUser(user);
    setViewDialogOpen(true);
  };

  const handleEditUser = (user: any) => {
    setSelectedUser(user);
    setEditDialogOpen(true);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'inactive': return 'error';
      case 'pending': return 'warning';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">
          User Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<Person />}
          size="small"
        >
          Add New User
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>User</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Biometric Methods</TableCell>
              <TableCell>Last Login</TableCell>
              <TableCell>Registration Date</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id} hover>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar sx={{ width: 32, height: 32 }}>
                      {user.firstName.charAt(0)}
                    </Avatar>
                    <Box>
                      <Typography variant="body2" fontWeight="medium">
                        {user.firstName} {user.lastName}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        @{user.username}
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {user.email}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    label={user.status}
                    color={getStatusColor(user.status) as any}
                    size="small"
                    icon={user.status === 'active' ? <CheckCircle /> : <Cancel />}
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={`${user.biometricMethods} methods`}
                    variant="outlined"
                    size="small"
                    color="primary"
                  />
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {new Date(user.lastLogin).toLocaleDateString()}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {new Date(user.registrationDate).toLocaleDateString()}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Tooltip title="View Dashboard">
                      <IconButton
                        size="small"
                        color="primary"
                        onClick={() => onViewUserDashboard?.(user)}
                      >
                        <Dashboard />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="View Details">
                      <IconButton
                        size="small"
                        onClick={() => handleViewUser(user)}
                      >
                        <Visibility />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Edit User">
                      <IconButton
                        size="small"
                        onClick={() => handleEditUser(user)}
                      >
                        <Edit />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete User">
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => onDeleteUser(user)}
                      >
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

      {/* View User Dialog */}
      <Dialog open={viewDialogOpen} onClose={() => setViewDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>User Details</DialogTitle>
        <DialogContent>
          {selectedUser && (
            <Box sx={{ mt: 2 }}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Personal Information
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="body2">
                      <strong>Name:</strong> {selectedUser.firstName} {selectedUser.lastName}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Username:</strong> {selectedUser.username}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Email:</strong> {selectedUser.email}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Status:</strong> {selectedUser.status}
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Account Information
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="body2">
                      <strong>Registration Date:</strong> {new Date(selectedUser.registrationDate).toLocaleString()}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Last Login:</strong> {new Date(selectedUser.lastLogin).toLocaleString()}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Biometric Methods:</strong> {selectedUser.biometricMethods}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialogOpen(false)}>Close</Button>
          <Button
            variant="contained"
            onClick={() => {
              setViewDialogOpen(false);
              handleEditUser(selectedUser);
            }}
          >
            Edit User
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit User Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit User</DialogTitle>
        <DialogContent>
          {selectedUser && (
            <Box sx={{ mt: 2 }}>
              <TextField
                fullWidth
                label="First Name"
                defaultValue={selectedUser.firstName}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Last Name"
                defaultValue={selectedUser.lastName}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Email"
                defaultValue={selectedUser.email}
                margin="normal"
                type="email"
              />
              <TextField
                fullWidth
                label="Status"
                defaultValue={selectedUser.status}
                margin="normal"
                select
              >
                <MenuItem value="active">Active</MenuItem>
                <MenuItem value="inactive">Inactive</MenuItem>
                <MenuItem value="pending">Pending</MenuItem>
              </TextField>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button variant="contained">Save Changes</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UserManagement; 