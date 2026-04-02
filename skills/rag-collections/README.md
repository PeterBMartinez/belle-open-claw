# Multi-Agent RAG Orchestration Skill

A skill for interacting with a multi-agent Retrieval-Augmented Generation (RAG) orchestration system running on pi-01.

## Features

- **Health Monitoring**: Check system status and metrics
- **Collection Management**: Create, list, and manage vector stores
- **Document Operations**: Upload, retrieve, and process documents
- **Semantic Search**: Query collections with natural language
- **Agent Orchestration**: Manage chat conversations and agent tasks
- **Context Storage**: Global key/value context management
- **Notion Integration**: Import Notion pages into collections
- **Backup Management**: Create and restore system backups

## Installation

This skill is automatically available in OpenClaw when placed in the skills directory.

## Usage

### Basic Commands

```bash
# Health check
openclaw rag-collections health

# Get system metrics
openclaw rag-collections metrics

# List all collections
openclaw rag-collections collection list

# Create a new collection
openclaw rag-collections collection create --name "project-docs" --description "Project documentation"
```

### Document Operations

```bash
# Upload a document to a collection
openclaw rag-collections document upload /path/to/file.pdf --collection "project-docs"

# List documents in a collection
openclaw rag-collections document list --collection "project-docs"

# Delete a document
openclaw rag-collections document delete <document-id> --collection "project-docs"
```

### Query Operations

```bash
# Perform semantic search
openclaw rag-collections query "What are the key features?" --collection "project-docs"

# Advanced query with parameters
openclaw rag-collections query "How does it work?" \
  --collection "project-docs" \
  --limit 5 \
  --similarity-threshold 0.7
```

### Chat Operations

```bash
# Create a new chat conversation
openclaw rag-collections chat conversation create --title "Project Discussion"

# List available agents
openclaw rag-collections chat agents list

# Send message to agent
openclaw rag-collections chat message send \
  --conversation <conversation-id> \
  --agent <agent-name> \
  "What is the status of feature X?"
```

### Context Management

```bash
# Set context value
openclaw rag-collections context set project-status "active"

# Get context value
openclaw rag-collections context get project-status

# List all context keys
openclaw rag-collections context list
```

### Notion Integration

```bash
# Search Notion workspace
openclaw rag-collections notion search --query "project requirements"

# Import a Notion page
openclaw rag-collections notion import <page-id>
```

### Backup Operations

```bash
# Create backup
openclaw rag-collections backup create

# List backups
openclaw rag-collections backup list

# Get latest backup info
openclaw rag-collections backup latest
```

## Infrastructure

All services run on **pi-01** (`100.84.93.86`) via Docker:

| Service | Port | Description |
|---------|------|-------------|
| cluster-api | `:8000` / `:8080` | Main API (Swagger UI at `:8000/docs`) |
| cluster-web | `:3001` | Web UI |
| Postgres 16 | `:5433` | Database |
| Redis 7 | `:6379` / `:6380` | Cache and pub/sub |
| Qdrant v1.7.4 | `:6333-6336` | Vector database |
| MinIO | `:9000-9003` | Object storage |
| Grafana | `:3000` | Monitoring dashboard |
| Prometheus | `:9090` | Metrics collection |
| Portainer | `:9443` | Container management |

## API Reference

See `SKILL.md` for detailed API documentation and OpenAPI specification.

## Development

To extend this skill:
1. Add new functions to `index.js`
2. Update the CLI commands in the main OpenClaw configuration
3. Document new features in `README.md` and `SKILL.md`

## Support

For issues or questions, refer to the OpenClaw documentation at https://docs.openclaw.ai