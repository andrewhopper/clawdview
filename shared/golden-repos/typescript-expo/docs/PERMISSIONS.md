# Device Permissions Guide

This document outlines all device permissions configured in this Expo React Native application.

## Overview

The application is configured with comprehensive device permissions for camera, location, media library, calendar/reminders, sensors (accelerometer, gyroscope), LiDAR (via ARKit), and microphone access.

## Required Packages

All necessary Expo packages are included in `package.json`:

```json
{
  "expo-av": "~14.0.0",           // Audio/Video (Microphone)
  "expo-calendar": "~13.0.0",      // Calendar & Reminders
  "expo-camera": "~16.0.0",        // Camera
  "expo-document-picker": "~12.0.0", // File System Access
  "expo-file-system": "~18.0.0",   // File System Operations
  "expo-location": "~18.0.0",      // Location Services
  "expo-media-library": "~17.0.0", // Photo Library
  "expo-sensors": "~14.0.0"        // Accelerometer, Gyroscope
}
```

## iOS Permissions (Info.plist)

All iOS permissions are configured in `app.json` under `ios.infoPlist`:

### Camera
- **Key**: `NSCameraUsageDescription`
- **Description**: "This app requires camera access to capture photos and videos."
- **API**: `expo-camera`

### Microphone
- **Key**: `NSMicrophoneUsageDescription`
- **Description**: "This app requires microphone access to record audio and videos."
- **API**: `expo-av`

### Photo Library
- **Keys**:
  - `NSPhotoLibraryUsageDescription` - Read access
  - `NSPhotoLibraryAddUsageDescription` - Write access
- **Description**: "This app requires photo library access to save and retrieve media files."
- **API**: `expo-media-library`

### Location
- **Keys**:
  - `NSLocationWhenInUseUsageDescription` - Foreground location
  - `NSLocationAlwaysUsageDescription` - Background location
  - `NSLocationAlwaysAndWhenInUseUsageDescription` - Combined permission
- **Description**: "This app requires location access to provide location-based features."
- **API**: `expo-location`

### Calendar & Reminders
- **Keys**:
  - `NSCalendarsUsageDescription` - Calendar access
  - `NSRemindersUsageDescription` - Reminders access
- **Descriptions**:
  - Calendar: "This app requires calendar access to create and manage reminders."
  - Reminders: "This app requires access to reminders to create and manage tasks."
- **API**: `expo-calendar`

### Motion & Sensors
- **Key**: `NSMotionUsageDescription`
- **Description**: "This app requires motion and fitness tracking access to use the accelerometer and gyroscope."
- **API**: `expo-sensors`

### LiDAR (Depth Sensing)
- **Key**: `UIRequiredDeviceCapabilities: ["arkit"]`
- **Purpose**: Enables ARKit which provides access to LiDAR depth data on supported devices (iPhone 12 Pro and later, iPad Pro 2020 and later)
- **Note**: This makes the app require ARKit-capable devices. Remove if you want to support non-ARKit devices.

## Android Permissions (AndroidManifest.xml)

All Android permissions are configured in `app.json` under `android.permissions`:

### Camera
- **Permission**: `CAMERA`
- **API**: `expo-camera`

### Microphone
- **Permission**: `RECORD_AUDIO`
- **API**: `expo-av`

### Storage & Media
- **Permissions**:
  - `READ_EXTERNAL_STORAGE` - Read files (Android < 13)
  - `WRITE_EXTERNAL_STORAGE` - Write files (Android < 13)
  - `READ_MEDIA_IMAGES` - Read images (Android 13+)
  - `READ_MEDIA_VIDEO` - Read videos (Android 13+)
  - `READ_MEDIA_AUDIO` - Read audio (Android 13+)
- **API**: `expo-media-library`, `expo-document-picker`, `expo-file-system`

### Location
- **Permissions**:
  - `ACCESS_FINE_LOCATION` - Precise location
  - `ACCESS_COARSE_LOCATION` - Approximate location
  - `ACCESS_BACKGROUND_LOCATION` - Background location (Android 10+)
- **API**: `expo-location`

### Calendar
- **Permissions**:
  - `READ_CALENDAR` - Read calendar/reminders
  - `WRITE_CALENDAR` - Write calendar/reminders
- **API**: `expo-calendar`

### Sensors
- **Permissions**:
  - `BODY_SENSORS` - Access to sensors
  - `HIGH_SAMPLING_RATE_SENSORS` - High-frequency sensor data (Android 12+)
