"""Tapix AI - OpenAI-compatible client with live price checks."""

from .client import Tapix, DEFAULT_BASE_URL, list_prices, estimated_cost

__version__ = "0.1.0"
__all__ = ["Tapix", "DEFAULT_BASE_URL", "list_prices", "estimated_cost"]
