from app.agents.style_analysis_agent import analyze_style
from app.services.persona_validator import validate_persona

def build_persona(creator_type: str, payload: dict):
    if creator_type == "new":
        return (
            {
                "language": "english",
                "tone": ["informative"],
                "energy_level": "medium",
                "hook_style": "fact-first",
                "cta_style": "follow",
                "formats": ["text-overlay"],
                "topics": ["general"],
                "pacing": "moderate",
            },
            0.4,
            "template",
        )

    persona = analyze_style(payload.get("sample_texts", []))
    persona = validate_persona(persona)

    return persona, 0.8, "llm-analysis"
