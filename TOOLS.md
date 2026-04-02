# Tools & Skills Reference

You have access to the following tools and skills. Always call them directly — never describe what you would do or ask for information you can retrieve yourself.

## Core Tools

### read
Read a file from the filesystem.
- Required: path (absolute path to the file)
- Example: read /home/peter/.openclaw/workspace/MEMORY.md

### write
Write content to a file.
- Required: path, content

### exec
Run a shell command on the Pi.
- Required: command
- Example: exec ls ~/.openclaw/workspace/

### web_search
Search the web for information.
- Required: query

### memory_search
Search OpenClaw's memory store.
- Required: query

## Skills

### rag-collections
Access Peter's RAG collections and semantic search system (WashUp, Warp9, Hercules, TruckSpy, family, etc).
- **Always read the skill file first:** /home/peter/.openclaw/workspace/skills/rag-collections/SKILL.md
- This is for external collection search and retrieval, not OpenClaw memory
- API endpoint: http://100.84.93.86:8000
- Use `curl` with `/api/v1/query` for semantic search
- Example: `curl -X POST http://100.84.93.86:8000/api/v1/query -H "Content-Type: application/json" -d '{"collection_name": "family", "query": "search term", "top_k": 5}'`

### notion
Access Peter's Notion workspace. The API key is already configured — use it directly, never ask Peter for it.
- Search pages: openclaw notion search --query "page title"
- Get page content: openclaw notion get-page --query "page title"

### gh-issues
Access GitHub issues and pull requests.
- List issues: openclaw gh-issues list --repo owner/repo
- Get issue: openclaw gh-issues get --repo owner/repo --number 123

## Peter's Setup

- Pi hostname: pi-02 (100.99.6.88 via Tailscale)
- Mac IP: 100.126.245.12 (Tailscale)
- Notion: Connected, API key configured
- GitHub: gh-issues skill enabled
- Timezone: America/New_York (EDT)

## Rules

1. Call tools immediately — never ask Peter for information you can look up yourself.
2. Always include all required parameters when calling a tool.
3. After tool results come back, synthesize them into a clear response.
4. If a tool fails, try an alternative approach — do not ask Peter to do it manually.

## Available Reports

These scripts exist on the Pi and are ready to run. When Peter asks for any of these reports, execute them immediately without asking for clarification.

### Daily Project Report (all projects)
Covers Warp9, TruckSpy, WashUp, Hercules — task movement, time logged today.
```
exec python3 ~/.openclaw/scripts/clickup-daily-report.py
```

### WashUp Admin Portal Report
Sprint 32 velocity, backlog status, SOW scope alignment check, engineer load.
```
exec python3 ~/.openclaw/scripts/washup-admin-portal-report.py
```

### WashUp Modernization Report
UI overhaul track — tasks updated today, velocity, stale items, recently shipped.
```
exec python3 ~/.openclaw/scripts/washup-modernization-report.py
```

**Trigger phrases** (run the matching script immediately when Peter says any of these):
- "run the daily report" / "project report" / "clickup report" → clickup-daily-report.py
- "WashUp Admin Portal report" / "admin portal report" / "sprint report" → washup-admin-portal-report.py
- "WashUp Modernization report" / "modernization report" / "washup mod" → washup-modernization-report.py
- "run all WashUp reports" → run both washup scripts back to back
