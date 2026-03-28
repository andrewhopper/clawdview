#!/usr/bin/env node

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');

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

const pkg = require('../package.json');
const program = new Command();

program
  .name('clawdview')
  .description('Universal rapid prototyping tool for instant code preview')
  .version(pkg.version);

program
  .command('start')
  .description('Start ClawdView server in current directory')
  .option('-p, --port <port>', 'Server port', '3333')
  .option('-d, --dir <directory>', 'Directory to watch', process.cwd())
  .option('--no-open', 'Don\'t auto-open browser')
  .option('--tunnel <provider>', `Expose via tunnel (${TunnelService.supportedProviders.join(', ')})`)
  .action(async (options) => {
    const watchDir = path.resolve(options.dir);

    if (!fs.existsSync(watchDir)) {
      console.error(`Directory not found: ${watchDir}`);
      process.exit(1);
    }

    const port = parseInt(options.port);
    let tunnel = null;

    console.log(`Starting ClawdView server...`);
    console.log(`Watching: ${watchDir}`);
    console.log(`Port: ${port}`);

    const server = new ClawdViewServer({
      port: port,
      watchDir: watchDir,
      autoOpen: options.open,
      host: options.tunnel ? '0.0.0.0' : 'localhost'
    });

    server.start();

    if (options.tunnel) {
      const provider = options.tunnel.toLowerCase();
      if (!TunnelService.supportedProviders.includes(provider)) {
        console.error(`Unknown tunnel provider: "${options.tunnel}"`);
        console.error(`Supported providers: ${TunnelService.supportedProviders.join(', ')}`);
        server.stop();
        process.exit(1);
      }

      tunnel = new TunnelService({ provider, port });
      console.log(`Starting ${provider} tunnel...`);

      try {
        const url = await tunnel.start();
        console.log(`Remote URL: ${url}`);
        console.log(`Share this URL to access ClawdView remotely.`);
        console.log('');
      } catch (err) {
        console.error(`Failed to start tunnel: ${err.message}`);
        server.stop();
        process.exit(1);
      }
    }

    process.on('SIGINT', async () => {
      console.log('\nShutting down ClawdView Server...');
      if (tunnel) {
        console.log('Closing tunnel...');
        await tunnel.stop();
      }
      server.stop();
      process.exit(0);
    });
  });

program
  .command('init')
  .description('Initialize ClawdView in current project')
  .action(() => {
    const currentDir = process.cwd();
    const packageJsonPath = path.join(currentDir, 'package.json');

    if (fs.existsSync(packageJsonPath)) {
      try {
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
        if (!packageJson.scripts) packageJson.scripts = {};
        packageJson.scripts.preview = 'clawdview start';
        packageJson.scripts['preview:port'] = 'clawdview start --port';
        fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
        console.log('Added ClawdView scripts to package.json');
      } catch (error) {
        console.error('Failed to update package.json:', error.message);
      }
    }

    const examples = {
      'clawdview-demo.html': `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ClawdView Demo</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }
        .demo-section { margin: 30px 0; padding: 20px; border: 2px solid #4ade80; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>ClawdView Demo</h1>
    <p>This is a demo HTML file to test ClawdView!</p>
    <div class="demo-section">
        <h2>Interactive Elements</h2>
        <button onclick="alert('ClawdView is working!')">Click me!</button>
        <input type="text" placeholder="Type something...">
    </div>
    <div class="demo-section">
        <h2>Dynamic Content</h2>
        <p id="time">Current time will appear here</p>
    </div>
    <script>
        setInterval(() => { document.getElementById('time').textContent = new Date().toLocaleTimeString(); }, 1000);
    </script>
</body>
</html>`,
      'clawdview-demo.py': `#!/usr/bin/env python3
import datetime, random

def main():
    print("ClawdView Python Demo")
    print("=" * 30)
    print(f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    data = [random.randint(1, 100) for _ in range(10)]
    print(f"Random data: {data}")
    print(f"Sum: {sum(data)}, Average: {sum(data)/len(data):.2f}")

if __name__ == "__main__":
    main()`,
    };

    let createdFiles = 0;
    Object.entries(examples).forEach(([filename, content]) => {
      const filePath = path.join(currentDir, filename);
      if (!fs.existsSync(filePath)) {
        fs.writeFileSync(filePath, content);
        console.log(`Created ${filename}`);
        createdFiles++;
      }
    });

    if (createdFiles > 0) {
      console.log(`\nClawdView initialized! Created ${createdFiles} demo files.`);
      console.log('Run "clawdview start" to begin previewing your files.');
    } else {
      console.log('ClawdView configuration updated.');
    }
  });

program
  .command('info')
  .description('Show ClawdView information and supported file types')
  .action(() => {
    console.log(`
ClawdView - Universal Rapid Prototyping Tool
=============================================

Supported File Types:
  HTML/CSS/JavaScript - Live preview with hot reload
  React Components (JSX) - Interactive component rendering
  Python Scripts - Execute and view output
  SVG Graphics - Vector graphics preview
  Markdown - Formatted text preview
  JSON/YAML - Formatted data display

Default server: http://localhost:3333

Quick Start:
  clawdview start                       # Start server locally
  clawdview start -p 4000               # Use custom port
  clawdview start --tunnel localtunnel  # Free tunnel
  clawdview init                        # Add demo files to project
    `);
  });

if (process.argv.length === 2) {
  program.outputHelp();
}

program.parse();
