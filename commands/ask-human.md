# Ask Human - Get Real-Time Human Feedback

Use this skill when you need human input, approval, or selection during a task.

## When to Use

- Need approval before proceeding (delete files, deploy, etc.)
- Need user to choose between options
- Need user to provide text input
- Need user to rate or rank items
- Need user to select from images or visual options

## Quick Start

```bash
# Set working directory
export HUMANDO_DIR="/home/user/protoflow/projects/personal/lambda-streaming-approval/iot-core"

# Step 1: Start (generates URL)
# URL is auto-detected: Lambda URL in Claude env, humando.b.lfg.new otherwise
cd $HUMANDO_DIR && uv run python cli/approval_iot.py \
  --start \
  --innerHTML '<YOUR_HTML_HERE>'

# Step 2: Parse output for session ID
# Output: [timestamp] session:abc123
#         [timestamp] url:https://...

# Step 3: Show URL to user (they open on phone)

# Step 4: Wait for response
cd $HUMANDO_DIR && uv run python cli/approval_iot.py \
  --wait SESSION_ID \
  --timeout 300
```

## HTML Templates

### Yes/No Approval
```html
<div style="display:flex;flex-direction:column;gap:16px;padding:20px;">
  <h2 style="color:#f1f5f9;margin:0;text-align:center;">TITLE_HERE</h2>
  <p style="color:#94a3b8;text-align:center;">DESCRIPTION_HERE</p>
  <button onclick="decide('approved')" style="background:#10b981;color:white;padding:16px;border:none;border-radius:12px;font-size:18px;font-weight:600;">Approve</button>
  <button onclick="decide('denied')" style="background:#ef4444;color:white;padding:16px;border:none;border-radius:12px;font-size:18px;font-weight:600;">Deny</button>
</div>
```

### Multiple Choice (Single Select)
```html
<div style="display:flex;flex-direction:column;gap:12px;padding:20px;">
  <h2 style="color:#f1f5f9;margin:0;">QUESTION_HERE</h2>
  <button onclick="decide('option1')" style="background:#1e293b;color:#f1f5f9;padding:16px;border:2px solid #334155;border-radius:12px;font-size:16px;text-align:left;">Option 1</button>
  <button onclick="decide('option2')" style="background:#1e293b;color:#f1f5f9;padding:16px;border:2px solid #334155;border-radius:12px;font-size:16px;text-align:left;">Option 2</button>
  <button onclick="decide('option3')" style="background:#1e293b;color:#f1f5f9;padding:16px;border:2px solid #334155;border-radius:12px;font-size:16px;text-align:left;">Option 3</button>
</div>
```

### Text Input
```html
<div style="display:flex;flex-direction:column;gap:16px;padding:20px;">
  <h2 style="color:#f1f5f9;margin:0;">PROMPT_HERE</h2>
  <input type="text" id="userInput" placeholder="Type here..." style="background:#1e293b;color:#f1f5f9;padding:16px;border:2px solid #334155;border-radius:12px;font-size:16px;">
  <button onclick="decide(document.getElementById('userInput').value)" style="background:#3b82f6;color:white;padding:16px;border:none;border-radius:12px;font-size:18px;font-weight:600;">Submit</button>
</div>
```

### Image Grid (Tap to Select)
```html
<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;padding:20px;">
  <div onclick="decide('item1')" style="cursor:pointer;border:3px solid transparent;border-radius:12px;overflow:hidden;">
    <img src="IMAGE_URL_1" style="width:100%;aspect-ratio:1;object-fit:cover;">
    <p style="color:#f1f5f9;text-align:center;padding:8px;margin:0;">Label 1</p>
  </div>
  <div onclick="decide('item2')" style="cursor:pointer;border:3px solid transparent;border-radius:12px;overflow:hidden;">
    <img src="IMAGE_URL_2" style="width:100%;aspect-ratio:1;object-fit:cover;">
    <p style="color:#f1f5f9;text-align:center;padding:8px;margin:0;">Label 2</p>
  </div>
</div>
```

### Star Rating (1-5)
```html
<div style="padding:20px;">
  <h2 style="color:#f1f5f9;margin:0 0 16px 0;">ITEM_NAME</h2>
  <div style="display:flex;gap:8px;justify-content:center;">
    <button onclick="decide('1')" style="background:none;border:none;font-size:32px;cursor:pointer;">⭐</button>
    <button onclick="decide('2')" style="background:none;border:none;font-size:32px;cursor:pointer;">⭐</button>
    <button onclick="decide('3')" style="background:none;border:none;font-size:32px;cursor:pointer;">⭐</button>
    <button onclick="decide('4')" style="background:none;border:none;font-size:32px;cursor:pointer;">⭐</button>
    <button onclick="decide('5')" style="background:none;border:none;font-size:32px;cursor:pointer;">⭐</button>
  </div>
</div>
```

