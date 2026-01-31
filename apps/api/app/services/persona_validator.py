REQUIRED_KEYS = {
    "language",
    "tone",
    "energy_level",
    "hook_style",
    "cta_style",
    "formats",
    "topics",
    "pacing",
}

def validate_persona(persona: dict) -> dict:
    missing = REQUIRED_KEYS - persona.keys()
    if missing:
        raise ValueError(f"Missing persona fields: {missing}")

    return persona
