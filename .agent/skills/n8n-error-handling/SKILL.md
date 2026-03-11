---
name: n8n-error-handling
description: Error handling patterns for n8n workflows including error workflows, Error Trigger, Stop And Error, Continue On Fail, retry logic, and production error monitoring. Use when implementing error handling, building error workflows, debugging failed executions, or setting up alerting.
---

# n8n Error Handling — Complete Reference

Production-grade error handling patterns for n8n workflows.

**Source**: https://docs.n8n.io/flow-logic/error-handling/

---

## 1. Error Handling Overview

### Error Handling Mechanisms

| Mechanism | Scope | Purpose |
|-----------|-------|---------|
| **Error Workflow** | Workflow-level | Runs separate workflow on failure |
| **Error Trigger** | Node in error workflow | Receives error data |
| **Stop And Error** | Node in main workflow | Force deliberate failure |
| **Continue On Fail** | Per-node setting | Prevent node from stopping workflow |
| **Retry On Fail** | Per-node setting | Auto-retry failed node |
| **Always Output Data** | Per-node setting | Output data even on failure |
| **Try/Catch in Code** | Code node | Handle errors in custom code |

---

## 2. Error Workflows

### Creating an Error Workflow

**Step 1**: Create a new workflow with Error Trigger as first node:

```
Error Trigger → Set (format error) → Slack/Email (send alert)
```

**Step 2**: Configure alert message:

```javascript
// In Set node, format the error notification
{
  "errorMessage": "={{$json.execution.error.message}}",
  "workflowName": "={{$json.workflow.name}}",
  "executionId": "={{$json.execution.id}}",
  "executionUrl": "={{$json.execution.url}}",
  "failedNode": "={{$json.execution.lastNodeExecuted}}",
  "mode": "={{$json.execution.mode}}",
  "timestamp": "={{$now.toISO()}}"
}
```

**Step 3**: Assign to main workflow:
1. Main workflow → **Options → Settings**
2. **Error workflow** → select your error handler
3. Save

### Error Trigger Data Structure

**Standard execution error**:
```json
[
  {
    "execution": {
      "id": "231",
      "url": "https://n8n.example.com/execution/231",
      "retryOf": "34",
      "error": {
        "message": "Example Error Message",
        "stack": "Stacktrace"
      },
      "lastNodeExecuted": "Node With Error",
      "mode": "manual"
    },
    "workflow": {
      "id": "1",
      "name": "Example Workflow"
    }
  }
]
```

**Trigger node activation error** (different structure):
```json
{
  "trigger": {
    "error": {
      "context": {},
      "name": "WorkflowActivationError",
      "cause": {
        "message": "Connection refused",
        "stack": "Error: connect ECONNREFUSED..."
      },
      "timestamp": 1654609328787,
      "message": "Workflow could not be activated",
      "node": {
        "name": "Webhook",
        "type": "n8n-nodes-base.webhook"
      }
    },
    "mode": "trigger"
  },
  "workflow": {
    "id": "5",
    "name": "My Webhook Workflow"
  }
}
```

### Error Data Fields

| Field | Available | Description |
|-------|-----------|-------------|
| `execution.id` | When saved to DB | Execution identifier |
| `execution.url` | When saved to DB | Direct link to execution |
| `execution.retryOf` | On retries only | ID of original failed execution |
| `execution.error.message` | Always | Human-readable error |
| `execution.error.stack` | Always | Stack trace |
| `execution.lastNodeExecuted` | Always | Node that failed |
| `execution.mode` | Always | `manual`, `trigger`, `webhook` |
| `workflow.id` | Always | Workflow identifier |
| `workflow.name` | Always | Workflow name |

---

## 3. Stop And Error Node

### Purpose

Force a workflow to fail deliberately under your conditions. This triggers the error workflow.

### Use Cases

- **Validation failures**: Missing required data
- **Business rule violations**: Invalid amounts, unauthorized access
- **Threshold exceeded**: Rate limits, quotas
- **Data integrity checks**: Mismatched records

### Configuration

```javascript
{
  "errorType": "message",                    // "message" or "object"
  "message": "Validation failed: email is required"
}
```

### Pattern: Validation → Stop And Error

```
Webhook → IF (email exists?)
           → [Yes] → Continue processing
           → [No]  → Stop And Error ("Missing email")
                     → triggers Error Workflow
```

```
Trigger → Code (validate) → IF (valid?)
                              → [Yes] → Process
                              → [No]  → Stop And Error
```

---

## 4. Per-Node Error Settings

### Continue On Fail

**Location**: Node Settings → On Error → Continue On Fail

**What it does**: Node errors don't stop the workflow. Error data is passed as output.

**Error output format**:
```json
[
  {
    "json": {
      "error": {
        "message": "404 Not Found",
        "description": "The requested resource was not found"
      }
    }
  }
]
```

**Pattern**: Handle errors inline
```
HTTP Request (Continue On Fail) → IF (has error?)
                                   → [Yes] → Log error → Fallback action
                                   → [No]  → Process response
```

### Retry On Fail

**Location**: Node Settings → On Error → Retry On Fail

**Configuration**:
- **Max Retries**: Number of retry attempts (1-5)
- **Wait Between**: Milliseconds between retries (0-5000)

**Use for**: Transient errors (network timeouts, rate limits, temporary unavailability).

### Always Output Data

**Location**: Node Settings → Always Output Data

**What it does**: If a node returns no output data, it creates an empty item instead of stalling the workflow.

---

