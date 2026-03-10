---
version: 1.1.0
last_updated: 2025-12-18
description: SSH tunnels and port forwarding for testing (local, remote, EC2+SSM strategies)
---

# Tunnel Testing

Guide for using SSH tunnels and port forwarding to test applications in restricted network environments.

## Usage

```bash
# Get help with tunnel strategies
/tunnel-testing

# Specific scenarios
/tunnel-testing local-forward    # Access remote service locally
/tunnel-testing remote-forward   # Expose local service remotely
/tunnel-testing socks-proxy      # Dynamic SOCKS proxy
/tunnel-testing ec2-ssm          # AWS EC2 + SSM strategy (no SSH needed)
```

---

## ⚠️ Claude Code Web - SSH NOT Available

**SSH tunnels do NOT work in Claude Code Web.** The environment has:

| Feature | Status | Reason |
|---------|--------|--------|
| SSH binary | ❌ Not installed | Cannot install (apt blocked) |
| Raw TCP sockets | ❌ Blocked | Proxy-only network |
| Python SSH (paramiko) | ❌ Won't work | Proxy blocks SSH protocol |
| SSH over port 443 | ❌ Won't work | Deep packet inspection allows only TLS |
| HTTPS requests | ✅ Works | Allowed through proxy |
| AWS APIs (SSM) | ✅ Works | Uses HTTPS |

**Recommended approach for Claude Code Web:** Use **EC2 + SSM** (see below).

### Environment Detection

```python
import os
import shutil

def detect_environment():
    """Detect if running in Claude Code Web"""
    # Check for SSH
    has_ssh = shutil.which('ssh') is not None

    # Check for Claude Code Web proxy
    proxy = os.environ.get('https_proxy', '')
    is_claude_web = 'claude_code_remote' in proxy or 'anthropic' in proxy

    if is_claude_web or not has_ssh:
        print("⚠️  Claude Code Web detected - use EC2+SSM for testing")
        return "claude-web"
    else:
        print("✅ SSH available - tunnels will work")
        return "local"
```

### Why Python SSH Libraries Don't Work

Even with `paramiko` installed, SSH won't work because:

1. HTTP CONNECT tunnel opens successfully (proxy returns `200 OK`)
2. Proxy does **deep packet inspection** on tunneled traffic
3. Only TLS-looking traffic is forwarded
4. SSH protocol banner (`SSH-2.0-...`) is silently dropped

```
You → Proxy → [DPI: Is this TLS?] → Yes: Forward / No: Drop
```

---

## SSH Tunnel Fundamentals

### Local Port Forwarding (-L)

**Use case**: Access a remote service as if it were local

```bash
# Syntax
ssh -L [local_port]:[remote_host]:[remote_port] user@jump_host

# Example: Access remote database through bastion
ssh -L 5432:db.internal:5432 user@bastion.example.com

# Now connect locally
psql -h localhost -p 5432 -U myuser mydb
```

**Diagram**:
```
┌─────────────┐     SSH Tunnel      ┌─────────────┐     ┌─────────────┐
│   Local     │ ═══════════════════ │   Bastion   │ ──→ │  Database   │
│ localhost:  │                     │   Server    │     │ db:5432     │
│   5432      │                     │             │     │             │
└─────────────┘                     └─────────────┘     └─────────────┘
     You                              Jump Host           Target
```

### Remote Port Forwarding (-R)

**Use case**: Expose local service to remote network

```bash
# Syntax
ssh -R [remote_port]:[local_host]:[local_port] user@remote_host

# Example: Expose local dev server to remote
ssh -R 8080:localhost:3000 user@remote-server.com

# Remote users can now access your local server at remote-server.com:8080
```

**Diagram**:
```
┌─────────────┐     SSH Tunnel      ┌─────────────┐
│   Local     │ ═══════════════════ │   Remote    │
│ localhost:  │                     │  Server:    │
│   3000      │ ←───────────────────│   8080      │
└─────────────┘                     └─────────────┘
  Your dev                           Accessible
   server                            externally
```

### Dynamic Port Forwarding (-D)

**Use case**: SOCKS proxy for browser/application traffic

```bash
# Create SOCKS proxy
ssh -D 1080 user@proxy-server.com

# Configure browser to use SOCKS5 proxy: localhost:1080
# All traffic routes through proxy-server
```

---

## Common Testing Scenarios

### 1. Test Remote Web App Locally

```bash
# Scenario: Web app at internal.corp:443, accessible via bastion

# Create tunnel
ssh -L 8443:internal.corp:443 user@bastion.corp.com

# Test locally
curl https://localhost:8443 --insecure
# Or open browser: https://localhost:8443
```

### 2. Test Local API from Remote Server

```bash
# Scenario: Your API runs on localhost:3000, need to test from remote

# Create reverse tunnel
ssh -R 3000:localhost:3000 user@test-server.com

# SSH to test server and test
ssh user@test-server.com
curl http://localhost:3000/api/health
```

