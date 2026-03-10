import { forwardRef } from 'react';
import { TextInput, TextInputProps, StyleSheet, View, ViewStyle } from 'react-native';
import { useTheme } from '@/lib/theme';
import { Text } from './Text';

export interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
  containerStyle?: ViewStyle;
}

export const Input = forwardRef<TextInput, InputProps>(
  ({ label, error, containerStyle, style, ...props }, ref) => {
    const { colors, borderRadius, spacing } = useTheme();

    return (
      <View style={containerStyle}>
        {label && (
          <Text
            variant="default"
            size="sm"
            style={{ marginBottom: spacing.xs, fontWeight: '500' }}
          >
            {label}
          </Text>
        )}
        <TextInput
          ref={ref}
          style={[
            styles.input,
            {
              backgroundColor: colors.background,
              borderColor: error ? colors.destructive : colors.input,
              borderRadius: borderRadius.md,
              color: colors.foreground,
              paddingHorizontal: spacing.md,
            },
            style,
          ]}
          placeholderTextColor={colors.mutedForeground}
          {...props}
        />
        {error && (
          <Text
            variant="default"
            size="sm"
            style={{ marginTop: spacing.xs, color: colors.destructive }}
          >
            {error}
          </Text>
        )}
      </View>
    );
  }
);

Input.displayName = 'Input';

const styles = StyleSheet.create({
  input: {
    height: 44,
    borderWidth: 1,
    fontSize: 16,
  },
});
