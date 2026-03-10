# Ask Human Skill

Use the Lambda streaming approval system to ask the human for input using interactive forms.

## Usage

### Simple wrapper (recommended)

```bash
uv run --project /Users/andyhop/dev/protoflow python3 \
  /Users/andyhop/dev/protoflow/hmode/shared/tools/ask_human.py \
  --template <TEMPLATE> \
  --data '<JSON_DATA>' \
  --timeout 300
```

The URL will automatically open in Chrome. Use `--no-open` to disable.

### Direct usage (advanced)

```bash
uv run --project /Users/andyhop/dev/protoflow python3 \
  /Users/andyhop/dev/protoflow/projects/personal/lambda-streaming-approval/iot-core/cli/approval_iot.py \
  --url https://hwxtyo3untyxcpfshuvv6crlha0wikdr.lambda-url.us-east-1.on.aws \
  --template <TEMPLATE> \
  --data '<JSON_DATA>' \
  --timeout 300
```

## Templates

### 1. single-choice
Present a list of options, user selects one.

**Data format:**
```json
{
  "title": "Question title",
  "description": "Optional description",
  "options": [
    {"id": "1", "label": "Option 1", "description": "Optional description"},
    {"id": "2", "label": "Option 2", "description": "Optional description"}
  ]
}
```

**Response:** `{"selected": "1"}`

### 2. multi-choice
Present a list of options, user can select multiple.

**Data format:**
```json
{
  "title": "Select items",
  "description": "Optional description",
  "options": [
    {"id": "opt1", "label": "Option 1"},
    {"id": "opt2", "label": "Option 2"}
  ]
}
```

**Response:** `{"selected": ["opt1", "opt2"]}`

### 3. approve-deny
Simple approve/deny decision.

**Data format:**
```json
{
  "title": "Approve this action?",
  "description": "Optional description"
}
```

**Response:** `"approved"` or `"denied"`

### 4. rating
1-5 star rating.

**Data format:**
```json
{
  "title": "Rate this",
  "description": "Optional description",
  "max": 5
}
```

**Response:** `{"rating": 4}`

### 5. text-input
Free-form text input.

**Data format:**
```json
{
  "title": "Enter text",
  "description": "Optional description",
  "placeholder": "Type here..."
}
```

**Response:** `{"text": "user input"}`

### 6. compare-ab
Side-by-side comparison of two options.

**Data format:**
```json
{
  "title": "Which is better?",
  "optionA": {"label": "Option A", "description": "Description"},
  "optionB": {"label": "Option B", "description": "Description"}
}
```

**Response:** `{"selected": "a"}` or `{"selected": "b"}`

## Auto-open in Chrome

The script should automatically detect the URL from output and open it:

```python
import subprocess
import re

# Run the approval command and capture output
output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)

# Extract URL from output
url_match = re.search(r'url:\s+(https://[^\s]+)', output)
if url_match:
    url = url_match.group(1)
    subprocess.run(['open', '-a', 'Google Chrome', url])
```

## Example: Tic-Tac-Toe

```bash
uv run --project /Users/andyhop/dev/protoflow python3 \
  /Users/andyhop/dev/protoflow/hmode/shared/tools/ask_human.py \
  --template single-choice \
  --data '{
    "title": "Tic-Tac-Toe - Your Turn (X)",
    "description": "Board:\n  |   |  \n---------\n  |   |  \n---------\n  |   |  ",
    "options": [
      {"id": "1", "label": "Position 1", "description": "Top-left"},
      {"id": "5", "label": "Position 5", "description": "Center"},
      {"id": "9", "label": "Position 9", "description": "Bottom-right"}
    ]
  }' \
  --timeout 300
```

## Python API

```python
from shared.tools.ask_human import ask_human

# Simple approval
result = ask_human("approve-deny", {
    "title": "Deploy to production?",
    "description": "This will deploy v2.0.0 to prod"
})
# Returns: "approved" or "denied"

# Single choice
result = ask_human("single-choice", {
    "title": "Select environment",
    "options": [
        {"id": "dev", "label": "Development"},
        {"id": "staging", "label": "Staging"},
        {"id": "prod", "label": "Production"}
    ]
})
# Returns: {"selected": "dev"}
```
