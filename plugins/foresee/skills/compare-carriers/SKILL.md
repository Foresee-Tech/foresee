---
name: compare-carriers
description: This skill should be used when the user wants to compare auto-insurance carriers or shop around — e.g. "compare car insurance companies", "who is cheapest for me", "is GEICO or Progressive cheaper", "should I switch from State Farm", or asks which carrier to pick. Ranks per-carrier point estimates and reasons about the coverage ladder across carriers.
version: 0.2.0
---

# Compare Carriers

Help the user shop auto insurance by ranking carriers for their profile using the
`foresee` MCP tools, and — when it matters — reasoning about *how the coverage is set
up*, because the cheapest carrier changes with the coverage selection.

## When this applies

The user wants a side-by-side of carriers, asks who is cheapest, names two carriers
to compare, is deciding whether to switch, or wants to trade coverage against price.

## How to run it

1. Gather profile basics (see the `quote-my-car` skill for the field list). State/ZIP
   is essential; the rest improves accuracy.
2. If the user named specific carriers, pass them via the `carriers` argument (carrier
   keys like `geico`, `progressive`, `statefarm`, `allstate`, `libertymutual`,
   `usaa`). Otherwise omit it to compare everything available in that state.
3. Call **`auto_insurance_quote_profile`** for the point estimate per carrier. Each
   carrier comes back with `monthly`, a `confidence_interval`, a `cells` sub-coverage
   breakdown, and (where loaded) `coverage_options` — the filed limits/deductibles that
   carrier actually offers.
4. Optionally call **`auto_insurance_engine_coverage`** first to see which carriers are
   available for the state, so you can frame what's covered.

## Presenting results

- **Rank by the point-estimate `monthly`**, cheapest first.
- Show a compact table: carrier | monthly | confidence interval | notable warnings.
- **Ties within the interval are noise.** If two carriers' point estimates fall inside
  each other's `confidence_interval`, say they're effectively tied rather than
  declaring a $3/mo "winner".
- Include per-carrier `warnings` and any `failures` (carriers that couldn't be priced
  for this profile/state) rather than silently dropping them.

## Reasoning about the coverage ladder across carriers

The ranking can flip depending on how coverage is set. A carrier that's cheapest at a
$500 collision deductible may not be cheapest at $1000, and limits behave the same way.
This is a real lever — use it when the user cares about a specific coverage level or
wants to trade coverage for price.

- **Re-price an explicit selection everywhere at once.** Pass `coverage_selection`
  (e.g. `{"bi": "100/300", "coll_deductible": 1000, "comp_deductible": 1000}`) to
  `auto_insurance_quote_profile` and every carrier re-prices at that exact rung. Compare
  the resulting `monthly` values to answer "who's cheapest at a $1000 deductible?"
- **Sweep the axis** by calling it once per rung (e.g. $500 then $1000) and comparing.
  This is how you surface statements like *"Liberty Mutual is cheapest at a low
  deductible, but you want a high one, so GEICO wins for you."*
- **Snapping.** Carriers have different filed ladders. When a requested rung doesn't
  exist for a carrier, the cell reports what it was `snapped_to` — keep comparisons
  honest by noting when two carriers were priced at slightly different rungs.
- Use `coverage_options` (when present) to stay on each carrier's filed ladder rather
  than requesting a level that doesn't exist.

## The one hard rule: never invent a price

Rank, filter, and pivot only over numbers Foresee returned. **Do not** compute a
premium by multiplying `steps` factors, interpolate a deductible we didn't price, or
synthesize a carrier's number from another's. If you want a cell we didn't return
(another carrier, another coverage selection), call the tool again — the server prices
it. This is what keeps "every number is validated" true.

## Honesty guardrails

- Do not invent carriers or prices. If a carrier returns nothing, say it couldn't be
  priced and why.
- USAA is military-affiliated only — flag that if it appears and the user isn't
  eligible.
- If the user's state isn't covered, the tool returns a clear "no coverage yet"
  error — relay it plainly rather than guessing.
