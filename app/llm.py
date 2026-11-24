from openai import OpenAI
from app.config import settings
from app.prompts import SYSTEM_PROMPT, FEW_SHOT
from app.schemas import Answer

client = OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key, timeout=30)

def ask_llm(question: str) -> tuple[Answer, dict]:
    resp = client.chat.completions.parse(
        model=settings.llm_model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  *FEW_SHOT,
                  {"role": "user", "content": question}],
        response_format=Answer,      # the model must return this exact shape
        temperature=0.2,
    )
    msg = resp.choices[0].message
    if msg.parsed is None:
        raise ValueError(msg.refusal or "Model did not return a valid answer")
    usage = {"input_tokens": resp.usage.prompt_tokens,
             "output_tokens": resp.usage.completion_tokens}
    return msg.parsed, usage