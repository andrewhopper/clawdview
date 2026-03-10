# Safe CLI Commands Reference

Non-destructive, read-only CLI commands that don't modify state. Use these freely for inspection, monitoring, and debugging.

**Generated:** 2025-12-15
**Category:** Reference

---

## 1.0 AWS CLI

### 1.1 Logs & Monitoring

| Command | Description |
|---------|-------------|
| `aws logs tail <log-group>` | Stream CloudWatch logs in real-time |
| `aws logs tail <log-group> --follow` | Continuously tail logs |
| `aws logs describe-log-groups` | List all log groups |
| `aws logs describe-log-streams --log-group-name <name>` | List streams in a log group |
| `aws logs filter-log-events --log-group-name <name>` | Search log events |
| `aws logs get-log-events --log-group-name <name> --log-stream-name <stream>` | Get specific log events |

### 1.2 EC2

| Command | Description |
|---------|-------------|
| `aws ec2 describe-instances` | List all EC2 instances |
| `aws ec2 describe-instances --instance-ids <id>` | Get instance details |
| `aws ec2 describe-instance-status` | Get instance health status |
| `aws ec2 describe-security-groups` | List security groups |
| `aws ec2 describe-vpcs` | List VPCs |
| `aws ec2 describe-subnets` | List subnets |
| `aws ec2 describe-volumes` | List EBS volumes |
| `aws ec2 describe-images --owners self` | List owned AMIs |
| `aws ec2 describe-key-pairs` | List SSH key pairs |
| `aws ec2 describe-tags` | List all resource tags |

### 1.3 S3

| Command | Description |
|---------|-------------|
| `aws s3 ls` | List all buckets |
| `aws s3 ls s3://<bucket>` | List bucket contents |
| `aws s3 ls s3://<bucket>/<prefix> --recursive` | List with prefix recursively |
| `aws s3api get-bucket-location --bucket <name>` | Get bucket region |
| `aws s3api get-bucket-versioning --bucket <name>` | Check versioning status |
| `aws s3api get-bucket-policy --bucket <name>` | View bucket policy |
| `aws s3api head-object --bucket <name> --key <key>` | Get object metadata |

### 1.4 Lambda

| Command | Description |
|---------|-------------|
| `aws lambda list-functions` | List all Lambda functions |
| `aws lambda get-function --function-name <name>` | Get function details |
| `aws lambda get-function-configuration --function-name <name>` | Get function config |
| `aws lambda list-versions-by-function --function-name <name>` | List function versions |
| `aws lambda list-aliases --function-name <name>` | List function aliases |
| `aws lambda get-policy --function-name <name>` | Get function policy |

### 1.5 IAM

| Command | Description |
|---------|-------------|
| `aws iam list-users` | List IAM users |
| `aws iam list-roles` | List IAM roles |
| `aws iam list-policies --scope Local` | List custom policies |
| `aws iam get-user` | Get current user details |
| `aws iam get-role --role-name <name>` | Get role details |
| `aws iam list-attached-user-policies --user-name <name>` | List user's policies |
| `aws iam list-attached-role-policies --role-name <name>` | List role's policies |
| `aws sts get-caller-identity` | Get current credentials info |

### 1.6 DynamoDB

| Command | Description |
|---------|-------------|
| `aws dynamodb list-tables` | List all tables |
| `aws dynamodb describe-table --table-name <name>` | Get table details |
| `aws dynamodb scan --table-name <name>` | Read all items (use carefully on large tables) |
| `aws dynamodb query --table-name <name> --key-condition-expression ...` | Query items |
| `aws dynamodb get-item --table-name <name> --key ...` | Get single item |

### 1.7 CloudFormation / CDK

| Command | Description |
|---------|-------------|
| `aws cloudformation list-stacks` | List all stacks |
| `aws cloudformation describe-stacks` | Get stack details |
| `aws cloudformation describe-stack-resources --stack-name <name>` | List stack resources |
| `aws cloudformation describe-stack-events --stack-name <name>` | Get stack events |
| `aws cloudformation get-template --stack-name <name>` | Get stack template |
| `cdk list` | List CDK stacks |
| `cdk diff` | Show pending changes |
| `cdk synth` | Synthesize CloudFormation template |

