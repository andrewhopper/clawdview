/**
 * Main App component - shows when no command is provided.
 */

import React from 'react';
import { Box, Text } from 'ink';

export function App() {
  return (
    <Box flexDirection="column" padding={1}>
      <Text bold color="cyan">
        Welcome to the Ink CLI Template!
      </Text>
      <Box marginTop={1}>
        <Text>Run with --help to see available commands.</Text>
      </Box>
    </Box>
  );
}
