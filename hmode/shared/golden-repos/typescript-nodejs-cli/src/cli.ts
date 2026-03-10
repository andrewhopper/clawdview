#!/usr/bin/env node
/**
 * CLI entry point.
 */

import { Command } from 'commander';
import { getConfig } from './config.js';
import { getLogger } from './logger.js';
import { greetCommand } from './commands/greet.js';
import { processCommand } from './commands/process.js';

const config = getConfig();
const log = getLogger('cli');

const program = new Command();

program
  .name('mycli')
  .description('Gold standard TypeScript CLI template')
  .version('0.1.0')
  .option('-v, --verbose', 'Enable verbose output')
  .hook('preAction', (thisCommand) => {
    if (thisCommand.opts().verbose) {
      log.level = 'debug';
    }
  });

// Register commands
program.addCommand(greetCommand);
program.addCommand(processCommand);

// Parse and execute
program.parse();
