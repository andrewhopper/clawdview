/**
 * Reusable text input prompt component.
 */

import React, { useState } from 'react';
import { Box, Text } from 'ink';
import TextInput from 'ink-text-input';

interface TextPromptProps {
  prompt: string;
  placeholder?: string;
  onSubmit: (value: string) => void;
}

export function TextPrompt({ prompt, placeholder = '', onSubmit }: TextPromptProps) {
  const [value, setValue] = useState('');

  return (
    <Box flexDirection="column" padding={1}>
      <Text bold color="cyan">
        {prompt}
      </Text>
      <Box marginTop={1}>
        <Text color="gray">&gt; </Text>
        <TextInput
          value={value}
          onChange={setValue}
          onSubmit={onSubmit}
          placeholder={placeholder}
        />
      </Box>
    </Box>
  );
}
