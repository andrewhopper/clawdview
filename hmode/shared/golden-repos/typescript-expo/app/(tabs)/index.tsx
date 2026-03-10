import { View, ScrollView } from 'react-native';
import { Text } from '@/components/ui/Text';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Container } from '@/components/layout/Container';
import { useTheme } from '@/lib/theme';

export default function HomeScreen() {
  const { colors, spacing } = useTheme();

  return (
    <Container>
      <ScrollView
        contentContainerStyle={{ padding: spacing.lg }}
        showsVerticalScrollIndicator={false}
      >
        <View style={{ gap: spacing.lg }}>
          <View style={{ gap: spacing.sm }}>
            <Text variant="h1">Welcome</Text>
            <Text variant="muted">
              Gold standard Expo template with design system components.
            </Text>
          </View>

          <Card>
            <Card.Header>
              <Card.Title>Getting Started</Card.Title>
              <Card.Description>
                This template includes pre-built components following shadcn/ui patterns.
              </Card.Description>
            </Card.Header>
            <Card.Content>
              <Text>
                Edit app/(tabs)/index.tsx to start building your app.
              </Text>
            </Card.Content>
            <Card.Footer>
              <Button onPress={() => console.log('Pressed!')}>
                Get Started
              </Button>
            </Card.Footer>
          </Card>

          <View style={{ gap: spacing.md }}>
            <Text variant="h3">Button Variants</Text>
            <View style={{ gap: spacing.sm }}>
              <Button variant="default">Default</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="outline">Outline</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="destructive">Destructive</Button>
            </View>
          </View>

          <View style={{ gap: spacing.md }}>
            <Text variant="h3">Button Sizes</Text>
            <View style={{ gap: spacing.sm }}>
              <Button size="sm">Small</Button>
              <Button size="default">Default</Button>
              <Button size="lg">Large</Button>
            </View>
          </View>
        </View>
      </ScrollView>
    </Container>
  );
}
