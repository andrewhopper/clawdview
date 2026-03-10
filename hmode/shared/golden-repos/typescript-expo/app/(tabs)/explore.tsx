import { View, ScrollView } from 'react-native';
import { Text } from '@/components/ui/Text';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Input } from '@/components/ui/Input';
import { Container } from '@/components/layout/Container';
import { useTheme } from '@/lib/theme';

const features = [
  {
    title: 'Type-Safe Navigation',
    description: 'Expo Router with typed routes for compile-time safety.',
    badge: 'Core',
  },
  {
    title: 'Design System',
    description: 'Pre-built components following shadcn/ui patterns.',
    badge: 'UI',
  },
  {
    title: 'Dark Mode',
    description: 'Automatic dark mode support with theme context.',
    badge: 'Theme',
  },
  {
    title: 'Zod Validation',
    description: 'Schema validation for forms and API responses.',
    badge: 'Data',
  },
];

export default function ExploreScreen() {
  const { spacing } = useTheme();

  return (
    <Container>
      <ScrollView
        contentContainerStyle={{ padding: spacing.lg }}
        showsVerticalScrollIndicator={false}
      >
        <View style={{ gap: spacing.lg }}>
          <View style={{ gap: spacing.sm }}>
            <Text variant="h1">Explore</Text>
            <Text variant="muted">
              Discover the features included in this template.
            </Text>
          </View>

          <Input placeholder="Search features..." />

          <View style={{ gap: spacing.md }}>
            {features.map((feature) => (
              <Card key={feature.title}>
                <Card.Header>
                  <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Card.Title>{feature.title}</Card.Title>
                    <Badge variant="secondary">{feature.badge}</Badge>
                  </View>
                  <Card.Description>{feature.description}</Card.Description>
                </Card.Header>
              </Card>
            ))}
          </View>
        </View>
      </ScrollView>
    </Container>
  );
}