### Time Slot Picker
```html
<div style="display:flex;flex-direction:column;gap:8px;padding:20px;">
  <h2 style="color:#f1f5f9;margin:0 0 12px 0;">Select a time</h2>
  <button onclick="decide('9:00 AM')" style="background:#1e293b;color:#f1f5f9;padding:14px;border:2px solid #334155;border-radius:8px;">9:00 AM</button>
  <button onclick="decide('10:00 AM')" style="background:#1e293b;color:#f1f5f9;padding:14px;border:2px solid #334155;border-radius:8px;">10:00 AM</button>
  <button onclick="decide('11:00 AM')" style="background:#1e293b;color:#f1f5f9;padding:14px;border:2px solid #334155;border-radius:8px;">11:00 AM</button>
  <button onclick="decide('2:00 PM')" style="background:#1e293b;color:#f1f5f9;padding:14px;border:2px solid #334155;border-radius:8px;">2:00 PM</button>
</div>
```

## Response Handling

The `--wait` command outputs the decision value directly:
- `approved` / `denied` for yes/no
- `option1`, `option2`, etc. for choices
- User's text for input fields
- `timeout` if no response within timeout period

Exit codes:
- `0` = valid response received
- `1` = timeout or error

## Multi-Page Review (Stream Mode)

For reviewing multiple pages of items (e.g., 5 pages of candidates), use `--stream` mode.
The CLI waits for multiple responses until it receives `done: true`.

### Stream Mode Usage

```bash
# Start session (same as single-page)
cd $HUMANDO_DIR && uv run python cli/approval_iot.py \
  --start \
  --innerHTML '<YOUR_PAGINATED_HTML>'

# Wait for multiple responses (stream mode)
cd $HUMANDO_DIR && uv run python cli/approval_iot.py \
  --wait SESSION_ID \
  --stream \
  --timeout 600

# Or collect all responses as JSON array at end
cd $HUMANDO_DIR && uv run python cli/approval_iot.py \
  --wait SESSION_ID \
  --stream \
  --aggregate
```

### Stream Output Formats

**Default (real-time):**
```
[page1] {"page": 1, "selected": ["item-a", "item-b"]}
[page2] {"page": 2, "selected": ["item-c"]}
[page3] {"page": 3, "selected": []}
[done] {"page": 4, "selected": ["item-x"], "done": true}
```

**Aggregate mode (`--aggregate`):**
```
[{"page":1,"selected":["item-a","item-b"]},{"page":2,"selected":["item-c"]},{"page":3,"selected":[]},{"page":4,"selected":["item-x"],"done":true}]
```

### Multi-Page HTML Template

```html
<div style="display:flex;flex-direction:column;gap:16px;padding:20px;">
  <h2 style="color:#f1f5f9;margin:0;">Review Items (Page <span id="pageNum">1</span> of 5)</h2>

  <!-- Item list with checkboxes -->
  <div id="items" style="display:flex;flex-direction:column;gap:8px;">
    <!-- Items injected here per page -->
  </div>

  <!-- Navigation -->
  <div style="display:flex;gap:12px;margin-top:16px;">
    <button id="nextBtn" onclick="submitPage(false)"
      style="flex:1;background:#3b82f6;color:white;padding:14px;border:none;border-radius:8px;font-size:16px;font-weight:600;">
      Next →
    </button>
    <button id="doneBtn" onclick="submitPage(true)" style="display:none;flex:1;background:#10b981;color:white;padding:14px;border:none;border-radius:8px;font-size:16px;font-weight:600;">
      Finish ✓
    </button>
  </div>

  <p style="color:#64748b;font-size:14px;text-align:center;">
    Select items to approve, then click Next
  </p>
</div>

<script>
  const TOTAL_PAGES = 5;
  let currentPage = 1;

  // Your page data (injected by AI)
  const pageData = {
    1: [{id: 'a', label: 'Item A'}, {id: 'b', label: 'Item B'}],
    2: [{id: 'c', label: 'Item C'}, {id: 'd', label: 'Item D'}],
    // ... etc
  };

  function renderPage(page) {
    const items = pageData[page] || [];
    document.getElementById('items').innerHTML = items.map(item => `
      <label style="display:flex;align-items:center;padding:12px;background:#1e293b;border-radius:8px;cursor:pointer;">
        <input type="checkbox" value="${item.id}" style="width:20px;height:20px;margin-right:12px;">
        <span style="color:#f1f5f9;">${item.label}</span>
      </label>
    `).join('');
    document.getElementById('pageNum').textContent = page;

    // Show Done button on last page
    if (page === TOTAL_PAGES) {
      document.getElementById('nextBtn').style.display = 'none';
      document.getElementById('doneBtn').style.display = 'block';
    }
  }

  function submitPage(isDone) {
    const selected = [...document.querySelectorAll('#items input:checked')].map(c => c.value);
    const payload = {
      page: currentPage,
      selected: selected
    };
    if (isDone) {
      payload.done = true;
    }

    decide(JSON.stringify(payload));

    if (!isDone && currentPage < TOTAL_PAGES) {
      currentPage++;
      renderPage(currentPage);
    }
  }

  // Initialize first page
  renderPage(1);
</script>
```

