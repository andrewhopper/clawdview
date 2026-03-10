# Auth Domain Model

Authentication and authorization domain model for identity, access control, and session management.

## Overview

This domain provides a complete semantic model for:
- **Identity**: Users, service accounts, and principals
- **Access Control**: Roles, permissions, and policies (RBAC + ABAC)
- **Sessions**: Token-based authentication with refresh
- **Credentials**: Multiple auth methods (password, OAuth, certificates, MFA)

## Entities

| Entity | Description |
|--------|-------------|
| `User` | Human user identity |
| `ServiceAccount` | Non-human identity for services |
| `Principal` | Base class for any authenticated entity |
| `Role` | Named collection of permissions |
| `Permission` | Granular access right (`resource:action`) |
| `Policy` | Conditional access rules (ABAC) |
| `Session` | Authenticated session with tokens |
| `Credential` | Authentication mechanism |

## Credential Types

| Type | Description |
|------|-------------|
| `PasswordCredential` | Username/password |
| `TokenCredential` | JWT, API key, bearer token |
| `OAuthCredential` | OAuth 2.0 / OIDC |
| `CertificateCredential` | X.509 / mTLS |
| `MFACredential` | TOTP, SMS, hardware key |

## Actions

### Authentication
- `AuthenticateAction` - Verify credentials, create session
- `RefreshSessionAction` - Exchange refresh token for new access token
- `RevokeSessionAction` - Logout (invalidate session)
- `RevokeAllSessionsAction` - Force logout everywhere

### Authorization
- `AuthorizeAction` - Check permission for action on resource
- `AssignRoleAction` - Grant role to principal
- `RevokeRoleAction` - Remove role from principal

### User Management
- `CreateUserAction` - Register new user
- `DisableUserAction` - Prevent user from logging in
- `ResetPasswordAction` - Change password

## Permission Format

Permissions use `resource:action` format:

```
auth:login          - Can authenticate
auth:logout         - Can revoke own session
auth:refresh        - Can refresh session
auth:check          - Can check authorization
auth:manage_roles   - Can assign/revoke roles
auth:create_user    - Can create new users
auth:admin          - Full admin access
email:send          - Can send email
email:read          - Can read email
```

## Usage

### Generate TypeScript Types

```bash
cd /shared/semantic/tools/generator
npm run generate -- --domain auth --lang typescript
```

### Generated Types

```typescript
// From generated/typescript/auth.types.ts
interface User extends Principal {
  userId: string;
  email: string;
  username: string;
  displayName?: string;
  isActive: boolean;
  createdAt: Date;
  lastLoginAt?: Date;
  roles: Role[];
  credentials: Credential[];
}

interface Session {
  sessionId: string;
  accessToken: string;
  refreshToken: string;
  expiresAt: Date;
  status: SessionStatus;
  ipAddress?: string;
  userAgent?: string;
}

enum SessionStatus {
  Active = 'active',
  Expired = 'expired',
  Revoked = 'revoked',
  Suspended = 'suspended'
}
```

## Files

| File | Purpose |
|------|---------|
| `ontology.ttl` | RDF/OWL entity and action definitions |
| `rules.shacl.ttl` | SHACL validation constraints |
| `version.json` | Metadata and changelog |
| `generated/` | Auto-generated TypeScript/Python/Rust types |

## Standards

- W3C RDF (Resource Description Framework)
- W3C OWL (Web Ontology Language)
- W3C SHACL (Shapes Constraint Language)
- OAuth 2.0 / OpenID Connect alignment
- NIST Digital Identity Guidelines (SP 800-63)
