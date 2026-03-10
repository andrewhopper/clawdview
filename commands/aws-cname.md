---
uuid: cmd-aws-cname-6f7g8h9i
---

# AWS CNAME Creator

Create Route 53 CNAME or A records for AWS resources (Amplify apps, S3 buckets, EC2 instances, EIPs).

## Usage
```bash
/aws-cname <record-name> <target> [domain] [--type=CNAME|A] [--ttl=300]
```

## Parameters
- `record-name`: DNS record name (e.g., "kiro-v2", "myapp")
- `target`: Target resource (IP address, EIP ID, Amplify URL, S3 bucket, etc.)
- `domain`: Domain name (default: **aws.demo1983.com**)
- `--type`: Record type (default: auto-detect - A for IPs, CNAME for hostnames)
- `--ttl`: Time to live in seconds (default: 300)

## Examples
```bash
# Create A record for EC2 Elastic IP (uses default domain)
/aws-cname kiro-v2 3.225.24.129

# Create CNAME for Amplify app
/aws-cname myapp d1a2b3c4d5e6f7.amplifyapp.com

# Create A record in custom domain
/aws-cname api 54.123.45.67 mycompany.com

# Create CNAME with custom TTL
/aws-cname www myapp.cloudfront.net --ttl=600
```

## What it does
1. Detects Route 53 hosted zone for the domain
2. Auto-detects record type:
   - A record for IP addresses (x.x.x.x format)
   - CNAME record for hostnames
3. Creates or updates the DNS record
4. Returns the change ID and status

## Notes
- Default domain is **aws.demo1983.com** (can be overridden)
- Requires AWS credentials with Route53 permissions
- Uses AWS CLI (no Python dependencies required)
- Changes typically propagate within 60 seconds
