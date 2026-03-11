---
name: n8n-data-handling
description: Understanding n8n data structure, transformation, mapping, pinning, binary data, and expressions. Use when working with data flowing between nodes, transforming data, understanding the [{json}] format, handling binary files, or mapping fields between nodes.
---

# n8n Data Handling — Complete Reference

Comprehensive guide to how data flows, transforms, and maps in n8n workflows.

**Source**: https://docs.n8n.io/data/

---

## 1. Data Structure

### The Universal Format

**All data in n8n is an array of objects with a `json` key**:

```javascript
[
  {
    "json": {
      "name": "Alice",
      "email": "alice@example.com",
      "age": 30
    }
  },
  {
    "json": {
      "name": "Bob",
      "email": "bob@example.com",
      "age": 25
    }
  }
]
```

### Binary Data Format

For files, images, PDFs:

```javascript
[
  {
    "json": {
      "fileName": "report.pdf"
    },
    "binary": {
      "data": {
        "data": "base64-encoded-content",   // Required
        "mimeType": "application/pdf",       // Recommended
        "fileExtension": "pdf",              // Recommended
        "fileName": "report.pdf"             // Recommended
      }
    }
  }
]
```

### Auto-wrapping in Code Nodes

Since n8n 0.166.0+, Code nodes auto-wrap:
- Missing `json` key → auto-added
- Missing array wrapper `[]` → auto-added

```javascript
// ✅ This works in Code nodes (auto-wrapped):
return [{name: "Alice"}];
// n8n converts to: [{json: {name: "Alice"}}]

// ✅ Full explicit format (always correct):
return [{json: {name: "Alice"}}];
```

**⚠️ Custom nodes MUST still return proper format.**

---

## 2. How Data Flows Within Nodes

### Item-by-Item Processing

Each node processes **every input item** automatically:

```
Input: [{json: {name: "Alice"}}, {json: {name: "Bob"}}]
       ↓
Slack Node (send message with {{$json.name}})
       ↓
Result: 2 messages sent (one per item)
```

### Node Input/Output

- **Input panel**: Shows data received from previous node
- **Output panel**: Shows data produced by this node
- **Table/JSON/Schema views**: Toggle between display formats

---

## 3. Data Mapping

### What Is Data Mapping?

Data mapping references data from previous nodes in current node parameters.

### Drag and Drop Mapping

1. Open node output panel (left side)
2. Drag a field from output to the target parameter
3. n8n creates an expression automatically: `{{ $json.fieldName }}`

### Expression-based Mapping

```javascript
// Current node's input
{{ $json.email }}
{{ $json.user.name }}
{{ $json['field with spaces'] }}
{{ $json.items[0].id }}

// From specific node
{{ $node["HTTP Request"].json.data }}
{{ $node["Webhook"].json.body.email }}

// Environment variables
{{ $env.API_KEY }}
{{ $env.DATABASE_URL }}

// Workflow metadata
{{ $workflow.id }}
{{ $workflow.name }}
{{ $execution.id }}
{{ $execution.mode }}
```

### Item Linking

n8n tracks which input items map to which output items. This enables:
- Referencing data from **non-directly-connected** nodes
- **Paired items**: Track data lineage through transformations

---

## 4. Transforming Data

### Built-in Transformation Nodes

| Node | Purpose | When to Use |
|------|---------|-------------|
| **Set** | Map/rename/add/remove fields | Simple field operations |
| **Aggregate** | Combine items into groups | Totals, averages, grouping |
| **Split Out** | Split one item into many | Expanding arrays |
| **Sort** | Order items | Sorting by field |
| **Limit** | Restrict item count | Top N results |
| **Remove Duplicates** | Deduplicate | Unique items |
| **Rename Keys** | Rename field names | API format conversion |
| **Summarize** | Statistical operations | Reports, analytics |
| **Code** | Custom JavaScript/Python | Complex transformations |
| **AI Transform** | AI-powered transformation | Natural language transforms |
| **Filter** | Keep items matching criteria | Conditional filtering |

### Set Node Patterns

