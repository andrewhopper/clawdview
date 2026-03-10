import { Ionicons } from '@expo/vector-icons';
import type { ComponentProps } from 'react';

type IoniconsName = ComponentProps<typeof Ionicons>['name'];

export interface TabBarIconProps {
  name: IoniconsName;
  color: string;
  size?: number;
}

export function TabBarIcon({ name, color, size = 24 }: TabBarIconProps) {
  return <Ionicons name={name} size={size} color={color} />;
}
