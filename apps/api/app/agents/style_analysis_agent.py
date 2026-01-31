import json
from app.llm.client import call_llm
from app.prompts.style_analysis import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

def analyze_style(sample_texts: list[str]) -> dict:
    samples = "\n".join(sample_texts)

    prompt = USER_PROMPT_TEMPLATE.format(samples=samples)

    response = call_llm(SYSTEM_PROMPT, prompt)

    try:
        persona = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")

    return persona
