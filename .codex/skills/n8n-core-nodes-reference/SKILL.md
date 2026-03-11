---
name: n8n-core-nodes-reference
description: Complete reference of all n8n core nodes with descriptions, use cases, and configurations. Use when looking up available nodes, understanding node purposes, or building workflows with core n8n capabilities.
---

# n8n Core Nodes — Complete Reference

All built-in core nodes available in n8n Community (free) edition.

**Source**: https://docs.n8n.io/integrations/builtin/core-nodes/

---

## Trigger Nodes

Start workflow execution.

| Node | Internal Name | Purpose | Free? |
|------|---------------|---------|-------|
| **Manual Trigger** | `n8n-nodes-base.manualTrigger` | Start workflow manually | ✅ |
| **Schedule Trigger** | `n8n-nodes-base.scheduleTrigger` | Run on cron/interval schedule | ✅ |
| **Webhook** | `n8n-nodes-base.webhook` | HTTP endpoint trigger | ✅ |
| **Error Trigger** | `n8n-nodes-base.errortrigger` | Start error workflow | ✅ |
| **Execute Sub-workflow Trigger** | `n8n-nodes-base.executeworkflowtrigger` | Called by parent workflow | ✅ |
| **Activation Trigger** | `n8n-nodes-base.activationtrigger` | Fires on workflow activation/deactivation | ✅ |
| **Chat Trigger** | `n8n-nodes-base.chatTrigger` | Built-in chat interface | ✅ |
| **Email Trigger (IMAP)** | `n8n-nodes-base.emailReadImap` | Watch for new emails | ✅ |
| **Local File Trigger** | `n8n-nodes-base.localFileTrigger` | Watch for file changes | ✅ |
| **SSE Trigger** | `n8n-nodes-base.sseTrigger` | Server-Sent Events listener | ✅ |

### Schedule Trigger Configuration

```javascript
// Cron expressions
{
  "rule": {
    "interval": [
      {"field": "cronExpression", "expression": "0 9 * * *"}  // 9 AM daily
    ]
  }
}

// Interval
{
  "rule": {
    "interval": [
      {"field": "minutes", "minutesInterval": 15}  // Every 15 minutes
    ]
  }
}
```

### Webhook Node Configuration

```javascript
{
  "path": "my-webhook",           // URL path
  "httpMethod": "POST",           // GET, POST, PUT, DELETE, PATCH, HEAD
  "responseMode": "onReceived",   // "onReceived" | "lastNode"
  "responseCode": 200,
  "responseData": "allEntries"    // "allEntries" | "firstEntryJson" | "firstEntryBinary" | "noData"
}
```

**Webhook URL Format**: `https://your-n8n-domain/webhook/<path>`
**Test URL**: `https://your-n8n-domain/webhook-test/<path>`

---

## Flow Control Nodes

Control workflow execution flow.

| Node | Internal Name | Purpose | Free? |
|------|---------------|---------|-------|
| **IF** | `n8n-nodes-base.if` | Binary conditional branching | ✅ |
| **Switch** | `n8n-nodes-base.switch` | Multi-way branching | ✅ |
| **Merge** | `n8n-nodes-base.merge` | Combine data from branches | ✅ |
| **Loop Over Items** | `n8n-nodes-base.splitinbatches` | Process items in batches | ✅ |
| **Wait** | `n8n-nodes-base.wait` | Pause execution | ✅ |
| **Stop And Error** | `n8n-nodes-base.stopanderror` | Force execution failure | ✅ |
| **No Operation** | `n8n-nodes-base.noOp` | Pass-through (placeholder) | ✅ |
| **Execute Workflow** | `n8n-nodes-base.executeworkflow` | Call sub-workflow | ✅ |
| **Filter** | `n8n-nodes-base.filter` | Filter items by condition | ✅ |
| **Compare Datasets** | `n8n-nodes-base.comparedatasets` | Find differences between datasets | ✅ |

