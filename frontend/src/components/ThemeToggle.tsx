import React from 'react';
import { IconButton, Tooltip, useTheme as useMuiTheme } from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import { useTheme } from '../contexts/ThemeContext';

interface ThemeToggleProps {
  size?: 'small' | 'medium' | 'large';
  showTooltip?: boolean;
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ 
  size = 'medium', 
  showTooltip = true 
}) => {
  const { isDarkMode, toggleTheme } = useTheme();
  const muiTheme = useMuiTheme();

  const button = (
    <IconButton
      onClick={toggleTheme}
      size={size}
      sx={{
        color: muiTheme.palette.text.primary,
        backgroundColor: muiTheme.palette.mode === 'dark' 
          ? 'rgba(255, 255, 255, 0.1)' 
          : 'rgba(0, 0, 0, 0.05)',
        '&:hover': {
          backgroundColor: muiTheme.palette.mode === 'dark' 
            ? 'rgba(255, 255, 255, 0.2)' 
            : 'rgba(0, 0, 0, 0.1)',
          transform: 'scale(1.1)',
        },
        transition: 'all 0.3s ease',
      }}
    >
      {isDarkMode ? <Brightness7 /> : <Brightness4 />}
    </IconButton>
  );

  if (showTooltip) {
    return (
      <Tooltip title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}>
        {button}
      </Tooltip>
    );
  }

  return button;
};

export default ThemeToggle; 