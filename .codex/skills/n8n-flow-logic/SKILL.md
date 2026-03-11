---
name: n8n-flow-logic
description: Master n8n flow logic including splitting with IF/Switch, merging data, looping, waiting, sub-workflows, error handling, and execution order. Use when designing workflow branching, controlling execution flow, building loops, creating modular sub-workflows, or understanding multi-branch execution behavior.
---

# n8n Flow Logic — Complete Reference

Comprehensive guide to all flow control mechanisms in n8n workflows.

**Source**: https://docs.n8n.io/flow-logic/

---

## 1. Splitting with Conditionals

Splitting turns a single-branch workflow into a multi-branch workflow using conditional logic.

### IF Node (`n8n-nodes-base.if`)

**Purpose**: Binary branching — sends data down one of two paths (true/false).

```
Trigger → IF (condition) → [True branch]
                         → [False branch]
```

**Configuration**:
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.status}}",
        "operation": "equals",
        "value2": "active"
      }
    ]
  }
}
```

**Condition Types Available**:

| Type | Operators |
|------|-----------|
| **String** | equals, notEquals, contains, notContains, startsWith, endsWith, isEmpty, isNotEmpty, regex |
| **Number** | equals, notEquals, greaterThan, lessThan, greaterThanOrEqual, lessThanOrEqual, isEmpty, isNotEmpty |
| **Boolean** | equals, notEquals, isEmpty, isNotEmpty |
| **Date/Time** | after, before, equals |
| **Object** | isEmpty, isNotEmpty |
| **Array** | contains, notContains, lengthEquals, lengthNotEquals, lengthGreaterThan, lengthLessThan, isEmpty, isNotEmpty |

**Combine Conditions**:
- **AND**: All conditions must be true
- **OR**: At least one condition must be true

### Switch Node (`n8n-nodes-base.switch`)

**Purpose**: Multi-way branching — sends data down one of many paths.

```
Trigger → Switch → [Output 0]
                 → [Output 1]
                 → [Output 2]
                 → [Fallback]
```

**Use cases**:
- Route by status: `pending`, `approved`, `rejected`, `cancelled`
- Route by region: `US`, `EU`, `APAC`
- Route by type: `email`, `slack`, `webhook`

**Configuration**:
```javascript
{
  "mode": "rules",
  "rules": {
    "rules": [
      {
        "output": 0,
        "conditions": {
          "string": [{"value1": "={{$json.region}}", "operation": "equals", "value2": "US"}]
        }
      },
      {
        "output": 1,
        "conditions": {
          "string": [{"value1": "={{$json.region}}", "operation": "equals", "value2": "EU"}]
        }
      }
    ],
    "fallbackOutput": 2
  }
}
```

### Decision Guide: IF vs Switch

| Scenario | Use |
|----------|-----|
| Yes/No check | **IF** |
| 2 paths | **IF** |
| 3+ paths | **Switch** |
| Status routing | **Switch** |
| Threshold check | **IF** |
| Category routing | **Switch** |

---

## 2. Merging Data

Combining data from multiple branches back into a single stream.

### Merge Node (`n8n-nodes-base.merge`)

**Modes**:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Append** | Combines all items from both inputs | Collecting results from parallel branches |
| **Combine** | Joins items using matching fields | Enriching data from multiple sources |
| **Choose Branch** | Takes data from one input only | Using IF-like output selection |

**Append Mode**:
```
[Branch 1: items A, B] → Merge (Append) → [items A, B, C, D]
[Branch 2: items C, D] ↗
```

**Combine Mode** (like SQL JOIN):
```javascript
// Inner Join: only matching records
// Left Join: all from Input 1, matching from Input 2
// Outer Join: all records from both
{
  "mode": "combine",
  "mergeByFields": {
    "values": [{"field1": "id", "field2": "userId"}]
  },
  "joinMode": "inner"  // "inner" | "left" | "outer"
}
```

### Compare Datasets Node (`n8n-nodes-base.comparedatasets`)

**Purpose**: Find differences between two datasets.

**Operations**:
- Items that exist only in Input 1
- Items that exist only in Input 2
- Items that exist in both (matching)
- Items that are different between datasets

### Code Node for Custom Merging

```javascript
// Merge data from multiple inputs using Code node
const input1 = $input.all();
const input2 = $node["Other Node"].json;

const merged = input1.map(item => ({
  json: {
    ...item.json,
    enrichedField: input2[item.json.id] || 'not found'
  }
}));

