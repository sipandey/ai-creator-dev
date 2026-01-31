# Creator AI – File Index (Canonical Code Map)

> This file is the **authoritative map of the entire codebase**.
> It tells any LLM or engineer **what exists, where it lives, and why it exists**.
> Must be kept in sync with `project-context.md`.

---

## 1. Repository Root

creator-ai/

yaml
Copy code

| Path               | Description                                   |
| ------------------ | --------------------------------------------- |
| README.md          | High-level project overview & setup           |
| project-context.md | Canonical product + architecture decisions    |
| file_index.md      | This file – complete code map                 |
| DEPLOYMENT.md      | Production deployment guide (Vercel + Render) |

---

## 2. Backend – FastAPI (`apps/api/app/`)

apps/api/app/

yaml
Copy code

---

### 2.1 Core Infrastructure

| File             | Description                                  |
| ---------------- | -------------------------------------------- |
| main.py          | FastAPI entry point; registers all routers   |
| core/database.py | SQLAlchemy engine, session, Base             |
| core/deps.py     | Common dependencies (DB, auth, current user) |
| core/auth.py     | JWT token creation & config                  |
| core/security.py | Password hashing (bcrypt)                    |
| core/config.py   | Environment configuration                    |

---

### 2.2 Models (Database Layer)

| File                     | Description                                  |
| ------------------------ | -------------------------------------------- |
| models/user.py           | User ORM model                               |
| models/persona.py        | CreatorPersona ORM model (core memory)       |
| models/feedback.py       | Feedback ORM model (learning loop)           |
| models/preference.py     | Preference ORM model (hard/soft constraints) |
| models/content_source.py | Source material model (videos/links)         |

> Models define **what the system remembers**.

---

### 2.3 Schemas (Validation Layer)

| File                      | Description                         |
| ------------------------- | ----------------------------------- |
| schemas/auth.py           | Signup & login request validation   |
| schemas/user.py           | User profile schemas                |
| schemas/persona_schema.py | Detailed persona validation schemas |

> Schemas protect the system from invalid input.

---

### 2.4 Services (Business Logic)

| File                                    | Description                                               |
| --------------------------------------- | --------------------------------------------------------- |
| services/auth_service.py                | User creation & authentication                            |
| services/persona_service.py             | Persona persistence (upsert)                              |
| services/persona_builder.py             | Persona creation orchestration                            |
| services/persona_validator.py           | Persona schema validation                                 |
| services/persona_refinement_service.py  | Apply feedback to persona                                 |
| services/preference_service.py          | Load & structure preferences                              |
| services/enhanced_persona_service.py    | Multi-modal persona orchestration                         |
| services/multi_modal_persona_service.py | Processing text/video/audio inputs                        |
| services/video_processing_service.py    | Video/audio extraction & transcription                    |
| services/strategy_service.py            | Strategy generation, invalidation, and regeneration logic |

> Services coordinate **agents + DB**, but contain no HTTP logic.

---

### 2.5 Agents (Reasoning Layer)

| File                                    | Description                   |
| --------------------------------------- | ----------------------------- |
| agents/style_analysis_agent.py          | LLM-based persona extraction  |
| agents/strategy_agent.py                | Weekly content strategy agent |
| agents/script_agent.py                  | Reel script generation agent  |
| agents/persona_refinement_agent.py      | Conservative persona updates  |
| agents/enhanced_style_analysis_agent.py | Advanced multi-modal analysis |

> Agents are **stateless**, deterministic in structure, and LLM-backed.

---

### 2.6 LLM Integration

| File          | Description                               |
| ------------- | ----------------------------------------- |
| llm/client.py | OpenAI client wrapper (provider-agnostic) |

> All LLM calls go through this layer.

---

### 2.7 Prompts (LLM Control)

| File                      | Description               |
| ------------------------- | ------------------------- |
| prompts/style_analysis.py | Persona extraction prompt |

> Prompts are **versionable product logic**, not ad-hoc strings.

---

### 2.8 API Routes (HTTP Layer)

| File                       | Description                         |
| -------------------------- | ----------------------------------- |
| routes/auth.py             | Signup & login endpoints            |
| routes/persona.py          | Persona read/write                  |
| routes/persona_builder.py  | Persona creation endpoint           |
| routes/strategy.py         | Weekly strategy endpoint            |
| routes/script.py           | Script generation endpoint          |
| routes/feedback.py         | Feedback submission endpoint        |
| routes/persona_refine.py   | Manual persona refinement           |
| routes/preferences.py      | Preference management               |
| routes/enhanced_persona.py | Multi-modal persona analysis routes |
| routes/users.py            | User management routes              |

> Routes are **thin controllers**, no business logic.

---

## 3. Frontend – Next.js (`apps/web/`) — PHASE 10

apps/web/

pgsql
Copy code

| Path                | Description                  |
| ------------------- | ---------------------------- |
| app/                | Next.js App Router root      |
| app/login/          | Login page                   |
| app/signup/         | Signup page                  |
| app/onboarding/     | Creator onboarding flow      |
| app/dashboard/      | Main creator dashboard       |
| app/strategy/       | Weekly plan UI               |
| app/script/         | Script generation UI         |
| app/preferences/    | Preferences & constraints UI |
| app/about/          | About page                   |
| components/         | Shared UI components         |
| services/api.ts     | API client wrapper           |
| services/auth.ts    | Auth helpers                 |
| services/persona.ts | Persona-related API calls    |

> Frontend is **presentation + orchestration only**.
> No AI logic lives here.

---

## 4. Shared Packages (`packages/`)

packages/

yaml
Copy code

| Folder     | Description                         |
| ---------- | ----------------------------------- |
| schemas/   | Shared TypeScript schemas (planned) |
| constants/ | Persona templates, limits (planned) |
| utils/     | Shared helpers (future)             |

---

## 5. Infra & Config

apps/api/

yaml
Copy code

| File             | Description                                |
| ---------------- | ------------------------------------------ |
| Dockerfile       | Container definition for Render deployment |
| requirements.txt | Python dependencies                        |

---

## 6. Phase Coverage Status

| Phase                           | Status       |
| ------------------------------- | ------------ |
| Phase 1 – Architecture          | ✅           |
| Phase 2 – Monorepo              | ✅           |
| Phase 3 – Database              | ✅           |
| Phase 4 – Auth                  | ✅           |
| Phase 5 – Persona               | ✅           |
| Phase 6 – LLM Persona           | ✅           |
| Phase 7 – Strategy & Scripts    | ✅           |
| Phase 8 – Feedback              | ✅           |
| Phase 9 – Preferences           | ✅           |
| Phase 10 – Frontend UI          | ✅ Completed |
| Phase 11 – Enhanced Multi-Modal | ✅ Completed |

---

## 7. Update Rules (MANDATORY)

- Every new file → add here
- Every deleted file → remove here
- Every repurposed file → update description

This file + `project-context.md` together form **system memory**.

---

## 8. LLM Resume Instruction (Reusable)

When resuming work with any LLM, say:

> “You are working on the Creator AI project.  
> Read `project-context.md` for decisions and `file_index.md` for code structure.
> Continue from Phase 11 (Enhanced Multi-Modal).”

---

**This file is authoritative. Keep it in sync.**
