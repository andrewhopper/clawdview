# TypeScript Expo Template

Gold standard Expo React Native template with design system components following shadcn/ui patterns.

## Quick Start

```bash
cd typescript-expo
npm install
npm run start
# Press 'i' for iOS, 'a' for Android, 'w' for web
```

## Features

- **Expo SDK 52** - Latest Expo with New Architecture enabled
- **Expo Router** - File-based routing with typed routes
- **Design System** - Native components following shadcn/ui patterns
- **Dark Mode** - Automatic dark mode support with theme context
- **TypeScript Strict** - Full type safety with strict mode
- **Zod Validation** - Schema validation for config and forms
- **Testing** - Jest + React Native Testing Library setup
- **Device Permissions** - Pre-configured camera, location, media, calendar, sensors, LiDAR, and microphone access

## Structure

```
typescript-expo/
├── app/                    # Expo Router screens
│   ├── _layout.tsx         # Root layout with theme
│   ├── index.tsx           # Entry redirect
│   └── (tabs)/             # Tab navigation
│       ├── _layout.tsx     # Tab bar config
│       ├── index.tsx       # Home screen
│       ├── explore.tsx     # Explore screen
│       ├── theme.tsx       # Theme demo screen
│       └── settings.tsx    # Settings screen
├── src/
│   ├── components/
│   │   ├── ui/             # Design system components
│   │   │   ├── Button.tsx
│   │   │   ├── Text.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Separator.tsx
│   │   │   └── TabBarIcon.tsx
│   │   └── layout/         # Layout components
│   │       └── Container.tsx
│   ├── hooks/              # Custom hooks
│   │   ├── useDebounce.ts
│   │   ├── useToggle.ts
│   │   └── useAsyncStorage.ts
│   ├── lib/
│   │   ├── theme.tsx       # Theme system
│   │   ├── fonts.ts        # Font configurations
│   │   └── themes/         # Theme variants
│   │       ├── aws.ts      # AWS brand theme
│   │       └── index.ts    # Theme exports
│   ├── config/             # App configuration
│   └── constants/          # App constants
├── tests/                  # Test files
├── assets/                 # Images, fonts
├── app.json                # Expo config
├── package.json
└── tsconfig.json
```

## Design System Components

### Button

```tsx
import { Button } from '@/components/ui';

// Variants: default, secondary, outline, ghost, destructive, link
<Button variant="default">Click me</Button>
<Button variant="outline" size="lg">Large Outline</Button>
<Button loading>Loading...</Button>
```

### Text

```tsx
import { Text } from '@/components/ui';

// Variants: default, h1, h2, h3, h4, muted, link, code
<Text variant="h1">Heading 1</Text>
<Text variant="muted" size="sm">Small muted text</Text>
```

### Card

```tsx
import { Card } from '@/components/ui';

<Card>
  <Card.Header>
    <Card.Title>Title</Card.Title>
    <Card.Description>Description</Card.Description>
  </Card.Header>
  <Card.Content>
    <Text>Content goes here</Text>
  </Card.Content>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card>
```

### Input

```tsx
import { Input } from '@/components/ui';

<Input
  label="Email"
  placeholder="Enter email"
  error="Invalid email"
/>
```

### Badge

```tsx
import { Badge } from '@/components/ui';

// Variants: default, secondary, outline, destructive
<Badge variant="secondary">New</Badge>
```

## Theme System

The template includes a complete theme system with light/dark mode support and multiple theme variants.

### Basic Usage

```tsx
import { useTheme, ThemeProvider, DefaultTheme, DarkTheme } from '@/lib/theme';

// In components
const { colors, spacing, borderRadius } = useTheme();

// Theme colors match shadcn/ui
colors.primary        // Primary color
colors.secondary      // Secondary color
colors.muted          // Muted background
colors.destructive    // Error/destructive color
colors.border         // Border color
```

### Theme Variants

Two theme variants are available:

