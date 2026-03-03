# 🚀 ClawdView - Universal Rapid Prototyping Tool

A powerful, universal rapid prototyping tool for Mac that provides instant preview and execution of code files with live reload capabilities.

## ✨ Features

- **🌐 HTML/CSS/JavaScript** - Live preview with hot reload
- **⚛️ React Components (JSX)** - Interactive component rendering with Babel transpilation
- **🐍 Python Scripts** - Execute and view output in real-time
- **🎨 SVG Graphics** - Vector graphics preview
- **📝 Markdown** - Formatted text preview
- **📊 JSON/YAML** - Formatted data display
- **🔍 File Tree Navigation** - Browse and select files easily
- **🔄 Hot Reload** - Automatic refresh when files change
- **📱 Responsive Interface** - Works on all screen sizes

## 🛠️ Installation

```bash
# Install dependencies
cd ~/clawdview-tool
npm install

# Install globally for easy access
npm run install-global

# Or link for development
npm link
```

## 🚀 Usage

### Basic Commands

```bash
# Start server in current directory
clawdview start

# Use custom port
clawdview start --port 4000

# Watch specific directory
clawdview start --dir /path/to/project

# Don't auto-open browser
clawdview start --no-open

# Initialize demo files in current project
clawdview init

# Show information and supported formats
clawdview info
```

### Using in Your Projects

```bash
# Navigate to your project
cd /path/to/your/project

# Start ClawdView
clawdview start

# Browser will open to http://localhost:3333
```

## 🖥️ Interface Overview

### Main Interface
- **Sidebar**: File tree navigation with file type icons
- **Preview Tab**: Live preview of your content
- **Code Tab**: Syntax-highlighted source code
- **Output Tab**: Python script execution results

### Supported File Types
- `.html` - Rendered in iframe with full interactivity
- `.jsx` - React components with live rendering
- `.py` - Python scripts with execution capability
- `.svg` - Scalable vector graphics
- `.md` - Markdown with basic formatting
- `.json` - Pretty-printed JSON data
- `.css`, `.js` - Syntax-highlighted code view

## 🔧 Features in Detail

### HTML/CSS/JavaScript Preview
- Full interactive preview in iframe
- Live reload when files change
- External link button to open in new tab

### React Component Rendering
- Babel transpilation for JSX
- Live component rendering
- Error handling and display
- Support for React hooks and state

### Python Script Execution
- Execute Python scripts with a click
- View output and errors in real-time
- Secure execution in temporary files
- Support for matplotlib, numpy, etc.

### File Watching
- Automatic detection of file changes
- Real-time updates without page refresh
- Support for new file creation and deletion

## 📝 Example Files

When you run `clawdview init`, it creates example files:

- `clawdview-demo.html` - Interactive HTML demo
- `clawdview-demo.py` - Python script with calculations
- `clawdview-demo.jsx` - React component with state

## 🔧 Configuration

ClawdView runs with sensible defaults, but you can customize:

```javascript
// Programmatic usage
const ClawdViewServer = require('clawdview-tool');

const server = new ClawdViewServer({
  port: 3333,
  watchDir: '/path/to/project',
  autoOpen: true
});

server.start();
```

## 🛡️ Security

- Python scripts run in isolated temporary files
- No persistent file modifications
- Secure iframe sandboxing for HTML content
- Local-only server (not exposed to network)

## 🚨 Troubleshooting

### Port Already in Use
```bash
clawdview start --port 4000
```

### Python Scripts Not Running
- Ensure Python 3 is installed: `python3 --version`
- Check if script has syntax errors in Code tab

### React Components Not Rendering
- Ensure JSX syntax is valid
- Check browser console for errors
- Component must be exported properly

## 🤝 Contributing

This is a personal tool, but feel free to fork and modify for your needs.

## 📄 License

MIT License - see LICENSE file for details.

---

**Made with ❤️ for rapid prototyping and development**