import hashlib
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def compress_persona_for_prompt(persona: Dict[str, Any]) -> str:
    """Compress persona data for more efficient prompts"""
    compressed = {
        "lang": persona.get("language", "english"),
        "tone": persona.get("tone", []),
        "energy": persona.get("energy_level", "medium"),
        "hook": persona.get("hook_style", "story-first"),
        "cta": persona.get("cta_style", "soft"),
        "formats": persona.get("formats", []),
        "topics": persona.get("topics", [])[:3],  # Limit topics
        "pacing": persona.get("pacing", "moderate"),
        "vocab": persona.get("communication_patterns", {}).get("vocabulary_level", "casual"),
        "empathy": persona.get("emotional_markers", {}).get("empathy_level", "medium"),
        "confidence": persona.get("confidence_score", 0.5)
    }
    return json.dumps(compressed, separators=(',', ':'))  # Compact JSON

def create_compact_schema_prompt(schema: Dict[str, Any]) -> str:
    """Create a more compact schema representation for prompts"""
    def compact_dict(d: Dict[str, Any]) -> str:
        items = []
        for k, v in d.items():
            if isinstance(v, dict):
                items.append(f'"{k}":{compact_dict(v)}')
            elif isinstance(v, list):
                if v and isinstance(v[0], str):
                    items.append(f'"{k}":["{v[0]}", ...]')
                else:
                    items.append(f'"{k}":[]')
            else:
                items.append(f'"{k}":"{v}"')
        return f"{{{','.join(items)}}}"

    return compact_dict(schema)