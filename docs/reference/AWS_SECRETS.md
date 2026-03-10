# AWS Secrets Manager Reference

## Account: protoflow (default)

**AWS Account ID:** `502455296080`
**Region:** `us-east-1`
**Profile:** default

| Name | ARN | Description |
|------|-----|-------------|
| `dev/Rhythm` | `arn:aws:secretsmanager:us-east-1:502455296080:secret:dev/Rhythm-M8MEzn` | RDS Postgres user login |
| `dev/Rhythm/Postgres` | `arn:aws:secretsmanager:us-east-1:502455296080:secret:dev/Rhythm/Postgres-oSAeiV` | - |
| `/bp-front/env` | `arn:aws:secretsmanager:us-east-1:502455296080:secret:/bp-front/env-FpLgiL` | - |
| `/bodypilot/env` | `arn:aws:secretsmanager:us-east-1:502455296080:secret:/bodypilot/env-ZYKJGx` | - |
| `rds!db-b24bfc97-...` | `arn:aws:secretsmanager:us-east-1:502455296080:secret:rds!db-b24bfc97-fde0-40ec-9cf3-a34e2de1f719-H9iqMf` | Primary RDS DB instance (protoflow-dev) |
| `cloudfront-auth/google-oauth` | `arn:aws:secretsmanager:us-east-1:502455296080:secret:cloudfront-auth/google-oauth-cEa6W7` | Google OAuth client credentials |

---

## Account: supabase

**AWS Account ID:** `507745175693`
**Region:** `us-east-1`
**Profile:** supabase

| Name | ARN | Description |
|------|-----|-------------|
| `mo-app/expo-token` | `arn:aws:secretsmanager:us-east-1:507745175693:secret:mo-app/expo-token-IT6PiN` | Expo EAS token for Mo app builds |
| `sonicui/openai-api-key` | `arn:aws:secretsmanager:us-east-1:507745175693:secret:sonicui/openai-api-key-tKoNEP` | OpenAI API key for SonicUI transcription |
| `mo/resend-api-key` | `arn:aws:secretsmanager:us-east-1:507745175693:secret:mo/resend-api-key-oP9Zge` | Resend API key for Mo voice notes email notifications |
| `gocoder-dev-test-user-credentials` | `arn:aws:secretsmanager:us-east-1:507745175693:secret:gocoder-dev-test-user-credentials-Rtemva` | Test user credentials for GoCoder smoke tests |
| `gocoder/anthropic-api-key` | `arn:aws:secretsmanager:us-east-1:507745175693:secret:gocoder/anthropic-api-key-DJKfj9` | Anthropic API key for GoCoder |
| `openrouter/api-key` | `arn:aws:secretsmanager:us-east-1:507745175693:secret:openrouter/api-key-ZN9zFn` | OpenRouter API key for LLM access |
| `cloudfront-auth/google-oauth` | `arn:aws:secretsmanager:us-east-1:507745175693:secret:cloudfront-auth/google-oauth-CQsk41` | Google OAuth client credentials |
| `github-oauth` | `arn:aws:secretsmanager:us-east-1:507745175693:secret:github-oauth-vKimzj` | GitHub OAuth client credentials |

---

## Usage

```bash
# List all secrets (default account)
aws secretsmanager list-secrets --query 'SecretList[*].[Name,ARN]' --output table

# List secrets (supabase account)
AWS_PROFILE=supabase aws secretsmanager list-secrets --query 'SecretList[*].[Name,ARN]' --output table

# Get a secret value
aws secretsmanager get-secret-value --secret-id <secret-name> --query 'SecretString' --output text | jq .
```

## Related Infrastructure

- **CloudFront Auth:** Uses `cloudfront-auth/google-oauth` for Google OAuth signed cookies
- **RDS:** `protoflow-dev` database uses the `rds!db-*` managed secret
- **Rhythm App:** Uses `dev/Rhythm` and `dev/Rhythm/Postgres` for database access
- **GoCoder:** Uses `gocoder/anthropic-api-key` for AI, `gocoder-dev-test-user-credentials` for tests
- **Mo App:** Uses `mo-app/expo-token` for builds, `mo/resend-api-key` for email
