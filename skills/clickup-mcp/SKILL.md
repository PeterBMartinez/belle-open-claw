---
name: clickup-mcp
description: Access ClickUp directly via API token for search, task lookup, updates, comments, docs, chat, and time tracking. Prefer direct API access over MCP/OAuth.
homepage: https://clickup.com
metadata: {"clawdbot":{"emoji":"✅","requires":{"env":["CLICKUP_TOKEN"]}}}
---

# ClickUp API Token Access

Use ClickUp directly via API token from OpenClaw. This is the default and preferred path for this workspace.

## Default Policy

- **Use direct ClickUp API/token access first** for lookups, search, task reads, comments, updates, docs, and time-tracking actions.
- **Do not require MCP, mcporter, or Claude Code OAuth** for normal ClickUp work in this workspace.
- Only consider MCP in the future if there is a specific capability the direct API cannot provide cleanly.

## Authentication

Set this environment variable wherever OpenClaw can access it:

```bash
CLICKUP_TOKEN=your_clickup_api_token
```

Use the token as a bearer token in API requests:

```bash
Authorization: Bearer $CLICKUP_TOKEN
```

## API Base

```bash
https://api.clickup.com/api/v2
```

## Recommended Access Pattern

When Peter asks to "look something up in ClickUp":

1. Use the API token directly.
2. Prefer the smallest number of API calls needed.
3. Search first when IDs are unknown.
4. Fetch task details only for the matching items you actually need.
5. Summarize results clearly instead of dumping raw JSON.

## Common Operations

### Search / Find Tasks

Use workspace/team/list-aware endpoints when possible. If the exact location is unknown, search by name or keywords using the best available endpoint for the configured workspace.

Typical shell pattern:

```bash
curl -s https://api.clickup.com/api/v2/... \
  -H "Authorization: Bearer $CLICKUP_TOKEN" \
  -H "Content-Type: application/json"
```

### Get Task Details

```bash
curl -s https://api.clickup.com/api/v2/task/TASK_ID \
  -H "Authorization: Bearer $CLICKUP_TOKEN"
```

### Get List Tasks

```bash
curl -s "https://api.clickup.com/api/v2/list/LIST_ID/task" \
  -H "Authorization: Bearer $CLICKUP_TOKEN"
```

### Create Comment

```bash
curl -s -X POST "https://api.clickup.com/api/v2/task/TASK_ID/comment" \
  -H "Authorization: Bearer $CLICKUP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment_text":"Status updated."}'
```

### Update Task

```bash
curl -s -X PUT "https://api.clickup.com/api/v2/task/TASK_ID" \
  -H "Authorization: Bearer $CLICKUP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"in progress"}'
```

## Expected Use in This Workspace

This workspace tracks several active projects, including Wash Up. For questions like:

- "What tasks are currently running with Modernization in WashUp?"
- "Find the ClickUp task for X"
- "Show me blocked WashUp items"
- "Comment on task Y"

...use the ClickUp token directly, not MCP.

## Notes

- Prefer direct API access because it is simpler, more reliable here, and avoids OAuth/client allowlist friction.
- Be mindful of rate limits; prefer fewer larger reads over many tiny requests.
- If custom fields, statuses, or list mappings are needed often, document them in memory files or project config notes.

## Resources

- ClickUp API Reference: https://clickup.com/api
- Developer Docs: https://developer.clickup.com/docs/
