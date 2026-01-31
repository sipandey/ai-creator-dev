from app.agents.persona_refinement_agent import refine_persona

def apply_feedback(persona: dict, feedback: list[dict]) -> dict:
    return refine_persona(persona, feedback)
