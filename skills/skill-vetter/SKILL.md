---
name: skill-vetter
version: 1.0.0
description: Practical skill vetting for this OpenClaw workspace. Use before installing skills from ClawHub, GitHub, or other sources. Review source, files touched, command behavior, network access, and secret exposure risk.
---

# Skill Vetter 🔒

Practical security-first vetting protocol for skills in this OpenClaw workspace. Use judgment, not rigid blanket rules.

## When to Use

- Before installing any skill from ClawHub
- Before manually copying in skills from GitHub repos or gists
- When evaluating skills shared by other agents or external sources
- Anytime a skill includes scripts, hooks, network calls, or touches sensitive files

## Vetting Protocol

### Step 1: Source Check

```
Questions to answer:
- [ ] Where did this skill come from?
- [ ] Is the author known/reputable?
- [ ] How many downloads/stars does it have?
- [ ] When was it last updated?
- [ ] Are there reviews from other agents?
```

### Step 2: Code Review (MANDATORY)

Read the skill files that actually define behavior: `SKILL.md`, scripts, hooks, handler files, manifests, and metadata. Check for these red flags and context questions:

```
🚨 HIGH-CONCERN SIGNALS
─────────────────────────────────────────
• Sends data to unexpected external servers
• Requests credentials/tokens/API keys without a clear user-approved need
• Reads ~/.ssh, ~/.aws, ~/.config, browser profiles, or credential stores without clear reason
• Uses eval() / exec() with untrusted or external input
• Modifies files outside the workspace without a strong reason
• Installs packages or binaries without clearly saying so
• Uses obfuscated, encoded, minified, or intentionally hard-to-read code
• Requests elevated/sudo permissions
• Accesses cookies, sessions, or auth stores
• Hides network behavior behind helper scripts or encoded payloads
─────────────────────────────────────────
```

Notes:
- Access to workspace files like `MEMORY.md`, `USER.md`, `SOUL.md`, or `TOOLS.md` is **not automatically malicious** in OpenClaw; judge whether that access matches the skill’s stated purpose.
- Network calls are not automatically bad; check whether the destination and purpose are expected and clearly disclosed.
- Base64 or compressed content is not automatically bad either, but it deserves closer inspection if it hides behavior.

### Step 3: Permission Scope

```
Evaluate:
- [ ] What files does it need to read?
- [ ] What files does it need to write?
- [ ] What commands does it run?
- [ ] Does it need network access? To where?
- [ ] Is the scope minimal for its stated purpose?
```

### Step 4: Risk Classification

| Risk Level | Examples | Action |
|------------|----------|--------|
| 🟢 LOW | Notes, weather, formatting | Basic review, install OK |
| 🟡 MEDIUM | File ops, browser, APIs | Full code review required |
| 🔴 HIGH | Credentials, trading, system | Human approval required |
| ⛔ EXTREME | Security configs, root access | Do NOT install |

## Output Format

After vetting, produce this report:

```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name]
Source: [ClawdHub / GitHub / other]
Author: [username]
Version: [version]
───────────────────────────────────────
METRICS:
• Downloads/Stars: [count]
• Last Updated: [date]
• Files Reviewed: [count]
───────────────────────────────────────
RED FLAGS: [None / List them]

PERMISSIONS NEEDED:
• Files: [list or "None"]
• Network: [list or "None"]  
• Commands: [list or "None"]
───────────────────────────────────────
RISK LEVEL: [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]

VERDICT: [✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / ❌ DO NOT INSTALL]

NOTES: [Any observations]
═══════════════════════════════════════
```

## Quick Vet Commands

For GitHub-hosted skills:
```bash
# Check repo stats
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'

# List skill files
curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'

# Fetch and review SKILL.md
curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
```

## Trust Hierarchy

1. **Official OpenClaw skills** → Lower scrutiny (still review)
2. **High-star repos (1000+)** → Moderate scrutiny
3. **Known authors** → Moderate scrutiny
4. **New/unknown sources** → Maximum scrutiny
5. **Skills requesting credentials** → Human approval always

## Workspace Vetting Heuristics

Use these practical rules in this workspace:

- Prefer `clawhub inspect <slug> --files` or reading installed files before trusting a skill
- Treat official OpenClaw/OpenClaw-skills sources as lower risk, not zero risk
- Match the requested capability to the permissions the skill actually needs
- Ask Peter before enabling anything high-risk, especially hooks, credential access, destructive file operations, or broad external network behavior
- Document non-obvious conclusions when a skill is reviewed and approved

## Remember

- No skill is worth compromising security
- When in doubt, pause or install cautiously
- Ask your human for high-risk decisions
- Document what you vet for future reference

---

*Paranoia is a feature.* 🔒🦀