---

## Data Transformation Nodes

Transform, restructure, and manipulate data.

| Node | Internal Name | Purpose | Free? |
|------|---------------|---------|-------|
| **Set** | `n8n-nodes-base.set` | Add/modify/remove fields | ✅ |
| **Code** | `n8n-nodes-base.code` | Custom JavaScript/Python code | ✅ |
| **Aggregate** | `n8n-nodes-base.aggregate` | Group and aggregate items | ✅ |
| **Split Out** | `n8n-nodes-base.splitOut` | Split one item into many | ✅ |
| **Sort** | `n8n-nodes-base.sort` | Order items by field | ✅ |
| **Limit** | `n8n-nodes-base.limit` | Restrict number of items | ✅ |
| **Remove Duplicates** | `n8n-nodes-base.removeDuplicates` | Deduplicate items | ✅ |
| **Rename Keys** | `n8n-nodes-base.renameKeys` | Rename field names | ✅ |
| **Summarize** | `n8n-nodes-base.summarize` | Calculate statistics | ✅ |
| **Date & Time** | `n8n-nodes-base.dateTime` | Format/modify dates | ✅ |
| **Crypto** | `n8n-nodes-base.crypto` | Hash/encrypt/HMAC | ✅ |
| **HTML** | `n8n-nodes-base.html` | Parse/extract HTML | ✅ |
| **XML** | `n8n-nodes-base.xml` | Convert XML/JSON | ✅ |
| **Markdown** | `n8n-nodes-base.markdown` | Convert Markdown/HTML | ✅ |
| **AI Transform** | `n8n-nodes-base.aiTransform` | AI-powered data transform | ✅ |
| **Item Lists** | `n8n-nodes-base.itemLists` | Sort/limit/concatenate items | ✅ |

---

## Communication Nodes

HTTP requests, email, and file operations.

| Node | Internal Name | Purpose | Free? |
|------|---------------|---------|-------|
| **HTTP Request** | `n8n-nodes-base.httpRequest` | Make HTTP/REST API calls | ✅ |
| **Respond to Webhook** | `n8n-nodes-base.respondToWebhook` | Send webhook response | ✅ |
| **Send Email** | `n8n-nodes-base.emailSend` | Send SMTP emails | ✅ |
| **Read Binary File** | `n8n-nodes-base.readBinaryFile` | Read file from disk | ✅ |
| **Write Binary File** | `n8n-nodes-base.writeBinaryFile` | Write file to disk | ✅ |
| **Read Binary Files** | `n8n-nodes-base.readBinaryFiles` | Read multiple files | ✅ |
| **RSS Read** | `n8n-nodes-base.rssFeedRead` | Read RSS feeds | ✅ |
| **Spreadsheet File** | `n8n-nodes-base.spreadsheetFile` | Read/write CSV/XLSX | ✅ |
| **FTP** | `n8n-nodes-base.ftp` | FTP/SFTP file operations | ✅ |
| **SSH** | `n8n-nodes-base.ssh` | Execute SSH commands | ✅ |
| **Execute Command** | `n8n-nodes-base.executeCommand` | Run shell commands | ✅ |

### HTTP Request Cheat Sheet

```javascript
// GET request
{ "method": "GET", "url": "https://api.example.com/users", "authentication": "none" }

// POST with JSON body
{
  "method": "POST",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "={{$json.name}}",
      "email": "={{$json.email}}"
    }
  }
}

// With headers
{
  "method": "GET",
  "url": "https://api.example.com/data",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {"name": "Authorization", "value": "Bearer {{$env.API_TOKEN}}"},
      {"name": "Content-Type", "value": "application/json"}
    ]
  }
}

// With query parameters
{
  "method": "GET",
  "url": "https://api.example.com/search",
  "sendQuery": true,
  "queryParameters": {
    "parameters": [
      {"name": "q", "value": "={{$json.query}}"},
      {"name": "limit", "value": "100"}
    ]
  }
}

// Authentication types
// "none" | "predefinedCredentialType" | "genericCredentialType"
```

