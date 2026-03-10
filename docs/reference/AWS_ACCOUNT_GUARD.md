# AWS Account Guard Rails

## Overview

Prevents accessing wrong AWS accounts from wrong computers using shell-level guards.

**Key Features:**
- Computer-type detection (work vs personal)
- Pre-command validation for AWS CLI, CDK, Terraform, SAM
- Clear error messages when blocked
- Claude Code integration

## Quick Start

### Initial Setup (Both Computers)

```bash
# Run interactive setup
~/dev/lab/bin/aws-account-guard-setup

# Reload shell
exec zsh  # or: exec bash

# Check status
aws-guard-status
```

### Configuration Per Computer

**Work Computer:**
- Computer Type: `work`
- Allowed Accounts: Work AWS account ID(s) only
- Example: `507745175693`

**Personal Computer:**
- Computer Type: `personal`
- Allowed Accounts: Personal AWS account ID(s) only
- Example: `123456789012`

## How It Works

### Shell-Level Protection

The guard wraps these commands:
- `aws` - AWS CLI
- `cdk` - AWS CDK
- `terraform` - Terraform
- `sam` - AWS SAM CLI

Before execution, it:
1. Checks current AWS account ID
2. Compares against allowed list
3. Blocks if mismatch
4. Shows clear error message

### Example Block

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚫 AWS ACCOUNT ACCESS BLOCKED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Computer Type:  work
Current Account: 123456789012
Allowed Accounts: 507745175693

This computer is configured for work AWS accounts only.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Claude Code Integration

### How Claude Respects Guards

When Claude Code executes AWS commands, it:
1. Checks `~/.aws-account-guard.conf` exists
2. Validates current credentials match allowed accounts
3. Blocks execution if mismatch
4. Informs user of the restriction

### Configuration File

Location: `~/.aws-account-guard.conf`

```bash
# AWS Account Guard Configuration
COMPUTER_TYPE="work"
ALLOWED_AWS_ACCOUNTS=(507745175693)
SHOW_GUARD_ON_STARTUP="false"
```

### Manual Check (for Claude)

```bash
# Check current credentials
~/dev/lab/hmode/bin/claude-aws-guard-check current

# Check specific account
~/dev/lab/hmode/bin/claude-aws-guard-check 507745175693
```

**Exit codes:**
- `0` - Account allowed
- `1` - Account blocked
- `2` - Configuration error

## Commands

### Status Check

```bash
aws-guard-status
```

Output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️  AWS Account Guard Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Computer Type:    work
Allowed Accounts:  507745175693
Current Account:   507745175693 ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Reconfigure

```bash
# Run setup again
~/dev/lab/bin/aws-account-guard-setup

# Reload shell
exec zsh
```

### Temporarily Bypass (Emergency)

```bash
# Use command directly (bypasses wrapper)
command aws sts get-caller-identity

# Disable for session (use carefully!)
unset -f aws cdk terraform sam
```

## Setup on Both Computers

### Work Computer Setup

```bash
# 1. Run setup
~/dev/lab/bin/aws-account-guard-setup

# Selections:
#   Computer Type: [1] Work computer
#   Account ID: 507745175693 (or your work account)
#   Show on startup: [N]

# 2. Reload shell
exec zsh

# 3. Verify
aws-guard-status

# 4. Test
aws sts get-caller-identity
```

### Personal Computer Setup

```bash
# 1. Run setup
~/dev/lab/bin/aws-account-guard-setup

# Selections:
#   Computer Type: [2] Personal computer
#   Account ID: 123456789012 (or your personal account)
#   Show on startup: [N]

# 2. Reload shell
exec zsh

# 3. Verify
aws-guard-status

# 4. Test
aws sts get-caller-identity
```

## Troubleshooting

### Guard Not Loading

**Problem:** Commands still work with wrong account

**Solution:**
```bash
# Check if guard is in shell config
grep "aws-account-guard" ~/.zshrc

# If missing, add manually:
echo 'source ~/dev/lab/bin/aws-account-guard' >> ~/.zshrc

# Reload
exec zsh
```

### Wrong Account Detected

**Problem:** Guard blocks legitimate account

**Solution:**
```bash
# Check current account
aws sts get-caller-identity --query Account --output text

# Check allowed accounts
cat ~/.aws-account-guard.conf | grep ALLOWED_AWS_ACCOUNTS

# If mismatch, reconfigure:
~/dev/lab/bin/aws-account-guard-setup
```

### Multiple Profiles

**Problem:** Need to allow multiple accounts on one computer

**Solution:**
```bash
# Edit config directly
nano ~/.aws-account-guard.conf

# Change to array:
ALLOWED_AWS_ACCOUNTS=(507745175693 123456789012 999888777666)

# Reload
exec zsh
```

### Claude Using Wrong Account

**Problem:** Claude Code tries to use wrong AWS account

**Behavior:** Claude will check the guard before executing AWS commands and will refuse if blocked

**What Claude sees:**
```
Checking AWS account guard...
BLOCKED
Computer: work
Account: 123456789012
Allowed: 507745175693

I cannot execute this AWS command because this work computer
is configured to only allow access to account 507745175693.
```

## Files

```
~/dev/lab/bin/
├── aws-account-guard              # Main guard script
├── aws-account-guard-setup        # Interactive setup
└── claude-aws-guard-check         # Validation utility

~/.aws-account-guard.conf          # Configuration (gitignored)
```

## Security Layers

This implements **Layer 3** (shell guard rails) from the full security model:

1. **Layer 1:** Don't configure wrong credentials (baseline)
2. **Layer 2:** IAM IP restrictions (optional, for work accounts)
3. **Layer 3:** Shell guard rails (this solution) ✓
4. **Layer 4:** AWS SSO with device trust (enterprise)

## Next Steps

**Optional enhancements:**

1. **Add IAM IP restrictions** (Layer 2)
   - Restrict work account to work network IPs
   - Adds defense-in-depth

2. **Alert on violations**
   - Log blocked attempts
   - Send notification on repeated blocks

3. **Audit trail**
   - Log all AWS commands executed
   - Track which accounts accessed when

**Want to implement any of these?**
