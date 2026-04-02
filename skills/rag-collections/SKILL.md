---
name: rag-collections
description: Access Peter's external RAG collections and semantic search system for project, family, and knowledge-base retrieval. Use when searching collection-backed knowledge outside OpenClaw memory, including WashUp, Warp9, Hercules, TruckSpy, family, Phycology, and related document collections.
---

# RAG Collections API

## Description
Use this skill to query Peter's external collection-backed RAG system. This is not OpenClaw memory; it is the separate retrieval layer for project collections, family knowledge, and uploaded document corpora hosted on pi-01 (100.84.93.86:8000).

## Key Features
- **Collections**: Create, list, retrieve, and delete document collections
- **Documents**: Upload, manage, and query documents within collections
- **Conversations**: Manage conversation threads with message history
- **Agents**: List available agents for orchestration
- **Semantic Search**: Perform vector-based searches on document content
- **Metrics**: System health and usage statistics

## API Endpoints

### Health & Metrics
- `GET /api/v1/health` - Check system health
- `GET /api/v1/metrics` - Get system metrics (collections, documents, agents, uptime)

### Collections
- `GET /api/v1/collections` - List all collections
- `POST /api/v1/collections` - Create a new collection
- `GET /api/v1/collections/{collection_id}` - Get collection details
- `DELETE /api/v1/collections/{collection_id}` - Delete a collection

### Documents
- `GET /api/v1/documents?collection_id={collection_id}` - List documents in collection
- `POST /api/v1/documents` - Upload document to collection
- `GET /api/v1/documents/{document_id}` - Get document details
- `DELETE /api/v1/documents/{document_id}` - Delete document

### Queries
- `POST /api/v1/query` - Perform semantic search on collection

### Conversations
- `GET /api/v1/conversations` - List all conversations
- `POST /api/v1/conversations` - Create a new conversation
- `GET /api/v1/conversations/{conversation_id}` - Get conversation details
- `DELETE /api/v1/conversations/{conversation_id}` - Delete conversation
- `GET /api/v1/conversations/{conversation_id}/messages` - List messages in conversation
- `POST /api/v1/conversations/{conversation_id}/messages` - Send message to conversation

### Agents
- `GET /api/v1/agents` - List all available agents

## Usage Examples

### Create a Collection
```bash
curl -X POST http://100.84.93.86:8000/api/v1/collections \
  -H "Content-Type: application/json" \
  -d '{"name": "project-docs", "description": "Project documentation"}'
```

### Upload a Document
```bash
curl -X POST http://100.84.93.86:8000/api/v1/documents/upload \
  -F "file=@document.pdf" \
  -F "collection_id=<collection_id>"
```

### Upload a Markdown Document
```bash
curl -X POST http://100.84.93.86:8000/api/v1/documents/upload \
  -F "file=@document.md;type=text/markdown" \
  -F "collection_id=<collection_id>"
```

**Important:** when uploading `.md` files, explicitly set the multipart file content type to `text/markdown`. If omitted, some clients send Markdown as `application/octet-stream`, which causes ingestion to fail with `Unsupported file type: application/octet-stream`.

### Query Documents
```bash
curl -X POST http://100.84.93.86:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"collection_name": "family", "query": "What is the API design?", "top_k": 5}'
```

### List Documents in Collection
```bash
curl http://100.84.93.86:8000/api/v1/documents?collection_id=<collection_id>
```

### Create Conversation
```bash
curl -X POST http://100.84.93.86:8000/api/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "API Discussion", "agent_id": "rag-agent-1"}'
```

## Authentication
No authentication required for current implementation (development environment).

## Rate Limiting
Default rate limiting applies:
- 100 requests per minute per IP address

## Error Handling
Standard HTTP status codes are returned:
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Resource deleted
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Data Models

### Collection
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Document
```json
{
  "id": "string",
  "collection_id": "string",
  "filename": "string",
  "content_type": "string",
  "size_bytes": "integer",
  "created_at": "datetime"
}
```

### Query Request
```json
{
  "query": "string",
  "top_k": "integer (default: 5)",
  "filter": "optional filter object"
}
```

### Search Results
```json
{
  "results": [
    {
      "document_id": "string",
      "score": "float",
      "content": "string",
      "metadata": "object"
    }
  ]
}
```

### Conversation
```json
{
  "id": "string",
  "title": "string",
  "agent_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Message
```json
{
  "id": "string",
  "conversation_id": "string",
  "role": "user|assistant|system",
  "content": "string",
  "created_at": "datetime"
}
```

## Integration Notes
- The API is designed for programmatic access from OpenClaw agents
- Use the `exec` tool to make HTTP requests or call external scripts
- For complex workflows, consider creating a sub-agent dedicated to RAG operations
- Collections can be used to organize documents by project or topic
- Conversations maintain message history for context-aware responses

## Troubleshooting
1. **Connection Issues**: Verify pi-01 is online and the service is running
2. **Timeout Errors**: Check network connectivity between nodes
3. **Permission Errors**: Ensure proper file permissions on document uploads
4. **Rate Limit Errors**: Reduce request frequency or cache responses

## References
- OpenAPI Specification: `openapi.yaml` in this directory
- Server Location: pi-01 (100.84.93.86)
- Port: 8000