# HTTP Tunnel Command

Expose a local port via HTTP tunnel for web preview.

## Arguments

- `$ARGUMENTS` - Port number to expose (required)

## Execution

You are activating the HTTP tunnel skill to expose a local port.

**Port to expose:** $ARGUMENTS

### Steps to Execute:

1. **Check if a server is running on the port**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$ARGUMENTS || echo "not running"
   ```

2. **If no server running, ask user what to serve** or start a simple HTTP server:
   ```bash
   python -m http.server $ARGUMENTS &
   ```

3. **Start the tunnel client**
   ```bash
   python /home/user/protoflow/projects/unspecified/active/docker-port-tunnel-dqbax/tunnel_client.py \
     --relay ${TUNNEL_RELAY_URL} \
     --port $ARGUMENTS
   ```

4. **Return the public URL** to the user so they can open it in their browser.

### Important Notes:

- If `TUNNEL_RELAY_URL` is not set, inform the user they need to deploy a relay first:
  ```bash
  cd /home/user/protoflow/projects/unspecified/active/docker-port-tunnel-dqbax
  python deploy_lambda.py deploy --region us-east-1
  ```

- The tunnel runs in the foreground. Use `&` to background it if needed.

- To stop: `pkill -f tunnel_client.py`

### Example Usage:

```
/tunnel 3000     # Expose port 3000
/tunnel 8080     # Expose port 8080
```
