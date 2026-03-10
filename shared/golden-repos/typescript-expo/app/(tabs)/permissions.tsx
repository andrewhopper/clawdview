import { useState } from 'react';
import { ScrollView, StyleSheet, Alert, Platform } from 'react-native';
import { Camera } from 'expo-camera';
import * as Location from 'expo-location';
import * as MediaLibrary from 'expo-media-library';
import * as Calendar from 'expo-calendar';
import { Accelerometer, Gyroscope } from 'expo-sensors';
import { Audio } from 'expo-av';
import * as DocumentPicker from 'expo-document-picker';
import { Container } from '@/components/layout';
import { Text, Button, Card, Badge } from '@/components/ui';
import { useTheme } from '@/lib/theme';

type PermissionStatus = 'undetermined' | 'granted' | 'denied';

interface PermissionState {
  status: PermissionStatus;
  result?: string;
}

export default function PermissionsScreen() {
  const { spacing } = useTheme();
  const [camera, setCamera] = useState<PermissionState>({ status: 'undetermined' });
  const [microphone, setMicrophone] = useState<PermissionState>({ status: 'undetermined' });
  const [location, setLocation] = useState<PermissionState>({ status: 'undetermined' });
  const [mediaLibrary, setMediaLibrary] = useState<PermissionState>({ status: 'undetermined' });
  const [calendarPerm, setCalendarPerm] = useState<PermissionState>({ status: 'undetermined' });
  const [sensors, setSensors] = useState<PermissionState>({ status: 'undetermined' });

  const getStatusBadge = (status: PermissionStatus) => {
    switch (status) {
      case 'granted':
        return <Badge variant="default">Granted</Badge>;
      case 'denied':
        return <Badge variant="destructive">Denied</Badge>;
      default:
        return <Badge variant="secondary">Not Requested</Badge>;
    }
  };

  const handleRequestCamera = async () => {
    try {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setCamera({
        status: status === 'granted' ? 'granted' : 'denied',
        result: `Camera permission: ${status}`,
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to request camera permission');
    }
  };

  const handleTestCamera = async () => {
    const { status } = await Camera.getCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Required', 'Please grant camera permission first');
      return;
    }
    setCamera({ ...camera, result: 'Camera is ready to use! You can now capture photos/videos.' });
  };

  const handleRequestMicrophone = async () => {
    try {
      const { status } = await Audio.requestPermissionsAsync();
      setMicrophone({
        status: status === 'granted' ? 'granted' : 'denied',
        result: `Microphone permission: ${status}`,
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to request microphone permission');
    }
  };

  const handleTestMicrophone = async () => {
    const { status } = await Audio.getPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Required', 'Please grant microphone permission first');
      return;
    }
    setMicrophone({ ...microphone, result: 'Microphone is ready! You can now record audio.' });
  };

  const handleRequestLocation = async () => {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      setLocation({
        status: status === 'granted' ? 'granted' : 'denied',
        result: `Location permission: ${status}`,
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to request location permission');
    }
  };

  const handleTestLocation = async () => {
    try {
      const { status } = await Location.getForegroundPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permission Required', 'Please grant location permission first');
        return;
      }
      const location = await Location.getCurrentPositionAsync({});
      setLocation({
        ...location,
        result: `Lat: ${location.coords.latitude.toFixed(4)}, Lon: ${location.coords.longitude.toFixed(4)}`,
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to get location');
    }
  };

  const handleRequestMediaLibrary = async () => {
    try {
      const { status } = await MediaLibrary.requestPermissionsAsync();
      setMediaLibrary({
        status: status === 'granted' ? 'granted' : 'denied',
        result: `Media library permission: ${status}`,
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to request media library permission');
    }
  };

  const handleTestMediaLibrary = async () => {
    try {
      const { status } = await MediaLibrary.getPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permission Required', 'Please grant media library permission first');
        return;
      }
      const albums = await MediaLibrary.getAlbumsAsync();
      setMediaLibrary({
        ...mediaLibrary,
        result: `Found ${albums.length} photo albums`,
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to access media library');
    }
  };

  const handleRequestCalendar = async () => {
    try {
      const { status } = await Calendar.requestCalendarPermissionsAsync();
      setCalendarPerm({
        status: status === 'granted' ? 'granted' : 'denied',
        result: `Calendar permission: ${status}`,
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to request calendar permission');
    }
  };

  const handleTestCalendar = async () => {
    try {
      const { status } = await Calendar.getCalendarPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permission Required', 'Please grant calendar permission first');
        return;
      }
      const calendars = await Calendar.getCalendarsAsync();
      setCalendarPerm({
        ...calendarPerm,
        result: `Found ${calendars.length} calendars`,
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to access calendar');
    }
  };

  const handleTestSensors = () => {
    try {
      const subscription = Accelerometer.addListener((data) => {
        setSensors({
          status: 'granted',
          result: `X: ${data.x.toFixed(2)}, Y: ${data.y.toFixed(2)}, Z: ${data.z.toFixed(2)}`,
        });
        subscription.remove();
      });
      Accelerometer.setUpdateInterval(100);

      // Auto-remove after getting first reading
      setTimeout(() => {
        if (subscription) subscription.remove();
      }, 1000);
    } catch (error) {
      Alert.alert('Error', 'Failed to access sensors');
    }
  };

  const handleTestFilePicker = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: '*/*',
        copyToCacheDirectory: true,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const file = result.assets[0];
        Alert.alert('File Selected', `${file.name}\nSize: ${file.size} bytes`);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to pick document');
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Container>
        <Text variant="h2" style={{ marginBottom: spacing.lg }}>
          Device Permissions Demo
        </Text>
        <Text variant="muted" style={{ marginBottom: spacing.xl }}>
          Test all device permissions with interactive examples
        </Text>

        {/* Camera */}
        <Card style={{ marginBottom: spacing.md }}>
          <Card.Header>
            <Card.Title>Camera</Card.Title>
            <Card.Description>
              Access camera for photos and videos
            </Card.Description>
            {getStatusBadge(camera.status)}
          </Card.Header>
          <Card.Content>
            {camera.result && (
              <Text variant="muted" size="sm" style={{ marginBottom: spacing.sm }}>
                {camera.result}
              </Text>
            )}
            <Button
              variant="outline"
              onPress={handleRequestCamera}
              style={{ marginBottom: spacing.sm }}
            >
              Request Permission
            </Button>
            <Button onPress={handleTestCamera}>Test Camera</Button>
          </Card.Content>
        </Card>

        {/* Microphone */}
        <Card style={{ marginBottom: spacing.md }}>
          <Card.Header>
            <Card.Title>Microphone</Card.Title>
            <Card.Description>
              Record audio and videos with sound
            </Card.Description>
            {getStatusBadge(microphone.status)}
          </Card.Header>
          <Card.Content>
            {microphone.result && (
              <Text variant="muted" size="sm" style={{ marginBottom: spacing.sm }}>
                {microphone.result}
              </Text>
            )}
            <Button
              variant="outline"
              onPress={handleRequestMicrophone}
              style={{ marginBottom: spacing.sm }}
            >
              Request Permission
            </Button>
            <Button onPress={handleTestMicrophone}>Test Microphone</Button>
          </Card.Content>
        </Card>

        {/* Location */}
        <Card style={{ marginBottom: spacing.md }}>
          <Card.Header>
            <Card.Title>Location</Card.Title>
            <Card.Description>
              Access GPS and location services
            </Card.Description>
            {getStatusBadge(location.status)}
          </Card.Header>
          <Card.Content>
            {location.result && (
              <Text variant="muted" size="sm" style={{ marginBottom: spacing.sm }}>
                {location.result}
              </Text>
            )}
            <Button
              variant="outline"
              onPress={handleRequestLocation}
              style={{ marginBottom: spacing.sm }}
            >
              Request Permission
            </Button>
            <Button onPress={handleTestLocation}>Get Current Location</Button>
          </Card.Content>
        </Card>

        {/* Media Library */}
        <Card style={{ marginBottom: spacing.md }}>
          <Card.Header>
            <Card.Title>Media Library</Card.Title>
            <Card.Description>
              Access photos and videos from library
            </Card.Description>
            {getStatusBadge(mediaLibrary.status)}
          </Card.Header>
          <Card.Content>
            {mediaLibrary.result && (
              <Text variant="muted" size="sm" style={{ marginBottom: spacing.sm }}>
                {mediaLibrary.result}
              </Text>
            )}
            <Button
              variant="outline"
              onPress={handleRequestMediaLibrary}
              style={{ marginBottom: spacing.sm }}
            >
              Request Permission
            </Button>
            <Button onPress={handleTestMediaLibrary}>List Albums</Button>
          </Card.Content>
        </Card>

        {/* Calendar */}
        <Card style={{ marginBottom: spacing.md }}>
          <Card.Header>
            <Card.Title>Calendar & Reminders</Card.Title>
            <Card.Description>
              Access calendar events and reminders
            </Card.Description>
            {getStatusBadge(calendarPerm.status)}
          </Card.Header>
          <Card.Content>
            {calendarPerm.result && (
              <Text variant="muted" size="sm" style={{ marginBottom: spacing.sm }}>
                {calendarPerm.result}
              </Text>
            )}
            <Button
              variant="outline"
              onPress={handleRequestCalendar}
              style={{ marginBottom: spacing.sm }}
            >
              Request Permission
            </Button>
            <Button onPress={handleTestCalendar}>List Calendars</Button>
          </Card.Content>
        </Card>

        {/* Sensors */}
        <Card style={{ marginBottom: spacing.md }}>
          <Card.Header>
            <Card.Title>Sensors</Card.Title>
            <Card.Description>
              Accelerometer, gyroscope, and motion data
            </Card.Description>
            {getStatusBadge(sensors.status)}
          </Card.Header>
          <Card.Content>
            {sensors.result && (
              <Text variant="muted" size="sm" style={{ marginBottom: spacing.sm }}>
                Accelerometer: {sensors.result}
              </Text>
            )}
            <Text variant="muted" size="sm" style={{ marginBottom: spacing.sm }}>
              Note: Sensors don't require permission on most devices
            </Text>
            <Button onPress={handleTestSensors}>Read Accelerometer</Button>
          </Card.Content>
        </Card>

        {/* File System */}
        <Card style={{ marginBottom: spacing.xl }}>
          <Card.Header>
            <Card.Title>File System</Card.Title>
            <Card.Description>
              Pick documents and access files
            </Card.Description>
          </Card.Header>
          <Card.Content>
            <Text variant="muted" size="sm" style={{ marginBottom: spacing.sm }}>
              Note: File picker doesn't require explicit permission
            </Text>
            <Button onPress={handleTestFilePicker}>Pick Document</Button>
          </Card.Content>
        </Card>

        {/* LiDAR Note */}
        <Card style={{ marginBottom: spacing.xl }}>
          <Card.Header>
            <Card.Title>LiDAR / ARKit</Card.Title>
            <Card.Description>
              Depth sensing for supported devices
            </Card.Description>
          </Card.Header>
          <Card.Content>
            <Text variant="muted" size="sm">
              LiDAR is available through ARKit on iPhone 12 Pro and later, iPad Pro 2020 and later.
              Requires separate implementation with expo-gl and expo-three.
            </Text>
          </Card.Content>
        </Card>
      </Container>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
