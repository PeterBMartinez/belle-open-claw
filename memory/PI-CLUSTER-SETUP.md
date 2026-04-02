# Pi Cluster Setup Analysis

_Last updated: 2026-04-02_

## Overview

Peter currently has a 3-node Raspberry Pi cluster connected on both local LAN (`10.0.0.x`) and Tailscale (`100.x.x.x`). The fleet now has mutual SSH trust configured, so each node can SSH to the others using hostname aliases (`pi-01`, `pi-02`, `pi-03`) without prompts.

## Fleet Summary

| Host | LAN IP | Tailscale IP | Hardware | RAM | Primary Role |
|---|---:|---:|---|---:|---|
| pi-01 | 10.0.0.3 | 100.84.93.86 | Raspberry Pi 4 Model B Rev 1.5 | ~8 GB | RAG / vector / storage / monitoring stack |
| pi-02 | 10.0.0.5 | 100.99.6.88 | Raspberry Pi 4 Model B Rev 1.5 | ~8 GB | OpenClaw + DM automations + reverse proxy |
| pi-03 | 10.0.0.4 | 100.121.226.64 | Raspberry Pi 4 Model B Rev 1.2 | ~4 GB | Lightweight auxiliary node / Portainer agent |

All three nodes are running:
- Debian GNU/Linux 13 (trixie)
- Kernel `6.12.47+rpt-rpi-v8`
- `tailscaled`
- `ssh`
- `cron`
- `docker` + `containerd`

## Network Structure

### Local network
- pi-01 → `10.0.0.3`
- pi-03 → `10.0.0.4`
- pi-02 → `10.0.0.5`

### Tailscale network
- pi-01 → `100.84.93.86`
- pi-02 → `100.99.6.88`
- pi-03 → `100.121.226.64`

### SSH access
Mutual ed25519 trust and SSH config aliases are in place. Operationally, this means:
- Any Pi can SSH to any other Pi directly
- Host aliases work consistently (`ssh pi-01`, `ssh pi-02`, `ssh pi-03`)
- Cross-node management and automation are now much easier

## Node-by-Node Detail

## pi-01

### Role
pi-01 is the heaviest infrastructure node in the fleet. It appears to be the data/services host for Peter’s RAG platform and observability stack.

### System profile
- Hostname: `pi-01`
- Model: Raspberry Pi 4 Model B Rev 1.5
- RAM: `8008420 kB` (~8 GB)
- Root disk: 59 GB card, 25% used
- Extra storage:
  - `sda` 223.6 GB
  - mounted as `/mnt/vectordb`

This strongly suggests pi-01 is the best place for persistent data-heavy workloads.

### Running platform services
Systemd:
- `docker.service`
- `containerd.service`
- `tailscaled.service`
- `ssh.service`
- `cron.service`

Docker containers:
- `cluster-orchestrator`
- `cluster-web`
- `cluster-api`
- `cluster-embedding`
- `cluster-postgres`
- `cluster-redis`
- `cluster-qdrant`
- `cluster-minio`
- `portainer`
- `prometheus`
- `grafana`
- `node-exporter`

### Exposed ports / likely services
- `8000`, `8080` → cluster API
- `8001`, `8002` → embedding service
- `3001` → cluster web
- `5433` → Postgres
- `6379`, `6380` → Redis
- `6333`, `6334`, `6335`, `6336` → Qdrant
- `9000`, `9001`, `9002`, `9003` → MinIO / MinIO console variants
- `9443` → Portainer
- `9090` → Prometheus
- `3000` → Grafana
- `9100` → node-exporter
- `22` → SSH

### Assessment
pi-01 is effectively the backend services and storage node:
- RAG API and embedding stack
- vector database (Qdrant)
- object storage (MinIO)
- relational DB and cache (Postgres + Redis)
- monitoring/observability (Prometheus + Grafana + node-exporter)
- container management (Portainer)

This is the most infrastructure-dense node in the fleet.

## pi-02

### Role
pi-02 is the automation and control plane node. It runs OpenClaw and related web entrypoints.

