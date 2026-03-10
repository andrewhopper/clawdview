import { forwardRef } from 'react';
import {
  Pressable,
  Text,
  StyleSheet,
  ViewStyle,
  TextStyle,
  PressableProps,
  ActivityIndicator,
} from 'react-native';
import { useTheme } from '@/lib/theme';

export type ButtonVariant = 'default' | 'secondary' | 'outline' | 'ghost' | 'destructive' | 'link';
export type ButtonSize = 'sm' | 'default' | 'lg' | 'icon';

export interface ButtonProps extends Omit<PressableProps, 'style'> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  children: React.ReactNode;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export const Button = forwardRef<React.ElementRef<typeof Pressable>, ButtonProps>(
  (
    {
      variant = 'default',
      size = 'default',
      loading = false,
      disabled,
      children,
      style,
      textStyle,
      ...props
    },
    ref
  ) => {
    const { colors, borderRadius, spacing } = useTheme();

    const getVariantStyles = (): { container: ViewStyle; text: TextStyle } => {
      switch (variant) {
        case 'default':
          return {
            container: { backgroundColor: colors.primary },
            text: { color: colors.primaryForeground },
          };
        case 'secondary':
          return {
            container: { backgroundColor: colors.secondary },
            text: { color: colors.secondaryForeground },
          };
        case 'outline':
          return {
            container: {
              backgroundColor: 'transparent',
              borderWidth: 1,
              borderColor: colors.border,
            },
            text: { color: colors.foreground },
          };
        case 'ghost':
          return {
            container: { backgroundColor: 'transparent' },
            text: { color: colors.foreground },
          };
        case 'destructive':
          return {
            container: { backgroundColor: colors.destructive },
            text: { color: colors.destructiveForeground },
          };
        case 'link':
          return {
            container: { backgroundColor: 'transparent' },
            text: { color: colors.primary, textDecorationLine: 'underline' },
          };
      }
    };

    const getSizeStyles = (): { container: ViewStyle; text: TextStyle } => {
      switch (size) {
        case 'sm':
          return {
            container: { height: 36, paddingHorizontal: spacing.md },
            text: { fontSize: 14 },
          };
        case 'default':
          return {
            container: { height: 44, paddingHorizontal: spacing.lg },
            text: { fontSize: 16 },
          };
        case 'lg':
          return {
            container: { height: 52, paddingHorizontal: spacing.xl },
            text: { fontSize: 18 },
          };
        case 'icon':
          return {
            container: { height: 44, width: 44, paddingHorizontal: 0 },
            text: { fontSize: 16 },
          };
      }
    };

    const variantStyles = getVariantStyles();
    const sizeStyles = getSizeStyles();

    return (
      <Pressable
        ref={ref}
        disabled={disabled || loading}
        style={({ pressed }) => [
          styles.base,
          { borderRadius: borderRadius.md },
          variantStyles.container,
          sizeStyles.container,
          (disabled || loading) && styles.disabled,
          pressed && styles.pressed,
          style,
        ]}
        {...props}
      >
        {loading ? (
          <ActivityIndicator color={variantStyles.text.color} size="small" />
        ) : typeof children === 'string' ? (
          <Text style={[styles.text, variantStyles.text, sizeStyles.text, textStyle]}>
            {children}
          </Text>
        ) : (
          children
        )}
      </Pressable>
    );
  }
);

Button.displayName = 'Button';

const styles = StyleSheet.create({
  base: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  text: {
    fontWeight: '500',
  },
  disabled: {
    opacity: 0.5,
  },
  pressed: {
    opacity: 0.9,
  },
});
