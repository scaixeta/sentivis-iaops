---
name: n8n-api-reference
description: n8n REST API reference for programmatic workflow management, execution control, credential handling, and automation. Use when building integrations with n8n, automating workflow deployment, or managing n8n instances programmatically.
---

# n8n REST API — Complete Reference

Programmatic control of n8n instances via REST API.

**Source**: https://docs.n8n.io/api/

---

## 1. Authentication

### API Key Authentication

**Generate API Key**: Settings → API → Create API Key

**Usage**:
```bash
# Header authentication (recommended)
curl -H "X-N8N-API-KEY: your-api-key" \
  https://your-n8n.com/api/v1/workflows

# Query parameter (not recommended)
curl "https://your-n8n.com/api/v1/workflows?apiKey=your-api-key"
```

### Base URL

```
https://your-n8n-instance.com/api/v1/
```

---

## 2. Workflows API

### List All Workflows

```bash
GET /api/v1/workflows

# With filters
GET /api/v1/workflows?active=true
GET /api/v1/workflows?tags=production
GET /api/v1/workflows?limit=10&cursor=next-page-cursor
```

**Response**:
```json
{
  "data": [
    {
      "id": "1",
      "name": "My Workflow",
      "active": true,
      "createdAt": "2024-01-01T00:00:00.000Z",
      "updatedAt": "2024-01-02T00:00:00.000Z",
      "tags": [{"id": "1", "name": "production"}]
    }
  ],
  "nextCursor": "next-page-cursor"
}
```

### Get Workflow by ID

```bash
GET /api/v1/workflows/:id
```

### Create Workflow

```bash
POST /api/v1/workflows
Content-Type: application/json

{
  "name": "New Workflow",
  "nodes": [
    {
      "parameters": {},
      "name": "Start",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "values": {
          "string": [{"name": "message", "value": "Hello"}]
        }
      },
      "name": "Set",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [460, 300]
    }
  ],
  "connections": {
    "Start": {
      "main": [[{"node": "Set", "type": "main", "index": 0}]]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

### Update Workflow

```bash
PUT /api/v1/workflows/:id
Content-Type: application/json

{
  "name": "Updated Workflow",
  "nodes": [...],
  "connections": {...},
  "settings": {...}
}
```

### Delete Workflow

```bash
DELETE /api/v1/workflows/:id
```

### Activate/Deactivate Workflow

```bash
POST /api/v1/workflows/:id/activate
POST /api/v1/workflows/:id/deactivate
```

### Transfer Workflow (between users)

```bash
PUT /api/v1/workflows/:id/transfer
Content-Type: application/json

{"destinationProjectId": "project-id"}
```

---

## 3. Executions API

### List Executions

```bash
GET /api/v1/executions

# With filters
GET /api/v1/executions?status=error
GET /api/v1/executions?status=success
GET /api/v1/executions?status=waiting
GET /api/v1/executions?workflowId=1
GET /api/v1/executions?limit=20&cursor=next-page-cursor
```

### Get Execution by ID

```bash
GET /api/v1/executions/:id

# Include execution data (full node outputs)
GET /api/v1/executions/:id?includeData=true
```

### Delete Execution

```bash
DELETE /api/v1/executions/:id
```

### Retry Failed Execution

```bash
POST /api/v1/executions/:id/retry
```

---

## 4. Credentials API

### List Credentials

```bash
GET /api/v1/credentials
```

### Get Credential by ID

```bash
GET /api/v1/credentials/:id
# Note: Credential values (secrets) are not returned
```

### Create Credential

```bash
POST /api/v1/credentials
Content-Type: application/json

{
  "name": "My API Key",
  "type": "httpHeaderAuth",
  "data": {
    "name": "Authorization",
    "value": "Bearer my-secret-token"
  }
}
```

### Delete Credential

```bash
DELETE /api/v1/credentials/:id
```

### Get Credential Schema

```bash
GET /api/v1/credentials/schema/:credentialType
```

---

## 5. Tags API

### List Tags

```bash
GET /api/v1/tags
```

### Create Tag

```bash
POST /api/v1/tags
Content-Type: application/json

