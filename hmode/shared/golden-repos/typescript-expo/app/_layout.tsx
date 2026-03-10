import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useColorScheme } from 'react-native';
import { ThemeProvider, DefaultTheme, DarkTheme } from '@/lib/theme';
import { AWSLightTheme, AWSDarkTheme } from '@/lib/themes/aws';

// Change this to 'aws' to use AWS theme, or 'default' for shadcn/ui theme
const THEME_VARIANT: 'default' | 'aws' = 'default';

function getThemes(variant: 'default' | 'aws') {
  switch (variant) {
    case 'aws':
      return { light: AWSLightTheme, dark: AWSDarkTheme };
    case 'default':
    default:
      return { light: DefaultTheme, dark: DarkTheme };
  }
}

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const themes = getThemes(THEME_VARIANT);

  return (
    <ThemeProvider
      lightTheme={themes.light}
      darkTheme={themes.dark}
      initialDark={colorScheme === 'dark'}
    >
      <Stack
        screenOptions={{
          headerShown: false,
        }}
      />
      <StatusBar style="auto" />
    </ThemeProvider>
  );
}
