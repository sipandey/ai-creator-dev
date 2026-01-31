from openai import OpenAI
import os
import httpx

# Create httpx client without proxies
http_client = httpx.Client()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=http_client)

def call_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
