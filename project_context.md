# Creator AI – Project Context (Canonical)

This document is the single source of truth for all architectural, product, and technical decisions.
Any LLM or engineer should read this first before making changes.
This file is designed to act as long-term system memory.

## 1. Product Vision

**Creator AI** is an agentic AI platform for short-form video creators (Instagram Reels / Shorts / TikTok).

**Core idea:**
Help creators ideate, plan, and script content that sounds like them, not generic AI output.

**Supported creators:**
- New / faceless creators (no historical content)
- Existing creators (with past content)

## 2. Design Principles (LOCKED)

These principles must not be violated:
- **Persona is the single source of truth**
- Agents are isolated from HTTP & DB layers
- LLMs are replaceable components, not the system
- Validation always before persistence
- Learning is incremental and conservative
- MVP first, rigidity later
- Avoid premature ENUMs
- Avoid early automation
- Avoid platform lock-in

## 3. High-Level Architecture

```plaintext
Client (Next.js UI)
↓
FastAPI Backend
↓
Agent Layer (LLM + reasoning)
↓
Persona / Preferences / Memory
↓
Postgres (Neon)
```

## 4. Phase History & Ordering (UPDATED)

- **Phase 1 – Architecture**
    - Agent-first system design
    - Persona-centric intelligence model
    - Backend-first execution
- **Phase 2 – Monorepo**
    - `apps/api` (FastAPI)
    - `apps/web` (Next.js)
    - `packages/*` reserved for shared context
- **Phase 3 – Database**
    - Neon (serverless Postgres)
    - SQLAlchemy 2.x
    - Alembic migrations
    - ENUMs avoided for MVP flexibility
- **Phase 4 – Auth & Users**
    - Email/password auth
    - JWT-based authentication
    - User model
    - `creator_type` persisted
- **Phase 5 – Persona Foundation**
    - Persona schema defined and locked
    - Rule-based style analysis (v0)
    - Persona persisted per user
    - Confidence score introduced
- **Phase 6 – LLM Persona Analysis**
    - LLM-backed Style Analysis Agent
    - Prompt isolation
    - JSON-only outputs
    - Persona validation before persistence
- **Phase 7 – Strategy & Script Generation**
    - Weekly content strategy agent
    - Reel script generation agent
    - Persona reused across all agents
- **Phase 8 – Feedback Loop & Learning**
    - Explicit feedback capture
    - Feedback persistence
    - Conservative persona refinement
    - Confidence evolution
- **Phase 9 – Preferences & Constraints**
    - Hard vs soft preferences
    - Preference persistence
    - Agents respect constraints
    - Deep personalization achieved
- **✅ Phase 10 – Frontend UI (Completed)**
    - Creator onboarding UI
    - Persona visibility & editing
    - Strategy view (weekly plan)
    - Script generation UI
    - Feedback & preference controls
- **1️⃣1️⃣ Phase 11 – Enhanced Multi-Modal Persona (Completed)**
    - Video/Audio processing pipeline (FFmpeg)
    - Instagram API integration (Service layer)
    - Multi-modal persona analysis agent
    - Advanced persona refinement
- **1️⃣2️⃣ Phase 12 – Automation & Draft Workflow (FUTURE)**
    - Draft queues
    - Content calendar
    - Human-in-the-loop approvals
    - Optional scheduling (no auto-posting initially)

## 5. Persona Schema (LOCKED CONTRACT)

**Persona JSON v2 (Enhanced - Current Standard):**

```json
{
  "language": "english | hinglish | hindi",
  "tone": ["empathetic", "honest", "informative", "motivational"],
  "energy_level": "low | medium | high",
  "hook_style": "problem-first | story-first | fact-first",
  "cta_style": "soft | direct | follow",
  "formats": ["talking-head", "text-overlay", "b-roll"],
  "topics": ["string"],
  "pacing": "slow | moderate | fast",
  "communication_patterns": {
    "sentence_complexity": "simple | moderate | complex",
    "vocabulary_level": "casual | professional | academic",
    "filler_words": ["string"],
    "signature_phrases": ["string"],
    "question_frequency": "low | medium | high"
  },
  "emotional_markers": {
    "enthusiasm_indicators": ["string"],
    "vulnerability_expressions": ["string"],
    "humor_style": "witty | sarcastic | wholesome | dry | none",
    "empathy_level": "low | medium | high",
    "authenticity_markers": ["string"]
  },
  "visual_preferences": {
    "color_schemes": ["string"],
    "text_positioning": "top | center | bottom | dynamic",
    "visual_metaphors": ["string"],
    "background_style": "minimal | busy | branded | natural"
  },
  "timing_patterns": {
    "pause_frequency": "low | medium | high",
    "speech_rhythm": "steady | varied | dramatic",
    "content_pacing": "slow | moderate | fast",
    "hook_timing": 3.5
  },
  "version": "v2",
  "confidence_score": 0.85
}
```