## 5. Code Node Error Handling

### Try/Catch Pattern

```javascript
try {
  const response = await $helpers.httpRequest({
    method: 'POST',
    url: 'https://api.example.com/data',
    body: { name: $json.body.name }
  });

  return [{
    json: {
      success: true,
      data: response,
      timestamp: new Date().toISOString()
    }
  }];
} catch (error) {
  return [{
    json: {
      success: false,
      error: error.message,
      statusCode: error.statusCode || 500,
      timestamp: new Date().toISOString()
    }
  }];
}
```

### Validation with Explicit Errors

```javascript
const items = $input.all();

if (!items || items.length === 0) {
  throw new Error('No input data received');
}

const data = items[0].json;

if (!data.email) {
  throw new Error('Missing required field: email');
}

if (!data.email.includes('@')) {
  throw new Error(`Invalid email format: ${data.email}`);
}

// Continue processing...
return [{json: {validated: true, ...data}}];
```

### Batch Error Handling

```javascript
const items = $input.all();
const results = [];
const errors = [];

for (const item of items) {
  try {
    const processed = transformItem(item.json);
    results.push({ json: { ...processed, status: 'success' } });
  } catch (error) {
    errors.push({
      json: {
        originalItem: item.json,
        error: error.message,
        status: 'failed'
      }
    });
  }
}

// Return both successes and failures
return [...results, ...errors];
```

---

## 6. Production Error Handling Patterns

### Pattern 1: Centralized Error Handler

```
Error Workflow:
  Error Trigger
    → Set (format error data)
    → Switch (by severity)
      → [Critical] → PagerDuty + Slack #alerts
      → [Warning]  → Slack #warnings
      → [Info]     → Log to database
```

### Pattern 2: Self-Healing Retry

```
Main Workflow:
  Trigger → HTTP Request (Retry: 3, Wait: 2000ms, Continue On Fail)
    → IF (success?)
      → [Yes] → Process
      → [No]  → Wait 30s → Execute Sub-workflow (same logic)
                           → IF (still failed?)
                             → [Yes] → Stop And Error
                             → [No]  → Process
```

### Pattern 3: Dead Letter Queue

```
Main Workflow:
  Trigger → Process (Continue On Fail)
    → IF (has error?)
      → [Yes] → Postgres (insert into dead_letter_queue)
               → Slack (notify about failed item)
      → [No]  → Continue normal flow
```

### Pattern 4: Circuit Breaker

```javascript
// In Code node: Check error count before proceeding
const errorCount = $node["Count Errors"].json.count || 0;
const threshold = 5;

if (errorCount >= threshold) {
  // Circuit is OPEN - skip processing
  return [{
    json: {
      circuitState: 'OPEN',
      message: `Too many errors (${errorCount}). Skipping.`,
      nextRetry: DateTime.now().plus({minutes: 15}).toISO()
    }
  }];
}

// Circuit is CLOSED - proceed normally
return [{json: {circuitState: 'CLOSED', proceed: true}}];
```

### Pattern 5: Graceful Degradation

```
Trigger → HTTP Request Primary API (Continue On Fail)
  → IF (success?)
    → [Yes] → Use primary data
    → [No]  → HTTP Request Fallback API (Continue On Fail)
              → IF (success?)
                → [Yes] → Use fallback data
                → [No]  → Use cached/default data
```

---

## 7. Investigating Errors

### Execution History

- **Single workflow**: Open workflow → Executions tab
- **All workflows**: Main menu → Executions
- Filter by: status (success/error), date range, workflow

### Execution Debug Mode

1. Open failed execution from Executions list
2. Click "Debug" to load failed data into editor
3. Modify and re-run from the failed node

### Log Streaming (Enterprise)

Stream execution logs to external services:
- Sentry
- Datadog
- Custom HTTP endpoint

---

## 8. Error Handling Checklist

### For Every Production Workflow

- [ ] **Error workflow assigned** in workflow settings
- [ ] **Critical nodes** have Continue On Fail or Retry On Fail
- [ ] **API calls** have retry logic (Retry: 3, Wait: 1000ms)
- [ ] **Validation** before processing (IF nodes or Code validation)
- [ ] **Meaningful error messages** in Stop And Error nodes
- [ ] **Alert routing** in error workflow (Slack/email/PagerDuty)
- [ ] **Error context** includes workflow name, execution ID, failed node
- [ ] **Edge cases** handled (empty data, null values, timeout)

### Error Workflow Template

```
Error Trigger
  → Set Node:
      errorMessage: ={{$json.execution.error.message}}
      workflowName: ={{$json.workflow.name}}
      executionId: ={{$json.execution.id}}
      executionUrl: ={{$json.execution.url}}
      failedNode: ={{$json.execution.lastNodeExecuted}}
      timestamp: ={{$now.toISO()}}

  → Slack Node:
      Channel: #workflow-errors
      Text: |
        🚨 Workflow Error
        Workflow: {{$json.workflowName}}
        Error: {{$json.errorMessage}}
        Failed Node: {{$json.failedNode}}
        Execution: {{$json.executionUrl}}
        Time: {{$json.timestamp}}
```

---

## Related Skills

- **n8n-flow-logic** — Error handling in context of flow control
- **n8n-code-javascript** — Try/catch in Code nodes
- **n8n-workflow-patterns** — Error handling in workflow patterns
- **n8n-node-configuration** — Configure error settings per node

---

**Documentation Source**: https://docs.n8n.io/flow-logic/error-handling/
