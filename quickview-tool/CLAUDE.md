# 🤖 Claude Code Integration for QuickView

This file contains instructions for using QuickView with Claude Code for rapid artifact prototyping.

## Quick Start

**1. Start QuickView in any project:**
```bash
cd /your/project/directory
quickview start
# Browser opens to http://localhost:3333
```

**2. Claude creates artifacts using standard Write commands:**
```bash
Write artifact-dashboard.html [content]     # → Live HTML preview
Write component-button.jsx [content]        # → Interactive React component
Write script-data-viz.py [content]          # → Python script execution
```

**3. Files auto-appear in QuickView** with live preview and hot reload!

## 📁 Naming Conventions for Claude

Use these prefixes for automatic organization and preview:

```bash
# HTML artifacts (live preview in iframe)
artifact-[name].html
# Examples: artifact-landing-page.html, artifact-dashboard.html

# React components (live JSX rendering)  
component-[name].jsx
# Examples: component-todo-list.jsx, component-user-card.jsx

# Python scripts (executable with output panel)
script-[name].py  
# Examples: script-data-analysis.py, script-web-scraper.py

# CSS styles (syntax highlighted)
style-[name].css
# Examples: style-dark-theme.css, style-animations.css

# JSON data (formatted display)
data-[name].json
# Examples: data-users.json, data-config.json

# SVG graphics (rendered preview)
graphic-[name].svg
# Examples: graphic-logo.svg, graphic-chart.svg

# Markdown docs (formatted preview)
doc-[name].md
# Examples: doc-api-reference.md, doc-user-guide.md

# Slidev presentations (interactive slide viewer)
slides-[name].md
# Examples: slides-intro.md, slides-product-demo.md
```

## 🔧 Claude Commands for QuickView

### Creating Single Artifacts
```bash
# HTML page with interactivity
Write artifact-contact-form.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact Form</title>
    <style>
        body { font-family: system-ui; max-width: 500px; margin: 40px auto; }
        .form-group { margin: 15px 0; }
        input, textarea { width: 100%; padding: 8px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; }
    </style>
</head>
<body>
    <h1>Contact Us</h1>
    <form onsubmit="handleSubmit(event)">
        <div class="form-group">
            <label>Name:</label>
            <input type="text" id="name" required>
        </div>
        <div class="form-group">
            <label>Message:</label>
            <textarea id="message" rows="4" required></textarea>
        </div>
        <button type="submit">Send Message</button>
    </form>
    
    <script>
        function handleSubmit(e) {
            e.preventDefault();
            alert(`Thanks ${document.getElementById('name').value}! Message received.`);
        }
    </script>
</body>
</html>
```

### React Component Creation
```bash
# Interactive React component
Write component-counter.jsx
```javascript
function Counter() {
    const [count, setCount] = React.useState(0);
    const [step, setStep] = React.useState(1);
    
    return React.createElement('div', {
        style: { 
            textAlign: 'center', 
            padding: '20px',
            fontFamily: 'system-ui'
        }
    }, [
        React.createElement('h2', { key: 'title' }, '🔢 Interactive Counter'),
        React.createElement('div', { 
            key: 'display',
            style: { fontSize: '48px', margin: '20px 0', color: '#007bff' }
        }, count),
        React.createElement('div', { key: 'controls' }, [
            React.createElement('button', {
                key: 'dec',
                onClick: () => setCount(count - step),
                style: { margin: '5px', padding: '10px 15px', fontSize: '16px' }
            }, `-${step}`),
            React.createElement('button', {
                key: 'inc', 
                onClick: () => setCount(count + step),
                style: { margin: '5px', padding: '10px 15px', fontSize: '16px' }
            }, `+${step}`),
            React.createElement('button', {
                key: 'reset',
                onClick: () => setCount(0),
                style: { margin: '5px', padding: '10px 15px', fontSize: '16px' }
            }, 'Reset')
        ]),
        React.createElement('div', { key: 'step-control', style: { marginTop: '20px' } }, [
            React.createElement('label', { key: 'label' }, 'Step: '),
            React.createElement('input', {
                key: 'input',
                type: 'number',
                value: step,
                onChange: (e) => setStep(parseInt(e.target.value) || 1),
                style: { width: '60px', marginLeft: '10px' }
            })
        ])
    ]);
}

// Export for QuickView
window.Counter = Counter;
```

# Create demo page for React component
Write artifact-counter-demo.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Counter Demo</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
    <div id="root"></div>
    <script src="./component-counter.jsx"></script>
    <script>
        ReactDOM.render(React.createElement(Counter), document.getElementById('root'));
    </script>
</body>
</html>
```

### Python Script Execution
```bash
# Data analysis script
Write script-sales-analysis.py
```python
#!/usr/bin/env python3

import json
import datetime
from collections import defaultdict
import random

