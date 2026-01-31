from openai import OpenAI
import os
import httpx
import hashlib
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

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

# Create httpx client without proxies
http_client = httpx.Client()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=http_client)

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Basic LLM call without caching"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise

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

def call_llm_uncached(system_prompt: str, user_prompt: str) -> str:
    """LLM call without caching (for dynamic content)"""
    return call_llm_cached(system_prompt, user_prompt, use_cache=False)