### 1.8 ECS / Fargate

| Command | Description |
|---------|-------------|
| `aws ecs list-clusters` | List ECS clusters |
| `aws ecs list-services --cluster <name>` | List services in cluster |
| `aws ecs describe-services --cluster <name> --services <svc>` | Get service details |
| `aws ecs list-tasks --cluster <name>` | List running tasks |
| `aws ecs describe-tasks --cluster <name> --tasks <task-id>` | Get task details |
| `aws ecs describe-task-definition --task-definition <name>` | Get task definition |

### 1.9 RDS

| Command | Description |
|---------|-------------|
| `aws rds describe-db-instances` | List RDS instances |
| `aws rds describe-db-clusters` | List Aurora clusters |
| `aws rds describe-db-snapshots` | List snapshots |
| `aws rds describe-db-parameter-groups` | List parameter groups |

### 1.10 SSM

| Command | Description |
|---------|-------------|
| `aws ssm describe-instance-information` | List managed instances |
| `aws ssm get-parameter --name <name>` | Get parameter value |
| `aws ssm get-parameters-by-path --path <path>` | Get parameters by path |
| `aws ssm describe-parameters` | List all parameters |

### 1.11 Secrets Manager

| Command | Description |
|---------|-------------|
| `aws secretsmanager list-secrets` | List all secrets |
| `aws secretsmanager describe-secret --secret-id <id>` | Get secret metadata |
| `aws secretsmanager get-secret-value --secret-id <id>` | Get secret value |

### 1.12 CloudWatch

| Command | Description |
|---------|-------------|
| `aws cloudwatch list-metrics` | List available metrics |
| `aws cloudwatch get-metric-statistics ...` | Get metric data |
| `aws cloudwatch describe-alarms` | List CloudWatch alarms |
| `aws cloudwatch describe-alarm-history` | Get alarm history |

### 1.13 API Gateway

| Command | Description |
|---------|-------------|
| `aws apigateway get-rest-apis` | List REST APIs |
| `aws apigatewayv2 get-apis` | List HTTP/WebSocket APIs |
| `aws apigateway get-resources --rest-api-id <id>` | List API resources |
| `aws apigateway get-stages --rest-api-id <id>` | List API stages |

### 1.14 SNS / SQS

| Command | Description |
|---------|-------------|
| `aws sns list-topics` | List SNS topics |
| `aws sns list-subscriptions` | List subscriptions |
| `aws sqs list-queues` | List SQS queues |
| `aws sqs get-queue-attributes --queue-url <url> --attribute-names All` | Get queue details |

### 1.15 Amplify

| Command | Description |
|---------|-------------|
| `aws amplify list-apps` | List Amplify apps |
| `aws amplify get-app --app-id <id>` | Get app details |
| `aws amplify list-branches --app-id <id>` | List app branches |
| `aws amplify list-jobs --app-id <id> --branch-name <branch>` | List deployments |

---

## 2.0 Git

### 2.1 Status & Information

| Command | Description |
|---------|-------------|
| `git status` | Show working tree status |
| `git status -s` | Short status format |
| `git log` | Show commit history |
| `git log --oneline` | Compact commit history |
| `git log --oneline -n 10` | Last 10 commits |
| `git log --graph --oneline --all` | Visual branch graph |
| `git log --author="name"` | Filter by author |
| `git log --since="2 weeks ago"` | Filter by date |
| `git show <commit>` | Show commit details |
| `git show --stat <commit>` | Show commit file changes |

### 2.2 Diff & Comparison

| Command | Description |
|---------|-------------|
| `git diff` | Show unstaged changes |
| `git diff --staged` | Show staged changes |
| `git diff <branch1>..<branch2>` | Compare branches |
| `git diff <commit1>..<commit2>` | Compare commits |
| `git diff --stat` | Summary of changes |
| `git diff --name-only` | List changed files only |

### 2.3 Branch & Remote

| Command | Description |
|---------|-------------|
| `git branch` | List local branches |
| `git branch -a` | List all branches (local + remote) |
| `git branch -v` | List with last commit |
| `git branch --merged` | List merged branches |
| `git remote -v` | List remotes with URLs |
| `git remote show origin` | Detailed remote info |

