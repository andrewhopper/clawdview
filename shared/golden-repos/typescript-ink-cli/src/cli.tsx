#!/usr/bin/env node
/**
 * Ink CLI entry point.
 */

import React from 'react';
import { render } from 'ink';
import meow from 'meow';
import { App } from './App.js';
import { GreetCommand } from './commands/Greet.js';
import { ProcessCommand } from './commands/Process.js';

const cli = meow(
  `
  Usage
    $ mycli <command> [options]

  Commands
    greet <name>     Greet a user
    process <files>  Process files with progress

  Options
    --loud, -l       Greet loudly
    --dry-run, -d    Show what would be processed
    --help           Show help
    --version        Show version

  Examples
    $ mycli greet World
    $ mycli greet World --loud
    $ mycli process file1.txt file2.txt
    $ mycli process file1.txt --dry-run
`,
  {
    importMeta: import.meta,
    flags: {
      loud: {
        type: 'boolean',
        shortFlag: 'l',
      },
      dryRun: {
        type: 'boolean',
        shortFlag: 'd',
      },
    },
  }
);

const [command, ...args] = cli.input;

function Main() {
  switch (command) {
    case 'greet':
      return <GreetCommand name={args[0] || 'World'} loud={cli.flags.loud} />;
    case 'process':
      return <ProcessCommand files={args} dryRun={cli.flags.dryRun} />;
    default:
      return <App />;
  }
}

render(<Main />);
