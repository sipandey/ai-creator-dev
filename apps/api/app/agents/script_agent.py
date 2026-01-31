import json
from app.llm.client import call_llm

SYSTEM_PROMPT = """
You are an expert short-form video scriptwriting AI.

You write scripts that STRICTLY follow a given creator persona.

CRITICAL RULES:
- Audio script is the single source of truth
- Scenes MUST map directly to parts of the audio script
- Total script duration MUST be <= 60 seconds
- If content is short, do NOT pad unnecessarily

OUTPUT RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- Natural, spoken language
- Maintain consistent creator voice
"""


def generate_script(persona, topic: str, preferences: dict) -> dict:
    # SAFETY: ensure persona is a dict
    if isinstance(persona, str):
        try:
            persona = json.loads(persona)
        except json.JSONDecodeError:
            raise ValueError("Persona must be valid JSON string or dict")

    if not isinstance(persona, dict):
        raise TypeError(f"Persona must be dict, got {type(persona)}")

    hard = preferences.get("hard", {})
    soft = preferences.get("soft", {})

    user_prompt = f"""
CREATOR PERSONA (use strictly as instructions):

Language & Speech:
- Language: {persona.get("language")}
- Vocabulary level: {persona.get("communication_patterns", {}).get("vocabulary_level")}
- Sentence complexity: {persona.get("communication_patterns", {}).get("sentence_complexity")}
- Filler words you MAY naturally include: {persona.get("communication_patterns", {}).get("filler_words", [])}
- Signature phrases you MAY use sparingly: {persona.get("communication_patterns", {}).get("signature_phrases", [])}

Tone & Emotion:
- Tone: {persona.get("tone")}
- Energy level: {persona.get("energy_level")}
- Empathy level: {persona.get("emotional_markers", {}).get("empathy_level")}
- Humor style: {persona.get("emotional_markers", {}).get("humor_style")}
- Authenticity markers to reflect subtly: {persona.get("emotional_markers", {}).get("authenticity_markers", [])}

Structure & Timing:
- Hook style: {persona.get("hook_style")}
- Content pacing: {persona.get("pacing")}
- Speech rhythm: {persona.get("timing_patterns", {}).get("speech_rhythm")}
- Pause frequency: {persona.get("timing_patterns", {}).get("pause_frequency")}
- Hook should occur within first {persona.get("timing_patterns", {}).get("hook_timing")} seconds
- TOTAL SCRIPT DURATION MUST NOT EXCEED 60 SECONDS

Formats & Visual Thinking:
- Preferred formats: {persona.get("formats")}
- Visual metaphors you can reference in scenes: {persona.get("visual_preferences", {}).get("visual_metaphors", [])}
- Background style: {persona.get("visual_preferences", {}).get("background_style")}

CTA:
- CTA style: {persona.get("cta_style")}
- Confidence score (adjust assertiveness): {persona.get("confidence_score")}

Content boundaries:
- Allowed topics: {persona.get("topics")}

CREATOR PREFERENCES:
Hard constraints (MUST NEVER be violated):
{json.dumps(hard, indent=2)}

Soft preferences (respect if possible):
{json.dumps(soft, indent=2)}

Reel topic:
\"{topic}\"

PRIORITY ORDER:
1. Hard constraints
2. Soft preferences
3. Persona instructions

TASK:
1. Write a SINGLE continuous audio script (spoken narration).
2. Ensure the script fits naturally within 60 seconds.
3. Break the audio script into scenes.
4. Each scene MUST reference an exact excerpt from the audio script.
5. Assign realistic timestamps to each scene.
6. Do NOT repeat or paraphrase audio across scenes.

OUTPUT STRICTLY IN THIS JSON SCHEMA:

{{
  "hook": "string",
  "audio_script": "string",
  "scenes": [
    {{
      "scene_id": number,
      "start_sec": number,
      "end_sec": number,
      "audio_excerpt": "string",
      "visual_direction": "string"
    }}
  ],
  "caption": "string",
  "cta": "string",
  "estimated_duration_sec": number
}}
"""
    response = call_llm(SYSTEM_PROMPT, user_prompt)
    return json.loads(response)