### 3. Run Playwright Tests Through Tunnel

```bash
# Scenario: Test internal app from CI server

# Option A: Tunnel from CI to internal network
ssh -L 8080:internal-app:80 user@bastion &
npx playwright test --config=tunnel.config.ts

# Option B: SOCKS proxy
ssh -D 1080 user@bastion &
HTTP_PROXY=socks5://localhost:1080 npx playwright test
```

### 4. Database Testing Through Jump Host

```bash
# PostgreSQL through bastion
ssh -L 5432:prod-db.internal:5432 user@bastion.example.com -N &

# Run migrations/tests
DATABASE_URL="postgres://user:pass@localhost:5432/mydb" npm run test

# MySQL
ssh -L 3306:mysql.internal:3306 user@bastion.example.com -N &
mysql -h 127.0.0.1 -P 3306 -u user -p
```

---

## AWS EC2 + SSM Strategy ⭐ RECOMMENDED

**When to use**:
- Claude Code Web (SSH not available)
- Corporate networks with restrictive proxies
- Environments where SSH is blocked but HTTPS works
- Need a clean browser environment for E2E tests

**Why it works**: SSM uses HTTPS to communicate with AWS APIs, bypassing SSH restrictions.

### Overview

```
┌──────────────────┐                    ┌──────────────────┐
│  Your Machine    │   HTTP/HTTPS       │   AWS EC2        │
│  (blocked SSH)   │ ═════════════════→ │  (SSM Agent)     │
│                  │   via SSM API      │                  │
└──────────────────┘                    └──────────────────┘
        │                                       │
        │ Can't reach                          Can reach
        │ target directly                      anything
        ↓                                       ↓
   ┌──────────────┐                     ┌──────────────────┐
   │   Target     │ ←───────────────────│  Runs Playwright │
   │   Web App    │   EC2 has network   │  or curl tests   │
   └──────────────┘   access            └──────────────────┘
```

### Implementation

**Step 1: Create IAM Role for SSM**

```python
import boto3

iam = boto3.client('iam')

# Create role with SSM policy
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "ec2.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}

iam.create_role(
    RoleName='test-ssm-role',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)

iam.attach_role_policy(
    RoleName='test-ssm-role',
    PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
)

# Create instance profile
iam.create_instance_profile(InstanceProfileName='test-ssm-profile')
iam.add_role_to_instance_profile(
    InstanceProfileName='test-ssm-profile',
    RoleName='test-ssm-role'
)
```

**Step 2: Launch EC2 Instance**

```python
ec2 = boto3.client('ec2')

# Amazon Linux 2023 with SSM agent pre-installed
response = ec2.run_instances(
    ImageId='ami-0c02fb55956c7d316',  # Amazon Linux 2023
    InstanceType='t3.micro',
    MinCount=1,
    MaxCount=1,
    IamInstanceProfile={'Name': 'test-ssm-profile'},
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'Name', 'Value': 'E2E-Test-Runner'}]
    }]
)

instance_id = response['Instances'][0]['InstanceId']
```

**Step 3: Wait for SSM Registration**

```python
ssm = boto3.client('ssm')

# Wait for SSM agent to register (up to 2 minutes)
for _ in range(24):
    response = ssm.describe_instance_information(
        Filters=[{'Key': 'InstanceIds', 'Values': [instance_id]}]
    )
    if response['InstanceInformationList']:
        print("SSM agent registered!")
        break
    time.sleep(5)
```

**Step 4: Run Commands via SSM**

```python
# Install dependencies
ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [
        'curl -fsSL https://rpm.nodesource.com/setup_20.x | bash -',
        'dnf install -y nodejs',
        'npm install -g playwright',
        'npx playwright install chromium',
        # Install Chromium dependencies for Amazon Linux
        'dnf install -y atk at-spi2-atk cups-libs libdrm libXcomposite ' +
        'libXdamage libXrandr mesa-libgbm pango alsa-lib gtk3 nss libxkbcommon'
    ]}
)

# Run Playwright test
result = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [
        'cd /tmp',
        'cat > test.js << "EOF"',
        test_script_content,
        'EOF',
        'node test.js'
    ]}
)

# Get output
command_id = result['Command']['CommandId']
output = ssm.get_command_invocation(
    CommandId=command_id,
    InstanceId=instance_id
)
print(output['StandardOutputContent'])
```

**Step 5: Cleanup**

```python
# Terminate instance
ec2.terminate_instances(InstanceIds=[instance_id])

# Delete IAM resources
iam.remove_role_from_instance_profile(
    InstanceProfileName='test-ssm-profile',
    RoleName='test-ssm-role'
)
iam.delete_instance_profile(InstanceProfileName='test-ssm-profile')
iam.detach_role_policy(
    RoleName='test-ssm-role',
    PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
)
iam.delete_role(RoleName='test-ssm-role')
```

