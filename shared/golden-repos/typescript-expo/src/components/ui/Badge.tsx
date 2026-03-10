import { View, ViewStyle, TextStyle } from 'react-native';
import { useTheme } from '@/lib/theme';
import { Text } from './Text';

export type BadgeVariant = 'default' | 'secondary' | 'outline' | 'destructive';

export interface BadgeProps {
  variant?: BadgeVariant;
  children: React.ReactNode;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export function Badge({
  variant = 'default',
  children,
  style,
  textStyle,
}: BadgeProps) {
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
      case 'destructive':
        return {
          container: { backgroundColor: colors.destructive },
          text: { color: colors.destructiveForeground },
        };
    }
  };

  const variantStyles = getVariantStyles();

  return (
    <View
      style={[
        {
          paddingHorizontal: spacing.sm,
          paddingVertical: spacing.xs,
          borderRadius: borderRadius.full,
          alignSelf: 'flex-start',
        },
        variantStyles.container,
        style,
      ]}
    >
      <Text
        size="xs"
        style={[{ fontWeight: '500' }, variantStyles.text, textStyle]}
      >
        {children}
      </Text>
    </View>
  );
}
