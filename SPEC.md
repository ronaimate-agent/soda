# Soda — AI-Powered Developer Kanban Board

## Summary

A local developer tool for managing projects with Kanban boards and AI-powered task execution. No authentication — all users are visual entities (human or AI). Designed to work with any agentic CLI tool (OpenCode, Codex, etc.) via a callback mechanism.

## Navigation

- **Ideas** — Global idea collection, project-independent
- **Projects** — Switcher in header, each project has its own Kanban board
- **Users** — Global user management (human and AI)
- **Settings** — Global settings

## Ideas

Project-independent idea collection. Each idea card has:
- Title, description
- "Create Project" button — selects which Architect AI user runs the generation
- Configurable system prompt per idea for the Architect AI

Generation flow:
1. Architect AI receives idea description + configured system prompt
2. If AI has questions → project goes to "Awaiting Input" status
3. User answers questions (iterative)
4. When AI is ready → creates project + Backlog items

## Kanban Columns

| Column | Description |
|--------|-------------|
| **Backlog** | Task waiting, no active work |
| **Running** | Agent actively working |
| **Blocked** | AI has questions, waiting for user |
| **Review** | AI completed work, user needs to review |
| **Done** | Completed tasks |

## Task Card

| Field | Description |
|-------|-------------|
| Title | Summary |
| Description | Detailed text |
| Assignee | One user (human or AI) |
| Complexity | XS / S / M / L / XL |
| Comments | Question-answer history, review notes |

## Task Lifecycle

1. **Backlog → Running** (manual drag) — app executes the assignee AI's command
2. If AI has questions → **Blocked** + question as comment
3. User answers → manually drags back to **Running** (with comment history)
4. When complete → **Review** (AI auto-reviews if configured)
5. User decides: back to **Running** or to **Done**

## Callback Mechanism

The app exposes `POST /api/callback` for the execute command to report status:

```json
{
  "taskId": 1,
  "status": "blocked" | "review",
  "question": "...",
  "summary": "..."
}
```

The execute command is responsible for calling this endpoint when done.

## User Configuration

| Field | Human | AI |
|-------|-------|-----|
| Name | ✓ | ✓ |
| Role | ✓ | ✓ |
| Type | Human | AI |
| Provider | – | ✓ |
| API Key | – | ✓ |
| Model | – | ✓ |
| System Prompt | – | ✓ |
| Execute Command | – | ✓ (with template variables) |

### Template Variables for Execute Command

| Variable | Description |
|----------|-------------|
| `{{task.id}}` | Task ID |
| `{{task.title}}` | Task title |
| `{{task.description}}` | Task description |
| `{{task.complexity}}` | XS/S/M/L/XL |
| `{{task.comments}}` | Comment history as JSON |
| `{{project.name}}` | Project name |
| `{{callback.url}}` | Callback endpoint URL |

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python 3.12+) |
| Database | PostgreSQL 16 (SQLAlchemy 2.0 + asyncpg) |
| Frontend | HTML / CSS / JS (Jinja2 templates) |
| AI Integration | OpenCode CLI (in-container, auth managed via UI) |
| Container | Single Docker image (`ghcr.io/ronaimate-agent/soda:latest`) |
| CI/CD | GitHub Actions → GHCR |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Project list |
| `GET` | `/ideas` | Ideas sheet |
| `GET` | `/project/:id` | Kanban board |
| `GET` | `/users` | User management |
| `GET` | `/settings` | Settings |
| `GET` | `/api/projects` | List projects |
| `POST` | `/api/projects` | Create project |
| `GET` | `/api/projects/:id/tasks` | List tasks |
| `POST` | `/api/projects/:id/tasks` | Create task |
| `PATCH` | `/api/tasks/:id` | Update task |
| `DELETE` | `/api/tasks/:id` | Delete task |
| `POST` | `/api/tasks/:id/move` | Move task to column |
| `POST` | `/api/tasks/:id/comments` | Add comment |
| `GET` | `/api/ideas` | List ideas |
| `POST` | `/api/ideas` | Create idea |
| `POST` | `/api/ideas/:id/generate` | Generate project |
| `GET` | `/api/users` | List users |
| `POST` | `/api/users` | Create user |
| `PATCH` | `/api/users/:id` | Update user |
| `DELETE` | `/api/users/:id` | Delete user |
| `GET` | `/api/settings` | Get settings |
| `PATCH` | `/api/settings` | Update settings |
| `POST` | `/api/callback` | Task callback endpoint |

## Deployment

Single container via Portainer. OpenCode CLI pre-installed in image. API keys managed via the UI (saved directly to OpenCode auth.json).

### Prerequisites
- PostgreSQL database named `soda` must exist (app creates tables automatically)
- `DATABASE_URL` environment variable in SQLAlchemy format

### Proxy Host
- Domain: `soda.home`
- Forward: `soda:8000`
