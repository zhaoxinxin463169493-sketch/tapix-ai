"""Check what a call costs before you make it."""

from tapix_ai import estimated_cost, list_prices

cheap = sorted(list_prices(), key=lambda m: float(m.get("sell_out") or 9e9))[:5]
for m in cheap:
    print(m["id"], "->", m.get("sell_in"), "/", m.get("sell_out"), "per 1M")

print()
print("1M in + 1M out on claude-sonnet-5 = $", round(estimated_cost("claude-sonnet-5", 1_000_000, 1_000_000), 4))
