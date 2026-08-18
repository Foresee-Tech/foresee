---
name: explain-coverage
description: This skill should be used when the user asks what auto-insurance coverage means or which limits/deductibles to choose — e.g. "what does 100/300 mean", "explain liability vs full coverage", "what deductible should I pick", "what coverage do I need in <state>", or wants to understand how changing a limit or deductible changes the price.
version: 0.2.0
---

# Explain Coverage

Explain auto-insurance coverage terms, limits, and deductibles in plain language,
grounded in the real per-coverage data the `foresee` MCP tools return — and, when it
helps, show the user what a coverage change actually costs.

## When this applies

The user is confused about coverage terminology, limits (e.g. `100/300/100`),
deductibles, or which coverage level to carry, or asks how changing coverage affects
their price.

## How to run it

1. If the question is state- or carrier-specific, call
   **`auto_insurance_engine_coverage`** for the user's state to ground the answer in
   the carriers and filed coverage actually available.
2. Explain the concepts the user asked about:
   - **Liability (BI/PD)** — e.g. `100/300/100` = $100k per person / $300k per
     accident bodily injury, $100k property damage.
   - **Collision** and **Comprehensive** — with **deductibles** (what you pay before
     coverage kicks in; higher deductible → lower premium).
   - **UM/UIM, PIP** and other lines as they come up.
3. When a quote is in play, ground it in that user's real numbers: the `cells`
   sub-coverage breakdown from `auto_insurance_quote_profile` shows each coverage line's
   own monthly cost and the selected limit/deductible — so "what am I paying for
   collision?" has a concrete answer, not just a definition.

## The coverage ladder — where the money moves

The single most useful thing to teach: **coverage is a ladder, and moving a rung
changes both what you're covered for and what you pay.** Raise a deductible and the
premium drops (you keep more risk); raise a limit and it rises (you offload more).

- Show the delta, don't just assert it. Call `auto_insurance_quote_profile` with a
  `coverage_selection` (e.g. `{"coll_deductible": 1000}` vs `{"coll_deductible": 500}`)
  and compare the returned `monthly` so the user sees the actual dollar trade-off for
  *their* profile and carrier.
- Use `coverage_options` (when present) to show which rungs a carrier actually files —
  don't offer a limit or deductible that isn't on their ladder.
- Different carriers file different ladders, and the best carrier can change with the
  rung — if the user is optimizing a specific coverage level, hand off to
  `compare-carriers`.

## The one hard rule: never invent a price

Every number you show must be one Foresee returned. Do not estimate the cost of a
coverage change by multiplying factors or interpolating — call the tool with the new
`coverage_selection` and report what it prices. Definitions can be general; **dollars
must be computed.**

## Guardrails

- State minimums vary; if you're unsure of a state's legal minimum, say so rather than
  stating a specific number you can't verify.
- Keep it practical and short; define jargon the first time it appears.
