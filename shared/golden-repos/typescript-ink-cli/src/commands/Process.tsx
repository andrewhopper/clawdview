/**
 * Process command component with progress indication.
 */

import React, { useState, useEffect } from 'react';
import { Box, Text } from 'ink';
import Spinner from 'ink-spinner';

interface ProcessCommandProps {
  files: string[];
  dryRun?: boolean;
}

export function ProcessCommand({ files, dryRun = false }: ProcessCommandProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    if (dryRun || files.length === 0) {
      setIsComplete(true);
      return;
    }

    const timer = setInterval(() => {
      setCurrentIndex((prev) => {
        if (prev >= files.length - 1) {
          clearInterval(timer);
          setIsComplete(true);
          return prev;
        }
        return prev + 1;
      });
    }, 500);

    return () => clearInterval(timer);
  }, [files.length, dryRun]);

  if (dryRun) {
    return (
      <Box flexDirection="column" padding={1}>
        <Text color="yellow">Dry run mode - no changes will be made</Text>
        <Box flexDirection="column" marginTop={1}>
          {files.map((file) => (
            <Text key={file}>  Would process: {file}</Text>
          ))}
        </Box>
      </Box>
    );
  }

  if (files.length === 0) {
    return (
      <Box padding={1}>
        <Text color="red">No files provided</Text>
      </Box>
    );
  }

  if (isComplete) {
    return (
      <Box padding={1}>
        <Text color="green">✓ Successfully processed {files.length} files</Text>
      </Box>
    );
  }

  return (
    <Box padding={1}>
      <Text color="cyan">
        <Spinner type="dots" />
        {' '}Processing {files[currentIndex]} ({currentIndex + 1}/{files.length})
      </Text>
    </Box>
  );
}
