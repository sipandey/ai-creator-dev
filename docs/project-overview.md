# Project Overview

## Product Vision

Creator AI is an agentic AI platform for short-form video creators (Instagram Reels / Shorts / TikTok).

**Core Idea:** Help creators ideate, plan, and script content that sounds like them, not generic AI output.

**Supported Creators:**
- New / faceless creators (no historical content)
- Existing creators (with past content)

## Design Principles (LOCKED)

These principles must not be violated:

- **Persona is the single source of truth**
- **Agents are isolated from HTTP & DB layers**
- **LLMs are replaceable components, not the system**
- **Validation always before persistence**
- **Learning is incremental and conservative**
- **MVP first, rigidity later**
- **Avoid premature ENUMs**
- **Avoid early automation**
- **Avoid platform lock-in**

## Memory Model

The system has three memory layers:

- **Persona** → Identity (who I am)
- **Preferences** → Intent (how I want things)
- **Feedback** → Learning (how I react)

Agents must respect all three layers.

## Explicit Non-Goals (For Now)

- Instagram / Meta Graph APIs
- Auto-posting
- Analytics dashboards
- Video uploads / processing
- Monetization logic