```javascript
// Add new field
{
  "mode": "manual",
  "fields": {
    "values": [
      {"name": "fullName", "value": "={{$json.firstName}} {{$json.lastName}}"},
      {"name": "timestamp", "value": "={{$now.toISO()}}"}
    ]
  }
}

// Keep only specific fields
{
  "mode": "manual",
  "includeOtherFields": false,  // Drop everything else
  "fields": {
    "values": [
      {"name": "id", "value": "={{$json.id}}"},
      {"name": "email", "value": "={{$json.email}}"}
    ]
  }
}
```

### Code Node Transformations

```javascript
// Flatten nested objects
const items = $input.all();
return items.map(item => ({
  json: {
    id: item.json.id,
    userName: item.json.user?.name || 'Unknown',
    userEmail: item.json.user?.email || '',
    city: item.json.address?.city || ''
  }
}));
```

```javascript
// Group items by category
const items = $input.all();
const grouped = {};

for (const item of items) {
  const category = item.json.category || 'uncategorized';
  if (!grouped[category]) grouped[category] = [];
  grouped[category].push(item.json);
}

return Object.entries(grouped).map(([category, items]) => ({
  json: { category, items, count: items.length }
}));
```

```javascript
// Pivot/Unpivot data
const items = $input.all();
const pivoted = {};

for (const item of items) {
  const key = item.json.date;
  if (!pivoted[key]) pivoted[key] = { date: key };
  pivoted[key][item.json.metric] = item.json.value;
}

return Object.values(pivoted).map(row => ({ json: row }));
```

### AI Transform Node

Natural language data transformation:
- "Convert all dates to ISO format"
- "Extract email addresses from text"
- "Calculate tax at 15% and add to total"

---

## 5. Expressions Deep Reference

### Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `$json` | Current item's data | `{{$json.email}}` |
| `$node["Name"]` | Data from specific node | `{{$node["Set"].json.value}}` |
| `$now` | Current timestamp (Luxon DateTime) | `{{$now.toFormat('yyyy-MM-dd')}}` |
| `$today` | Today at midnight | `{{$today}}` |
| `$env` | Environment variables | `{{$env.API_KEY}}` |
| `$workflow` | Workflow metadata | `{{$workflow.name}}` |
| `$execution` | Execution metadata | `{{$execution.id}}` |
| `$runIndex` | Current run index (loops) | `{{$runIndex}}` |
| `$itemIndex` | Index of current item | `{{$itemIndex}}` |
| `$input` | Input data handle | `{{$input.first().json}}` |
| `$prevNode` | Previous node data | `{{$prevNode.name}}` |

### Built-in Methods

**String Methods**:
```javascript
{{ $json.name.toUpperCase() }}
{{ $json.email.toLowerCase() }}
{{ $json.text.trim() }}
{{ $json.name.replace('old', 'new') }}
{{ $json.csv.split(',') }}
{{ $json.url.includes('https') }}
{{ $json.text.substring(0, 50) }}
{{ $json.name.length }}
{{ $json.text.match(/\d+/) }}
{{ $json.name.startsWith('A') }}
{{ $json.name.endsWith('z') }}
{{ $json.text.replaceAll(' ', '_') }}
{{ $json.name.slice(0, 5) }}
```

**Number Methods**:
```javascript
{{ $json.price.toFixed(2) }}
{{ Math.round($json.value) }}
{{ Math.ceil($json.score) }}
{{ Math.floor($json.rating) }}
{{ Math.abs($json.difference) }}
{{ Math.max($json.a, $json.b) }}
{{ Math.min($json.x, $json.y) }}
{{ parseInt($json.stringNumber) }}
{{ parseFloat($json.decimalString) }}
```

**DateTime (Luxon)**:
```javascript
{{ $now.toFormat('yyyy-MM-dd') }}
{{ $now.toFormat('HH:mm:ss') }}
{{ $now.toISO() }}
{{ $now.toMillis() }}
{{ $now.plus({days: 7}).toFormat('yyyy-MM-dd') }}
{{ $now.minus({hours: 24}).toISO() }}
{{ $now.startOf('month').toFormat('yyyy-MM-dd') }}
{{ $now.endOf('month').toFormat('yyyy-MM-dd') }}
{{ $now.weekday }}     // 1=Monday, 7=Sunday
{{ $now.daysInMonth }} // 28-31
{{ DateTime.fromISO($json.dateStr).toFormat('MMMM dd, yyyy') }}
{{ DateTime.fromMillis($json.timestamp).toISO() }}
{{ DateTime.fromFormat($json.date, 'dd/MM/yyyy').toISO() }}
```

