import hashlib
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from app.llm.client import call_llm

logger = logging.getLogger(__name__)

class LLMCache:
    """Simple in-memory cache for LLM responses with TTL"""

    def __init__(self, ttl_seconds: int = 3600):  # 1 hour default
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds

    def _get_cache_key(self, system_prompt: str, user_prompt: str) -> str:
        """Generate cache key from prompts"""
        combined = f"{system_prompt}:{user_prompt}"
        return hashlib.md5(combined.encode()).hexdigest()

    def get(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Get cached response if valid"""
        cache_key = self._get_cache_key(system_prompt, user_prompt)
        cached_item = self.cache.get(cache_key)

        if cached_item:
            created_at = cached_item['created_at']
            if datetime.now() - created_at < timedelta(seconds=self.ttl_seconds):
                logger.info(f"LLM cache hit for key: {cache_key[:8]}")
                return cached_item['response']

            # Remove expired cache entry
            del self.cache[cache_key]

        return None

    def set(self, system_prompt: str, user_prompt: str, response: str):
        """Cache response"""
        cache_key = self._get_cache_key(system_prompt, user_prompt)
        self.cache[cache_key] = {
            'response': response,
            'created_at': datetime.now()
        }
        logger.info(f"Cached LLM response for key: {cache_key[:8]}")

# Global cache instance
llm_cache = LLMCache()

def call_llm_cached(system_prompt: str, user_prompt: str, use_cache: bool = True) -> str:
    """Enhanced LLM call with optional caching"""
    if use_cache:
        cached_response = llm_cache.get(system_prompt, user_prompt)
        if cached_response:
            return cached_response

    response = call_llm(system_prompt, user_prompt)

    if use_cache:
        llm_cache.set(system_prompt, user_prompt, response)

    return response

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