### System profile
- Hostname: `pi-02`
- Model: Raspberry Pi 4 Model B Rev 1.5
- RAM: `8008420 kB` (~8 GB)
- Root disk: 29 GB card, 27% used

### Running platform services
Systemd / host services:
- `openclaw-gateway` listening on loopback port `18789`
- `nginx.service`
- `docker.service`
- `containerd.service`
- `tailscaled.service`
- `ssh.service`
- `cron.service`

### Exposed ports / likely services
- `80`, `443` → nginx reverse proxy / web ingress
- `18789` on `127.0.0.1` and `::1` → OpenClaw gateway internal listener
- `9001` → likely Portainer agent or related Docker management endpoint
- `9100` → node-exporter
- `22` → SSH

### Known function from Peter’s notes
- OpenClaw runs here
- DM automations run here
- OpenClaw was restored from backup on 2026-04-02
- Full local execution access is enabled on this node

### Assessment
pi-02 appears to be the operational front door and orchestration node:
- OpenClaw runtime / gateway
- likely reverse proxy and HTTPS termination via nginx
- automation host for delivery-manager or assistant workflows
- likely safer to treat as the “control” node, not the storage-heavy node

## pi-03

### Role
pi-03 is currently the lightest-weight node and seems to be reserved for future expansion.

### System profile
- Hostname: `pi-03`
- Model: Raspberry Pi 4 Model B Rev 1.2
- RAM: `3887860 kB` (~4 GB)
- Root disk: 29 GB card, 18% used

### Running platform services
Systemd:
- `docker.service`
- `containerd.service`
- `tailscaled.service`
- `ssh.service`
- `cron.service`

Docker containers:
- `node-exporter`
- `portainer-agent`

### Exposed ports / likely services
- `9001` → Portainer agent
- `9100` → node-exporter
- `22` → SSH

### Assessment
pi-03 is currently a standby / expansion node with:
- observability visibility
- Portainer remote management support
- no major application workload yet

It is a good candidate for:
- experimental services
- replicas / workers
- backups / scheduled jobs
- lower-risk testing before promoting to pi-01 or pi-02

## Architecture Interpretation

The fleet currently looks like this:

- **pi-01 = data + backend services**
  - vector DB
  - object storage
  - cache
  - Postgres
  - RAG / embedding APIs
  - observability stack

- **pi-02 = control + automation**
  - OpenClaw
  - nginx ingress
  - DM automations
  - interactive operational workflows

- **pi-03 = spare / support node**
  - managed by Portainer
  - visible in monitoring
  - ready for future workloads

That’s actually a pretty sensible split:
- storage-heavy and service-heavy workloads isolated to pi-01
- user-facing orchestration isolated to pi-02
- spare capacity and future experimentation on pi-03

## Notable Gaps / Follow-up Items

These details are still missing if Peter wants a fuller infrastructure dossier:
- exact CPU/storage specs beyond what Linux reports
- docker compose file locations / service definitions
- backup jobs and restore strategy across nodes
- nginx virtual host config on pi-02
- which services are exposed to the internet vs Tailscale-only
- whether Portainer on pi-01 manages all nodes centrally
- whether `/mnt/vectordb` on pi-01 is the SSD Peter referenced
- what pi-03 is intended to become long-term

## Practical Recommendations

1. Treat this document as the baseline topology reference.
2. Next useful step: capture config sources:
   - Docker compose files on pi-01
   - nginx config on pi-02
   - backup scripts / cron jobs on all nodes
3. Add a small service ownership map:
   - what depends on what
   - which node is authoritative for each service
4. Confirm external exposure:
   - public internet vs LAN-only vs Tailscale-only
5. Decide a strategic role for pi-03 before loading it with random services.

## Quick Summary

If described in one sentence:

> Peter’s Pi cluster is a three-node Debian/Tailscale fleet where **pi-01** hosts the data and RAG infrastructure stack, **pi-02** runs OpenClaw and automation ingress, and **pi-03** is a lighter standby/support node ready for future workloads.