**Array Methods**:
```javascript
{{ $json.tags.length }}
{{ $json.items.join(', ') }}
{{ $json.users[0].name }}
{{ $json.list[$json.list.length - 1] }}
```

**Conditional (Ternary)**:
```javascript
{{ $json.status === 'active' ? 'Active User' : 'Inactive' }}
{{ $json.score >= 80 ? 'Pass' : 'Fail' }}
{{ $json.email || 'no-email@example.com' }}
{{ $json.name ?? 'Anonymous' }}
```

### JMESPath Queries

```javascript
// In Code nodes:
$jmespath($json, 'users[?age >= `18`].name')
$jmespath($json, 'items[*].{id: id, name: name}')
$jmespath($json, 'max_by(scores, &value)')
```

---

## 6. Data Pinning & Mocking

### Data Pinning

**Freeze node output** for development and testing:

1. Execute node to get data
2. Click pin icon on output panel
3. Pinned data is used in subsequent test runs instead of re-executing

**Use cases**:
- Avoid repeated API calls during development
- Test with consistent data
- Work offline with cached data

### Editing Pinned Data

- Click on pinned data to edit JSON directly
- Modify values for edge case testing
- Add/remove items to test different scenarios

### Best Practices

- ✅ Pin data when developing/testing downstream nodes
- ✅ Unpin before production activation
- ✅ Use pinning for expensive API calls
- ❌ Don't leave stale pinned data in production
- ❌ Don't pin overly large datasets (memory)

---

## 7. Binary Data Handling

### Working with Files

**Read file**:
```javascript
// Using Read Binary File node
const fileData = $input.first().binary.data;
const content = Buffer.from(fileData.data, 'base64').toString('utf-8');
```

**Write file**:
```javascript
// In Code node, create binary data
const csvContent = "name,email\nAlice,alice@email.com";
const binaryData = Buffer.from(csvContent).toString('base64');

return [{
  json: { fileName: 'data.csv' },
  binary: {
    data: {
      data: binaryData,
      mimeType: 'text/csv',
      fileName: 'data.csv',
      fileExtension: 'csv'
    }
  }
}];
```

### Common Binary Operations

| Operation | Node/Method |
|-----------|-------------|
| Read file from disk | Read Binary File |
| Write file to disk | Write Binary File |
| Convert to/from Base64 | Code node |
| Download from URL | HTTP Request (binary response) |
| Upload to service | HTTP Request with binary body |
| Extract text from PDF | Extract from File |
| Create spreadsheet | Spreadsheet File |

---

## 8. Data Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "Cannot read property 'x' of undefined" | Missing nested property | Use optional chaining: `$json?.user?.email` |
| Empty output | Previous node returned no data | Check input data, add IF to handle empty |
| Webhook data not found | Wrong path | Use `$json.body.fieldName` for webhooks |
| Expression shows as text | Missing `{{ }}` | Wrap in double curly braces |
| Wrong item count | Data structure mismatch | Check array wrapping, use Split Out or Aggregate |
| Binary data empty | Not piped correctly | Check binary key name matches |

### Debugging Steps

1. **Check Input**: Click node → view Input panel
2. **Check Output**: Verify Output panel matches expectations
3. **Expression Editor**: Click `fx` icon → see live preview
4. **Console.log**: In Code nodes, use `console.log()` for debugging
5. **Execution Log**: Review past executions for data flow

---

## Related Skills

- **n8n-expression-syntax** — Detailed expression writing guide
- **n8n-code-javascript** — JavaScript in Code nodes
- **n8n-code-python** — Python in Code nodes
- **n8n-flow-logic** — Data transformation in flow context
- **n8n-node-configuration** — Configure transformation nodes

---

**Documentation Source**: https://docs.n8n.io/data/
