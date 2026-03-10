/**
 * Greet command component.
 */

import React from 'react';
import { Box, Text } from 'ink';

interface GreetCommandProps {
  name: string;
  loud?: boolean;
}

export function GreetCommand({ name, loud = false }: GreetCommandProps) {
  const greeting = `Hello, ${name}!`;

  return (
    <Box padding={1}>
      <Text bold={loud} color="green">
        {loud ? greeting.toUpperCase() : greeting}
      </Text>
    </Box>
  );
}
