"""Streaming with reasoning tokens."""

import os

from tapix_ai import Tapix

client = Tapix(api_key=os.environ["TAPIX_API_KEY"])

stream = client.chat.completions.create(
    model="claude-sonnet-5",
    messages=[{"role": "user", "content": "Think briefly, then say OK"}],
    reasoning_effort="low",
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta
    reasoning = getattr(delta, "reasoning_content", None)
    if reasoning:
        print("[thinking]", reasoning, end="")
    if delta.content:
        print(delta.content, end="")
print()
