# BACKLOG.md

A lightweight backlog / parking lot for Peter's ideas, asks, experiments, and future work.

How to use:
- Peter can tell Belle to add something to the backlog.
- Peter can ask to remove, complete, reprioritize, or review backlog items.
- Keep entries concise but useful.
- This is a working memory surface, not a polished project plan.

## Active

- [ ] Give Belle all the details to document the Pi cluster, including how it is networked, what resources each Pi has, and how the overall setup is structured.

## Completed

- [x] Give Belle SSH access to the other Pis in the network so she can help manage them.
  - Completed 2026-04-02.
  - Mutual SSH trust is now configured across pi-01, pi-02, and pi-03 using ed25519 keys and hostname aliases.
  - Any Pi can now SSH to the others without prompts over Tailscale.
