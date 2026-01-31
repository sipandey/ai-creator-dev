SYSTEM_PROMPT = """
You are a content strategist AI.

Your task:
Analyze a creator’s writing style and extract a structured persona.

Rules:
- Output ONLY valid JSON
- Follow the exact schema provided
- Do NOT add explanations
"""

USER_PROMPT_TEMPLATE = """
Given the following creator content samples:

{samples}

Extract the creator persona in this exact JSON schema:

{{
  "language": "english | hinglish | hindi",
  "tone": ["empathetic", "honest", "informative", "motivational"],
  "energy_level": "low | medium | high",
  "hook_style": "problem-first | story-first | fact-first",
  "cta_style": "soft | direct | follow",
  "formats": ["talking-head", "text-overlay", "b-roll"],
  "topics": ["string"],
  "pacing": "slow | moderate | fast"
}}
"""