**Rules:**
- Persona is stored in DB (now supports V2 with nested structures).
- Persona is reused by all agents.
- Persona updates happen only via controlled flows.
- V2 introduces multi-modal insights (visual, timing, emotional).

## 6. Memory Model (IMPORTANT)

The system has three memory layers:
1. **Persona** $\rightarrow$ Identity (who I am)
2. **Preferences** $\rightarrow$ Intent (how I want things)
3. **Feedback** $\rightarrow$ Learning (how I react)

Agents must respect all three.

## 7. Agent System

**Implemented Agents**

- **Style Analysis Agent**
    - Input: Sample texts
    - Output: Persona JSON
    - Engine: LLM-powered
- **Strategy Agent**
    - Input: Persona + Preferences
    - Output: Weekly content plan
- **Script Agent**
    - Input: Persona + Preferences + Topic
    - Output: Reel script
- **Enhanced Style Agent**
    - Input: Video/Audio/Text
    - Output: Multi-modal Persona Insights

**Agent Requirements:**
- Stateless
- JSON-in / JSON-out
- No DB or HTTP logic
- Replaceable implementations

## 8. Strategy Schema (v1)

**Strategy JSON:**

```json
{
  "week": "string",
  "goals": ["string"],
  "reels": [
    {
      "day": "Monday | Tuesday | Wednesday | Thursday | Friday",
      "topic": "string",
      "hook_angle": "string",
      "format": "talking-head | text-overlay | b-roll"
    }
  ]
}
```

**Persistence:**
- Strategy is now persisted per user/week (`content_strategies` table).
- Prevents re-generating plan on every page load.

## 9. Script Schema (v1)

**Script JSON:**

```json
{
  "hook": "string",
  "scenes": ["string"],
  "caption": "string",
  "cta": "string"
}
```

**Script Lifecycle (DB Model):**
- `status`: `DRAFT` | `FILMED` | `PUBLISHED` | `ARCHIVED`
- `performance_data`: JSON (views, likes, etc.)
- `script_json`: The content (hook, scenes, etc.)

## 10. Cloud & Infra (LOCKED)

- **Frontend:** Vercel
- **Backend:** Render (Free Tier)
- **Database:** Neon

**Principle:** Infrastructure must not slow a solo founder.

## 11. Current Status

- ✅ Phase 1 – Architecture
- ✅ Phase 2 – Monorepo
- ✅ Phase 3 – Database
- ✅ Phase 4 – Auth & Users
- ✅ Phase 5 – Persona Foundation
- ✅ Phase 6 – LLM Persona Analysis
- ✅ Phase 7 – Strategy & Scripts
- ✅ Phase 8 – Feedback Loop
- ✅ Phase 9 – Preferences
- ✅ Phase 10 – Frontend UI
- ✅ Phase 11 – Enhanced Multi-Modal Persona
- ⏭️ **Current focus: Phase 12 – Automation & Workflow**

## 12. Future Roadmap & Suggestions (Intelligence)

- **Multi-modal Inputs:** Deepen video analysis (pacing, visual style) beyond transcripts.
- **Trend Analysis:** Scrape trending topics (TikTok/Reels) to feed Strategy Agent.
- **Auto-Posting:** Leverage Instagram API for scheduled publishing.
- **Feedback Automation:** Use engagement data (views, likes) to refine persona confidence automatically.
- **Voice Cloning:** Synthesize scripts in the creator's voice for drafting/voiceovers.

## 13. How to Resume With Any LLM

Provide this file and instruct:

> "You are working on the Creator AI project. Read this file as canonical context. Continue from Phase 12 and ask for files if needed."

This file is the canonical long-term memory of the Creator AI system.