def generate_sample_data():
    """Generate sample sales data for demonstration"""
    products = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Monitor']
    data = []
    
    for i in range(100):
        sale = {
            'id': i + 1,
            'date': (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'product': random.choice(products),
            'amount': round(random.uniform(50, 2000), 2),
            'quantity': random.randint(1, 5),
            'region': random.choice(['North', 'South', 'East', 'West'])
        }
        data.append(sale)
    
    return data

def analyze_sales(data):
    """Analyze sales data and return insights"""
    total_revenue = sum(sale['amount'] for sale in data)
    total_quantity = sum(sale['quantity'] for sale in data)
    
    # Revenue by product
    product_revenue = defaultdict(float)
    for sale in data:
        product_revenue[sale['product']] += sale['amount']
    
    # Revenue by region
    region_revenue = defaultdict(float)
    for sale in data:
        region_revenue[sale['region']] += sale['amount']
    
    # Monthly trends (simplified)
    monthly_revenue = defaultdict(float)
    for sale in data:
        month = sale['date'][:7]  # YYYY-MM
        monthly_revenue[month] += sale['amount']
    
    return {
        'total_revenue': total_revenue,
        'total_quantity': total_quantity,
        'avg_order_value': total_revenue / len(data),
        'product_revenue': dict(product_revenue),
        'region_revenue': dict(region_revenue),
        'monthly_revenue': dict(sorted(monthly_revenue.items()))
    }

def print_report(analysis):
    """Print formatted analysis report"""
    print("📊 SALES ANALYSIS REPORT")
    print("=" * 50)
    print(f"💰 Total Revenue: ${analysis['total_revenue']:,.2f}")
    print(f"📦 Total Items Sold: {analysis['total_quantity']:,}")
    print(f"💵 Average Order Value: ${analysis['avg_order_value']:.2f}")
    
    print("\n🏆 TOP PRODUCTS BY REVENUE:")
    sorted_products = sorted(analysis['product_revenue'].items(), key=lambda x: x[1], reverse=True)
    for product, revenue in sorted_products:
        print(f"  {product}: ${revenue:,.2f}")
    
    print("\n🗺️  REVENUE BY REGION:")
    sorted_regions = sorted(analysis['region_revenue'].items(), key=lambda x: x[1], reverse=True)
    for region, revenue in sorted_regions:
        print(f"  {region}: ${revenue:,.2f}")
    
    print("\n📅 MONTHLY TRENDS (Last 6 months):")
    monthly_items = list(analysis['monthly_revenue'].items())[-6:]
    for month, revenue in monthly_items:
        print(f"  {month}: ${revenue:,.2f}")

def main():
    print("🚀 Generating sample sales data...")
    data = generate_sample_data()
    
    print(f"✅ Generated {len(data)} sales records")
    
    print("\n🔍 Analyzing data...")
    analysis = analyze_sales(data)
    
    print_report(analysis)
    
    # Save processed data
    with open('sales-analysis-output.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\n💾 Analysis saved to sales-analysis-output.json")
    print("🎉 Analysis complete!")

if __name__ == "__main__":
    main()
```

## 🔄 Live Editing Workflow

**Claude can iterate by editing existing files:**
```bash
# Update component with new features
Edit component-counter.jsx [enhanced-version-with-animations]

# Modify styles 
Edit style-dark-theme.css [updated-dark-mode-styles]

# Enhance HTML with new sections
Edit artifact-dashboard.html [add-charts-section]
```

**QuickView automatically:**
- ✅ Detects file changes
- ✅ Refreshes browser preview
- ✅ Maintains scroll position
- ✅ Preserves component state where possible

## 🎯 Multi-File Projects

**Create related files together:**
```bash
# 1. Create main component
Write component-todo-app.jsx [main-app-component]

# 2. Create individual components  
Write component-todo-item.jsx [individual-todo-component]
Write component-add-todo.jsx [add-todo-form-component]

# 3. Create styles
Write style-todo-app.css [app-styling]

# 4. Create demo page that combines everything
Write artifact-todo-demo.html [html-page-importing-all-components]

# 5. Create sample data
Write data-sample-todos.json [sample-todo-data]
```

## 🐍 Python Script Features

**QuickView provides:**
- **"Run" button** - Execute Python scripts with one click
- **Output panel** - View stdout/stderr in real-time  
- **Error handling** - Clear error messages and stack traces
- **File isolation** - Scripts run in temporary sandboxed environment

**Python script tips:**
```python
# Include informative prints
print("🔍 Starting data analysis...")
print(f"✅ Processed {len(data)} records")
print("💡 Tip: Check the generated output.json file")

# Use emoji and formatting for better UX
print("=" * 50)
print("📊 RESULTS:")
```

## 🎨 Advanced Features

### SVG Graphics
```bash
Write graphic-dashboard-chart.svg
```xml
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#4f46e5;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:1" />
        </linearGradient>
    </defs>
    
    <!-- Chart background -->
    <rect width="400" height="300" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    
    <!-- Chart title -->
    <text x="200" y="30" text-anchor="middle" font-family="system-ui" font-size="18" font-weight="bold" fill="#1e293b">Monthly Sales</text>
    
    <!-- Data bars -->
    <rect x="50" y="250" width="40" height="120" fill="url(#grad1)"/>
    <rect x="110" y="200" width="40" height="170" fill="url(#grad1)"/>
    <rect x="170" y="180" width="40" height="190" fill="url(#grad1)"/>
    <rect x="230" y="150" width="40" height="220" fill="url(#grad1)"/>
    <rect x="290" y="100" width="40" height="270" fill="url(#grad1)"/>
    
    <!-- Labels -->
    <text x="70" y="285" text-anchor="middle" font-size="12" fill="#64748b">Jan</text>
    <text x="130" y="285" text-anchor="middle" font-size="12" fill="#64748b">Feb</text>
    <text x="190" y="285" text-anchor="middle" font-size="12" fill="#64748b">Mar</text>
    <text x="250" y="285" text-anchor="middle" font-size="12" fill="#64748b">Apr</text>
    <text x="310" y="285" text-anchor="middle" font-size="12" fill="#64748b">May</text>
</svg>
```

### Markdown Documentation
```bash
Write doc-api-reference.md
```markdown
# 🚀 API Reference

## Overview
This API provides endpoints for managing user data and analytics.

## Authentication
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/users
```

## Endpoints

### GET /users
Retrieve all users.

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  ]
}
```

### POST /users
Create a new user.

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```
```

## 🚨 Troubleshooting

### QuickView not showing changes?
```bash
# Check if QuickView is running
curl -s http://localhost:3333 && echo "✅ Running" || echo "❌ Not running"

# Restart QuickView if needed
pkill -f quickview && quickview start
```

### Files not appearing in QuickView?
```bash
# Ensure you're in the right directory
pwd

# Check file naming conventions
ls artifact-* component-* script-* 2>/dev/null || echo "No artifacts found"
```

### Python scripts not executing?
```bash
# Verify Python installation
python3 --version

# Check script syntax
python3 -m py_compile script-your-file.py
```

## 💡 Pro Tips

1. **Use descriptive names**: `artifact-user-dashboard.html` vs `test.html`
2. **Create component demos**: Always pair React components with demo HTML
3. **Include sample data**: Add `data-*.json` files for components that need data
4. **Test interactivity**: Use console.log, alerts, and user interactions
5. **Iterate rapidly**: Edit files directly, QuickView handles the refresh

## 🛡️ Security & Safety Features

QuickView includes built-in safety measures for personal use:

### File Type Protection
- **Allowed file types**: `.html`, `.jsx`, `.js`, `.py`, `.css`, `.json`, `.md`, `.svg`, `.txt`, `.xml`, `.yaml`, `.yml`
- **Blocked types**: Executable files (`.exe`, `.sh`, `.bat`) are rejected for security
- **Hidden files**: System files like `.env`, `.ssh/` are protected from accidental access

### Python Execution Safety
- **Rate limiting**: Maximum 5 Python script executions per minute
- **Timeout protection**: Scripts automatically killed after 30 seconds
- **Size limits**: Python code limited to 50KB to prevent abuse
- **Temporary files**: Secure temp file handling with automatic cleanup

### Example Error Messages
```bash
# Trying to access hidden files
curl http://localhost:3333/api/file/.env
# Returns: "Access to hidden files denied"

# Trying to access blocked file types  
curl http://localhost:3333/api/file/malware.exe
# Returns: "File type not supported for security reasons"

# Executing too many Python scripts
# Returns: "Too many Python executions. Please wait a minute before trying again."
```

## 🎯 Real-World Usage Examples

### Example: AI Cultural Technology Visualization
```bash
# Claude creates elegant interactive visualization
Write artifact-ai-cultural-technology.html [complex-interactive-content]

# Result: Immediately viewable at http://localhost:3333
# Features: Animations, interactivity, responsive design
# No additional setup required!
```

### Example: Data Analysis Workflow  
```bash
# 1. Create Python analysis script
Write script-sales-analysis.py [data-processing-code]

# 2. Create sample data
Write data-sales-records.json [sample-dataset] 

# 3. Create visualization component
Write component-sales-chart.jsx [react-chart-component]

# 4. Create demo page combining everything
Write artifact-sales-dashboard.html [complete-dashboard]

# Result: Full interactive dashboard with live data processing!
```

## 🚀 Performance Notes

- **File watching**: Changes detected in <100ms
- **Hot reload**: Browser updates automatically on file saves  
- **Memory usage**: ~50MB typical usage
- **Startup time**: Server ready in <2 seconds
- **Concurrent users**: Designed for single-user (localhost only)

---

**This enables Claude Code to work seamlessly with QuickView for rapid prototyping!** 🎉

*Last updated: September 2025 - Includes security improvements and real-world testing*