### Simple Multi-Page (Server-Rendered)

For simpler cases, generate separate HTML for each page and update via /setup:

```html
<!-- Page 1 of 3 -->
<div style="display:flex;flex-direction:column;gap:16px;padding:20px;">
  <h2 style="color:#f1f5f9;margin:0;">Review Batch 1/3</h2>
  <button onclick="decide(JSON.stringify({page:1, selected:['a','b']}))"
    style="background:#3b82f6;color:white;padding:16px;border:none;border-radius:12px;">
    Submit & Next →
  </button>
</div>

<!-- Page 3 of 3 (final) -->
<div style="display:flex;flex-direction:column;gap:16px;padding:20px;">
  <h2 style="color:#f1f5f9;margin:0;">Review Batch 3/3</h2>
  <button onclick="decide(JSON.stringify({page:3, selected:['x'], done:true}))"
    style="background:#10b981;color:white;padding:16px;border:none;border-radius:12px;">
    Finish ✓
  </button>
</div>
```

## Best Practices

1. **Keep forms simple** - One question per form
2. **Large tap targets** - Min 44px height for buttons
3. **High contrast** - Dark background (#0f172a), light text (#f1f5f9)
4. **Clear labels** - User should understand instantly
5. **Single primary action** - One obvious next step
6. **JSON for complex data** - Use `JSON.stringify()` for multi-field forms

## Example: Full Workflow

```bash
# 1. Start approval (URL auto-detected based on environment)
cd /home/user/protoflow/projects/personal/lambda-streaming-approval/iot-core && \
uv run python cli/approval_iot.py \
  --start \
  --innerHTML '<div style="display:flex;flex-direction:column;gap:16px;padding:20px;"><h2 style="color:#f1f5f9;margin:0;text-align:center;">Deploy to Production?</h2><p style="color:#94a3b8;text-align:center;">This will update the live site.</p><button onclick="decide(\"deploy\")" style="background:#10b981;color:white;padding:16px;border:none;border-radius:12px;font-size:18px;font-weight:600;">Deploy Now</button><button onclick="decide(\"cancel\")" style="background:#64748b;color:white;padding:16px;border:none;border-radius:12px;font-size:18px;">Cancel</button></div>'

# Output:
# [14:30:01.100] using auto-detected URL: https://hwxtyo3...lambda-url.us-east-1.on.aws
# [14:30:01.123] session:a1b2c3d4
# [14:30:01.456] url:https://...?session=a1b2c3d4&...

# 2. Tell user the URL (they open on mobile)

# 3. Wait for response
cd /home/user/protoflow/projects/personal/lambda-streaming-approval/iot-core && \
uv run python cli/approval_iot.py \
  --wait a1b2c3d4 \
  --timeout 300

# Output:
# [14:30:02.001] wait: starting for session a1b2c3d4
# [14:30:02.234] wait: MQTT connected
# [14:30:02.567] wait: subscribed, waiting for input...
# [14:30:15.123] wait: MQTT message received
# [14:30:15.234] wait: done, decision = deploy
```

## URL Auto-Detection

The CLI automatically selects the URL based on environment:

| Environment | URL Used |
|-------------|----------|
| Claude Code (HOME=/root) | Lambda Function URL (direct) |
| Production/Local | https://humando.b.lfg.new |

Override with `--url` if needed:
```bash
uv run python cli/approval_iot.py --url "https://custom.domain" --start --innerHTML '...'
```

## Timestamps

All output includes timestamps in `[HH:MM:SS.mmm]` format to help identify delays:
- IoT endpoint fetch (~200ms typical)
- MQTT connect (~300ms typical)
- Human response time (variable)
- Message propagation (~100ms typical)