### 2.4 Inspection

| Command | Description |
|---------|-------------|
| `git blame <file>` | Show line-by-line authorship |
| `git blame -L 10,20 <file>` | Blame specific lines |
| `git shortlog -sn` | Contributor summary |
| `git rev-parse HEAD` | Get current commit hash |
| `git rev-parse --abbrev-ref HEAD` | Get current branch name |
| `git ls-files` | List tracked files |
| `git ls-tree HEAD` | List files at HEAD |
| `git config --list` | Show git configuration |

### 2.5 Search

| Command | Description |
|---------|-------------|
| `git log --grep="keyword"` | Search commit messages |
| `git log -S "code"` | Search for code changes |
| `git log -p -- <file>` | File change history |
| `git bisect` | Binary search for bugs |

---

## 3.0 Node.js / npm / pnpm

### 3.1 Package Information

| Command | Description |
|---------|-------------|
| `npm list` | List installed packages |
| `npm list --depth=0` | Top-level packages only |
| `npm list --global` | Global packages |
| `npm outdated` | Check for outdated packages |
| `npm audit` | Security vulnerability scan |
| `npm view <package>` | View package info |
| `npm view <package> versions` | View available versions |
| `npm info <package>` | Detailed package info |
| `npm explain <package>` | Why package is installed |
| `npm ls <package>` | Find package in tree |

### 3.2 pnpm Equivalents

| Command | Description |
|---------|-------------|
| `pnpm list` | List installed packages |
| `pnpm list --depth=0` | Top-level packages only |
| `pnpm outdated` | Check for outdated packages |
| `pnpm audit` | Security vulnerability scan |
| `pnpm why <package>` | Why package is installed |

### 3.3 Project Info

| Command | Description |
|---------|-------------|
| `npm run` | List available scripts |
| `npm config list` | Show npm configuration |
| `npm whoami` | Current npm user |
| `npm token list` | List auth tokens |

---

## 4.0 Python / pip / uv

### 4.1 Package Information

| Command | Description |
|---------|-------------|
| `pip list` | List installed packages |
| `pip list --outdated` | Show outdated packages |
| `pip show <package>` | Package details |
| `pip check` | Verify dependencies |
| `pip freeze` | Export installed packages |
| `pip index versions <package>` | Available versions |

### 4.2 uv Equivalents

| Command | Description |
|---------|-------------|
| `uv pip list` | List installed packages |
| `uv pip show <package>` | Package details |
| `uv pip check` | Verify dependencies |

### 4.3 Virtual Environment

| Command | Description |
|---------|-------------|
| `python --version` | Python version |
| `which python` | Python path |
| `python -m site` | Show site-packages location |
| `pip -V` | pip version and location |

---

## 5.0 Docker

### 5.1 Container & Image Info

