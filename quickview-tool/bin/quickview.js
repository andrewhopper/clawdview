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
let QuickViewServer, TunnelService;
try {
  ({ QuickViewServer } = require('../src/server/server'));
  ({ TunnelService } = require('../src/server/services/tunnel-service'));
} catch {
  ({ QuickViewServer } = require('../dist/server/server'));
  ({ TunnelService } = require('../dist/server/services/tunnel-service'));
}

const program = new Command();

program
  .name('quickview')
  .description('Universal rapid prototyping tool for instant code preview')
  .version('2.0.0');

program
  .command('start')
  .description('Start QuickView server in current directory')
  .option('-p, --port <port>', 'Server port', '3333')
  .option('-d, --dir <directory>', 'Directory to watch', process.cwd())
  .option('--no-open', 'Don\'t auto-open browser')
  .option('--s3-bucket <bucket>', 'S3 bucket for asset sharing')
  .option('--s3-region <region>', 'AWS region for S3', 'us-east-1')
  .option('--s3-prefix <prefix>', 'S3 key prefix for shared assets', 'quickview-shares')
  .option('--s3-endpoint <endpoint>', 'Custom S3 endpoint (for S3-compatible services)')
  .option('--project-name <name>', 'Project name for organizing S3 assets')
  .option('--tunnel <provider>', `Expose via tunnel (${TunnelService.supportedProviders.join(', ')})`)
  .action(async (options) => {
    const watchDir = path.resolve(options.dir);

    if (!fs.existsSync(watchDir)) {
      console.error(`Directory not found: ${watchDir}`);
      process.exit(1);
    }

    const port = parseInt(options.port);
    let tunnel = null;

    console.log(`Starting QuickView server...`);
    console.log(`Watching: ${watchDir}`);
    console.log(`Port: ${port}`);

    const s3Options = {};
    if (options.s3Bucket) s3Options.bucket = options.s3Bucket;
    if (options.s3Region) s3Options.region = options.s3Region;
    if (options.s3Prefix) s3Options.prefix = options.s3Prefix;
    if (options.s3Endpoint) s3Options.endpoint = options.s3Endpoint;
    if (options.projectName) s3Options.projectName = options.projectName;
    s3Options.projectName = s3Options.projectName || path.basename(watchDir);

    if (s3Options.bucket || process.env.QV_S3_BUCKET) {
      console.log(`S3 sharing: enabled (bucket: ${s3Options.bucket || process.env.QV_S3_BUCKET})`);
    }

    const server = new QuickViewServer({
      port: port,
      watchDir: watchDir,
      autoOpen: options.open,
      s3: s3Options,
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
        console.log(`Share this URL to access QuickView remotely.`);
        console.log('');
      } catch (err) {
        console.error(`Failed to start tunnel: ${err.message}`);
        server.stop();
        process.exit(1);
      }
    }

    process.on('SIGINT', async () => {
      console.log('\nShutting down QuickView Server...');
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
  .description('Initialize QuickView in current project')
  .action(() => {
    const currentDir = process.cwd();
    const packageJsonPath = path.join(currentDir, 'package.json');

    if (fs.existsSync(packageJsonPath)) {
      try {
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
        if (!packageJson.scripts) packageJson.scripts = {};
        packageJson.scripts.preview = 'quickview start';
        packageJson.scripts['preview:port'] = 'quickview start --port';
        fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
        console.log('Added QuickView scripts to package.json');
      } catch (error) {
        console.error('Failed to update package.json:', error.message);
      }
    }

    const examples = {
      'quickview-demo.html': `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuickView Demo</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }
        .demo-section { margin: 30px 0; padding: 20px; border: 2px solid #4ade80; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>QuickView Demo</h1>
    <p>This is a demo HTML file to test QuickView!</p>
    <div class="demo-section">
        <h2>Interactive Elements</h2>
        <button onclick="alert('QuickView is working!')">Click me!</button>
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
      'quickview-demo.py': `#!/usr/bin/env python3
import datetime, random

def main():
    print("QuickView Python Demo")
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
      console.log(`\nQuickView initialized! Created ${createdFiles} demo files.`);
      console.log('Run "quickview start" to begin previewing your files.');
    } else {
      console.log('QuickView configuration updated.');
    }
  });

program
  .command('info')
  .description('Show QuickView information and supported file types')
  .action(() => {
    console.log(`
QuickView - Universal Rapid Prototyping Tool
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
  quickview start                       # Start server locally
  quickview start -p 4000               # Use custom port
  quickview start --tunnel localtunnel  # Free tunnel
  quickview init                        # Add demo files to project
    `);
  });

if (process.argv.length === 2) {
  program.outputHelp();
}

program.parse();
