import { View, ViewStyle } from 'react-native';
import { useTheme } from '@/lib/theme';

export interface SeparatorProps {
  orientation?: 'horizontal' | 'vertical';
  style?: ViewStyle;
}

export function Separator({ orientation = 'horizontal', style }: SeparatorProps) {
  const { colors, spacing } = useTheme();

  const isHorizontal = orientation === 'horizontal';

  return (
    <View
      style={[
        {
          backgroundColor: colors.border,
          ...(isHorizontal
            ? { height: 1, width: '100%', marginVertical: spacing.md }
            : { width: 1, height: '100%', marginHorizontal: spacing.md }),
        },
        style,
      ]}
    />
  );
}
