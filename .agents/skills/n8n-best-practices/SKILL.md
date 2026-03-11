---
name: n8n-best-practices
description: Community-sourced best practices, performance tips, common gotchas, and production patterns for n8n workflows. Use when designing production workflows, optimizing performance, avoiding common mistakes, or looking for proven patterns from the n8n community.
---

# n8n Best Practices & Community Knowledge

Production-grade patterns, tips, and gotchas from the n8n community, forums, and blog.

**Sources**: https://community.n8n.io/ · https://blog.n8n.io/ · https://docs.n8n.io/

---

## 1. Workflow Design Best Practices

### Naming Conventions

```
✅ Good Names:
  Workflow: "Daily Sales Report - Slack"
  Nodes: "Fetch Orders", "Filter Active", "Send to Slack"

❌ Bad Names:
  Workflow: "Test" or "Untitled"
  Nodes: "Set", "Code", "HTTP Request" (default names)
```

**Rules**:
- Prefix workflows with frequency: `[Daily]`, `[Hourly]`, `[On-demand]`
- Use descriptive node names that explain WHAT, not HOW
- Tag workflows: `production`, `staging`, `testing`, `archived`
- Add Sticky Notes to document complex logic sections

### Workflow Size Limits

| Metric | Recommendation |
|--------|---------------|
| Nodes per workflow | ≤ 30 (split into sub-workflows above this) |
| Workflow nesting depth | ≤ 3 levels of sub-workflows |
| Items per batch | 100-500 (use Loop Over Items) |
| Binary file size | ≤ 50MB per file |
| Execution timeout | Set appropriate limits per workflow type |

### Structure Patterns

**Small Workflow** (3-5 nodes):
```
Trigger → Transform → Action
```

**Medium Workflow** (6-15 nodes):
```
Trigger → Validate → Transform → Action → Notify → Log
         └→ Error path
```

**Large Workflow** (15+ nodes → split):
```
Main: Trigger → Sub-wf:Validate → Sub-wf:Process → Sub-wf:Notify
Error: Error Trigger → Format → Alert
```

---

## 2. Performance Optimization

### Data Processing

```javascript
// ✅ GOOD: Filter EARLY, process LATE
Webhook → Filter (status=active) → Transform → Database Write

// ❌ BAD: Process ALL, filter LATE
Webhook → Transform ALL → Database Write ALL → Filter (status=active)
```

### Batch Processing for Large Datasets

```javascript
// ✅ Use Loop Over Items for large datasets
Fetch All Records (10,000)
  → Loop Over Items (batch=100)
  → HTTP Request (API call per batch)
  → [Loop back until done]

// ❌ Don't process 10,000 API calls at once
Fetch All Records (10,000) → HTTP Request (10,000 parallel calls) → 💥 OOM
```

### Memory-Efficient Patterns

1. **Sub-workflows**: Each sub-workflow has its own memory space
2. **Batch processing**: Process 100 items, not 10,000
3. **Binary data**: Stream don't load entirely into memory
4. **Prune executions**: Don't save all execution data forever
5. **Select only needed fields**: Use Set node to drop unnecessary data early

### Database Query Optimization

```javascript
// ✅ GOOD: Query only what you need
SELECT id, name, email FROM users WHERE status = 'active' LIMIT 100

// ❌ BAD: Fetch everything
SELECT * FROM users
```

---

## 3. Common Gotchas & Solutions

### Gotcha #1: Webhook Data Under `.body`

**Problem**: Can't find webhook POST data.

```javascript
// ❌ WRONG
{{ $json.email }}

// ✅ CORRECT
{{ $json.body.email }}
```

### Gotcha #2: Expression Syntax in Code Nodes

**Problem**: Using `{{ }}` in Code nodes.

```javascript
// ❌ WRONG (in Code node)
const email = '{{ $json.email }}';

// ✅ CORRECT (in Code node)
const email = $json.email;
// or
const email = $input.first().json.email;
```

### Gotcha #3: Missing Return in Code Node

**Problem**: Code node silently fails.

```javascript
// ❌ WRONG: No return
const items = $input.all();
items.map(i => i.json.processed = true);

// ✅ CORRECT: Always return
const items = $input.all();
return items.map(i => ({json: {...i.json, processed: true}}));
```

### Gotcha #4: Execution Order in Multi-branch

**Problem**: Branches execute in unexpected order.

**Solution**: Check Workflow Settings → Execution Order
- **v1** (default for new workflows): depth-first, top-to-bottom
- **v0** (legacy): breadth-first

### Gotcha #5: Lost Encryption Key

**Problem**: Can't decrypt credentials after migration.

**Solution**: **ALWAYS backup `N8N_ENCRYPTION_KEY`**. Without it, credentials are unrecoverable.

### Gotcha #6: Timezone Issues

**Problem**: Scheduled workflows run at wrong time.

**Solution**: Set both `GENERIC_TIMEZONE` and `TZ` environment variables:
```bash
GENERIC_TIMEZONE=America/Sao_Paulo
TZ=America/Sao_Paulo
```

### Gotcha #7: Webhook URL Mismatch

**Problem**: Webhooks return 404 in production.