{"name": "production"}
```

### Update Tag

```bash
PUT /api/v1/tags/:id
Content-Type: application/json

{"name": "staging"}
```

### Delete Tag

```bash
DELETE /api/v1/tags/:id
```

---

## 6. Users API

### List Users

```bash
GET /api/v1/users
```

### Get Current User

```bash
GET /api/v1/users/me
```

---

## 7. Source Control API

### Pull from Source Control

```bash
POST /api/v1/source-control/pull
Content-Type: application/json

{"force": false}
```

### Push to Source Control

```bash
POST /api/v1/source-control/push
Content-Type: application/json

{"message": "Deploy v1.2.3"}
```

---

## 8. Webhook Programmatic Access

### Execute via Webhook

```bash
# Production webhook
POST https://your-n8n.com/webhook/<path>
Content-Type: application/json

{"key": "value"}

# Test webhook (only when workflow is open in editor)
POST https://your-n8n.com/webhook-test/<path>
Content-Type: application/json

{"key": "value"}
```

---

## 9. Common API Patterns

### Automated Deployment Pipeline

```bash
#!/bin/bash
# Deploy workflow from file to n8n instance

API_KEY="your-api-key"
N8N_URL="https://your-n8n.com/api/v1"
WORKFLOW_FILE="workflow.json"

# Read workflow JSON
WORKFLOW=$(cat $WORKFLOW_FILE)

# Create or update workflow
WORKFLOW_ID=$(echo $WORKFLOW | jq -r '.id // empty')

if [ -z "$WORKFLOW_ID" ]; then
  # Create new
  curl -X POST "$N8N_URL/workflows" \
    -H "X-N8N-API-KEY: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$WORKFLOW"
else
  # Update existing
  curl -X PUT "$N8N_URL/workflows/$WORKFLOW_ID" \
    -H "X-N8N-API-KEY: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$WORKFLOW"
fi

# Activate
curl -X POST "$N8N_URL/workflows/$WORKFLOW_ID/activate" \
  -H "X-N8N-API-KEY: $API_KEY"
```

### Monitor Failed Executions

```bash
#!/bin/bash
# Check for failed executions in the last hour

API_KEY="your-api-key"
N8N_URL="https://your-n8n.com/api/v1"

FAILURES=$(curl -s "$N8N_URL/executions?status=error&limit=10" \
  -H "X-N8N-API-KEY: $API_KEY" | jq '.data | length')

if [ "$FAILURES" -gt 0 ]; then
  echo "⚠️ Found $FAILURES failed executions"
  curl -s "$N8N_URL/executions?status=error&limit=10" \
    -H "X-N8N-API-KEY: $API_KEY" | jq '.data[] | {id, workflowId, stoppedAt}'
fi
```

### Bulk Export Workflows

```bash
#!/bin/bash
# Export all workflows to individual JSON files

API_KEY="your-api-key"
N8N_URL="https://your-n8n.com/api/v1"

WORKFLOWS=$(curl -s "$N8N_URL/workflows" \
  -H "X-N8N-API-KEY: $API_KEY")

echo "$WORKFLOWS" | jq -c '.data[]' | while read -r workflow; do
  ID=$(echo "$workflow" | jq -r '.id')
  NAME=$(echo "$workflow" | jq -r '.name' | sed 's/ /_/g')

  curl -s "$N8N_URL/workflows/$ID" \
    -H "X-N8N-API-KEY: $API_KEY" > "exports/${NAME}_${ID}.json"

  echo "Exported: $NAME ($ID)"
done
```

---

## 10. Rate Limits & Best Practices

### API Best Practices

1. ✅ Use API keys (not basic auth)
2. ✅ Store keys in environment variables
3. ✅ Use pagination for large result sets
4. ✅ Handle rate limiting with exponential backoff
5. ✅ Cache workflow definitions locally
6. ❌ Don't hardcode API keys in scripts
7. ❌ Don't poll executions too frequently
8. ❌ Don't trust returned credential values (they're masked)

### Error Responses

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (invalid API key) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 500 | Internal Server Error |

---

**Documentation Source**: https://docs.n8n.io/api/
