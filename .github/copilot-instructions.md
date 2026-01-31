# Creator AI - Copilot Instructions

## Architecture Overview

- **Monorepo**: `apps/api` (FastAPI Python backend) + `apps/web` (Next.js TypeScript frontend)
- **Agent Layer**: Isolated business logic, stateless, JSON-in/JSON-out, LLM-agnostic
- **Memory Model**: Persona (identity) → Preferences (intent) → Feedback (learning)
- **Data Flow**: Web client → FastAPI → Agent layer → Postgres (Neon)

## Key Patterns & Conventions

### Agent Development

- Agents are pure functions in `apps/api/app/agents/` - no DB/HTTP/auth logic
- Input validation required, output must be valid JSON matching schemas in `packages/schemas/`
- LLM calls via `app.llm.client.call_llm(system_prompt, user_prompt)` - easily replaceable
- Example: `style_analysis_agent.py` - takes `list[str]` samples, returns persona dict

### API Structure

- Routes in `apps/api/app/routes/` include auth, persona, strategy, script, feedback, preferences
- Services layer calls agents, handles DB operations
- Models in `apps/api/app/models/` use SQLAlchemy, avoid ENUMs for flexibility
- Migrations via Alembic in `apps/api/alembic/`

### Frontend Integration

- API calls via `apps/web/services/api.ts` with Bearer token auth
- Components in `apps/web/components/` organized by feature (auth, dashboard, script, etc.)
- Types in `apps/web/types/` mirror API schemas

### Database & Persistence

- Validation always occurs before persistence
- Persona is single source of truth - all agents respect it
- Confidence scores evolve through feedback loops
- Use `alembic upgrade head` to apply migrations

## Development Workflows

### Running the Stack

- **API**: `cd apps/api && uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Web**: `cd apps/web && npm run dev` (starts on :3000)
- **DB Setup**: Ensure Neon Postgres connection, run migrations

### Adding Features

- New agents: Define in `agents/`, add route in `routes/`, call from service
- UI changes: Update components, ensure API integration via services
- Schema changes: Update models, create migration, update frontend types

## Design Principles (Non-Negotiable)

- Agents isolated from HTTP/DB layers
- LLMs are replaceable components, not core system
- Learning is incremental and conservative
- MVP first, rigidity later
- Avoid platform lock-in, premature automation

## Common Pitfalls

- Don't add DB logic to agents - use services layer
- Always validate inputs/outputs against schemas
- Don't hardcode LLM provider specifics
- Respect all three memory layers (persona/preferences/feedback)
