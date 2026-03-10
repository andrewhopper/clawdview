# AWS Amplify Custom Domain SOP

Deploy static sites to AWS Amplify with custom domains from Route 53.

---

## Quick Start

```bash
# Deploy with custom domain
python shared/scripts/amplify_deploy.py deploy ./dist \
  --app-name my-app \
  --domain myapp.example.com \
  --yes
```

---

## Prerequisites

1. **AWS credentials** with permissions for:
   - Amplify (create/update apps, domains)
   - Route 53 (manage DNS records)
   - ACM (implicit, for SSL certificates)

2. **Route 53 hosted zone** for your domain

3. **Built static site** (e.g., `npm run build` output)

---

## Manual Process

### Step 1: Build Your Site

```bash
cd your-project
npm run build
```

### Step 2: Create Deployment Zip

**CRITICAL:** Files must be at the **root** of the zip, not inside a subdirectory.

```bash
# CORRECT - files at root
cd dist && zip -r ../deploy.zip .

# WRONG - will cause 404s
zip -r deploy.zip dist/
```

### Step 3: Deploy to Amplify

```python
import boto3

amplify = boto3.client('amplify', region_name='us-east-1')

# Create or get existing app
app = amplify.create_app(name='my-app', platform='WEB')
app_id = app['app']['appId']

# Create branch
amplify.create_branch(appId=app_id, branchName='main', stage='PRODUCTION')

# Create deployment
deployment = amplify.create_deployment(appId=app_id, branchName='main')
job_id = deployment['jobId']
upload_url = deployment['zipUploadUrl']

# Upload zip via presigned URL
import urllib.request
with open('deploy.zip', 'rb') as f:
    req = urllib.request.Request(upload_url, data=f.read(), method='PUT',
                                   headers={'Content-Type': 'application/zip'})
    urllib.request.urlopen(req)

# Start deployment
amplify.start_deployment(appId=app_id, branchName='main', jobId=job_id)
```

### Step 4: Configure Custom Domain

```python
# Create domain association
domain_response = amplify.create_domain_association(
    appId=app_id,
    domainName='example.com',  # Parent domain in Route 53
    subDomainSettings=[{
        'prefix': 'myapp',     # Creates myapp.example.com
        'branchName': 'main'
    }]
)

domain_info = domain_response['domainAssociation']
```

### Step 5: Add DNS Records (CRITICAL)

**You need TWO CNAME records:**

1. **Certificate Validation Record** (for SSL):
   ```
   Name:  _abc123.example.com
   Type:  CNAME
   Value: _xyz789.acm-validations.aws.
   ```

   Get this from: `domain_info['certificateVerificationDNSRecord']`

2. **Subdomain Record** (for routing):
   ```
   Name:  myapp.example.com
   Type:  CNAME
   Value: d1abc123.cloudfront.net
   ```

   Get this from: `domain_info['subDomains'][0]['dnsRecord']`

   **WARNING:** Do NOT use the `amplifyapp.com` URL! Use the CloudFront distribution from the response.

```python
route53 = boto3.client('route53')
zone_id = 'Z1234567890ABC'  # Your hosted zone ID

# Parse certificate verification record
cert_record = domain_info['certificateVerificationDNSRecord']
# Format: "_name.domain. CNAME _target.acm-validations.aws."
parts = cert_record.split()
cert_name = parts[0]
cert_target = parts[2]

# Parse subdomain record
sub_record = domain_info['subDomains'][0]['dnsRecord']
# Format: "prefix CNAME target.cloudfront.net"
sub_parts = sub_record.split()
sub_prefix = sub_parts[0]
sub_target = sub_parts[2]

# Add both records
route53.change_resource_record_sets(
    HostedZoneId=zone_id,
    ChangeBatch={
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': cert_name,
                    'Type': 'CNAME',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': cert_target}]
                }
            },
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': f'{sub_prefix}.example.com',
                    'Type': 'CNAME',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': sub_target}]
                }
            }
        ]
    }
)
```

### Step 6: Wait for SSL Certificate

SSL certificate provisioning takes **10-30 minutes**. Check status:

```python
domain = amplify.get_domain_association(appId=app_id, domainName='example.com')
print(domain['domainAssociation']['domainStatus'])
# CREATING -> PENDING_VERIFICATION -> AVAILABLE
```

---

## Common Gotchas

### 1. 404 After Deployment

**Cause:** Zip file has files inside a subdirectory (e.g., `dist/index.html`)

**Fix:** Create zip from inside the build directory:
```bash
cd dist && zip -r ../deploy.zip .
```

### 2. SSL Certificate Stuck on "Pending"

**Cause:** Missing certificate validation CNAME record

**Fix:** Add the ACM validation record from `certificateVerificationDNSRecord`

### 3. Domain Not Resolving

**Cause:** Using wrong CNAME target (amplifyapp.com instead of cloudfront.net)

**Fix:** Use the `dnsRecord` value from the domain association response, which points to CloudFront

### 4. "Domain Already Associated" Error

**Cause:** Domain was previously linked to another app

**Fix:** Delete the old domain association first:
```python
amplify.delete_domain_association(appId=old_app_id, domainName='example.com')
```

---

## Domain Status Reference

| Status | Meaning | Action |
|--------|---------|--------|
| `CREATING` | Setting up | Wait |
| `AWAITING_APP_CNAME` | Need DNS records | Add CNAME records |
| `PENDING_VERIFICATION` | Validating SSL cert | Wait 10-30 min |
| `PENDING_DEPLOYMENT` | Deploying to edge | Wait |
| `AVAILABLE` | Ready | Done! |
| `FAILED` | Error occurred | Check `statusReason` |

---

## Using the CLI Tool

```bash
# Deploy with auto domain setup
python shared/scripts/amplify_deploy.py deploy ./dist \
  --app-name portfolio \
  --domain projects.b.lfg.new \
  --framework static \
  --yes

# Deploy with SNS notifications
python shared/scripts/amplify_deploy.py deploy ./dist \
  --app-name portfolio \
  --domain projects.b.lfg.new \
  --notify arn:aws:sns:us-east-1:507745175693:amplify-deployment-notifications \
  --yes

# Check status
python shared/scripts/amplify_deploy.py status portfolio

# List all apps
python shared/scripts/amplify_deploy.py list
```

## Deployment Notifications

SNS topic for deployment alerts:
- **Topic ARN:** `arn:aws:sns:us-east-1:507745175693:amplify-deployment-notifications`
- **Subscribers:** SMS (+1-727-743-6932), Email (demo@example.com)

Use `--notify SNS_ARN` to receive success/failure notifications.

---

## Related Tools

- `shared/scripts/amplify_deploy.py` - Main deployment script
- `shared/aws/route53_cname.py` - Route 53 CNAME manager
- `shared/infra-providers/aws/amplify.yml` - Build spec template

---

## References

- [Amplify Custom Domains](https://docs.aws.amazon.com/amplify/latest/userguide/custom-domains.html)
- [Route 53 DNS Validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html)
