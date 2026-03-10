// UI Components
export * from './components/ui';

// Layout Components
export * from './components/layout';

// Hooks
export * from './hooks';

// Config
export { config, getConfig, type Config } from './config';

// Constants
export * from './constants';

// Theme (Default)
export {
  useTheme,
  useThemeContext,
  ThemeProvider,
  DefaultTheme,
  DarkTheme,
  type Theme,
  type ThemeColors,
  type ThemeSpacing,
  type ThemeBorderRadius,
  type ThemeFonts,
} from './lib/theme';

// Theme Variants
export {
  AWSLightTheme,
  AWSDarkTheme,
  AWSLightThemeExtended,
  AWSDarkThemeExtended,
  awsColors,
  type AWSExtendedTheme,
} from './lib/themes/aws';

// All themes
export * from './lib/themes';

// Fonts
export {
  systemFonts,
  amazonEmberFonts,
  interFonts,
  fontWeights,
} from './lib/fonts';