---

## AI Nodes (LangChain)

| Node | Internal Name | Purpose | Free? |
|------|---------------|---------|-------|
| **AI Agent** | `@n8n/n8n-nodes-langchain.agent` | Autonomous AI agent with tools | ✅ |
| **Basic LLM Chain** | `@n8n/n8n-nodes-langchain.chainLlm` | Simple prompt → response | ✅ |
| **Retrieval QA Chain** | `@n8n/n8n-nodes-langchain.chainRetrievalQa` | RAG-based Q&A | ✅ |
| **Summarization Chain** | `@n8n/n8n-nodes-langchain.chainSummarization` | Document summarization | ✅ |
| **Information Extractor** | `@n8n/n8n-nodes-langchain.informationExtractor` | Structured data extraction | ✅ |
| **Text Classifier** | `@n8n/n8n-nodes-langchain.textClassifier` | Classification | ✅ |
| **Sentiment Analysis** | `@n8n/n8n-nodes-langchain.sentimentAnalysis` | Sentiment detection | ✅ |

### AI Sub-nodes (connect under AI nodes)

| Type | Nodes |
|------|-------|
| **Language Models** | OpenAI, Anthropic, Google Gemini, Ollama, Azure OpenAI, Groq, Mistral |
| **Memory** | Window Buffer Memory, Postgres Memory, Zep Memory, Redis Memory |
| **Tools** | HTTP Request, Code, Calculator, Wikipedia, SerpAPI, Custom tools |
| **Embeddings** | OpenAI Embeddings, Cohere, HuggingFace |
| **Vector Stores** | Pinecone, Qdrant, Supabase, PostgreSQL/pgvector, In-Memory |
| **Document Loaders** | File, URL, Notion, GitHub |
| **Text Splitters** | Recursive Character, Token |
| **Output Parsers** | Structured, Auto-fixing |
| **Retrievers** | Vector Store Retriever |

---

## Utility Nodes

| Node | Internal Name | Purpose | Free? |
|------|---------------|---------|-------|
| **Sticky Note** | `n8n-nodes-base.stickyNote` | Visual documentation on canvas | ✅ |
| **n8n** | `n8n-nodes-base.n8n` | Manage n8n workflows/executions | ✅ |
| **Function** | `n8n-nodes-base.function` | Legacy code node (use Code instead) | ✅ |
| **Function Item** | `n8n-nodes-base.functionItem` | Legacy per-item code | ✅ |

---

## Node Quick Reference by Use Case

| I want to... | Use this node |
|--------------|---------------|
| Receive HTTP requests | **Webhook** |
| Make API calls | **HTTP Request** |
| Run on schedule | **Schedule Trigger** |
| Add/modify fields | **Set** |
| Filter items | **Filter** or **IF** |
| Route to different paths | **IF** (2-way) or **Switch** (multi-way) |
| Combine branch data | **Merge** |
| Write custom logic | **Code** |
| Process in batches | **Loop Over Items** |
| Call another workflow | **Execute Workflow** |
| Pause execution | **Wait** |
| Handle errors | **Error Trigger** + error workflow |
| Force error | **Stop And Error** |
| Send email | **Send Email** |
| Read/write files | **Read/Write Binary File** |
| Run shell commands | **Execute Command** |
| Parse HTML | **HTML** |
| Work with AI | **AI Agent** or **Basic LLM Chain** |
| Sort data | **Sort** |
| Remove duplicates | **Remove Duplicates** |
| Group/aggregate | **Aggregate** or **Summarize** |
| Convert data formats | **XML**, **Markdown**, **Spreadsheet File** |

---

**Documentation Source**: https://docs.n8n.io/integrations/builtin/core-nodes/
