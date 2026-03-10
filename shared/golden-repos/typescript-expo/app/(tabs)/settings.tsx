import { View, ScrollView, Switch } from 'react-native';
import { Text } from '@/components/ui/Text';
import { Card } from '@/components/ui/Card';
import { Separator } from '@/components/ui/Separator';
import { Container } from '@/components/layout/Container';
import { useTheme } from '@/lib/theme';
import { useState } from 'react';

interface SettingRowProps {
  title: string;
  description?: string;
  children: React.ReactNode;
}

function SettingRow({ title, description, children }: SettingRowProps) {
  const { spacing } = useTheme();

  return (
    <View
      style={{
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingVertical: spacing.sm,
      }}
    >
      <View style={{ flex: 1, marginRight: spacing.md }}>
        <Text variant="default">{title}</Text>
        {description && <Text variant="muted" size="sm">{description}</Text>}
      </View>
      {children}
    </View>
  );
}

export default function SettingsScreen() {
  const { colors, spacing } = useTheme();
  const [notifications, setNotifications] = useState(true);
  const [analytics, setAnalytics] = useState(false);

  return (
    <Container>
      <ScrollView
        contentContainerStyle={{ padding: spacing.lg }}
        showsVerticalScrollIndicator={false}
      >
        <View style={{ gap: spacing.lg }}>
          <View style={{ gap: spacing.sm }}>
            <Text variant="h1">Settings</Text>
            <Text variant="muted">Manage your app preferences.</Text>
          </View>

          <Card>
            <Card.Header>
              <Card.Title>Notifications</Card.Title>
            </Card.Header>
            <Card.Content>
              <SettingRow
                title="Push Notifications"
                description="Receive push notifications for updates"
              >
                <Switch
                  value={notifications}
                  onValueChange={setNotifications}
                  trackColor={{ true: colors.primary, false: colors.muted }}
                />
              </SettingRow>
            </Card.Content>
          </Card>

          <Card>
            <Card.Header>
              <Card.Title>Privacy</Card.Title>
            </Card.Header>
            <Card.Content>
              <SettingRow
                title="Analytics"
                description="Help us improve by sharing usage data"
              >
                <Switch
                  value={analytics}
                  onValueChange={setAnalytics}
                  trackColor={{ true: colors.primary, false: colors.muted }}
                />
              </SettingRow>
              <Separator />
              <SettingRow title="Clear Cache" description="Free up storage space">
                <Text variant="link">Clear</Text>
              </SettingRow>
            </Card.Content>
          </Card>

          <Card>
            <Card.Header>
              <Card.Title>About</Card.Title>
            </Card.Header>
            <Card.Content>
              <SettingRow title="Version">
                <Text variant="muted">1.0.0</Text>
              </SettingRow>
              <Separator />
              <SettingRow title="Build">
                <Text variant="muted">2024.1</Text>
              </SettingRow>
            </Card.Content>
          </Card>
        </View>
      </ScrollView>
    </Container>
  );
}
