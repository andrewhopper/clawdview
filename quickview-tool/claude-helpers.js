#!/usr/bin/env node

/**
 * Claude CLI Helper Functions for ClawdView Integration
 * Add these patterns to your Claude Code workflow
 */

const fs = require('fs');
const path = require('path');

class ClaudeClawdViewHelper {
    constructor(baseDir = process.cwd()) {
        this.baseDir = baseDir;
        this.artifactDir = path.join(baseDir, 'artifacts');
        this.ensureDirectories();
    }

    ensureDirectories() {
        const dirs = [
            this.artifactDir,
            path.join(this.artifactDir, 'components'),
            path.join(this.artifactDir, 'pages'),
            path.join(this.artifactDir, 'scripts'),
            path.join(this.artifactDir, 'styles'),
            path.join(this.artifactDir, 'data')
        ];
        
        dirs.forEach(dir => {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
        });
    }

    generateArtifactName(type, name, includeTimestamp = true) {
        const timestamp = includeTimestamp ? '-' + new Date().toISOString().slice(0, 16).replace(/[:-]/g, '') : '';
        const extensions = {
            html: '.html',
            react: '.jsx', 
            component: '.jsx',
            python: '.py',
            script: '.py',
            style: '.css',
            css: '.css',
            data: '.json',
            json: '.json'
        };

        const prefix = type === 'react' || type === 'component' ? 'component' : 
                      type === 'python' || type === 'script' ? 'script' :
                      type === 'style' || type === 'css' ? 'style' :
                      type === 'data' || type === 'json' ? 'data' :
                      'artifact';

        return `${prefix}-${name}${timestamp}${extensions[type] || '.html'}`;
    }

    getArtifactPath(filename) {
        const subDirs = {
            'component-': 'components',
            'artifact-': 'pages',
            'script-': 'scripts', 
            'style-': 'styles',
            'data-': 'data'
        };

        const subDir = Object.keys(subDirs).find(prefix => filename.startsWith(prefix));
        const targetDir = subDir ? path.join(this.artifactDir, subDirs[subDir]) : this.artifactDir;
        
        return path.join(targetDir, filename);
    }

    createArtifact(type, name, content, options = {}) {
        const filename = this.generateArtifactName(type, name, options.timestamp !== false);
        const filepath = this.getArtifactPath(filename);
        
        try {
            fs.writeFileSync(filepath, content, 'utf8');
            console.log(`✅ Created artifact: ${path.relative(this.baseDir, filepath)}`);
            
            if (options.openClawdView !== false) {
                console.log(`🔗 View at: http://localhost:3333`);
            }
            
            return {
                filename,
                filepath,
                relativePath: path.relative(this.baseDir, filepath),
                url: `http://localhost:3333`
            };
        } catch (error) {
            console.error(`❌ Failed to create artifact: ${error.message}`);
            return null;
        }
    }

    createReactComponent(name, componentCode, options = {}) {
        const demoHtml = options.createDemo !== false ? this.generateReactDemo(name, componentCode) : null;
        
        const component = this.createArtifact('react', name, componentCode, options);
        
        if (demoHtml && component) {
            const demoName = `${name}-demo`;
            const demo = this.createArtifact('html', demoName, demoHtml, { 
                ...options, 
                timestamp: false 
            });
            
            console.log(`🎭 React component with demo created`);
            return { component, demo };
        }
        
        return { component };
    }

