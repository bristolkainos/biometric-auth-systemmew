import { createTheme, ThemeOptions } from '@mui/material/styles';

// Color palette for the unified theme
const colors = {
  primary: {
    main: '#667eea',
    light: '#8fa4f1',
    dark: '#4c63d2',
    contrastText: '#ffffff',
  },
  secondary: {
    main: '#764ba2',
    light: '#9a7bb8',
    dark: '#5a3a7a',
    contrastText: '#ffffff',
  },
  success: {
    main: '#4caf50',
    light: '#81c784',
    dark: '#388e3c',
    contrastText: '#ffffff',
  },
  warning: {
    main: '#ff9800',
    light: '#ffb74d',
    dark: '#f57c00',
    contrastText: '#ffffff',
  },
  error: {
    main: '#f44336',
    light: '#e57373',
    dark: '#d32f2f',
    contrastText: '#ffffff',
  },
  info: {
    main: '#2196f3',
    light: '#64b5f6',
    dark: '#1976d2',
    contrastText: '#ffffff',
  },
  grey: {
    50: '#fafafa',
    100: '#f5f5f5',
    200: '#eeeeee',
    300: '#e0e0e0',
    400: '#bdbdbd',
    500: '#9e9e9e',
    600: '#757575',
    700: '#616161',
    800: '#424242',
    900: '#212121',
  },
  background: {
    default: '#f8fafc',
    paper: '#ffffff',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    card: 'rgba(255, 255, 255, 0.95)',
    cardHover: 'rgba(255, 255, 255, 0.98)',
  },
  text: {
    primary: '#2d3748',
    secondary: '#718096',
    disabled: '#a0aec0',
  },
};

// Typography configuration
const typography = {
  fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  h1: {
    fontSize: '2.5rem',
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.02em',
  },
  h2: {
    fontSize: '2rem',
    fontWeight: 600,
    lineHeight: 1.3,
    letterSpacing: '-0.01em',
  },
  h3: {
    fontSize: '1.75rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h4: {
    fontSize: '1.5rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h5: {
    fontSize: '1.25rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h6: {
    fontSize: '1.125rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  subtitle1: {
    fontSize: '1rem',
    fontWeight: 500,
    lineHeight: 1.5,
  },
  subtitle2: {
    fontSize: '0.875rem',
    fontWeight: 500,
    lineHeight: 1.5,
  },
  body1: {
    fontSize: '1rem',
    fontWeight: 400,
    lineHeight: 1.6,
  },
  body2: {
    fontSize: '0.875rem',
    fontWeight: 400,
    lineHeight: 1.6,
  },
  button: {
    fontSize: '0.875rem',
    fontWeight: 600,
    lineHeight: 1.5,
    textTransform: 'none',
  },
  caption: {
    fontSize: '0.75rem',
    fontWeight: 400,
    lineHeight: 1.5,
  },
  overline: {
    fontSize: '0.75rem',
    fontWeight: 600,
    lineHeight: 1.5,
    textTransform: 'uppercase',
    letterSpacing: '0.1em',
  },
};

