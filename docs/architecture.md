# System Architecture

## High-Level Architecture
Client (Next.js UI) ↓ FastAPI Backend ↓ Agent Layer (LLM + reasoning) ↓ Persona / Preferences / Memory ↓ Postgres (Neon)

## Monorepo Structure
creator-ai/ ├── apps/ │ ├── api/ # FastAPI backend │ └── web/ # Next.js frontend ├── packages/ # Shared context └── infra/ # Infrastructure code


## Agent Architecture

### Core Requirements

- **Stateless** - No internal state between calls
- **JSON-in / JSON-out** - Clean data contracts
- **No DB or HTTP logic** - Pure business logic
- **Replaceable implementations** - LLM agnostic

### Agent Isolation

Agents are completely isolated from:
- HTTP request/response handling
- Database operations
- Authentication/authorization
- External API calls

All I/O is handled by the service layer.