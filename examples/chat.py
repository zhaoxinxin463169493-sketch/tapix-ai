"""Minimal chat completion."""

import os

from tapix_ai import Tapix

client = Tapix(api_key=os.environ["TAPIX_API_KEY"])

resp = client.chat.completions.create(
    model="claude-sonnet-5",
    messages=[{"role": "user", "content": "Reply with OK"}],
    max_tokens=16,
)
print(resp.choices[0].message.content)
print("billed:", resp.usage.total_tokens, "tokens")
