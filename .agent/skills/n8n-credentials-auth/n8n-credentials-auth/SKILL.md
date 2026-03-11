---
name: n8n-credentials-auth
description: Credential types, OAuth flows, API key management, and authentication security in n8n. Use when configuring credentials for integrations, setting up OAuth, managing API keys, or understanding how n8n stores and encrypts secrets.
---

# n8n Credentials & Authentication — Complete Reference

How to configure, manage, and secure credentials in n8n.

**Source**: https://docs.n8n.io/credentials/

---

## 1. Credential System Overview

### How Credentials Work in n8n

- Credentials are **stored encrypted** in the n8n database
- Encryption uses `N8N_ENCRYPTION_KEY` (auto-generated or user-set)
- Credentials are **never exposed** in workflow JSON exports by default
- Each credential type has a specific schema (required/optional fields)
- Credentials are **shared** across workflows that need them

### Credential Storage

```
┌─────────────────────────┐
│  n8n Credential Store   │
│  (AES-256 encrypted)    │
│                         │
│  ┌───────────────────┐  │
│  │ API Keys          │  │
│  │ OAuth Tokens      │  │
│  │ DB Passwords      │  │
│  │ SSH Keys          │  │
│  └───────────────────┘  │
│                         │
│  Key: N8N_ENCRYPTION_KEY│
└─────────────────────────┘
```

---

## 2. Credential Types

### API Key Authentication

**Most common type**. Used by REST APIs.

```javascript
// Header Auth
{
  "type": "httpHeaderAuth",
  "data": {
    "name": "Authorization",       // Header name
    "value": "Bearer sk-abc123..."  // Header value
  }
}

// Query Parameter Auth
{
  "type": "httpQueryAuth",
  "data": {
    "name": "api_key",
    "value": "abc123..."
  }
}
```

**Common services**: OpenAI, Stripe, SendGrid, Twilio, etc.

### Basic Authentication

```javascript
{
  "type": "httpBasicAuth",
  "data": {
    "user": "username",
    "password": "password"
  }
}
```

### Digest Authentication

```javascript
{
  "type": "httpDigestAuth",
  "data": {
    "user": "username",
    "password": "password"
  }
}
```

### OAuth2

**Used by**: Google, Microsoft, Slack, GitHub, etc.

**Setup Steps**:
1. **Create app** in service provider (e.g., Google Cloud Console)
2. **Get Client ID and Client Secret**
3. **Set callback URL** in provider: `https://your-n8n.com/rest/oauth2-credential/callback`
4. **Configure credential** in n8n with Client ID + Secret
5. **Click "Connect"** button to authorize

```javascript
{
  "type": "oAuth2Api",
  "data": {
    "clientId": "your-client-id",
    "clientSecret": "your-client-secret",
    "accessTokenUrl": "https://oauth2.googleapis.com/token",
    "authUrl": "https://accounts.google.com/o/oauth2/v2/auth",
    "scope": "https://www.googleapis.com/auth/spreadsheets",
    "authQueryParameters": "",
    "grantType": "authorizationCode"
  }
}
```

**OAuth2 Callback URL Format**:
```
https://your-n8n-domain.com/rest/oauth2-credential/callback
```

### OAuth1

**Used by**: Twitter/X (legacy)

```javascript
{
  "type": "oAuth1Api",
  "data": {
    "consumerKey": "...",
    "consumerSecret": "...",
    "requestTokenUrl": "...",
    "authorizationUrl": "...",
    "accessTokenUrl": "...",
    "signatureMethod": "HMAC-SHA1"
  }
}
```

### Service-Specific Credentials

Most integration nodes have dedicated credential types:

| Service | Credential Type | Auth Method |
|---------|----------------|-------------|
| **Slack** | `slackApi` | OAuth2 or Bot Token |
| **Google Sheets** | `googleSheetsOAuth2Api` | OAuth2 |
| **GitHub** | `githubApi` | Personal Access Token |
| **PostgreSQL** | `postgres` | Username/Password |
| **MySQL** | `mySql` | Username/Password |
| **MongoDB** | `mongoDb` | Connection String |
| **OpenAI** | `openAiApi` | API Key |
| **AWS** | `aws` | Access Key + Secret Key |
| **Azure** | Various | Client ID/Secret + Tenant |
| **SMTP** | `smtp` | Username/Password + Host |
| **SSH** | `sshPassword` or `sshPrivateKey` | Password or Private Key |
| **FTP** | `ftp` | Username/Password + Host |

---

## 3. Creating Credentials

### Via UI

1. Go to **Credentials** in left sidebar
2. Click **Add Credential**
3. Search for credential type
4. Fill in required fields
5. Click **Save** (or **Connect** for OAuth)

### Via API