return merged;
```

---

## 3. Looping

### Automatic Looping (Default Behavior)

**n8n automatically loops over all items**. Most nodes process each input item individually without needing explicit loops.

```
Trigger → [5 items] → Slack (sends 5 messages automatically)
```

**Key Concept**: Each item = one execution of the downstream node. No explicit loop needed.

### When to Use Explicit Loops

Use the **Loop Over Items** node (`n8n-nodes-base.splitinbatches`) when:
- Processing items in **batches** (e.g., API rate limits)
- Need to **accumulate results** across iterations
- Working with **node exceptions** that don't auto-loop
- Need **conditional termination** mid-loop

### Loop Over Items Node

```
Trigger → Loop Over Items (batch size: 10) → Process → [back to Loop]
                                                      → [Done output]
```

**Configuration**:
```javascript
{
  "batchSize": 10,     // Items per batch
  "options": {
    "reset": false     // Whether to reset on retry
  }
}
```

### Loop Until Condition Met

```
Start → Do Something → IF (condition met?)
                        → [Yes] → Continue workflow
                        → [No]  → back to "Do Something"
```

**Pattern**: Connect the IF node's "false" output back to a previous node to create a loop.

### Node Exceptions (Require Manual Looping)

These nodes **don't auto-loop** and need the Loop Over Items node:
- **HTTP Request** (with pagination)
- Some **trigger nodes**
- Nodes that perform **batch operations**

### Executing Nodes Once

To run a node only once regardless of input items, use the**"Execute Once"** setting in node settings.

---

## 4. Waiting

### Wait Node (`n8n-nodes-base.wait`)

**Purpose**: Pause workflow execution for a specified time or until a webhook is received.

**Wait Types**:

| Type | Description | Use Case |
|------|-------------|----------|
| **Time interval** | Wait fixed duration | Rate limiting, delays |
| **Specific date/time** | Wait until specific time | Scheduled actions |
| **On webhook call** | Wait until webhook received | External approval flows |

**Time Interval Example**:
```javascript
{
  "resume": "timeInterval",
  "amount": 5,
  "unit": "minutes"    // "seconds" | "minutes" | "hours" | "days"
}
```

**Webhook Wait Example** (approval flows):
```
Start → Send approval email → Wait (on webhook) → Process approved/rejected
```

**⚠️ Important**: Wait node pauses the entire execution. For self-hosted n8n, executions waiting on webhook calls persist in the database.

---

## 5. Sub-workflows

### What Are Sub-workflows?

Sub-workflows let you call one workflow from another, enabling:
- **Modularity**: Break complex workflows into reusable components
- **Memory management**: Avoid memory issues in large workflows
- **Reusability**: Same sub-workflow used by many parent workflows
- **Organization**: Clean separation of concerns

**💡 Sub-workflow executions don't count towards plan execution limits.**

### Setup Pattern

**Parent Workflow**:
```
Trigger → Process → Execute Sub-workflow → Continue
```

**Sub-workflow** (child):
```
Execute Sub-workflow Trigger → Process → End (returns data)
```

### Nodes Used

| Node | Purpose |
|------|---------|
| `Execute Workflow` | Calls another workflow (parent side) |
| `Execute Sub-workflow Trigger` | Receives call in sub-workflow (child side) |

### Data Flow Between Workflows

1. **Execute Sub-workflow** node sends data to the **Execute Sub-workflow Trigger** in the child
2. The **last node** of the child workflow sends data back to the parent
3. Parent workflow continues with the returned data

### Configuration

**Parent (Execute Workflow node)**:
```javascript
{
  "workflowId": "123",        // ID of sub-workflow
  // or
  "source": "database",       // "database" | "localFile" | "url"
  "mode": "each"              // "once" | "each" (per item or all at once)
}
```

**Sub-workflow Trigger**:
- Start the sub-workflow with the **Execute Sub-workflow Trigger** node
- This node is titled "When executed by another node" on the canvas

---

## 6. Error Handling

### Error Workflow Pattern

```
Main Workflow (fails) → triggers → Error Workflow
                                   └→ Error Trigger → Slack/Email alert
