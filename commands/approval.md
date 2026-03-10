# Human Approval Request

Request human approval via IoT Core. AI generates custom HTML form.

## Two-Step Pattern

**Step 1: Start** (POST form HTML, return URL)
```bash
cd /home/user/protoflow/projects/personal/lambda-streaming-approval/iot-core && uv run python cli/approval_iot.py --url "https://humando.b.lfg.new/" --message "$ARGUMENTS" --innerHTML '<YOUR_HTML>' --start
```

**Step 2: Wait** (subscribe to IoT, block until response)
```bash
cd /home/user/protoflow/projects/personal/lambda-streaming-approval/iot-core && uv run python cli/approval_iot.py --url "https://humando.b.lfg.new/" --wait SESSION_ID --timeout 300
```

## HTML Guidelines

Generate mobile-optimized HTML. Call `decide('value')` to submit.

**Single-select (tap to submit immediately):**
```html
<button style="background:#10b981;color:white;padding:14px 32px;border:none;border-radius:8px;font-size:16px;margin:8px;" onclick="decide('yes')">Yes</button>
<button style="background:#ef4444;color:white;padding:14px 32px;border:none;border-radius:8px;font-size:16px;margin:8px;" onclick="decide('no')">No</button>
```

**Text input:**
```html
<input type="text" id="val" style="width:100%;padding:12px;border:2px solid #e2e8f0;border-radius:8px;font-size:16px;margin-bottom:12px;">
<button style="width:100%;background:#3b82f6;color:white;padding:14px;border:none;border-radius:8px;font-size:16px;" onclick="decide(document.getElementById('val').value)">Submit</button>
```

**Multi-select (needs submit button):**
```html
<label style="display:block;padding:12px;border:2px solid #e2e8f0;border-radius:8px;margin:8px 0;cursor:pointer;">
  <input type="checkbox" name="c" value="A" style="margin-right:12px;">Option A
</label>
<label style="display:block;padding:12px;border:2px solid #e2e8f0;border-radius:8px;margin:8px 0;cursor:pointer;">
  <input type="checkbox" name="c" value="B" style="margin-right:12px;">Option B
</label>
<button style="width:100%;background:#3b82f6;color:white;padding:14px;border:none;border-radius:8px;font-size:16px;margin-top:12px;" onclick="decide([...document.querySelectorAll('input[name=c]:checked')].map(x=>x.value).join(','))">Submit</button>
```

## Output

**--start:** `session:abc123` + `url:https://...`
**--wait:** `subscribed` then `<value>`

Exit 0 = response, Exit 1 = timeout/error
