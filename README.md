# tapix-ai

Python client for [Tapix AI](https://tapixai.com) — an OpenAI-compatible endpoint that serves Claude, GPT, Gemini, Grok, DeepSeek, Kimi and Qwen models at prices below the vendors' own list prices.

This package is deliberately thin: it is the official [`openai`](https://pypi.org/project/openai/) SDK pointed at a different `base_url`, plus a helper that reads the live price table so your code can check what a model actually costs before you call it.

## Why switch

The request and response shapes are identical to OpenAI's. That means:

- no rewrite of your prompts, tools, or streaming code
- no new SDK to learn
- switching back is one line

What differs is the bill and the model list.

## Install

```bash
pip install git+https://github.com/<your-org>/tapix-ai.git
```

Requires Python 3.9+ and `openai>=1.0`.

## Use it

```python
from tapix_ai import Tapix

client = Tapix(api_key="sk-...")          # or set TAPIX_API_KEY

resp = client.chat.completions.create(
    model="claude-sonnet-5",
    messages=[{"role": "user", "content": "Reply with OK"}],
    max_tokens=16,
)
print(resp.choices[0].message.content)
```

That is the whole migration. If you already have `OpenAI()` calls in your codebase, change the constructor and leave everything else alone:

```python
# before
# from openai import OpenAI
# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

from tapix_ai import Tapix
client = Tapix(api_key=os.environ["TAPIX_API_KEY"])
```

## Check the price before you spend

`list_prices()` returns the live catalog with per-model rates, the vendor's list price, and the discount. No API key required.

```python
from tapix_ai import list_prices

for m in list_prices():
    if m["id"] == "claude-sonnet-5":
        print(m["sell_in"], m["sell_out"], "vs list", m["list_in"], m["list_out"])
```

Cost of a call is `input_tokens / 1e6 * sell_in + output_tokens / 1e6 * sell_out`, billed in USD against prepaid credit.

## Streaming, tools, reasoning

All three work exactly as they do on OpenAI. Reasoning-capable models accept the standard `reasoning_effort` field (`none`, `low`, `medium`, `high`, and `xhigh`/`max` where the underlying model supports it); the reasoning text comes back in `message.reasoning_content`.

```python
stream = client.chat.completions.create(
    model="claude-sonnet-5",
    messages=[{"role": "user", "content": "think briefly, then answer"}],
    reasoning_effort="low",
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta
    if getattr(delta, "reasoning_content", None):
        print(delta.reasoning_content, end="")
    if delta.content:
        print(delta.content, end="")
```

## Billing model

Prepaid credit, billed per token, no subscription and no monthly minimum. `GET /v1/models` and the price table are free and need no key. Errors use OpenAI's shape (`{"error": {"message": ...}}`) so existing retry logic keeps working.

## Links

- Docs: https://tapixai.com/docs
- Live prices: https://tapixai.com/pricing
- Machine-readable prices: https://tapixai.com/pricing.md
- Verify any provider's responses: https://tapixai.com/verify

## License

MIT