| Command | Description |
|---------|-------------|
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker images` | List images |
| `docker images -a` | List all images (including intermediate) |
| `docker logs <container>` | View container logs |
| `docker logs -f <container>` | Follow container logs |
| `docker logs --tail 100 <container>` | Last 100 log lines |
| `docker inspect <container/image>` | Detailed JSON info |
| `docker stats` | Real-time resource usage |
| `docker top <container>` | Running processes in container |

### 5.2 Network & Volume

| Command | Description |
|---------|-------------|
| `docker network ls` | List networks |
| `docker network inspect <name>` | Network details |
| `docker volume ls` | List volumes |
| `docker volume inspect <name>` | Volume details |

### 5.3 System Info

| Command | Description |
|---------|-------------|
| `docker info` | Docker system info |
| `docker version` | Docker version |
| `docker system df` | Disk usage |
| `docker history <image>` | Image layer history |

### 5.4 Docker Compose

| Command | Description |
|---------|-------------|
| `docker compose ps` | List compose services |
| `docker compose logs` | View compose logs |
| `docker compose config` | Validate and view config |
| `docker compose images` | List images used |

---

## 6.0 Kubernetes (kubectl)

### 6.1 Resource Information

| Command | Description |
|---------|-------------|
| `kubectl get pods` | List pods |
| `kubectl get pods -A` | All namespaces |
| `kubectl get deployments` | List deployments |
| `kubectl get services` | List services |
| `kubectl get nodes` | List nodes |
| `kubectl get all` | List all resources |
| `kubectl get events` | Cluster events |

### 6.2 Details & Logs

| Command | Description |
|---------|-------------|
| `kubectl describe pod <name>` | Pod details |
| `kubectl describe node <name>` | Node details |
| `kubectl logs <pod>` | Pod logs |
| `kubectl logs -f <pod>` | Follow pod logs |
| `kubectl logs <pod> -c <container>` | Specific container logs |
| `kubectl top pods` | Pod resource usage |
| `kubectl top nodes` | Node resource usage |

### 6.3 Config & Context

| Command | Description |
|---------|-------------|
| `kubectl config view` | View kubeconfig |
| `kubectl config current-context` | Current context |
| `kubectl config get-contexts` | List contexts |
| `kubectl cluster-info` | Cluster info |
| `kubectl api-resources` | Available API resources |

---

## 7.0 System / Linux

### 7.1 Process & Resource

| Command | Description |
|---------|-------------|
| `ps aux` | List all processes |
| `ps aux \| grep <name>` | Find specific process |
| `top` | Real-time process monitor |
| `htop` | Interactive process monitor |
| `free -h` | Memory usage |
| `df -h` | Disk usage |
| `du -sh <dir>` | Directory size |
| `uptime` | System uptime |
| `who` | Logged in users |
| `w` | User activity |

### 7.2 Network

| Command | Description |
|---------|-------------|
| `netstat -tlnp` | Listening ports |
| `ss -tlnp` | Listening ports (modern) |
| `lsof -i :<port>` | Process using port |
| `curl -I <url>` | HTTP headers only |
| `curl -v <url>` | Verbose request |
| `ping <host>` | Test connectivity |
| `traceroute <host>` | Trace network path |
| `dig <domain>` | DNS lookup |
| `nslookup <domain>` | DNS lookup |
| `host <domain>` | DNS lookup |
| `ip addr` | Network interfaces |
| `ip route` | Routing table |

### 7.3 File System

| Command | Description |
|---------|-------------|
| `ls -la` | List files with details |
| `tree` | Directory tree |
| `tree -L 2` | Tree with depth limit |
| `file <file>` | File type info |
| `stat <file>` | File metadata |
| `wc -l <file>` | Line count |
| `head <file>` | First 10 lines |
| `tail <file>` | Last 10 lines |
| `tail -f <file>` | Follow file changes |

### 7.4 System Info

| Command | Description |
|---------|-------------|
| `uname -a` | System info |
| `hostname` | Machine hostname |
| `whoami` | Current user |
| `id` | User ID and groups |
| `env` | Environment variables |
| `printenv` | Environment variables |
| `which <cmd>` | Command location |
| `type <cmd>` | Command type |

---

## 8.0 Database Clients

### 8.1 PostgreSQL (psql)

| Command | Description |
|---------|-------------|
| `\l` | List databases |
| `\dt` | List tables |
| `\d <table>` | Describe table |
| `\dn` | List schemas |
| `\du` | List users/roles |
| `\di` | List indexes |
| `\df` | List functions |
| `\conninfo` | Connection info |
| `SELECT version();` | PostgreSQL version |
| `SELECT * FROM pg_stat_activity;` | Active connections |

### 8.2 MySQL

| Command | Description |
|---------|-------------|
| `SHOW DATABASES;` | List databases |
| `SHOW TABLES;` | List tables |
| `DESCRIBE <table>;` | Table structure |
| `SHOW INDEX FROM <table>;` | Table indexes |
| `SHOW PROCESSLIST;` | Active connections |
| `SHOW STATUS;` | Server status |
| `SELECT VERSION();` | MySQL version |

### 8.3 Redis (redis-cli)

| Command | Description |
|---------|-------------|
| `INFO` | Server info |
| `DBSIZE` | Key count |
| `KEYS *` | List all keys (use carefully) |
| `SCAN 0` | Iterate keys safely |
| `TYPE <key>` | Key type |
| `TTL <key>` | Key expiration |
| `GET <key>` | Get string value |
| `HGETALL <key>` | Get hash value |
| `LRANGE <key> 0 -1` | Get list values |
| `CLIENT LIST` | Connected clients |

---

## 9.0 Terraform

| Command | Description |
|---------|-------------|
| `terraform plan` | Preview changes |
| `terraform show` | Show current state |
| `terraform state list` | List resources in state |
| `terraform state show <resource>` | Resource details |
| `terraform output` | Show outputs |
| `terraform validate` | Validate configuration |
| `terraform graph` | Generate dependency graph |
| `terraform providers` | List providers |
| `terraform version` | Terraform version |

---

## 10.0 GitHub CLI (gh)

### 10.1 Repository

| Command | Description |
|---------|-------------|
| `gh repo view` | View current repo |
| `gh repo view <owner/repo>` | View specific repo |
| `gh repo list` | List your repos |
| `gh repo list <org>` | List org repos |

### 10.2 Issues & PRs

| Command | Description |
|---------|-------------|
| `gh issue list` | List issues |
| `gh issue view <number>` | View issue |
| `gh pr list` | List pull requests |
| `gh pr view <number>` | View PR |
| `gh pr diff <number>` | View PR diff |
| `gh pr checks <number>` | View PR checks |
| `gh pr status` | Your PR status |

### 10.3 Actions & Releases

| Command | Description |
|---------|-------------|
| `gh run list` | List workflow runs |
| `gh run view <run-id>` | View run details |
| `gh run view --log <run-id>` | View run logs |
| `gh release list` | List releases |
| `gh release view <tag>` | View release |

### 10.4 API

| Command | Description |
|---------|-------------|
| `gh api repos/<owner>/<repo>` | Get repo via API |
| `gh api repos/<owner>/<repo>/issues` | Get issues via API |
| `gh api user` | Get authenticated user |

---

## 11.0 tmux

| Command | Description |
|---------|-------------|
| `tmux list-sessions` | List sessions |
| `tmux list-windows` | List windows |
| `tmux list-panes` | List panes |
| `tmux show-options` | Show options |
| `tmux info` | Server info |
| `tmux display-message -p '#{...}'` | Query tmux variables |

---

## 12.0 Make

| Command | Description |
|---------|-------------|
| `make -n <target>` | Dry-run (show commands) |
| `make -p` | Print database |
| `make --version` | Make version |

---

## 13.0 jq (JSON Processing)

| Command | Description |
|---------|-------------|
| `jq '.'` | Pretty print JSON |
| `jq '.key'` | Extract key |
| `jq '.[]'` | Iterate array |
| `jq 'keys'` | List keys |
| `jq 'length'` | Count items |
| `jq 'type'` | Get type |

---

## 14.0 Quick Reference by Category

### Read-Only AWS Operations
```bash
# Logs
aws logs tail /aws/lambda/my-function --follow

