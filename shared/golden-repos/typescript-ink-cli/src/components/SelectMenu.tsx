/**
 * Reusable select menu component.
 */

import React from 'react';
import { Box, Text } from 'ink';
import SelectInput from 'ink-select-input';

interface SelectMenuProps<T> {
  title: string;
  items: Array<{ label: string; value: T }>;
  onSelect: (item: { label: string; value: T }) => void;
}

export function SelectMenu<T>({ title, items, onSelect }: SelectMenuProps<T>) {
  return (
    <Box flexDirection="column" padding={1}>
      <Text bold color="cyan">
        {title}
      </Text>
      <Box marginTop={1}>
        <SelectInput items={items} onSelect={onSelect} />
      </Box>
    </Box>
  );
}
