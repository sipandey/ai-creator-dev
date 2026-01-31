from openai import OpenAI
import os
import httpx
from .optimizer import call_llm_cached

# Create httpx client without proxies
http_client = httpx.Client()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=http_client)

def call_llm(system_prompt: str, user_prompt: str, use_cache: bool = True) -> str:
    """Enhanced LLM call with caching support"""
    return call_llm_cached(system_prompt, user_prompt, use_cache)

def call_llm_uncached(system_prompt: str, user_prompt: str) -> str:
    """LLM call without caching (for dynamic content)"""
    return call_llm_cached(system_prompt, user_prompt, use_cache=False)