- **API**: `expo-sensors`
- **Note**: Includes accelerometer, gyroscope, magnetometer

## Interactive Demo

The template includes a complete **Permissions Demo** screen accessible from the tab bar. This interactive demo allows you to:

- Request each permission with a single tap
- View permission status (granted/denied/not requested)
- Test permission functionality
- See real-world examples of each API

**Location:** `app/(tabs)/permissions.tsx`

The demo showcases:
- Camera permission with status badge
- Microphone permission and audio recording setup
- Location services with GPS coordinates
- Media library with album listing
- Calendar access with calendar enumeration
- Accelerometer sensor data reading
- File picker (document selection)

All examples use the design system components (Card, Button, Badge, Text) and follow React Native best practices.

## Usage Examples

### Camera
```typescript
import { Camera } from 'expo-camera';

const [permission, requestPermission] = Camera.useCameraPermissions();

if (!permission?.granted) {
  await requestPermission();
}
```

### Location
```typescript
import * as Location from 'expo-location';

const { status } = await Location.requestForegroundPermissionsAsync();
if (status === 'granted') {
  const location = await Location.getCurrentPositionAsync({});
}
```

### Media Library
```typescript
import * as MediaLibrary from 'expo-media-library';

const { status } = await MediaLibrary.requestPermissionsAsync();
if (status === 'granted') {
  const albums = await MediaLibrary.getAlbumsAsync();
}
```

### Calendar & Reminders
```typescript
import * as Calendar from 'expo-calendar';

const { status } = await Calendar.requestCalendarPermissionsAsync();
if (status === 'granted') {
  const calendars = await Calendar.getCalendarsAsync();
}

const { status: reminderStatus } = await Calendar.requestRemindersPermissionsAsync();
if (reminderStatus === 'granted') {
  // Access reminders
}
```

### Accelerometer
```typescript
import { Accelerometer } from 'expo-sensors';

Accelerometer.addListener(accelerometerData => {
  console.log(accelerometerData);
});
```

### Microphone (Audio Recording)
```typescript
import { Audio } from 'expo-av';

const { status } = await Audio.requestPermissionsAsync();
if (status === 'granted') {
  const recording = new Audio.Recording();
  await recording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
  await recording.startAsync();
}
```

### File Picker
```typescript
import * as DocumentPicker from 'expo-document-picker';

const result = await DocumentPicker.getDocumentAsync({
  type: '*/*',
  copyToCacheDirectory: true,
});
```

## Build Configuration

After updating permissions, run:

```bash
# Clean prebuild files
rm -rf ios android

# Regenerate native projects
npx expo prebuild

# Or build with EAS
eas build --platform ios
eas build --platform android
```

## Runtime Permission Requests

All permissions must be requested at runtime before use. The app should:

1. Check if permission is already granted
2. Request permission if not granted
3. Handle permission denial gracefully
4. Provide context to users about why the permission is needed

## Platform-Specific Notes

### iOS
- ARKit (LiDAR) is only available on iPhone 12 Pro and later, iPad Pro 2020 and later
- Background location requires additional App Store review justification
- Motion permission required on iOS 14+

### Android
- Scoped storage changes in Android 10+ affect file access
- Background location requires separate permission on Android 10+
- High sampling rate sensors require explicit permission on Android 12+
- Runtime permissions required for Android 6.0+

## Privacy & Compliance

Ensure your app's privacy policy covers:
- Camera and photo access
- Location tracking (especially background)
- Audio recording
- Motion and fitness data
- Calendar and reminder access
- File system access

## Testing

Test on both iOS and Android:
- First-time permission requests
- Permission denial handling
- Permission revocation (in system settings)
- Feature degradation when permissions denied

## References

- [Expo Camera Documentation](https://docs.expo.dev/versions/latest/sdk/camera/)
- [Expo Location Documentation](https://docs.expo.dev/versions/latest/sdk/location/)
- [Expo Media Library Documentation](https://docs.expo.dev/versions/latest/sdk/media-library/)
- [Expo Calendar Documentation](https://docs.expo.dev/versions/latest/sdk/calendar/)
- [Expo Sensors Documentation](https://docs.expo.dev/versions/latest/sdk/sensors/)
- [Expo AV Documentation](https://docs.expo.dev/versions/latest/sdk/av/)
- [iOS Privacy Keys](https://developer.apple.com/documentation/bundleresources/information_property_list/protected_resources)
- [Android Permissions](https://developer.android.com/reference/android/Manifest.permission)
