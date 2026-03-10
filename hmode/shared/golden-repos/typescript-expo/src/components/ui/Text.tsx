import { Text as RNText, TextProps as RNTextProps, StyleSheet, TextStyle } from 'react-native';
import { useTheme } from '@/lib/theme';

export type TextVariant = 'default' | 'h1' | 'h2' | 'h3' | 'h4' | 'muted' | 'link' | 'code';
export type TextSize = 'xs' | 'sm' | 'base' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl';

export interface TextProps extends RNTextProps {
  variant?: TextVariant;
  size?: TextSize;
  children: React.ReactNode;
}

export function Text({ variant = 'default', size, style, children, ...props }: TextProps) {
  const { colors } = useTheme();

  const getVariantStyles = (): TextStyle => {
    switch (variant) {
      case 'h1':
        return {
          fontSize: 32,
          fontWeight: '800',
          letterSpacing: -1,
          color: colors.foreground,
        };
      case 'h2':
        return {
          fontSize: 28,
          fontWeight: '700',
          letterSpacing: -0.5,
          color: colors.foreground,
        };
      case 'h3':
        return {
          fontSize: 24,
          fontWeight: '600',
          color: colors.foreground,
        };
      case 'h4':
        return {
          fontSize: 20,
          fontWeight: '600',
          color: colors.foreground,
        };
      case 'muted':
        return {
          fontSize: 14,
          color: colors.mutedForeground,
        };
      case 'link':
        return {
          fontSize: 16,
          color: colors.primary,
          textDecorationLine: 'underline',
        };
      case 'code':
        return {
          fontSize: 14,
          fontFamily: 'monospace',
          backgroundColor: colors.muted,
          color: colors.foreground,
        };
      default:
        return {
          fontSize: 16,
          color: colors.foreground,
        };
    }
  };

  const getSizeStyles = (): TextStyle => {
    const sizes: Record<TextSize, number> = {
      xs: 12,
      sm: 14,
      base: 16,
      lg: 18,
      xl: 20,
      '2xl': 24,
      '3xl': 30,
      '4xl': 36,
    };

    return size ? { fontSize: sizes[size] } : {};
  };

  return (
    <RNText style={[getVariantStyles(), getSizeStyles(), style]} {...props}>
      {children}
    </RNText>
  );
}
