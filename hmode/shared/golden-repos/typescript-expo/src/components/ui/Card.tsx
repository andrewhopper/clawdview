import { View, ViewProps, StyleSheet } from 'react-native';
import { useTheme } from '@/lib/theme';
import { Text } from './Text';

export interface CardProps extends ViewProps {
  children: React.ReactNode;
}

function CardRoot({ style, children, ...props }: CardProps) {
  const { colors, borderRadius, spacing } = useTheme();

  return (
    <View
      style={[
        styles.card,
        {
          backgroundColor: colors.card,
          borderColor: colors.border,
          borderRadius: borderRadius.lg,
          padding: spacing.lg,
        },
        style,
      ]}
      {...props}
    >
      {children}
    </View>
  );
}

function CardHeader({ style, children, ...props }: ViewProps) {
  const { spacing } = useTheme();

  return (
    <View style={[{ marginBottom: spacing.md }, style]} {...props}>
      {children}
    </View>
  );
}

interface CardTitleProps {
  children: React.ReactNode;
}

function CardTitle({ children }: CardTitleProps) {
  return <Text variant="h4">{children}</Text>;
}

interface CardDescriptionProps {
  children: React.ReactNode;
}

function CardDescription({ children }: CardDescriptionProps) {
  const { spacing } = useTheme();

  return (
    <Text variant="muted" style={{ marginTop: spacing.xs }}>
      {children}
    </Text>
  );
}

function CardContent({ style, children, ...props }: ViewProps) {
  return (
    <View style={style} {...props}>
      {children}
    </View>
  );
}

function CardFooter({ style, children, ...props }: ViewProps) {
  const { spacing } = useTheme();

  return (
    <View
      style={[
        { marginTop: spacing.lg, flexDirection: 'row', alignItems: 'center' },
        style,
      ]}
      {...props}
    >
      {children}
    </View>
  );
}

export const Card = Object.assign(CardRoot, {
  Header: CardHeader,
  Title: CardTitle,
  Description: CardDescription,
  Content: CardContent,
  Footer: CardFooter,
});

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
});
