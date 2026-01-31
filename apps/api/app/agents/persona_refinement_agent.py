import json
from app.llm.client import call_llm

SYSTEM_PROMPT = """
You are a persona calibration AI for a creator voice engine.

Your job:
Refine an EXISTING persona using user feedback.

STRICT RULES:
- Do NOT change persona structure or remove fields
- Make SMALL, conservative adjustments
- Do NOT overreact to limited feedback
- Prefer adjusting intensity, not identity
- If feedback is unclear, keep persona unchanged

IMPORTANT:
- Persona is a long-term identity
- Feedback represents short-term corrections
- Never invent new traits

OUTPUT RULES:
- Output ONLY valid JSON
- Preserve persona schema exactly
"""

def refine_persona(persona: dict, feedback: list[dict]) -> dict:
    # --- safety normalization ---
    if isinstance(persona, str):
        persona = json.loads(persona)

    if not feedback:
        return persona

    user_prompt = f"""
CURRENT PERSONA (do NOT rewrite fully, only refine carefully):
{json.dumps(persona, indent=2)}

USER FEEDBACK SIGNALS:
{json.dumps(feedback, indent=2)}

GUIDELINES:
- Feedback may conflict; resolve conservatively
- Negative feedback should slightly reduce intensity, not flip traits
- Use comments more than feedback_type when available
- If confidence_score is low, be extra conservative
- Update ONLY relevant fields

TASK:
Return an UPDATED persona JSON with:
- Minor refinements based on feedback
- Same schema, same keys
- Updated `last_updated`
- Incremented `version` (e.g. v2 → v2.1)

OUTPUT:
ONLY valid JSON.
"""

    response = call_llm(SYSTEM_PROMPT, user_prompt)
    updated_persona = json.loads(response)

    return updated_persona
