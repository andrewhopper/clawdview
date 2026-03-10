import { createContext, useContext, useState, useCallback, useMemo } from 'react';
import type { ReactNode } from 'react';

export interface ThemeColors {
  background: string;
  foreground: string;
  card: string;
  cardForeground: string;
  primary: string;
  primaryForeground: string;
  secondary: string;
  secondaryForeground: string;
  muted: string;
  mutedForeground: string;
  accent: string;
  accentForeground: string;
  destructive: string;
  destructiveForeground: string;
  border: string;
  input: string;
  ring: string;
}

export interface ThemeSpacing {
  xs: number;
  sm: number;
  md: number;
  lg: number;
  xl: number;
  '2xl': number;
}

export interface ThemeBorderRadius {
  sm: number;
  md: number;
  lg: number;
  full: number;
}

export interface ThemeFonts {
  regular: string;
  medium: string;
  semibold: string;
  bold: string;
}

export interface Theme {
  dark: boolean;
  colors: ThemeColors;
  spacing: ThemeSpacing;
  borderRadius: ThemeBorderRadius;
  fonts?: ThemeFonts;
}

// Default spacing and border radius
const defaultSpacing: ThemeSpacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  '2xl': 32,
};

const defaultBorderRadius: ThemeBorderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  full: 9999,
};

// Default Light Theme (shadcn/ui inspired)
export const DefaultTheme: Theme = {
  dark: false,
  colors: {
    background: '#ffffff',
    foreground: '#0a0a0a',
    card: '#ffffff',
    cardForeground: '#0a0a0a',
    primary: '#171717',
    primaryForeground: '#fafafa',
    secondary: '#f5f5f5',
    secondaryForeground: '#171717',
    muted: '#f5f5f5',
    mutedForeground: '#737373',
    accent: '#f5f5f5',
    accentForeground: '#171717',
    destructive: '#ef4444',
    destructiveForeground: '#fafafa',
    border: '#e5e5e5',
    input: '#e5e5e5',
    ring: '#0a0a0a',
  },
  spacing: defaultSpacing,
  borderRadius: defaultBorderRadius,
};

// Default Dark Theme
export const DarkTheme: Theme = {
  dark: true,
  colors: {
    background: '#0a0a0a',
    foreground: '#fafafa',
    card: '#0a0a0a',
    cardForeground: '#fafafa',
    primary: '#fafafa',
    primaryForeground: '#171717',
    secondary: '#262626',
    secondaryForeground: '#fafafa',
    muted: '#262626',
    mutedForeground: '#a3a3a3',
    accent: '#262626',
    accentForeground: '#fafafa',
    destructive: '#7f1d1d',
    destructiveForeground: '#fafafa',
    border: '#262626',
    input: '#262626',
    ring: '#d4d4d4',
  },
  spacing: defaultSpacing,
  borderRadius: defaultBorderRadius,
};

// Theme context value type
interface ThemeContextValue {
  theme: Theme;
  isDark: boolean;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue>({
  theme: DefaultTheme,
  isDark: false,
  toggleTheme: () => {},
  setTheme: () => {},
});

// Props for ThemeProvider
interface ThemeProviderProps {
  children: ReactNode;
  value?: Theme;
  lightTheme?: Theme;
  darkTheme?: Theme;
  initialDark?: boolean;
}

// Enhanced ThemeProvider with toggle support
export function ThemeProvider({
  children,
  value,
  lightTheme = DefaultTheme,
  darkTheme = DarkTheme,
  initialDark = false,
}: ThemeProviderProps) {
  const [isDark, setIsDark] = useState(initialDark);

  const toggleTheme = useCallback(() => {
    setIsDark((prev) => !prev);
  }, []);

  const setTheme = useCallback((theme: Theme) => {
    setIsDark(theme.dark);
  }, []);

  const contextValue = useMemo<ThemeContextValue>(
    () => ({
      theme: value ?? (isDark ? darkTheme : lightTheme),
      isDark,
      toggleTheme,
      setTheme,
    }),
    [value, isDark, lightTheme, darkTheme, toggleTheme, setTheme]
  );

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
}

// Hook to access theme
export function useTheme(): Theme {
  const context = useContext(ThemeContext);
  return context.theme;
}

// Hook to access full theme context (including toggle)
export function useThemeContext(): ThemeContextValue {
  return useContext(ThemeContext);
}