```

### Setting Up Error Workflows

1. Create a new workflow starting with **Error Trigger** node
2. Add notification nodes (Slack, Email, etc.)
3. Save the error workflow
4. In the main workflow: **Options → Settings → Error workflow** → select the error workflow

### Error Trigger Data Structure

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

**Trigger Node Errors** (different structure):
```json
{
  "trigger": {
    "error": {
      "name": "WorkflowActivationError",
      "cause": {"message": "", "stack": ""},
      "timestamp": 1654609328787,
      "message": "",
      "node": { }
    },
    "mode": "trigger"
  },
  "workflow": {"id": "", "name": ""}
}
```

### Stop And Error Node

Force workflow execution failure programmatically:
```javascript
// Use Stop And Error node to deliberately fail
// This triggers the error workflow
{
  "errorMessage": "Validation failed: missing required field 'email'"
}
```

### Per-Node Error Handling

**Continue On Fail**: Set on individual nodes to prevent workflow failure.
- Node Settings → **Always Output Data** → Enable
- Node Settings → **Continue On Fail** → Enable

When **Continue On Fail** is enabled:
- Node errors don't stop the workflow
- Error data is passed as output instead
- Downstream nodes can check for errors

### Error Handling Best Practices

1. ✅ **Always set an error workflow** for production workflows
2. ✅ Use **Stop And Error** for business logic validation failures
3. ✅ Enable **Continue On Fail** for non-critical nodes
4. ✅ Log errors to external systems (Slack, email, database)
5. ✅ Include workflow name and execution ID in error notifications
6. ❌ Don't ignore errors silently
7. ❌ Don't use error workflows for expected conditions (use IF instead)

---

## 7. Execution Order in Multi-branch Workflows

### Version-dependent Behavior

| Version | Execution Order |
|---------|----------------|
| **Pre-1.0** (v0) | Executes first node of each branch, then second of each branch (breadth-first) |
| **1.0+** (v1) | Completes one branch before starting another (depth-first) |

### v1 Branch Ordering (Current Default)

Branches execute based on **canvas position**:
1. **Topmost** branch first
2. If same height: **leftmost** branch first
3. Each branch completes entirely before the next starts

### Changing Execution Order

Go to: **Workflow Settings → Execution Order**
- `v0`: Legacy breadth-first
- `v1`: Current depth-first (recommended)

### Why This Matters

**Parallel branches into Merge node**:
- v0: Both branches partially execute simultaneously
- v1: First branch completes fully, then second branch, then Merge receives both

**Data dependencies**: If Branch B depends on Branch A's results, use v1 order.

---

## Quick Reference: Flow Logic Nodes

| Node | Type | Purpose |
|------|------|---------|
| **IF** | `n8n-nodes-base.if` | Binary conditional branching |
| **Switch** | `n8n-nodes-base.switch` | Multi-way conditional branching |
| **Merge** | `n8n-nodes-base.merge` | Combine data from branches |
| **Compare Datasets** | `n8n-nodes-base.comparedatasets` | Find data differences |
| **Loop Over Items** | `n8n-nodes-base.splitinbatches` | Batch processing loop |
| **Wait** | `n8n-nodes-base.wait` | Pause execution |
| **Execute Workflow** | `n8n-nodes-base.executeworkflow` | Call sub-workflow |
| **Execute Sub-workflow Trigger** | `n8n-nodes-base.executeworkflowtrigger` | Receive sub-workflow call |
| **Stop And Error** | `n8n-nodes-base.stopanderror` | Force execution failure |
| **Error Trigger** | `n8n-nodes-base.errortrigger` | Start error workflow |
| **Code** | `n8n-nodes-base.code` | Custom JavaScript/Python logic |

---

## Common Flow Patterns

### Pattern 1: Conditional Processing
```
Webhook → IF (valid?) → [Yes] → Process → Respond 200
                       → [No]  → Respond 400
```

### Pattern 2: Parallel Enrichment
```
Trigger → HTTP API 1 → Merge (Append) → Process combined
       → HTTP API 2 ↗
```

### Pattern 3: Retry Loop
```
Start → HTTP Request → IF (success?)
                       → [Yes] → Continue
                       → [No]  → Wait 5s → back to HTTP Request
```

### Pattern 4: Batch Processing
```
Get 1000 records → Loop Over Items (batch=100) → API Call → [loop back]
                                                           → [done] → Summary
```

### Pattern 5: Approval Flow
```
Webhook → Create ticket → Send approval email → Wait (webhook)
                                               → IF (approved?)
                                                 → [Yes] → Execute action
                                                 → [No]  → Notify rejected
```

### Pattern 6: Modular Microservices
```
Main Workflow:
  Webhook → Validate (sub-wf) → Process (sub-wf) → Notify (sub-wf) → Respond

Sub-workflow: Validate
  Trigger → Check fields → IF valid? → Return result

Sub-workflow: Process
  Trigger → Transform → Database write → Return result
```

---

## Related Skills

- **n8n-expression-syntax** — Write expressions for IF/Switch conditions
- **n8n-code-javascript** — Custom logic in Code nodes
- **n8n-workflow-patterns** — Complete workflow architectural patterns
- **n8n-node-configuration** — Configure individual flow logic nodes
- **n8n-error-handling** — Dedicated error handling patterns

---

**Documentation Source**: https://docs.n8n.io/flow-logic/
