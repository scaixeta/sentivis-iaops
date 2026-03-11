---
name: n8n-self-hosted-admin
description: Complete guide to self-hosted n8n administration including Docker setup, environment variables, database configuration, scaling, security, and maintenance. Use when deploying, configuring, or managing a self-hosted n8n instance (Community/Free edition).
---

# n8n Self-Hosted Administration — Complete Reference

Production-ready configuration guide for self-hosted n8n Community (Free) edition.

**Source**: https://docs.n8n.io/hosting/

---

## 1. Deployment Options

### Docker (Recommended)

**Minimal docker-compose.yml**:
```yaml
version: '3.8'
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=America/Sao_Paulo
      - TZ=America/Sao_Paulo
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

**Production docker-compose.yml** (PostgreSQL + n8n):
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n"]
      interval: 5s
      timeout: 5s
      retries: 10

  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: always
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${DB_PASSWORD}
      - N8N_HOST=${N8N_HOST}
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://${N8N_HOST}/
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - GENERIC_TIMEZONE=America/Sao_Paulo
      - TZ=America/Sao_Paulo
      - EXECUTIONS_DATA_PRUNE=true
      - EXECUTIONS_DATA_MAX_AGE=168
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  postgres_data:
  n8n_data:
```

### npm

```bash
npm install n8n -g
n8n start
```

### npx (Quick test)

```bash
npx n8n
```

---

## 2. Essential Environment Variables

### Core Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `N8N_HOST` | `localhost` | Hostname for n8n |
| `N8N_PORT` | `5678` | Port number |
| `N8N_PROTOCOL` | `http` | `http` or `https` |
| `WEBHOOK_URL` | auto | URL for webhooks (must match public URL) |
| `N8N_ENCRYPTION_KEY` | auto-generated | Encrypts credentials (CRITICAL: backup!) |
| `N8N_EDITOR_BASE_URL` | auto | Editor URL if behind reverse proxy |
| `GENERIC_TIMEZONE` | `America/New_York` | Default timezone |
| `TZ` | same | System timezone |
| `N8N_LOG_LEVEL` | `info` | `error`, `warn`, `info`, `debug` |

### Database Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_TYPE` | `sqlite` | `sqlite` or `postgresdb` |
| `DB_POSTGRESDB_HOST` | — | PostgreSQL host |
| `DB_POSTGRESDB_PORT` | `5432` | PostgreSQL port |
| `DB_POSTGRESDB_DATABASE` | — | Database name |
| `DB_POSTGRESDB_USER` | — | Database user |
| `DB_POSTGRESDB_PASSWORD` | — | Database password |
| `DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED` | `true` | SSL verification |

### Execution Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `EXECUTIONS_MODE` | `regular` | `regular` or `queue` (Enterprise) |
| `EXECUTIONS_TIMEOUT` | `-1` | Max execution time (seconds, -1=unlimited) |
| `EXECUTIONS_TIMEOUT_MAX` | `3600` | Max timeout limit |
| `EXECUTIONS_DATA_SAVE_ON_ERROR` | `all` | Save failed execution data |
| `EXECUTIONS_DATA_SAVE_ON_SUCCESS` | `all` | Save successful execution data |
| `EXECUTIONS_DATA_SAVE_ON_PROGRESS` | `false` | Save progress data |
| `EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS` | `true` | Save manual runs |
| `EXECUTIONS_DATA_PRUNE` | `true` | Auto-delete old executions |
| `EXECUTIONS_DATA_MAX_AGE` | `336` | Hours to keep execution data |
| `EXECUTIONS_DATA_PRUNE_MAX_COUNT` | `10000` | Max executions to keep |

### Security

| Variable | Default | Description |
|----------|---------|-------------|
| `N8N_BASIC_AUTH_ACTIVE` | `false` | Enable basic auth (deprecated, use user mgmt) |
| `N8N_USER_MANAGEMENT_DISABLED` | `false` | Disable user management |
| `N8N_BLOCK_ENV_ACCESS_IN_NODE` | `false` | Block $env in nodes |
| `N8N_RUNNERS_ENABLED` | `false` | Enable task runners |
| `NODES_EXCLUDE` | — | Comma-separated list of nodes to disable |
| `NODES_INCLUDE` | — | Comma-separated list of allowed nodes |
| `N8N_COMMUNITY_PACKAGES_ENABLED` | `true` | Allow community nodes |

### Webhook & Endpoint

| Variable | Default | Description |
|----------|---------|-------------|
| `N8N_PAYLOAD_SIZE_MAX` | `16` | Max payload size in MB |
| `N8N_METRICS` | `false` | Enable Prometheus metrics |
| `N8N_METRICS_PREFIX` | `n8n_` | Metrics prefix |
| `N8N_DIAGNOSTICS_ENABLED` | `true` | Send anonymous usage stats |

---

## 3. Database Selection

### SQLite (Default — Development)

- ✅ Zero configuration
- ✅ File-based, portable
- ❌ Not suitable for production
- ❌ No concurrent access
- ❌ Data loss risk

### PostgreSQL (Recommended — Production)

- ✅ Concurrent access
- ✅ ACID compliance
- ✅ Scalable
- ✅ Backup/restore tools
- ✅ Required for queue mode