// Component style overrides
const components = {
  MuiButton: {
    styleOverrides: {
      root: {
        borderRadius: 12,
        padding: '12px 24px',
        textTransform: 'none',
        fontWeight: 600,
        boxShadow: '0 2px 8px rgba(102, 126, 234, 0.15)',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: '0 4px 16px rgba(102, 126, 234, 0.25)',
        },
      },
      contained: {
        background: colors.background.gradient,
        '&:hover': {
          background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
        },
      },
      outlined: {
        borderWidth: 2,
        '&:hover': {
          borderWidth: 2,
        },
      },
    },
  },
  MuiCard: {
    styleOverrides: {
      root: {
        borderRadius: 16,
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
        transition: 'all 0.3s ease',
        '&:hover': {
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.12)',
          transform: 'translateY(-4px)',
        },
      },
    },
  },
  MuiPaper: {
    styleOverrides: {
      root: {
        borderRadius: 12,
      },
    },
  },
  MuiTextField: {
    styleOverrides: {
      root: {
        '& .MuiOutlinedInput-root': {
          borderRadius: 12,
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: colors.primary.main,
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: colors.primary.main,
            borderWidth: 2,
          },
        },
      },
    },
  },
  MuiChip: {
    styleOverrides: {
      root: {
        borderRadius: 20,
        fontWeight: 600,
      },
    },
  },
  MuiIconButton: {
    styleOverrides: {
      root: {
        borderRadius: 12,
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'scale(1.1)',
        },
      },
    },
  },
  MuiDialog: {
    styleOverrides: {
      paper: {
        borderRadius: 16,
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.12)',
      },
    },
  },
  MuiAlert: {
    styleOverrides: {
      root: {
        borderRadius: 12,
        fontWeight: 500,
      },
    },
  },
  MuiLinearProgress: {
    styleOverrides: {
      root: {
        borderRadius: 8,
        height: 8,
      },
    },
  },
  MuiCircularProgress: {
    styleOverrides: {
      root: {
        color: colors.primary.main,
      },
    },
  },
  MuiTabs: {
    styleOverrides: {
      root: {
        '& .MuiTabs-indicator': {
          height: 3,
          borderRadius: 2,
        },
      },
    },
  },
  MuiTab: {
    styleOverrides: {
      root: {
        textTransform: 'none',
        fontWeight: 600,
        fontSize: '0.875rem',
      },
    },
  },
};

// Create the unified theme
export const theme = createTheme({
  palette: {
    primary: colors.primary,
    secondary: colors.secondary,
    success: colors.success,
    warning: colors.warning,
    error: colors.error,
    info: colors.info,
    grey: colors.grey,
    background: colors.background,
    text: colors.text,
  },
  typography,
  components,
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0 2px 8px rgba(0, 0, 0, 0.08)',
    '0 4px 16px rgba(0, 0, 0, 0.12)',
    '0 8px 24px rgba(0, 0, 0, 0.16)',
    '0 12px 32px rgba(0, 0, 0, 0.20)',
    '0 16px 40px rgba(0, 0, 0, 0.24)',
    '0 20px 48px rgba(0, 0, 0, 0.28)',
    '0 24px 56px rgba(0, 0, 0, 0.32)',
    '0 28px 64px rgba(0, 0, 0, 0.36)',
    '0 32px 72px rgba(0, 0, 0, 0.40)',
    '0 36px 80px rgba(0, 0, 0, 0.44)',
    '0 40px 88px rgba(0, 0, 0, 0.48)',
    '0 44px 96px rgba(0, 0, 0, 0.52)',
    '0 48px 104px rgba(0, 0, 0, 0.56)',
    '0 52px 112px rgba(0, 0, 0, 0.60)',
    '0 56px 120px rgba(0, 0, 0, 0.64)',
    '0 60px 128px rgba(0, 0, 0, 0.68)',
    '0 64px 136px rgba(0, 0, 0, 0.72)',
    '0 68px 144px rgba(0, 0, 0, 0.76)',
    '0 72px 152px rgba(0, 0, 0, 0.80)',
    '0 76px 160px rgba(0, 0, 0, 0.84)',
    '0 80px 168px rgba(0, 0, 0, 0.88)',
    '0 84px 176px rgba(0, 0, 0, 0.92)',
    '0 88px 184px rgba(0, 0, 0, 0.96)',
    '0 92px 192px rgba(0, 0, 0, 1.00)',
  ],
} as ThemeOptions);

// Export color constants for use in components
export const themeColors = colors;

// Export theme utilities
export const getGradientBackground = (direction: string = '135deg') => 
  `linear-gradient(${direction}, ${colors.primary.main} 0%, ${colors.secondary.main} 100%)`;

export const getCardBackground = (opacity: number = 0.95) => 
  `rgba(255, 255, 255, ${opacity})`;

export const getHoverTransform = (y: number = -4) => 
  `translateY(${y}px)`;

export default theme; 