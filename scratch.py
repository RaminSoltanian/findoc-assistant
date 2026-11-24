"""M1 step 4: experiments with the chat API."""
import sys, time
from openai import OpenAI
from app.config import settings

client = OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
MODEL = settings.llm_model

def ask(messages, **kwargs):
    return client.chat.completions.create(model=MODEL, messages=messages, **kwargs)

# 1. Basic call: what comes back besides the text
def basic():
    r = ask([{"role": "user", "content": "In one sentence, what is CMHC?"}])
    print(r.choices[0].message.content)
    print("finish_reason:", r.choices[0].finish_reason)
    print("usage:", r.usage)

# 2. System prompt: same question, different instructions
def system_prompt():
    q = "What is a mortgage stress test?"
    for system in ["You are a precise assistant for bank employees. Answer in 2 sentences.",
                   "You explain things to a 10-year-old. Use a simple example.","Always end with a one-line summary"]:
        r = ask([{"role": "system", "content": system}, {"role": "user", "content": q}])
        print(f"\n--- {system}\n{r.choices[0].message.content}")

# 3. Temperature: how much answers vary
def temperature():
    q = "Write a one-sentence tagline for a Canadian bank's mortgage team."
    for t in (0, 1.0):
        print(f"\n--- temperature={t}")
        for _ in range(3):
            print("-", ask([{"role": "user", "content": q}], temperature=t).choices[0].message.content)

# 4. Length limit: what a cut-off answer looks like
def max_tokens():
    r = ask([{"role": "user", "content": "Explain how mortgage amortization works."}], max_tokens=30)
    print(r.choices[0].message.content)
    print("finish_reason:", r.choices[0].finish_reason)   # 'length' means it was cut off

# 5. Streaming: words arrive as they are generated
def streaming():
    start, first = time.perf_counter(), None
    stream = client.chat.completions.create(model=MODEL, stream=True,
        messages=[{"role": "user", "content": "In 5 short bullet points, what does OSFI do?"}])
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:   # Azure sends some empty chunks
            first = first or time.perf_counter() - start
            print(chunk.choices[0].delta.content, end="", flush=True)
    print(f"\n\nfirst words after {first:.2f}s, finished after {time.perf_counter() - start:.2f}s")

# 6. Tokens and cost
PRICE_IN, PRICE_OUT = 0.40, 1.60   # USD per 1M tokens; check Azure's pricing page for your region
def cost():
    r = ask([{"role": "user", "content": "Explain mortgage default insurance in 3 sentences."}])
    u = r.usage
    dollars = u.prompt_tokens / 1e6 * PRICE_IN + u.completion_tokens / 1e6 * PRICE_OUT
    print(f"input {u.prompt_tokens} tokens, output {u.completion_tokens} tokens, cost ${dollars:.6f}")
    print(f"about ${dollars * 1000:.2f} per 1,000 questions like this")

# 7. The model has no memory between calls
def memory():
    first = [{"role": "user", "content": "My name is Alex and I work in mortgage underwriting."}]
    r1 = ask(first)
    print("Without history:", ask([{"role": "user", "content": "What's my name?"}]).choices[0].message.content)
    history = first + [{"role": "assistant", "content": r1.choices[0].message.content},
                       {"role": "user", "content": "What's my name?"}]
    print("With history:   ", ask(history).choices[0].message.content)

if __name__ == "__main__":
    experiments = {f.__name__: f for f in [basic, system_prompt, temperature, max_tokens, streaming, cost, memory]}
    experiments[sys.argv[1] if len(sys.argv) > 1 else "basic"]()