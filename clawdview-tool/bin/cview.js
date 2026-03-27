#!/usr/bin/env node

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const readline = require('readline');
const { exec } = require('child_process');

// Use tsx to register TypeScript support for direct execution
try {
  require('tsx/cjs');
} catch {
  // If tsx is not available, fall back to compiled JS
}

// Try TypeScript source first, then compiled JS
let ClawdViewServer, TunnelService;
try {
  ({ ClawdViewServer } = require('../src/server/server'));
  ({ TunnelService } = require('../src/server/services/tunnel-service'));
} catch {
  ({ ClawdViewServer } = require('../dist/server/server'));
  ({ TunnelService } = require('../dist/server/services/tunnel-service'));
}

function prompt(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase());
    });
  });
}

async function launch(watchDir, options = {}) {
  const requestedPort = parseInt(options.port || '3333');
  const autoOpen = options.open !== false;
  const tunnelProvider = options.tunnel;

  console.log(`\n  ClawdView`);

  const server = new ClawdViewServer({
    port: requestedPort,
    watchDir,
    autoOpen,
    host: tunnelProvider ? '0.0.0.0' : 'localhost'
  });

  let actualPort;
  try {
    actualPort = await server.start();
  } catch (err) {
    console.error(`\n  Error: ${err.message}`);
    process.exit(1);
  }

  if (actualPort !== requestedPort) {
    console.log(`  Note:    requested port ${requestedPort} was in use`);
  }
  console.log('');

  if (autoOpen) {
    const url = `http://localhost:${actualPort}`;
    exec(`open ${url}`);
  }

  if (tunnelProvider) {
    const provider = tunnelProvider.toLowerCase();
    if (!TunnelService.supportedProviders.includes(provider)) {
      console.error(`Unknown tunnel provider: "${tunnelProvider}"`);
      console.error(`Supported: ${TunnelService.supportedProviders.join(', ')}`);
      server.stop();
      process.exit(1);
    }

    const tunnel = new TunnelService({ provider, port: actualPort });
    console.log(`Starting ${provider} tunnel...`);

    try {
      const url = await tunnel.start();
      console.log(`Remote URL: ${url}\n`);
    } catch (err) {
      console.error(`Failed to start tunnel: ${err.message}`);
      server.stop();
      process.exit(1);
    }

    process.on('SIGINT', async () => {
      console.log('\nShutting down...');
      await tunnel.stop();
      server.stop();
      process.exit(0);
    });
  } else {
    process.on('SIGINT', () => {
      console.log('\nShutting down...');
      server.stop();
      process.exit(0);
    });
  }
}

const program = new Command();

program
  .name('cview')
  .description('ClawdView - Universal rapid prototyping tool for instant code preview')
  .version('2.0.0')
  .argument('[directory]', 'Directory to watch')
  .option('-p, --port <port>', 'Server port', '3333')
  .option('--no-open', "Don't auto-open browser")
  .option('--tunnel <provider>', 'Expose via tunnel (ngrok, localtunnel)')
  .action(async (directory, options) => {
    if (directory) {
      const watchDir = path.resolve(directory);
      if (!fs.existsSync(watchDir)) {
        console.error(`Directory not found: ${watchDir}`);
        process.exit(1);
      }
      await launch(watchDir, options);
    } else {
      const cwd = process.cwd();
      const answer = await prompt(`Would you like to launch ClawdView in the current directory?\n  ${cwd}\n  [Y/n] `);
      if (answer === '' || answer === 'y' || answer === 'yes') {
        await launch(cwd, options);
      } else {
        console.log('Cancelled.');
        process.exit(0);
      }
    }
  });

program.parse();
