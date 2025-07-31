import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { ThemeProvider as MuiThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { theme as baseTheme, themeColors, getGradientBackground, getCardBackground } from '../theme';

interface ThemeContextType {
  isDarkMode: boolean;
  toggleTheme: () => void;
  theme: any;
  colors: typeof themeColors;
  getGradient: (direction?: string) => string;
  getCardBg: (opacity?: number) => string;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Check for saved theme preference or default to light mode
    const saved = localStorage.getItem('theme-mode');
    if (saved) {
      return saved === 'dark';
    }
    // Check system preference
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  // Create theme based on mode
  const theme = createTheme({
    ...baseTheme,
    palette: {
      ...baseTheme.palette,
      mode: isDarkMode ? 'dark' : 'light',
      background: {
        ...baseTheme.palette.background,
        default: isDarkMode ? '#121212' : '#f8fafc',
        paper: isDarkMode ? '#1e1e1e' : '#ffffff',
      },
      text: {
        ...baseTheme.palette.text,
        primary: isDarkMode ? '#ffffff' : '#2d3748',
        secondary: isDarkMode ? '#a0aec0' : '#718096',
      },
    },
  });

  const toggleTheme = () => {
    setIsDarkMode(prev => !prev);
  };

  // Save theme preference
  useEffect(() => {
    localStorage.setItem('theme-mode', isDarkMode ? 'dark' : 'light');
  }, [isDarkMode]);

  // Listen for system theme changes
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => {
      if (!localStorage.getItem('theme-mode')) {
        setIsDarkMode(e.matches);
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  const value: ThemeContextType = {
    isDarkMode,
    toggleTheme,
    theme,
    colors: themeColors,
    getGradient: getGradientBackground,
    getCardBg: getCardBackground,
  };

  return (
    <ThemeContext.Provider value={value}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export default ThemeProvider; 