1. **Default** (shadcn/ui inspired) - Neutral grayscale palette
2. **AWS** - Official AWS brand colors (Orange #FF9900, Squid Ink #232F3E)

### Switching to AWS Theme

In `app/_layout.tsx`, change the theme variant:

```tsx
// Change this to 'aws' to use AWS theme
const THEME_VARIANT: 'default' | 'aws' = 'aws';
```

### AWS Theme Colors

```tsx
import { AWSLightTheme, AWSDarkTheme, awsColors } from '@/lib/themes/aws';

// Brand colors
awsColors.orange      // #FF9900 - Amazon Orange
awsColors.squidInk    // #232F3E - Primary dark

// Service category colors
awsColors.compute     // #ED7100 - EC2, Lambda
awsColors.storage     // #3B48CC - S3
awsColors.database    // #3B48CC - RDS, DynamoDB
awsColors.networking  // #8C4FFF - VPC, CloudFront
awsColors.security    // #DD344C - IAM, Security Hub
awsColors.machineLearning // #01A88D - SageMaker

// Semantic colors
awsColors.success     // #037F0C
awsColors.warning     // #FFAC31
awsColors.error       // #D91515
awsColors.info        // #0972D3
```

### Extended AWS Theme

For access to service category colors in your theme:

```tsx
import { AWSLightThemeExtended, type AWSExtendedTheme } from '@/lib/themes/aws';

// Extended theme includes brand.services
const theme = AWSLightThemeExtended;
theme.brand.services.compute  // EC2/Lambda orange
theme.brand.services.storage  // S3 blue
```

### Amazon Ember Font

To use AWS's official Amazon Ember font:

1. Download font files from AWS Brand Portal
2. Place in `assets/fonts/`:
   - `AmazonEmber_Rg.ttf` (Regular)
   - `AmazonEmber_Md.ttf` (Medium)
   - `AmazonEmber_Bd.ttf` (Bold)
   - `AmazonEmber_Lt.ttf` (Light)

3. Load fonts in your app:

```tsx
import { useFonts } from 'expo-font';
import { amazonEmberFonts } from '@/lib/fonts';

const [fontsLoaded] = useFonts({
  'AmazonEmber-Regular': require('./assets/fonts/AmazonEmber_Rg.ttf'),
  'AmazonEmber-Medium': require('./assets/fonts/AmazonEmber_Md.ttf'),
  'AmazonEmber-Bold': require('./assets/fonts/AmazonEmber_Bd.ttf'),
});
```

### Theme Toggle

Use `useThemeContext` for runtime theme switching:

```tsx
import { useThemeContext } from '@/lib/theme';

function ThemeToggle() {
  const { isDark, toggleTheme } = useThemeContext();

  return (
    <Switch value={isDark} onValueChange={toggleTheme} />
  );
}
```

## Hooks

### useDebounce

```tsx
import { useDebounce } from '@/hooks';

const debouncedSearch = useDebounce(searchQuery, 300);
```

### useToggle

```tsx
import { useToggle } from '@/hooks';

const [isOpen, toggle, setIsOpen] = useToggle(false);
```

### useAsyncStorage

```tsx
import { useAsyncStorage } from '@/hooks';

const [value, setValue, loading] = useAsyncStorage('key', defaultValue);
```

## Configuration

Configuration with Zod validation:

```tsx
import { config } from '@/config';

const { apiUrl, environment, appVersion } = config();
```

Environment variables (`.env`):

```bash
EXPO_PUBLIC_ENVIRONMENT=development
EXPO_PUBLIC_API_URL=http://localhost:3000
```

## Testing

```bash
# Run tests
npm test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

## Building

```bash
# Create native builds (requires EAS CLI)
npm run prebuild              # Generate native projects
npm run build:ios             # Build iOS
npm run build:android         # Build Android
```

## Device Permissions

This template comes pre-configured with comprehensive device permissions for native hardware access. See [docs/PERMISSIONS.md](./docs/PERMISSIONS.md) for complete documentation.

### Included Permissions

- **Camera** - Photo and video capture
- **Microphone** - Audio recording
- **Location** - GPS, foreground and background tracking
- **Media Library** - Photo library read/write access
- **Calendar & Reminders** - Apple Reminders integration
- **Sensors** - Accelerometer, gyroscope, magnetometer
- **LiDAR** - Depth sensing via ARKit (iOS devices with LiDAR)
- **File System** - Document picker and file operations

### Interactive Demo

The template includes a **Permissions Demo** tab that showcases all device permissions with interactive examples. Test each permission with a single tap and see real results.

**Features:**
- Request permissions with status badges (granted/denied/not requested)
- Test camera, microphone, location, media library, calendar, sensors
- View real-time sensor data (accelerometer)
- Pick files with document picker
- Built with design system components

### Quick Usage

```tsx
import { Camera } from 'expo-camera';
import * as Location from 'expo-location';
import * as MediaLibrary from 'expo-media-library';

// Camera
const [permission, requestPermission] = Camera.useCameraPermissions();

// Location
const { status } = await Location.requestForegroundPermissionsAsync();

// Media Library
const { status } = await MediaLibrary.requestPermissionsAsync();
```

See [docs/PERMISSIONS.md](./docs/PERMISSIONS.md) for detailed usage examples, platform-specific notes, and privacy guidelines.

## Best Practices

### Type Safety

- All components have typed props with explicit interfaces
- Use Zod for runtime validation of external data
- Leverage TypeScript strict mode

### Component Patterns

- Use compound components for complex UI (Card.Header, Card.Content)
- Forward refs for pressable components
- Expose variant types for flexibility

### Styling

- Use theme values instead of hardcoded colors/spacing
- StyleSheet.create for static styles
- Dynamic styles via inline objects with theme values

### Navigation

- File-based routing with Expo Router
- Type-safe navigation with typed routes
- Tab navigation with icons

## Inherits From

This template inherits patterns from:

- **Design System**: Component variants, theme tokens from `@protoflow/design-system`
- **TypeScript Standards**: Strict mode, naming conventions from `shared/standards/code/typescript/`

## Scripts

| Script | Description |
|--------|-------------|
| `start` | Start Expo dev server |
| `ios` | Start on iOS simulator |
| `android` | Start on Android emulator |
| `web` | Start in web browser |
| `test` | Run tests |
| `lint` | Run ESLint |
| `typecheck` | Run TypeScript check |
| `prebuild` | Generate native projects |
