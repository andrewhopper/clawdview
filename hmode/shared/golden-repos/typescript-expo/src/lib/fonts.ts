/**
 * Font Configuration
 *
 * This module provides font family definitions for different theme variants.
 *
 * Amazon Ember Font:
 * - The official AWS brand font
 * - Must be licensed and downloaded separately from AWS Brand Portal
 * - Place font files in assets/fonts/ directory
 *
 * Font file naming convention:
 * - AmazonEmber_Rg.ttf (Regular)
 * - AmazonEmber_Md.ttf (Medium)
 * - AmazonEmber_Bd.ttf (Bold)
 * - AmazonEmber_Lt.ttf (Light)
 *
 * For Expo, use expo-font to load custom fonts.
 */

import type { ThemeFonts } from './theme';

// System fonts (default - uses platform defaults)
export const systemFonts: ThemeFonts = {
  regular: 'System',
  medium: 'System',
  semibold: 'System',
  bold: 'System',
};

// Amazon Ember fonts (AWS brand)
// These require the Amazon Ember font files to be loaded
export const amazonEmberFonts: ThemeFonts = {
  regular: 'AmazonEmber-Regular',
  medium: 'AmazonEmber-Medium',
  semibold: 'AmazonEmber-Bold', // Ember doesn't have semibold, use bold
  bold: 'AmazonEmber-Bold',
};

// Inter fonts (popular alternative, available via Google Fonts)
export const interFonts: ThemeFonts = {
  regular: 'Inter-Regular',
  medium: 'Inter-Medium',
  semibold: 'Inter-SemiBold',
  bold: 'Inter-Bold',
};

// Font asset map for expo-font loading
export const fontAssets = {
  // Amazon Ember (place files in assets/fonts/)
  'AmazonEmber-Regular': require('../../../assets/fonts/AmazonEmber_Rg.ttf'),
  'AmazonEmber-Medium': require('../../../assets/fonts/AmazonEmber_Md.ttf'),
  'AmazonEmber-Bold': require('../../../assets/fonts/AmazonEmber_Bd.ttf'),
  'AmazonEmber-Light': require('../../../assets/fonts/AmazonEmber_Lt.ttf'),
} as const;

// Safe font asset map (won't throw if files don't exist)
export function getFontAssets(): Record<string, number> | null {
  try {
    return fontAssets;
  } catch {
    console.warn('Amazon Ember fonts not found. Using system fonts.');
    return null;
  }
}

// Font weight mapping for StyleSheet
export const fontWeights = {
  light: '300' as const,
  regular: '400' as const,
  medium: '500' as const,
  semibold: '600' as const,
  bold: '700' as const,
};
