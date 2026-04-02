# Pi Cluster Current Setup

_Last updated: 2026-04-02_

## Quick answer on the RAM

The two Pis with **8 GB of RAM** are:
- **pi-01**
- **pi-02**

The one with **4 GB of RAM** is:
- **pi-03**

## Cluster Overview

Peter’s current Pi cluster is a 3-node Raspberry Pi fleet connected over both:
- local LAN (`10.0.0.x`)
- Tailscale (`100.x.x.x`)

Each node can now SSH to the others using:
- `ssh pi-01`
- `ssh pi-02`
- `ssh pi-03`

That makes the fleet workable as a small distributed home lab / automation cluster.

## Fleet Summary

| Host | LAN IP | Tailscale IP | Model | RAM | Root Disk | Main Role |
|---|---:|---:|---|---:|---:|---|
| pi-01 | 10.0.0.3 | 100.84.93.86 | Raspberry Pi 4 Model B Rev 1.5 | 8 GB | 59 GB | Data + RAG + storage + monitoring |
| pi-02 | 10.0.0.5 | 100.99.6.88 | Raspberry Pi 4 Model B Rev 1.5 | 8 GB | 29 GB | OpenClaw + automation + nginx |
| pi-03 | 10.0.0.4 | 100.121.226.64 | Raspberry Pi 4 Model B Rev 1.2 | 4 GB | 29 GB | Lightweight support / expansion node |

All three are running:
- Debian GNU/Linux 13 (trixie)
- Kernel `6.12.47+rpt-rpi-v8`
- Docker + containerd
- Tailscale
- SSH
- cron

---

## pi-01

### Specs
- **Model:** Raspberry Pi 4 Model B Rev 1.5
- **RAM:** 8 GB
- **Root disk:** 59 GB microSD
- **Extra storage:** 223.6 GB disk mounted at `/mnt/vectordb`
- **IPs:**
  - LAN: `10.0.0.3`
  - Tailscale: `100.84.93.86`

### Summary
pi-01 is the **main infrastructure/data node** in the cluster.

This is where the heavier backend stack lives, especially the pieces tied to Peter’s RAG and data platform.

### Main services observed
Docker containers and services on pi-01 include:
- cluster API
- cluster web
- cluster embedding service
- Postgres
- Redis
- Qdrant
- MinIO
- Portainer
- Prometheus
- Grafana
- node-exporter

### Role assessment
pi-01 is best understood as:
- the **data services node**
- the **RAG backend host**
- the **storage-heavy machine**
- the **observability hub**

This is the most infrastructure-dense Pi in the fleet.

---

## pi-02

### Specs
- **Model:** Raspberry Pi 4 Model B Rev 1.5
- **RAM:** 8 GB
- **Root disk:** 29 GB microSD
- **IPs:**
  - LAN: `10.0.0.5`
  - Tailscale: `100.99.6.88`

### Summary
pi-02 is the **control plane / automation node**.

This is the Pi running OpenClaw and the local automation surface Peter is actively using.

### Main services observed
Host services and ports indicate:
- OpenClaw gateway
- nginx
- Docker
- Tailscale
- SSH
- cron
- node-exporter / management-related services

### Known functional role
From Peter’s notes and the live inspection:
- OpenClaw runs here
- DM automations run here
- nginx is serving as ingress / reverse proxy
- this node was restored and reconfigured on 2026-04-02
- full local execution access is enabled here for OpenClaw

### Role assessment
pi-02 is best understood as:
- the **assistant/control node**
- the **automation node**
- the **entrypoint / reverse proxy node**

This is the Pi that feels most like the operational “front door” of the setup.

---

## pi-03

### Specs
- **Model:** Raspberry Pi 4 Model B Rev 1.2
- **RAM:** 4 GB
- **Root disk:** 29 GB microSD
- **IPs:**
  - LAN: `10.0.0.4`
  - Tailscale: `100.121.226.64`

### Summary
pi-03 is currently the **lightest-use node** and looks like the expansion / support machine.

### Main services observed
Currently it appears to be running a fairly minimal support stack:
- Portainer agent
- node-exporter
- Docker
- Tailscale
- SSH
- cron

### Role assessment
pi-03 is best understood as:
- the **spare / growth node**
- a good place for future experiments
- a lower-risk place to add new services later

Right now it is not carrying the same kind of workload as pi-01 or pi-02.

---

## Current Architecture Pattern

The cluster currently breaks down like this:

### pi-01 = data + backend infrastructure
- RAG stack
- vector DB
- object storage
- cache
- relational database
- monitoring stack

### pi-02 = assistant + automation + ingress
- OpenClaw
- nginx
- automation workflows
- interactive management surface

### pi-03 = standby / support / future capacity
- Portainer agent
- monitoring visibility
- room for future services

That split is actually pretty reasonable:
- heavy storage and backend services are isolated to pi-01
- user-facing automation is isolated to pi-02
- future experiments can land on pi-03

## One-Line Summary

Peter’s Pi cluster currently consists of **two 8 GB Raspberry Pi 4s (pi-01 and pi-02)** handling the main backend and automation roles, plus **one 4 GB Raspberry Pi 4 (pi-03)** acting as a lighter support and expansion node.
