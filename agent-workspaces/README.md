# Agent Workspaces

These folders are separate home bases for on-demand sub-agents.

## Layout
- `delivery-manager-orchestrator/`
- `washup-project-agent/`
- `warp9-project-agent/`
- `hercules-project-agent/`
- `truckspy-project-agent/`

## Launcher Map
See `launcher-map.json` for the canonical mapping from agent name to:
- display label
- working directory (`cwd`)
- prompt seed / role instructions

## Intent
Each agent can be spawned with its own cwd so project-specific notes, outputs, scripts, and scratch files stay isolated.
Shared portfolio context still lives in `/home/peter/.openclaw/workspace/memory/` unless deliberately copied or specialized.