    generateReactDemo(componentName, componentCode) {
        const capitalizedName = componentName.charAt(0).toUpperCase() + componentName.slice(1);
        
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${capitalizedName} Demo</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .demo-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .demo-header {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        .demo-content {
            min-height: 200px;
        }
    </style>
</head>
<body>
    <div class="demo-container">
        <div class="demo-header">
            <h1>🎭 ${capitalizedName} Component Demo</h1>
            <p>Live preview of the ${capitalizedName} React component</p>
        </div>
        <div class="demo-content">
            <div id="react-root"></div>
        </div>
    </div>

    <script type="text/babel">
        ${componentCode}
        
        // Try to find and render the component
        const componentName = '${capitalizedName}';
        const Component = window[componentName];
        
        if (Component) {
            ReactDOM.render(React.createElement(Component), document.getElementById('react-root'));
        } else {
            document.getElementById('react-root').innerHTML = 
                '<div style="color: #ef4444;">Component not found. Make sure to export it as: <code>window.${capitalizedName} = ${capitalizedName}</code></div>';
        }
    </script>
</body>
</html>`;
    }

    listArtifacts() {
        const artifacts = [];
        
        const scanDir = (dir, category = '') => {
            if (!fs.existsSync(dir)) return;
            
            fs.readdirSync(dir).forEach(file => {
                const fullPath = path.join(dir, file);
                const stat = fs.statSync(fullPath);
                
                if (stat.isFile() && (
                    file.startsWith('artifact-') || 
                    file.startsWith('component-') || 
                    file.startsWith('script-') ||
                    file.startsWith('style-') ||
                    file.startsWith('data-')
                )) {
                    artifacts.push({
                        name: file,
                        path: fullPath,
                        relativePath: path.relative(this.baseDir, fullPath),
                        category: category || 'general',
                        modified: stat.mtime,
                        size: stat.size
                    });
                }
            });
        };

        scanDir(this.artifactDir);
        scanDir(path.join(this.artifactDir, 'components'), 'components');
        scanDir(path.join(this.artifactDir, 'pages'), 'pages');
        scanDir(path.join(this.artifactDir, 'scripts'), 'scripts');
        scanDir(path.join(this.artifactDir, 'styles'), 'styles');
        scanDir(path.join(this.artifactDir, 'data'), 'data');

        return artifacts.sort((a, b) => b.modified - a.modified);
    }

    cleanup(olderThanDays = 7) {
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - olderThanDays);
        
        const artifacts = this.listArtifacts();
        let cleanedCount = 0;
        
        artifacts.forEach(artifact => {
            if (artifact.modified < cutoffDate) {
                try {
                    fs.unlinkSync(artifact.path);
                    console.log(`🗑️  Cleaned: ${artifact.relativePath}`);
                    cleanedCount++;
                } catch (error) {
                    console.error(`❌ Failed to clean: ${artifact.relativePath}`);
                }
            }
        });
        
        console.log(`🧹 Cleaned ${cleanedCount} old artifacts`);
    }

    getClawdViewStatus() {
        const http = require('http');
        
        return new Promise((resolve) => {
            const req = http.get('http://localhost:3333', (res) => {
                resolve({
                    running: true,
                    status: res.statusCode,
                    url: 'http://localhost:3333'
                });
            });
            
            req.on('error', () => {
                resolve({
                    running: false,
                    message: 'ClawdView not running. Start with: clawdview start'
                });
            });
            
            req.setTimeout(1000, () => {
                req.destroy();
                resolve({
                    running: false,
                    message: 'ClawdView not responding'
                });
            });
        });
    }
}

// CLI interface
if (require.main === module) {
    const helper = new ClaudeClawdViewHelper();
    const command = process.argv[2];
    
    switch (command) {
        case 'list':
            console.log('📋 ClawdView Artifacts:');
            const artifacts = helper.listArtifacts();
            artifacts.forEach(artifact => {
                console.log(`  ${artifact.relativePath} (${artifact.category})`);
            });
            break;
            
        case 'cleanup':
            const days = parseInt(process.argv[3]) || 7;
            helper.cleanup(days);
            break;
            
        case 'status':
            helper.getClawdViewStatus().then(status => {
                if (status.running) {
                    console.log(`✅ ClawdView running at ${status.url}`);
                } else {
                    console.log(`❌ ${status.message}`);
                }
            });
            break;
            
        case 'demo':
            // Create demo React component
            const demoComponent = `function DemoCounter() {
    const [count, setCount] = React.useState(0);
    
    return React.createElement('div', {
        style: { textAlign: 'center', padding: '20px' }
    }, [
        React.createElement('h2', { key: 'title' }, 'Demo Counter'),
        React.createElement('p', { key: 'count', style: { fontSize: '24px', margin: '20px 0' } }, 'Count: ' + count),
        React.createElement('button', {
            key: 'inc',
            onClick: () => setCount(count + 1),
            style: { margin: '0 10px', padding: '10px 20px', fontSize: '16px' }
        }, '+1'),
        React.createElement('button', {
            key: 'dec', 
            onClick: () => setCount(count - 1),
            style: { margin: '0 10px', padding: '10px 20px', fontSize: '16px' }
        }, '-1')
    ]);
}

window.DemoCounter = DemoCounter;`;
            
            helper.createReactComponent('demo-counter', demoComponent);
            break;
            
        default:
            console.log(`
🤖 Claude ClawdView Helper

Usage:
  node claude-helpers.js list     # List all artifacts
  node claude-helpers.js cleanup  # Clean old artifacts (7+ days)  
  node claude-helpers.js status   # Check ClawdView status
  node claude-helpers.js demo     # Create demo React component

Programmatic usage:
  const helper = require('./claude-helpers');
  helper.createArtifact('html', 'my-page', '<html>...</html>');
  helper.createReactComponent('my-button', 'function MyButton() {...}');
            `);
    }
}

module.exports = ClaudeClawdViewHelper;