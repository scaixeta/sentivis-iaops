---
name: n8n-workflow-api-updater
description: Execute raw n8n workflow updates via public REST API. Bypasses n8n-mcp restrictions by parsing JSON, stripping immutable metadata (createdAt, id, etc.), and making direct PUT requests to self-hosted instances.
---

# n8n Workflow API Updater Skill

This skill provides an advanced technique ("truque") to update n8n workflows when standard MCP tools (like `n8n-mcp`) fail or when direct JSON manipulation of the workflow is required without UI access. 

## When to use this skill
- When you receive `400 Bad Request` or validation errors trying to update workflows via n8n-mcp due to immutable fields (`createdAt`, `updatedAt`, `id`, `nodes.availableInMCP`).
- When you need to programmatically edit a workflow JSON file (e.g. `wf_current.json`), perform mass string replacements (like fixing `Multiple matches found` by appending `.first()`), and push the exact parsed result directly to the n8n instance.
- When you need to bypass standard front-end MCP workflow update tools to apply low-level structural changes.

## How it works

The technique relies on making direct `HTTPS/HTTP PUT` requests to the n8n REST API (typically `/api/v1/workflows/{id}`) using `curl` or Node.js scripts.

### 1. Extract and Clean the JSON Payload
n8n's API rejects full workflow JSON exports if they contain active metadata. You **MUST** strip everything except these 4 mandatory fields before sending the PUT request:
1. `name` (string)
2. `nodes` (array)
3. `connections` (object)
4. `settings` (object, even if empty, it is mandatory)

*Do NOT include: `createdAt`, `updatedAt`, `id`, or `pinData` unless explicitly expected by your specific n8n version.*

### 2. Node.js Script Template for Updating
Generate a local Node.js script (e.g., `push_wf.js`) to parse the local JSON file, clean it, and invoke the REST API:

```javascript
const fs = require('fs');
const http = require('http'); // or https depending on your n8n setup

// 1. Read your target workflow
const raw = fs.readFileSync('./wf_current.json', 'utf8');
const wf = JSON.parse(raw);

// 2. Extract ONLY allowed fields
const payload = JSON.stringify({
    name: wf.name,
    nodes: wf.nodes.map(n => {
        // optionally delete n.id if it causes conflicts, though usually allowed inside nodes array
        return n;
    }),
    connections: wf.connections,
    settings: wf.settings || {}
});

// 3. Setup Request Options
const options = {
    hostname: 'localhost', // or your n8n host
    port: 5678,
    path: '/api/v1/workflows/' + wf.id, // target workflow ID
    method: 'PUT',
    headers: {
        'X-N8N-API-KEY': process.env.N8N_API_KEY, // Ensure API key is configured
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
    }
};

// 4. Execute
const req = http.request(options, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        console.log('STATUS:', res.statusCode);
        if (res.statusCode >= 400) {
            console.error('ERROR:', data);
        } else {
            console.log('SUCCESS: Workflow Updated!');
        }
    });
});

req.on('error', console.error);
req.write(payload);
req.end();
```

### 3. Execution via terminal
```bash
# Export the API key if not in the environment
export N8N_API_KEY="your_api_key_here"
node push_wf.js
```

## Best Practices
1. **Always backup** the remote workflow before overwriting. Use a GET request or the n8n-mcp tool to read the workflow and save it locally as `backup.json`.
2. **Handle API Keys Securely:** Do not hardcode the API key in the script. Read it from a `.env` file or environment variables.
3. **Verify Node Logic:** When manipulating the `nodes` array via code, ensure referential integrity matches the `connections` object. If you change a node's `name`, you must update the `connections` dictionary that points to it.
4. **Error Handling:** If the API returns `400 Bad Request`, analyze the output to see which specific property n8n rejected, and exclude it from the payload map construction.
