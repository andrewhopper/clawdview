#!/usr/bin/env node

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const ClawdViewServer = require('../server');

const program = new Command();

program
  .name('clawdview')
  .description('Universal rapid prototyping tool for instant code preview')
  .version('1.0.0');

program
  .command('start')
  .description('Start ClawdView server in current directory')
  .option('-p, --port <port>', 'Server port', '3333')
  .option('-d, --dir <directory>', 'Directory to watch', process.cwd())
  .option('--no-open', 'Don\'t auto-open browser')
  .action((options) => {
    const watchDir = path.resolve(options.dir);

    if (!fs.existsSync(watchDir)) {
      console.error(`❌ Directory not found: ${watchDir}`);
      process.exit(1);
    }

    console.log(`🚀 Starting ClawdView server...`);
    console.log(`📁 Watching: ${watchDir}`);
    console.log(`🌐 Port: ${options.port}`);

    const server = new ClawdViewServer({
      port: parseInt(options.port),
      watchDir: watchDir,
      autoOpen: options.open
    });

    server.start();

    // Graceful shutdown
    process.on('SIGINT', () => {
      console.log('\n🛑 Shutting down ClawdView Server...');
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

    // Check if package.json exists
    if (fs.existsSync(packageJsonPath)) {
      try {
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

        // Add clawdview scripts
        if (!packageJson.scripts) {
          packageJson.scripts = {};
        }

        packageJson.scripts.preview = 'clawdview start';
        packageJson.scripts['preview:port'] = 'clawdview start --port';

        fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
        console.log('✅ Added ClawdView scripts to package.json');
      } catch (error) {
        console.error('❌ Failed to update package.json:', error.message);
      }
    }

    // Create example files
    const examples = {
      'clawdview-demo.html': `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ClawdView Demo</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
        }
        .demo-section {
            margin: 30px 0;
            padding: 20px;
            border: 2px solid #4ade80;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <h1>🚀 ClawdView Demo</h1>
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
        setInterval(() => {
            document.getElementById('time').textContent = new Date().toLocaleTimeString();
        }, 1000);
    </script>
</body>
</html>`,

      'clawdview-demo.py': `#!/usr/bin/env python3

import datetime
import random
import matplotlib.pyplot as plt

def main():
    print("🐍 ClawdView Python Demo")
    print("=" * 30)

    # Current time
    now = datetime.datetime.now()
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # Random data
    data = [random.randint(1, 100) for _ in range(10)]
    print(f"Random data: {data}")
    print(f"Sum: {sum(data)}")
    print(f"Average: {sum(data) / len(data):.2f}")

    # Simple calculation
    result = sum(i**2 for i in range(1, 11))
    print(f"Sum of squares 1-10: {result}")

if __name__ == "__main__":
    main()`,

      'clawdview-demo.jsx': `function ClawdViewDemo() {
    const [count, setCount] = React.useState(0);
    const [message, setMessage] = React.useState('Hello ClawdView!');

    return (
        <div style={{
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            maxWidth: '600px',
            margin: '40px auto',
            padding: '20px',
            textAlign: 'center'
        }}>
            <h1>⚛️ React Demo in ClawdView</h1>

            <div style={{
                background: '#f0f9ff',
                border: '2px solid #0ea5e9',
                borderRadius: '8px',
                padding: '20px',
                margin: '20px 0'
            }}>
                <h2>Interactive Counter</h2>
                <p style={{ fontSize: '24px', margin: '10px 0' }}>Count: {count}</p>
                <button
                    onClick={() => setCount(count + 1)}
                    style={{
                        background: '#0ea5e9',
                        color: 'white',
                        border: 'none',
                        padding: '10px 20px',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        margin: '0 5px'
                    }}
                >
                    Increment
                </button>
                <button
                    onClick={() => setCount(count - 1)}
                    style={{
                        background: '#ef4444',
                        color: 'white',
                        border: 'none',
                        padding: '10px 20px',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        margin: '0 5px'
                    }}
                >
                    Decrement
                </button>
            </div>

            <div style={{
                background: '#f0fdf4',
                border: '2px solid #22c55e',
                borderRadius: '8px',
                padding: '20px',
                margin: '20px 0'
            }}>
                <h2>Dynamic Message</h2>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    style={{
                        padding: '8px 12px',
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                        width: '300px',
                        marginBottom: '10px'
                    }}
                />
                <p style={{ fontSize: '18px', color: '#22c55e' }}>{message}</p>
            </div>
        </div>
    );
}`
    };

    let createdFiles = 0;
    Object.entries(examples).forEach(([filename, content]) => {
      const filePath = path.join(currentDir, filename);
      if (!fs.existsSync(filePath)) {
        fs.writeFileSync(filePath, content);
        console.log(`✅ Created ${filename}`);
        createdFiles++;
      }
    });

    if (createdFiles > 0) {
      console.log(`\n🎉 ClawdView initialized! Created ${createdFiles} demo files.`);
      console.log('Run "clawdview start" to begin previewing your files.');
    } else {
      console.log('✅ ClawdView configuration updated.');
    }
  });

program
  .command('info')
  .description('Show ClawdView information and supported file types')
  .action(() => {
    console.log(`
🚀 ClawdView - Universal Rapid Prototyping Tool
═══════════════════════════════════════════════

📋 Supported File Types:
  🌐 HTML/CSS/JavaScript - Live preview with hot reload
  ⚛️  React Components (JSX) - Interactive component rendering
  🐍 Python Scripts - Execute and view output
  🎨 SVG Graphics - Vector graphics preview
  📝 Markdown - Formatted text preview
  📊 JSON/YAML - Formatted data display

🛠️  Features:
  • Real-time file watching and hot reload
  • Interactive web-based interface
  • Code execution (Python)
  • Multi-tab layout (Preview, Code, Output)
  • File tree navigation
  • Responsive design

🌐 Default server: http://localhost:3333
📁 Watches current directory by default

💡 Quick Start:
  clawdview start          # Start server in current directory
  clawdview start -p 4000  # Use custom port
  clawdview init           # Add demo files to project
    `);
  });

// Show help if no command provided
if (process.argv.length === 2) {
  program.outputHelp();
}

program.parse();
