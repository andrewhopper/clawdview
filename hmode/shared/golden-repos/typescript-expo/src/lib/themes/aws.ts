/**
 * AWS Brand Theme
 *
 * Official AWS brand colors based on AWS Brand Guidelines.
 *
 * Primary Colors:
 * - Amazon Orange (Smile): #FF9900
 * - Squid Ink: #232F3E
 *
 * Extended palette derived from AWS console and service icons.
 *
 * Sources:
 * - https://brandpalettes.com/amazon-web-services-logo-colors/
 * - https://www.brandcolorcode.com/amazon-web-services-aws
 */

import type { Theme, ThemeColors, ThemeSpacing, ThemeBorderRadius } from '../theme';

// AWS Brand Color Tokens
export const awsColors = {
  // Primary brand colors
  orange: '#FF9900',        // Amazon Orange / Smile
  squidInk: '#232F3E',      // Primary text, dark backgrounds

  // Extended palette (from AWS console)
  orangeLight: '#FFAC31',   // Lighter orange for hover states
  orangeDark: '#EC7211',    // Darker orange for pressed states

  // Neutral palette
  white: '#FFFFFF',
  black: '#000000',

  // Grays (AWS console inspired)
  gray50: '#FAFAFA',
  gray100: '#F2F3F3',
  gray200: '#E9EBED',
  gray300: '#D1D5DB',
  gray400: '#9BA2AB',
  gray500: '#687078',
  gray600: '#545B64',
  gray700: '#414750',
  gray800: '#2D3339',
  gray900: '#1A1F25',

  // Service category colors (for accents)
  compute: '#ED7100',       // EC2, Lambda
  storage: '#3B48CC',       // S3
  database: '#3B48CC',      // RDS, DynamoDB
  networking: '#8C4FFF',    // VPC, CloudFront
  security: '#DD344C',      // IAM, Security Hub
  analytics: '#8C4FFF',     // Athena, QuickSight
  machineLearning: '#01A88D', // SageMaker

  // Semantic colors
  success: '#037F0C',       // Green for success states
  warning: '#FFAC31',       // Orange/yellow for warnings
  error: '#D91515',         // Red for errors
  info: '#0972D3',          // Blue for info
} as const;

// Shared spacing and border radius
const awsSpacing: ThemeSpacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  '2xl': 32,
};

const awsBorderRadius: ThemeBorderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  full: 9999,
};

// AWS Light Theme Colors
const awsLightColors: ThemeColors = {
  // Backgrounds
  background: awsColors.white,
  foreground: awsColors.squidInk,

  // Cards
  card: awsColors.white,
  cardForeground: awsColors.squidInk,

  // Primary (Orange)
  primary: awsColors.orange,
  primaryForeground: awsColors.white,

  // Secondary (Squid Ink)
  secondary: awsColors.gray100,
  secondaryForeground: awsColors.squidInk,

  // Muted
  muted: awsColors.gray100,
  mutedForeground: awsColors.gray500,

  // Accent (Orange tinted)
  accent: '#FFF4E5',  // Very light orange
  accentForeground: awsColors.orangeDark,

  // Destructive
  destructive: awsColors.error,
  destructiveForeground: awsColors.white,

  // Borders and inputs
  border: awsColors.gray200,
  input: awsColors.gray200,
  ring: awsColors.orange,
};

// AWS Dark Theme Colors (Console-inspired)
const awsDarkColors: ThemeColors = {
  // Backgrounds
  background: awsColors.squidInk,
  foreground: awsColors.gray50,

  // Cards
  card: awsColors.gray800,
  cardForeground: awsColors.gray50,

  // Primary (Orange - stays vibrant in dark mode)
  primary: awsColors.orange,
  primaryForeground: awsColors.squidInk,

  // Secondary
  secondary: awsColors.gray700,
  secondaryForeground: awsColors.gray50,

  // Muted
  muted: awsColors.gray700,
  mutedForeground: awsColors.gray400,

  // Accent
  accent: '#3D2A14',  // Dark orange tint
  accentForeground: awsColors.orangeLight,

  // Destructive
  destructive: '#7F1D1D',
  destructiveForeground: awsColors.gray50,

  // Borders and inputs
  border: awsColors.gray600,
  input: awsColors.gray600,
  ring: awsColors.orange,
};

// AWS Light Theme
export const AWSLightTheme: Theme = {
  dark: false,
  colors: awsLightColors,
  spacing: awsSpacing,
  borderRadius: awsBorderRadius,
};

// AWS Dark Theme
export const AWSDarkTheme: Theme = {
  dark: true,
  colors: awsDarkColors,
  spacing: awsSpacing,
  borderRadius: awsBorderRadius,
};

// Theme with extended AWS-specific properties
export interface AWSExtendedTheme extends Theme {
  brand: {
    orange: string;
    squidInk: string;
    services: {
      compute: string;
      storage: string;
      database: string;
      networking: string;
      security: string;
      analytics: string;
      machineLearning: string;
    };
    semantic: {
      success: string;
      warning: string;
      error: string;
      info: string;
    };
  };
}

// Extended AWS themes with service colors
export const AWSLightThemeExtended: AWSExtendedTheme = {
  ...AWSLightTheme,
  brand: {
    orange: awsColors.orange,
    squidInk: awsColors.squidInk,
    services: {
      compute: awsColors.compute,
      storage: awsColors.storage,
      database: awsColors.database,
      networking: awsColors.networking,
      security: awsColors.security,
      analytics: awsColors.analytics,
      machineLearning: awsColors.machineLearning,
    },
    semantic: {
      success: awsColors.success,
      warning: awsColors.warning,
      error: awsColors.error,
      info: awsColors.info,
    },
  },
};

export const AWSDarkThemeExtended: AWSExtendedTheme = {
  ...AWSDarkTheme,
  brand: {
    orange: awsColors.orange,
    squidInk: awsColors.squidInk,
    services: {
      compute: awsColors.compute,
      storage: awsColors.storage,
      database: awsColors.database,
      networking: awsColors.networking,
      security: awsColors.security,
      analytics: awsColors.analytics,
      machineLearning: awsColors.machineLearning,
    },
    semantic: {
      success: awsColors.success,
      warning: awsColors.warning,
      error: awsColors.error,
      info: awsColors.info,
    },
  },
};
