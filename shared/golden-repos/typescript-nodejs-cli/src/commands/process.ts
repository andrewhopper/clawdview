/**
 * Process command - example async command with spinner.
 */

import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import { getLogger } from '../logger.js';

const log = getLogger('process');

export const processCommand = new Command('process')
  .description('Process files with progress indication')
  .argument('<files...>', 'Files to process')
  .option('-d, --dry-run', 'Show what would be processed without doing it')
  .action(async (files: string[], options: { dryRun?: boolean }) => {
    log.debug({ files, options }, 'Starting process command');

    if (options.dryRun) {
      console.log(chalk.yellow('Dry run mode - no changes will be made'));
      files.forEach((file) => {
        console.log(`  Would process: ${file}`);
      });
      return;
    }

    const spinner = ora('Processing files...').start();

    try {
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        spinner.text = `Processing ${file} (${i + 1}/${files.length})`;

        // Simulate processing
        await new Promise((resolve) => setTimeout(resolve, 500));

        log.info({ file }, 'Processed file');
      }

      spinner.succeed(chalk.green(`Successfully processed ${files.length} files`));
    } catch (error) {
      spinner.fail(chalk.red('Processing failed'));
      log.error({ error }, 'Process command failed');
      process.exit(1);
    }
  });
