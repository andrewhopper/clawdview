import { Tabs } from 'expo-router';
import { useTheme } from '@/lib/theme';
import { TabBarIcon } from '@/components/ui/TabBarIcon';

export default function TabLayout() {
  const { colors } = useTheme();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.mutedForeground,
        tabBarStyle: {
          backgroundColor: colors.background,
          borderTopColor: colors.border,
        },
        headerStyle: {
          backgroundColor: colors.background,
        },
        headerTintColor: colors.foreground,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'home' : 'home-outline'} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="explore"
        options={{
          title: 'Explore',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'compass' : 'compass-outline'} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="theme"
        options={{
          title: 'Theme',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'color-palette' : 'color-palette-outline'} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="permissions"
        options={{
          title: 'Permissions',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'shield-checkmark' : 'shield-checkmark-outline'} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'Settings',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'settings' : 'settings-outline'} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