# Resources
aws ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name}'
aws s3 ls s3://my-bucket --recursive --summarize
aws lambda list-functions --query 'Functions[].FunctionName'

# Identity
aws sts get-caller-identity
aws iam get-user
```

### Git Inspection
```bash
# Status check
git status && git log --oneline -5

# Branch comparison
git diff main...feature-branch --stat

# Find changes
git log --oneline --all --grep="fix"
```

### Container Debugging
```bash
# Docker
docker logs -f --tail 100 my-container
docker stats --no-stream

# Kubernetes
kubectl logs -f deployment/my-app
kubectl top pods --sort-by=memory
```

---

## 15.0 Commands to Avoid (Destructive)

These commands **modify state** and should be used carefully:

| Category | Destructive Commands |
|----------|---------------------|
| **AWS** | `aws s3 rm`, `aws ec2 terminate-instances`, `aws lambda delete-function`, `aws cloudformation delete-stack` |
| **Git** | `git reset --hard`, `git push --force`, `git clean -fd`, `git rebase` (on shared branches) |
| **Docker** | `docker rm`, `docker rmi`, `docker system prune`, `docker volume rm` |
| **K8s** | `kubectl delete`, `kubectl apply`, `kubectl rollout restart` |
| **npm** | `npm install` (modifies node_modules), `npm uninstall`, `npm update` |
| **pip** | `pip install`, `pip uninstall` |
| **System** | `rm`, `mv`, `chmod`, `chown`, `kill` |

---

[END OF SAFE CLI COMMANDS REFERENCE]
