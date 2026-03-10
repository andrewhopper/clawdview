/**
 * Greet command - example simple command.
 */

import { Command } from 'commander';
import chalk from 'chalk';

export const greetCommand = new Command('greet')
  .description('Greet a user')
  .argument('<name>', 'Name to greet')
  .option('-l, --loud', 'Greet loudly')
  .action((name: string, options: { loud?: boolean }) => {
    const greeting = `Hello, ${name}!`;

    if (options.loud) {
      console.log(chalk.bold.green(greeting.toUpperCase()));
    } else {
      console.log(chalk.green(greeting));
    }
  });
