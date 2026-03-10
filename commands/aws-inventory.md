# AWS Resource Inventory Skill

## Overview
Discover and generate a comprehensive inventory of AWS resources across multiple services in markdown or Excel format.

## Capability
Generates detailed reports of AWS resources, grouped by:
- CloudFormation stacks
- Resource types
- Service categories

Supports both markdown and Excel output formats with multiple sheets.

## Parameters
- `profile`: AWS profile to use
  - Default: from AWS_PROFILE env or "default"
- `region`: AWS region to scan
  - Default: us-east-1
- `output`: Output file path (without extension for format=both)
  - Default: `aws-inventory-{profile}-{timestamp}.{ext}`
- `format`: Output format choice
  - Options: `markdown`, `excel`, `both`
  - Default: `markdown`

## Usage Examples

### Basic Usage (Markdown)
```bash
/aws-inventory
```
- Uses default AWS profile
- Scans us-east-1 region
- Generates markdown inventory in default location

### Excel Format
```bash
/aws-inventory format=excel
```
- Generates multi-sheet Excel workbook
- Includes summary, stacks, all resources, and per-service sheets

### Both Formats
```bash
/aws-inventory format=both output=~/reports/aws-inventory
```
- Generates both markdown and Excel reports
- Creates: aws-inventory.md and aws-inventory.xlsx

### Specific Profile and Region
```bash
/aws-inventory profile=my-custom-profile region=us-west-2 format=excel
```
- Uses specified AWS profile and region
- Generates Excel report

## Resource Types Discovered

### Compute & Containers
- Lambda Functions (runtime, memory, timeout)
- ECS Clusters (services, tasks, instances)
- ECR Repositories (image URIs)

### Storage
- S3 Buckets (region-filtered)
- DynamoDB Tables (item counts, size)

### Networking & APIs
- API Gateway (REST and HTTP APIs)
- Cognito User Pools
- Cognito Identity Pools

### Messaging & Queues
- SNS Topics
- SQS Queues (message counts)

### Application Services
- Amplify Apps (branches, repositories)

### Infrastructure
- CloudFormation Stacks (status, creation time)

## Generated Report Sections

### Markdown Format
1. Summary table of resource counts by service/type
2. CloudFormation stack details with status and creation dates
3. Resources grouped by CloudFormation stack
4. Standalone resources (not part of any stack)

### Excel Format (Multiple Sheets)
1. **Summary Sheet**: Resource counts, account info, generation timestamp
2. **CloudFormation Stacks Sheet**: All stacks with status and descriptions
3. **All Resources Sheet**: Complete inventory with ARNs, console URLs, tags
4. **Per-Service Sheets**: Dedicated sheet for each service (Lambda, S3, ECS, etc.) with service-specific metadata

## Performance
- Parallel resource discovery (12 concurrent service scans)
- Efficient AWS API pagination
- Comprehensive error handling and retry logic
- Auto-sized Excel columns for readability

## Security Considerations
- Uses AWS profile credentials (no hardcoded secrets)
- Follows AWS IAM permissions (read-only operations)
- Generates read-only inventory
- Includes console URLs for easy verification

## Installation Requirements

### Basic (Markdown only)
```bash
pip install boto3
```

### Excel Support
```bash
pip install boto3 openpyxl
```

## Troubleshooting

### Common Issues
- **"No AWS credentials found"**: Run `aws configure` or set AWS_PROFILE
- **"Access Denied"**: Ensure IAM permissions for List/Describe operations
- **"Excel export requires openpyxl"**: Install with `pip install openpyxl`

### Required IAM Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "cognito-idp:ListUserPools",
      "cognito-idp:DescribeUserPool",
      "cognito-identity:ListIdentityPools",
      "cognito-identity:DescribeIdentityPool",
      "amplify:ListApps",
      "dynamodb:ListTables",
      "dynamodb:DescribeTable",
      "apigateway:GET",
      "lambda:ListFunctions",
      "lambda:ListTags",
      "s3:ListAllMyBuckets",
      "s3:GetBucketLocation",
      "s3:GetBucketTagging",
      "ecs:ListClusters",
      "ecs:DescribeClusters",
      "ecr:DescribeRepositories",
      "ecr:ListTagsForResource",
      "sns:ListTopics",
      "sns:ListTagsForResource",
      "sqs:ListQueues",
      "sqs:GetQueueAttributes",
      "sqs:ListQueueTags",
      "cloudformation:DescribeStacks"
    ],
    "Resource": "*"
  }]
}
```

## Best Practices
- Refresh AWS credentials before running (Isengard expires after 1 hour)
- Use least-privilege IAM roles for production
- Review generated inventory for sensitive information before sharing
- Use `format=both` for comprehensive reporting and analysis
- Filter by region to reduce scope and execution time

## Advanced Configuration

### Environment Variables
```bash
export AWS_PROFILE=my-default-profile
export AWS_DEFAULT_REGION=us-west-2
```

### Running via Python
```bash
python3 bin/aws-inventory.py --profile default --region us-east-1 --format excel
```

## Output Examples

### Markdown Output
```
# AWS Resource Inventory

**Account:** 108782054816
**Region:** us-east-1
**Generated:** 2026-02-06T...

## Summary

| Resource Type | Count |
|--------------|-------|
| lambda/function | 14 |
| s3/bucket | 8 |
...
```

### Excel Output Structure
- **Sheet 1 (Summary)**: Overview with counts
- **Sheet 2 (CloudFormation Stacks)**: All stacks
- **Sheet 3 (All Resources)**: Combined view
- **Sheet 4-N**: Per-service sheets (LAMBDA, S3, ECS, ECR, SNS, SQS, etc.)

## Compatibility
- Python 3.9+
- boto3 library (AWS SDK)
- openpyxl library (optional, for Excel support)
- Works across all AWS environments (commercial, GovCloud)

## Version
- Skill Version: 2.0.0
- Last Updated: 2026-02-06
- Underlying Script: `bin/aws-inventory.py`
- Added: Lambda, S3, ECS, ECR, SNS, SQS discovery
- Added: Excel export with multiple sheets

## Related Commands
- `aws configure`: Set up AWS credentials
- `aws sts get-caller-identity`: Verify current AWS identity
- `aws organizations list-accounts`: List accounts in AWS Organizations
- `/aws-bootstrap`: Bootstrap AWS environment