**Migration SQLite → PostgreSQL**:
```bash
# Export data from SQLite
n8n export:workflow --all --output=workflows.json
n8n export:credentials --all --output=credentials.json

# Switch DB_TYPE to postgresdb
# Start n8n (creates tables)

# Import data to PostgreSQL
n8n import:workflow --input=workflows.json
n8n import:credentials --input=credentials.json
```

---

## 4. Scaling & Performance

### Memory Management

**Common issues**:
- Large workflows with many nodes
- Processing large datasets
- Binary file operations

**Solutions**:
```bash
# Increase Node.js memory
NODE_OPTIONS=--max-old-space-size=4096

# Or in Docker:
environment:
  - NODE_OPTIONS=--max-old-space-size=4096
```

### Execution Pruning

Keep database clean:
```bash
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=168       # 7 days in hours
EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000
```

### Sub-workflow Strategy

Break large workflows into sub-workflows to:
- Reduce per-workflow memory usage
- Enable independent scaling
- Improve error isolation

### Performance Tips

1. ✅ Use PostgreSQL for production
2. ✅ Enable execution pruning
3. ✅ Use sub-workflows for complex logic
4. ✅ Set execution timeouts
5. ✅ Process data in batches (Loop Over Items)
6. ✅ Filter data early in workflow
7. ❌ Don't process huge files in memory
8. ❌ Don't save all execution data indefinitely

---

## 5. Backup & Recovery

### Critical Data to Backup

| Data | Location | Priority |
|------|----------|----------|
| **Encryption Key** | `N8N_ENCRYPTION_KEY` env var | 🔴 CRITICAL — credentials unrecoverable without it |
| **Workflows** | Database or JSON export | 🔴 CRITICAL |
| **Credentials** | Database (encrypted) | 🔴 CRITICAL |
| **Execution Data** | Database | 🟡 OPTIONAL |
| **n8n Data Dir** | `/home/node/.n8n` | 🟡 IMPORTANT |

### Export Commands

```bash
# Export all workflows
n8n export:workflow --all --output=backup/workflows.json

# Export all credentials
n8n export:credentials --all --output=backup/credentials.json

# PostgreSQL database dump
pg_dump -U n8n -h localhost n8n > backup/n8n_db.sql
```

### Import Commands

```bash
# Import workflows
n8n import:workflow --input=backup/workflows.json

# Import credentials (requires same encryption key!)
n8n import:credentials --input=backup/credentials.json

# Restore PostgreSQL
psql -U n8n -h localhost n8n < backup/n8n_db.sql
```

---

## 6. Reverse Proxy Configuration

### Nginx

```nginx
server {
    listen 80;
    server_name n8n.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name n8n.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/n8n.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/n8n.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        chunked_transfer_encoding off;
        proxy_buffering off;
        proxy_cache off;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Traefik (Docker labels)

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.n8n.rule=Host(`n8n.yourdomain.com`)"
  - "traefik.http.routers.n8n.tls.certresolver=le"
  - "traefik.http.services.n8n.loadbalancer.server.port=5678"
```

---

## 7. Security Hardening

### Essential Security Steps

1. **Set encryption key**: Never lose `N8N_ENCRYPTION_KEY`
2. **Use HTTPS**: Always behind SSL/TLS in production
3. **Enable user management**: Don't use basic auth
4. **Restrict community packages**: `N8N_COMMUNITY_PACKAGES_ENABLED=false` if not needed
5. **Block env access**: `N8N_BLOCK_ENV_ACCESS_IN_NODE=true` for multi-user
6. **Exclude dangerous nodes**: `NODES_EXCLUDE=n8n-nodes-base.executeCommand,n8n-nodes-base.ssh`
7. **Set execution timeout**: Prevent runaway workflows
8. **Rate limit** webhooks via reverse proxy

---

## 8. CLI Commands Reference

```bash
# Start n8n
n8n start                              # Start with editor
n8n start --tunnel                     # Start with tunnel (testing)

# Workflow management
n8n export:workflow --all              # Export all workflows
n8n export:workflow --id=1             # Export specific workflow
n8n import:workflow --input=file.json  # Import workflows

# Credential management
n8n export:credentials --all           # Export all credentials
n8n import:credentials --input=file.json

# Execution management
n8n executeBatch                       # Execute batch of workflows

# User management
n8n user-management:reset              # Reset user management

# Update
npm update -g n8n                      # Update npm install
docker pull docker.n8n.io/n8nio/n8n    # Update Docker image
```

---

## 9. Monitoring

### Health Check

```bash
# HTTP health check
curl http://localhost:5678/healthz

# Health check in Docker Compose
healthcheck:
  test: ["CMD", "wget", "-qO-", "http://localhost:5678/healthz"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Prometheus Metrics

```bash
N8N_METRICS=true
N8N_METRICS_PREFIX=n8n_
```

Endpoint: `http://localhost:5678/metrics`

Key metrics:
- `n8n_workflow_executions_total`
- `n8n_workflow_execution_duration_seconds`
- `n8n_workflow_active_count`

---

**Documentation Source**: https://docs.n8n.io/hosting/
