---
name: explain-coverage
description: This skill should be used when the user asks what auto-insurance coverage means or which limits/tiers to choose — e.g. "what does 100/300 mean", "explain liability vs full coverage", "what deductible should I pick", "what coverage do I need in <state>", or wants the difference between minimum/standard/premium coverage.
version: 0.1.0
---

# Explain Coverage

Explain auto-insurance coverage terms, limits, and tiers in plain language, grounded
in the carrier/tier data the `standard-clearing` MCP tools return.

## When this applies

The user is confused about coverage terminology, limits (e.g. `100/300/100`),
deductibles, or the difference between minimum / standard / premium tiers, or asks
what coverage they should carry.

## How to run it

1. If the question is state- or carrier-specific, call
   **`auto_insurance_engine_coverage`** for the user's state to ground the answer in
   the actual tiers and carriers available.
2. Explain the concepts the user asked about:
   - **Liability (BI/PD)** — e.g. `100/300/100` = $100k per person / $300k per
     accident bodily injury, $100k property damage.
   - **Collision** and **Comprehensive** — with **deductibles** (what you pay before
     coverage kicks in; higher deductible → lower premium).
   - **Tiers**: `minimum` (state legal floor), `standard` (typical balanced coverage),
     `premium` (higher limits / lower deductibles).
3. When helpful, offer to price the tiers for their profile via `quote-my-car` /
   `compare-carriers` so they see the cost difference, not just the definitions.

## Guardrails

- State minimums vary; if you're unsure of a state's legal minimum, say so rather
  than stating a specific number you can't verify.
- Keep it practical and short; define jargon the first time it appears.
