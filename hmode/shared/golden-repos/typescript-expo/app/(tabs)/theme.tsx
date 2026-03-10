import { View, ScrollView, Switch, Pressable } from 'react-native';
import { Text } from '@/components/ui/Text';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Input } from '@/components/ui/Input';
import { Separator } from '@/components/ui/Separator';
import { Container } from '@/components/layout/Container';
import { useTheme, useThemeContext } from '@/lib/theme';
import { awsColors } from '@/lib/themes/aws';

interface ColorSwatchProps {
  name: string;
  color: string;
  textColor?: string;
}

function ColorSwatch({ name, color, textColor = '#ffffff' }: ColorSwatchProps) {
  const { spacing, borderRadius } = useTheme();

  return (
    <View
      style={{
        backgroundColor: color,
        padding: spacing.md,
        borderRadius: borderRadius.md,
        minWidth: 100,
        alignItems: 'center',
      }}
    >
      <Text style={{ color: textColor, fontSize: 12, fontWeight: '600' }}>{name}</Text>
      <Text style={{ color: textColor, fontSize: 10, opacity: 0.8 }}>{color}</Text>
    </View>
  );
}

function ServiceColorRow({ name, color }: { name: string; color: string }) {
  const { spacing, borderRadius } = useTheme();

  return (
    <View style={{ flexDirection: 'row', alignItems: 'center', gap: spacing.sm }}>
      <View
        style={{
          width: 24,
          height: 24,
          borderRadius: borderRadius.sm,
          backgroundColor: color,
        }}
      />
      <Text variant="default" size="sm">{name}</Text>
      <Text variant="muted" size="xs">{color}</Text>
    </View>
  );
}

export default function ThemeScreen() {
  const { colors, spacing } = useTheme();
  const { isDark, toggleTheme } = useThemeContext();

  return (
    <Container>
      <ScrollView
        contentContainerStyle={{ padding: spacing.lg }}
        showsVerticalScrollIndicator={false}
      >
        <View style={{ gap: spacing.lg }}>
          {/* Header */}
          <View style={{ gap: spacing.sm }}>
            <Text variant="h1">Theme</Text>
            <Text variant="muted">
              Design system colors and AWS brand theme preview.
            </Text>
          </View>

          {/* Dark Mode Toggle */}
          <Card>
            <Card.Header>
              <Card.Title>Appearance</Card.Title>
            </Card.Header>
            <Card.Content>
              <View
                style={{
                  flexDirection: 'row',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <View>
                  <Text variant="default">Dark Mode</Text>
                  <Text variant="muted" size="sm">
                    {isDark ? 'Using dark theme' : 'Using light theme'}
                  </Text>
                </View>
                <Switch
                  value={isDark}
                  onValueChange={toggleTheme}
                  trackColor={{ true: colors.primary, false: colors.muted }}
                />
              </View>
            </Card.Content>
          </Card>

          {/* Current Theme Colors */}
          <Card>
            <Card.Header>
              <Card.Title>Current Theme Colors</Card.Title>
              <Card.Description>
                Active color tokens from the theme context.
              </Card.Description>
            </Card.Header>
            <Card.Content>
              <View style={{ gap: spacing.md }}>
                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }}>
                  <ColorSwatch name="Primary" color={colors.primary} />
                  <ColorSwatch name="Secondary" color={colors.secondary} textColor={colors.secondaryForeground} />
                  <ColorSwatch name="Accent" color={colors.accent} textColor={colors.accentForeground} />
                  <ColorSwatch name="Destructive" color={colors.destructive} />
                </View>
                <Separator />
                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }}>
                  <ColorSwatch name="Background" color={colors.background} textColor={colors.foreground} />
                  <ColorSwatch name="Card" color={colors.card} textColor={colors.cardForeground} />
                  <ColorSwatch name="Muted" color={colors.muted} textColor={colors.mutedForeground} />
                  <ColorSwatch name="Border" color={colors.border} textColor={colors.foreground} />
                </View>
              </View>
            </Card.Content>
          </Card>

          {/* AWS Brand Colors Reference */}
          <Card>
            <Card.Header>
              <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                <Card.Title>AWS Brand Colors</Card.Title>
                <Badge variant="outline">Reference</Badge>
              </View>
              <Card.Description>
                Official AWS brand colors for reference.
              </Card.Description>
            </Card.Header>
            <Card.Content>
              <View style={{ gap: spacing.md }}>
                <Text variant="h4" size="sm">Primary</Text>
                <View style={{ flexDirection: 'row', gap: spacing.sm }}>
                  <ColorSwatch name="Orange" color={awsColors.orange} />
                  <ColorSwatch name="Squid Ink" color={awsColors.squidInk} />
                </View>

                <Text variant="h4" size="sm">Service Categories</Text>
                <View style={{ gap: spacing.xs }}>
                  <ServiceColorRow name="Compute" color={awsColors.compute} />
                  <ServiceColorRow name="Storage" color={awsColors.storage} />
                  <ServiceColorRow name="Database" color={awsColors.database} />
                  <ServiceColorRow name="Networking" color={awsColors.networking} />
                  <ServiceColorRow name="Security" color={awsColors.security} />
                  <ServiceColorRow name="ML/AI" color={awsColors.machineLearning} />
                </View>

                <Text variant="h4" size="sm">Semantic</Text>
                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }}>
                  <ColorSwatch name="Success" color={awsColors.success} />
                  <ColorSwatch name="Warning" color={awsColors.warning} textColor={awsColors.squidInk} />
                  <ColorSwatch name="Error" color={awsColors.error} />
                  <ColorSwatch name="Info" color={awsColors.info} />
                </View>
              </View>
            </Card.Content>
          </Card>

          {/* Component Preview */}
          <Card>
            <Card.Header>
              <Card.Title>Component Preview</Card.Title>
              <Card.Description>
                See how components look with current theme.
              </Card.Description>
            </Card.Header>
            <Card.Content>
              <View style={{ gap: spacing.md }}>
                <Text variant="h4" size="sm">Buttons</Text>
                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }}>
                  <Button variant="default" size="sm">Primary</Button>
                  <Button variant="secondary" size="sm">Secondary</Button>
                  <Button variant="outline" size="sm">Outline</Button>
                  <Button variant="destructive" size="sm">Destructive</Button>
                </View>

                <Text variant="h4" size="sm">Badges</Text>
                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }}>
                  <Badge variant="default">Default</Badge>
                  <Badge variant="secondary">Secondary</Badge>
                  <Badge variant="outline">Outline</Badge>
                  <Badge variant="destructive">Destructive</Badge>
                </View>

                <Text variant="h4" size="sm">Input</Text>
                <Input placeholder="Type something..." />
              </View>
            </Card.Content>
          </Card>

          {/* Typography */}
          <Card>
            <Card.Header>
              <Card.Title>Typography</Card.Title>
            </Card.Header>
            <Card.Content>
              <View style={{ gap: spacing.sm }}>
                <Text variant="h1">Heading 1</Text>
                <Text variant="h2">Heading 2</Text>
                <Text variant="h3">Heading 3</Text>
                <Text variant="h4">Heading 4</Text>
                <Text variant="default">Default body text</Text>
                <Text variant="muted">Muted text for secondary content</Text>
                <Text variant="link">Link text style</Text>
                <Text variant="code">code.example()</Text>
              </View>
            </Card.Content>
          </Card>
        </View>
      </ScrollView>
    </Container>
  );
}
