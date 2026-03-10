// Default themes (shadcn/ui inspired)
export { DefaultTheme, DarkTheme } from '../theme';

// AWS brand themes
export {
  AWSLightTheme,
  AWSDarkTheme,
  AWSLightThemeExtended,
  AWSDarkThemeExtended,
  awsColors,
  type AWSExtendedTheme,
} from './aws';

// Theme variant type
export type ThemeVariant = 'default' | 'aws';

// Helper to get themes by variant
export function getThemes(variant: ThemeVariant) {
  switch (variant) {
    case 'aws':
      return {
        light: require('./aws').AWSLightTheme,
        dark: require('./aws').AWSDarkTheme,
      };
    case 'default':
    default:
      return {
        light: require('../theme').DefaultTheme,
        dark: require('../theme').DarkTheme,
      };
  }
}
