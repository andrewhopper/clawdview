import '@testing-library/react-native/extend-expect';

// Mock expo-constants
jest.mock('expo-constants', () => ({
  expoConfig: {
    version: '1.0.0',
    extra: {
      environment: 'development',
      apiUrl: 'http://localhost:3000',
    },
  },
}));

// Mock AsyncStorage
jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock')
);

// Silence the warning: Animated: `useNativeDriver` is not supported
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
