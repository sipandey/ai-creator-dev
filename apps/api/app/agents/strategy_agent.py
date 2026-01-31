import json
from app.llm.client import call_llm
from app.llm.optimizer import compress_persona_for_prompt

SYSTEM_PROMPT = """
You are an expert content strategy AI for short-form video creators.

Your job is to DESIGN a weekly reel strategy, not write scripts.

CRITICAL RULES:
- Use the creator persona strictly as strategic guidance
- Do NOT invent new persona traits
- Do NOT write scripts or captions
- Keep plans realistic and repeatable

OUTPUT RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- Think like a creator planning content for consistency and growth
"""

def generate_weekly_plan(persona: dict, preferences: dict) -> dict:
    # --- safety normalization ---
    if isinstance(persona, str):
        persona = json.loads(persona)

    hard = preferences.get("hard", {})
    soft = preferences.get("soft", {})

    # Use compressed persona for efficiency
    compressed_persona = compress_persona_for_prompt(persona)

    user_prompt = f"""Generate weekly content strategy.

Persona: {compressed_persona}

Preferences:
Hard: {json.dumps(hard, separators=(',', ':'))}
Soft: {json.dumps(soft, separators=(',', ':'))}

Return JSON:
{{
  "week": "Week of [date]",
  "goals": ["3-5 strategic goals"],
  "reels": [
    {{
      "day": "Monday|Tuesday|Wednesday|Thursday|Friday",
      "topic": "specific topic",
      "hook_angle": "how to hook viewers",
      "format": "format from persona",
      "intent": "educational|motivational|relatable"
    }}
  ]
}}

Rules: 5 reels, balance topics, match persona, realistic goals."""
    response = call_llm(SYSTEM_PROMPT, user_prompt)
    return json.loads(response)