**Solution**: Set `WEBHOOK_URL` to your **public-facing URL**:
```bash
WEBHOOK_URL=https://n8n.yourdomain.com/
```

### Gotcha #8: Credentials Not Working After Update

**Problem**: API credentials fail after n8n version upgrade.

**Solution**: Some nodes change credential types between versions. Re-configure affected credentials.

### Gotcha #9: Continue On Fail Hiding Errors

**Problem**: Workflow appears to succeed but data is wrong.

**Solution**: Always check for error field in output when using Continue On Fail:
```javascript
// After node with Continue On Fail
IF → {{ $json.error }} exists?
  → [Yes] → Handle error
  → [No]  → Process normally
```

### Gotcha #10: Sub-workflow Data Size Limit

**Problem**: Large data transfer between parent and sub-workflow fails.

**Solution**: Pass only IDs/references, not full datasets. Let sub-workflow fetch its own data.

---

## 4. Security Best Practices

### Credential Security

1. ✅ **Always use n8n credential system** (never hardcode secrets)
2. ✅ **Backup encryption key** before any migration
3. ✅ **Use environment variables** for sensitive configs
4. ✅ **Restrict `$env` access**: `N8N_BLOCK_ENV_ACCESS_IN_NODE=true`
5. ❌ Never commit `.n8n` directory to git
6. ❌ Never share exported credentials without encryption

### Webhook Security

```javascript
// ✅ Validate webhook signatures
const crypto = require('crypto');
const secret = $env.WEBHOOK_SECRET;
const signature = $json.headers['x-signature'];
const payload = JSON.stringify($json.body);
const expected = crypto.createHmac('sha256', secret).update(payload).digest('hex');

if (signature !== expected) {
  throw new Error('Invalid webhook signature');
}
```

### Node Restrictions

```bash
# Disable dangerous nodes in multi-user environments
NODES_EXCLUDE=n8n-nodes-base.executeCommand,n8n-nodes-base.ssh,n8n-nodes-base.readBinaryFile,n8n-nodes-base.writeBinaryFile
```

---

## 5. Production Deployment Checklist

### Before Going Live

- [ ] **Error workflow assigned** to every production workflow
- [ ] **Execution timeout** set appropriately
- [ ] **Execution pruning** enabled with retention policy
- [ ] **PostgreSQL database** (not SQLite) for production
- [ ] **HTTPS** configured via reverse proxy
- [ ] **WEBHOOK_URL** set to public URL
- [ ] **N8N_ENCRYPTION_KEY** backed up securely
- [ ] **Timezone** configured correctly
- [ ] **Monitoring** (health checks, metrics) in place
- [ ] **Backup strategy** for DB + encryption key
- [ ] **User management** enabled (not basic auth)
- [ ] **Rate limiting** on webhooks (via proxy)
- [ ] **Node names** are descriptive
- [ ] **Sticky notes** document complex logic
- [ ] **Tags** organize workflows by environment/purpose

### After Going Live

- [ ] **Monitor first executions** for errors
- [ ] **Check execution logs** daily for first week
- [ ] **Verify webhook connectivity** from external services
- [ ] **Test error workflow** triggers correctly
- [ ] **Validate backup/restore** procedure works

---

## 6. Community Tips & Tricks

### Debugging Tips

1. **Pin data** to avoid repeated expensive API calls during development
2. **Use Manual Trigger** during development, switch to Schedule/Webhook for production
3. **Test with small datasets** first, then scale up
4. **Use Sticky Notes** liberally to document "why" decisions
5. **Check execution data** by clicking on completed nodes
6. **Use `console.log()`** in Code nodes for debugging
7. **Expression Editor** (`fx` icon) shows live previews

### Workflow Organization

| Strategy | Description |
|----------|-------------|
| **Tags** | `production`, `dev`, `scheduled`, `webhook`, `error-handler` |
| **Naming** | `[Env] Domain - Action` e.g., `[Prod] Orders - Daily Report` |
| **Folders** | Group related workflows (available in newer versions) |
| **Documentation** | README workflow that lists all workflows and their purposes |

### Version Control

```bash
# Export workflows to git
n8n export:workflow --all --output=workflows/
git add workflows/
git commit -m "Backup: $(date +%Y-%m-%d)"
git push
```

### Community Resources

| Resource | URL | Description |
|----------|-----|-------------|
| **Documentation** | https://docs.n8n.io/ | Official docs |
| **Community Forum** | https://community.n8n.io/ | Q&A and discussions |
| **n8n Blog** | https://blog.n8n.io/ | Tutorials and use cases |
| **Template Library** | https://n8n.io/workflows/ | Ready-made workflow templates |
| **GitHub** | https://github.com/n8n-io/n8n | Source code and issues |
| **Discord** | Community chat | Real-time help |

---

## Related Skills

- **n8n-flow-logic** — Flow control patterns
- **n8n-error-handling** — Production error handling
- **n8n-self-hosted-admin** — Hosting and configuration
- **n8n-data-handling** — Data transformation best practices
- **n8n-workflow-patterns** — Architectural patterns

---

**Sources**: n8n Community Forum, n8n Blog, Official Documentation
