# MEMORY.md - Long-Term Memory

## Peter's 4 Primary Projects (Active)

These are the core projects Peter is focusing on:

1. **Wash Up** - Outcode client project
   - Status: Active
   - Priority: High
   - Started: Feb 27, 2026
   - Tool: **ClickUp**
   - Lead: Peter Martinez

2. **Warp 9** - Outcode client project
   - Status: Active
   - Priority: High
   - Started: Dec 29, 2025
   - Tool: **ClickUp** (likely)
   - Lead: Peter Martinez

3. **Hercules** - Outcode client project (Hercules Portal)
   - Status: Active
   - Priority: High
   - Started: Jan 13, 2026
   - Tool: **Azure DevOps (ADO)**
   - Lead: Peter Martinez

4. **TruckSpy** - Outcode client project
   - Status: Active
   - Priority: High
   - Started: Dec 30, 2025
   - Tool: **ZenHub**
   - Lead: Peter Martinez

**Note:** Portfolio is distributed across 3 different project management tools (ClickUp, ZenHub, ADO). All 4 are active (not back burner). This requires a unified aggregation layer for PDHI scoring and DORA metrics.

---

## Knowledge Base

**Project Context:** See `memory/PROJECTS-KNOWLEDGE-BASE.md`
- Business objectives, team composition, client contacts
- Current health (PDHI), concerns, and immediate actions
- SoW details, milestones, recent decisions
- **UPDATE THIS** when Peter provides project context

**DM Playbook:** See `memory/DM-PLAYBOOK.md`
- Role definition, PDHI scoring guide, DORA metrics
- Weekly operating rhythm, delivery checklist
- Lead vs lag metrics

**Project Configuration:** See `memory/DM-PROJECT-CONFIG.md`
- Tool IDs, space IDs, workspace IDs (ClickUp, ADO, ZenHub)
- PDHI baselines (as of 2026-03-27)
- Credentials status (all configured)

**RAG Collections System:**
- Local skill name: `rag-collections`
- Purpose: external collection search/retrieval across project and family knowledge bases; distinct from OpenClaw memory files
- WashUp: `957a1df5-7e73-4663-b8e8-4c595fad82cb` (ID: 957a1df5)
- Warp9: `265aeb0a-2ecb-481d-a0a2-00364ce5d9d2` (ID: 265aeb0a)
- Hercules: `89a95082-79c4-4c59-af54-2d7b7b19e1e6` (ID: 89a95082)
- TruckSpy: `3dfdd3d6-45fb-4d66-b94e-8706ae66b104` (ID: 3dfdd3d6)
- Phycology: `1901a7ae-906a-4361-bd3b-832c44ed7472`
- child-phycology: `137db57c-7cd6-4f90-a9bf-53edac8e5ab7` (formerly Child-Phycology)

**RAG API Note:** As of 2026-03-27, all collection names MUST be lowercase. Migration completed. When creating new collections, always use lowercase names.

## Automation Preference

- If a task retries 3 times due to failure, or hangs for 10 minutes, cancel the task instead of letting it continue indefinitely.

## Pi Cluster

- Peter has a 3-node Raspberry Pi setup.
- **pi-01** = `100.84.93.86` (hosts the RAG API; also noted as running Qdrant and MinIO)
- **pi-02** = `100.99.6.88` (OpenClaw, DM Automations)
- **pi-03** = `100.121.226.64` (TBD)
- SSD setup is attached to **pi-01** (per Peter, tentative wording: "I think").
- As of 2026-04-02, mutual SSH cross-access is configured across all three Pis using ed25519 keys plus SSH config aliases, so any Pi can `ssh pi-01`, `ssh pi-02`, or `ssh pi-03` without prompts.

## OpenClaw Config Notes

- As of 2026-04-02, Peter restored pi-02 OpenClaw from `~/.openclaw/openclaw.json.bak.4` (March 26 backup) and restarted with `openclaw gateway --force`.
- OpenAI Codex access was restored from `openclaw.json.bak-2026-04-01-security`, with auth profile `openai-codex:petermartinez225@gmail.com`, `gpt-5.4` restored to the main agent models list, and set as default with LM Studio fallback.
- Full local execution access was enabled on pi-02:
  - `tools.exec.security = full`
  - `tools.exec.ask = off`
  - `tools.exec.host = gateway`
  - `agents.defaults.sandbox.mode = off`
  - `~/.openclaw/exec-approvals.json` sets `main` to `security=full`, `ask=off`
- Revert command saved by Peter:
  - `cp ~/.openclaw/openclaw.json.bak-20260401-220655-pre-full-access ~/.openclaw/openclaw.json`
  - `openclaw gateway --force`

## Backlog System

- Peter wants a lightweight assistant-managed backlog for ideas, asks, experiments, and future work.
- Backlog file: `/home/peter/.openclaw/workspace/BACKLOG.md`
- Peter can ask to add, remove, complete, reprioritize, or review items later.

## How to Update This File

- Add significant learnings, decisions, and context
- Review periodically and distill what matters long-term
- This file persists across all sessions, so write things you want to remember everywhere
- Keep it concise — this is curated wisdom, not a log
- **For project-specific context, update PROJECTS-KNOWLEDGE-BASE.md instead**
