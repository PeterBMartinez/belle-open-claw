# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260402-001] best_practice

**Logged**: 2026-04-02T22:28:48Z
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
Initialized the workspace self-improvement logging store and verified the OpenClaw hook is active.

### Details
The self-improving-agent skill was installed and its bootstrap reminder hook was active, but the workspace-level `.learnings/` directory and markdown files did not exist yet. Created the expected files and confirmed the `self-improvement` hook is ready in OpenClaw.

### Suggested Action
Use `.learnings/` for future corrections, errors, and feature requests; periodically promote recurring patterns into `SOUL.md`, `AGENTS.md`, or `TOOLS.md`.

### Metadata
- Source: conversation
- Related Files: .learnings/LEARNINGS.md, skills/self-improving-agent/SKILL.md
- Tags: self-improvement, openclaw, initialization

---
