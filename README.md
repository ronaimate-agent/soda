# Soda — AI-Powered Developer Kanban Board

A local developer tool for managing projects with Kanban boards and AI-powered task execution. Works with any agentic CLI tool (OpenCode, Codex, etc.) via a callback mechanism.

## Features

- **Kanban Board** — Drag & drop tasks across 5 columns (Backlog → Running → Blocked → Review → Done)
- **AI Task Execution** — Assign tasks to AI users, app runs their configured command automatically
- **Callback Mechanism** — CLI tool reports status back via HTTP callback
- **Ideas Sheet** — Generate projects from ideas using Architect AI
- **User Management** — Configurable human and AI users with per-user API keys, models, system prompts
- **Review Pipeline** — Optional AI code review on Review column entry

## Quick Start

### Prerequisites

1. PostgreSQL 16 with `soda` database created:
   ```sql
   CREATE DATABASE soda;
   ```
2. Docker + Portainer

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | – | PostgreSQL connection string (e.g. `postgresql+asyncpg://soda:***@postgres:5432/soda`) |

### Deployment (Portainer)

The `agent-deployments` repository includes the soda service. Add to your stack:

```yaml
services:
  soda:
    image: ghcr.io/ronaimate-agent/soda:latest
    container_name: soda
    restart: unless-stopped
    environment:
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - soda-uploads:/app/uploads
      - soda-data:/root/.local/share
    networks:
      - proxy-net
```

Then configure proxy host: `soda.home` → `soda:8000`.

### First Setup

1. Open `http://soda.home`
2. Go to **Users** → Create an **AI** user with:
   - Name, Provider, Model, API Key
   - System prompt (personality/specialty)
   - Execute command template (with `{{task.description}}`, `{{callback.url}}`, etc.)
3. Create a project and start adding tasks!

## Architecture

- **Single container** — FastAPI app + OpenCode CLI + PostgreSQL connection
- **API keys managed via UI** — saved to `~/.local/share/opencode/auth.json` on save
- **No auth** — local-only dev tool
- **Tool-agnostic** — app doesn't know which CLI runs, only executes configured commands

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python 3.12+) |
| Database | PostgreSQL 16 (SQLAlchemy 2.0 + asyncpg) |
| Frontend | HTML / CSS / JS (Jinja2 templates, modern dark theme) |
| AI CLI | OpenCode (in-container) |
| Container | Single Docker image (`ghcr.io/ronaimate-agent/soda:latest`) |

## License

MIT
