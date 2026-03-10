/**
 * AWS Theme with Amazon Ember Fonts
 *
 * Extended AWS theme that includes font configuration.
 * Requires Amazon Ember font files to be loaded via expo-font.
 */

import { AWSLightTheme, AWSDarkTheme } from './aws';
import { amazonEmberFonts } from '../fonts';
import type { Theme } from '../theme';

// AWS Light Theme with Amazon Ember fonts
export const AWSLightThemeWithFonts: Theme = {
  ...AWSLightTheme,
  fonts: amazonEmberFonts,
};

// AWS Dark Theme with Amazon Ember fonts
export const AWSDarkThemeWithFonts: Theme = {
  ...AWSDarkTheme,
  fonts: amazonEmberFonts,
};