```bash
POST /api/v1/credentials
Content-Type: application/json
X-N8N-API-KEY: your-api-key

{
  "name": "My OpenAI API Key",
  "type": "openAiApi",
  "data": {
    "apiKey": "sk-..."
  }
}
```

### In Workflow Nodes

1. Open node that needs credentials
2. Click **Credential** dropdown
3. Select existing or click **Create New**
4. Fill in the form
5. Test connection if available

---

## 4. HTTP Request Node Authentication

### Predefined Credential Types

```javascript
{
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "openAiApi"  // Uses existing n8n credential type
}
```

### Generic Credential Types

```javascript
// Header Auth
{
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth"
}

// Basic Auth
{
  "authentication": "genericCredentialType",
  "genericAuthType": "httpBasicAuth"
}

// Query Param Auth
{
  "authentication": "genericCredentialType",
  "genericAuthType": "httpQueryAuth"
}

// Digest Auth
{
  "authentication": "genericCredentialType",
  "genericAuthType": "httpDigestAuth"
}

// OAuth2
{
  "authentication": "genericCredentialType",
  "genericAuthType": "oAuth2Api"
}

// No Auth
{
  "authentication": "none"
}
```

---

## 5. Credential Security

### Encryption

- All credentials encrypted with **AES-256-CBC**
- Key: `N8N_ENCRYPTION_KEY` environment variable
- If not set: auto-generated on first start, stored in `~/.n8n/config`

### ⚠️ Critical: Backup Your Encryption Key

```bash
# Check your encryption key
echo $N8N_ENCRYPTION_KEY

# Or find in config
cat ~/.n8n/config | grep encryptionKey

# BACKUP THIS VALUE SECURELY!
# Without it, all credentials are permanently lost
```

### Credential Sharing

| Feature | Community (Free) | Enterprise |
|---------|------------------|------------|
| Owner access | ✅ | ✅ |
| Share with users | ❌ | ✅ |
| Project-level sharing | ❌ | ✅ |
| Role-based access | ❌ | ✅ |

### Export/Import Security

```bash
# Export credentials (encrypted with current key)
n8n export:credentials --all --output=creds.json

# Import credentials (REQUIRES SAME encryption key!)
n8n import:credentials --input=creds.json

# ⚠️ Different encryption key = import fails!
```

### Environment Variable Credentials

```javascript
// Access env vars in expressions
{{ $env.API_KEY }}

// Block env access for security:
N8N_BLOCK_ENV_ACCESS_IN_NODE=true
```

---

## 6. Credential Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "Credential not found" | Credential deleted or not shared | Re-create credential |
| "Invalid credentials" | Wrong API key/expired token | Update credential values |
| OAuth "redirect_uri_mismatch" | Wrong callback URL in provider | Set to `https://your-n8n/rest/oauth2-credential/callback` |
| "Cannot decrypt credentials" | Wrong encryption key | Restore correct `N8N_ENCRYPTION_KEY` |
| OAuth token expired | Token not auto-refreshing | Re-connect OAuth credential |
| SSL certificate error | Self-signed cert | Set `NODE_TLS_REJECT_UNAUTHORIZED=0` (dev only!) |

### Testing Credentials

1. Open credential editor
2. Click **Test** button (if available)
3. Check for green success message
4. If failing: verify all required fields, API key validity, network access

### OAuth Troubleshooting

1. **Callback URL**: Must match EXACTLY in both n8n and provider
2. **Scopes**: Ensure required scopes are requested
3. **App status**: Some providers require app review before prod use
4. **Token refresh**: n8n auto-refreshes OAuth2 tokens
5. **HTTP vs HTTPS**: Most OAuth2 providers require HTTPS callback

---

## 7. Credential Patterns

### Pattern: Multi-Environment Credentials

```
Production:
  Credential: "Stripe - Production"
  API Key: sk_live_xxx

Staging:
  Credential: "Stripe - Staging"
  API Key: sk_test_xxx

Workflows use appropriate credential per environment.
```

### Pattern: Rotating API Keys

```
1. Create new credential with new key
2. Update workflow to use new credential
3. Test workflow
4. Delete old credential
5. Revoke old key in provider
```

### Pattern: Credential via Environment Variables

```bash
# In environment
OPENAI_API_KEY=sk-xxx
SLACK_BOT_TOKEN=xoxb-xxx

# In n8n credential, reference env var
# (only works if N8N_BLOCK_ENV_ACCESS_IN_NODE is false)
```

---

## Related Skills

- **n8n-self-hosted-admin** — Encryption key management and security
- **n8n-api-reference** — Credentials API endpoints
- **n8n-node-configuration** — Authentication in HTTP Request nodes
- **n8n-best-practices** — Security best practices

---

**Documentation Source**: https://docs.n8n.io/credentials/
