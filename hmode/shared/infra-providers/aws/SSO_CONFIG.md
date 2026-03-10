# AWS SSO Configuration

## SSO Start URL
```
https://d-90679b11cc.awsapps.com/start/#/?tab=accounts
```

## Account Information
- **Account ID:** 507745175693
- **Region:** us-east-1

## Quick Login
```bash
# Configure SSO profile
aws configure sso

# Or use existing profile
aws sso login --profile your-profile-name
```

## AWS Profile Configuration with Isengard

For work accounts using Isengard credential management, add to `~/.aws/config`:

```ini
[profile andyhop]
output = json
region = us-east-1
credential_process = isengardcli credentials --awscli andyhop@amazon.com --role Admin-OneClick --region us-east-1
```

This configures automatic credential retrieval via Isengard CLI. The `credential_process` parameter tells AWS CLI to use Isengard for authentication instead of static credentials.

## CDK Deployer User
- **Username:** cdk-deployer
- **Policies:**
  - CDKDeployerPolicy (main)
  - CDKDeployerPolicyExtended (additional permissions)
