"""Client for the Tapix AI OpenAI-compatible endpoint.

The request and response shapes are identical to OpenAI's, so this is the
official openai SDK with a different base_url plus a price helper.
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any, Dict, List, Optional

from openai import OpenAI

DEFAULT_BASE_URL = "https://tapixai.com/v1"
MODELS_URL = "https://tapixai.com/api/models"


class Tapix(OpenAI):
    """Drop-in replacement for OpenAI() pointed at Tapix AI.

    Args:
        api_key: Tapix API key. Falls back to the TAPIX_API_KEY env var.
        base_url: Override only if you are using a branded or self-hosted entry.
        **kwargs: Passed straight to the openai client.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        **kwargs: Any,
    ) -> None:
        key = api_key or os.environ.get("TAPIX_API_KEY")
        if not key:
            raise ValueError(
                "No API key. Pass api_key=... or set the TAPIX_API_KEY environment variable."
            )
        super().__init__(api_key=key, base_url=base_url, **kwargs)


def list_prices(timeout: float = 15.0) -> List[Dict[str, Any]]:
    """Return the live model catalog with sell and list prices (no key needed).

    Each item contains at least: id, sell_in, sell_out, list_in, list_out, ctx, type.
    Prices are USD per 1,000,000 tokens.
    """
    req = urllib.request.Request(MODELS_URL, headers={"User-Agent": "tapix-ai-python"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if isinstance(data, dict):
        for k in ("models", "data", "items"):
            if isinstance(data.get(k), list):
                return data[k]
        return []
    return data if isinstance(data, list) else []


def estimated_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate the USD cost of a single call from the live price table.

    Raises KeyError if the model is not in the catalog.
    """
    for m in list_prices():
        if m.get("id") == model:
            return (input_tokens / 1_000_000.0) * float(m.get("sell_in") or 0) + (
                output_tokens / 1_000_000.0
            ) * float(m.get("sell_out") or 0)
    raise KeyError("unknown model: %s" % model)