### Complete E2E Test Runner Example

**Canonical locations:**
- `projects/personal/voice-review-agent/tests/e2e-ec2-runner.py`
- `projects/shared/tool-error-tracker-js-et001/packages/infra/test/e2e-ec2-runner.py`

**Usage:**
```bash
# With AWS credentials (uses SPOT instances by default)
export AWS_PROFILE=admin-507745175693
python e2e-ec2-runner.py

# Disable spot instances (use on-demand)
USE_SPOT=false python e2e-ec2-runner.py

# Keep instance for debugging
python e2e-ec2-runner.py --keep-instance
```

**What it does:**
1. Creates IAM role + instance profile (SSM permissions)
2. Launches EC2 SPOT instance (Amazon Linux 2023, t3.small) - ~70% cheaper than on-demand
3. Falls back to on-demand if spot capacity unavailable
4. Waits for SSM agent registration
5. Installs Node.js + Playwright + Chromium deps
6. Runs headless browser test via SSM `send_command`
7. Streams output back
8. Cleans up all resources (EC2, IAM, security group)

**Cost:**
- Spot:      ~$0.01-0.02 per test run (default)
- On-demand: ~$0.02-0.05 per test run

**TODO:** Extract to `hmode/shared/tools/e2e-ec2-runner.py` for reuse across projects.

---

## SSH Options Reference

### Keep Tunnel Alive

```bash
# Prevent timeout
ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -L 8080:target:80 user@host

# Background the tunnel
ssh -f -N -L 8080:target:80 user@host
# -f: Background after auth
# -N: No remote command (just tunnel)
```

### Multiple Tunnels

```bash
# Chain multiple forwards
ssh -L 5432:db:5432 -L 6379:redis:6379 -L 9200:elastic:9200 user@bastion

# Or use config file (~/.ssh/config)
Host bastion
    HostName bastion.example.com
    User myuser
    LocalForward 5432 db:5432
    LocalForward 6379 redis:6379
```

### Compression

```bash
# Enable compression for slow links
ssh -C -L 8080:target:80 user@host
```

### Jump Host (ProxyJump)

```bash
# Modern syntax (OpenSSH 7.3+)
ssh -J user@bastion user@internal-host

# For tunnels
ssh -J user@bastion -L 8080:internal-app:80 user@internal-host
```

---

## Troubleshooting

### Tunnel Not Working

```bash
# Check if port is listening
netstat -tlnp | grep 8080
lsof -i :8080

# Verbose SSH
ssh -v -L 8080:target:80 user@host

# Check firewall on jump host
sudo iptables -L -n
```

### Connection Refused

```bash
# Verify target is reachable from jump host
ssh user@bastion 'curl -v http://target:80'

# Check if target service is running
ssh user@bastion 'nc -zv target 80'
```

### Timeout Issues

```bash
# Increase connection timeout
ssh -o ConnectTimeout=30 -L 8080:target:80 user@host

# Keep connection alive
ssh -o ServerAliveInterval=30 -L 8080:target:80 user@host
```

### Permission Denied (Binding)

```bash
# Ports < 1024 require root
# Use higher port instead
ssh -L 8080:target:80 user@host  # Instead of -L 80:target:80
```

---

## Security Best Practices

1. **Use SSH keys**, not passwords
2. **Limit tunnel duration** - kill when done
3. **Use specific bindings** - `127.0.0.1:8080` not `0.0.0.0:8080`
4. **Audit tunnel usage** - log connections
5. **Restrict jump host access** - firewall rules

```bash
# Bind only to localhost (default, but explicit)
ssh -L 127.0.0.1:8080:target:80 user@host

# NOT this (exposes to all interfaces)
ssh -L 0.0.0.0:8080:target:80 user@host
```

---

## Quick Reference

| Scenario | Command | Claude Code Web |
|----------|---------|-----------------|
| Access remote DB | `ssh -L 5432:db:5432 user@bastion` | ❌ |
| Expose local API | `ssh -R 8080:localhost:3000 user@server` | ❌ |
| SOCKS proxy | `ssh -D 1080 user@proxy` | ❌ |
| Background tunnel | `ssh -f -N -L 8080:target:80 user@host` | ❌ |
| Via jump host | `ssh -J user@bastion -L 8080:target:80 user@internal` | ❌ |
| Keep alive | `ssh -o ServerAliveInterval=60 -L 8080:target:80 user@host` | ❌ |
| **EC2+SSM (no SSH)** | `python e2e-ec2-runner.py` | ✅ **Recommended** |
| HTTP tunnel (preview) | `/tunnel 3000` (see http-tunnel skill) | ✅ |

---

## See Also

- AWS SSM Session Manager: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html
- SSH Tunneling Guide: https://www.ssh.com/academy/ssh/tunneling
- Playwright Networking: https://playwright.dev/docs/network
