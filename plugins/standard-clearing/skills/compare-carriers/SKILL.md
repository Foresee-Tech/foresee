---
name: compare-carriers
description: This skill should be used when the user wants to compare auto-insurance carriers or shop around — e.g. "compare car insurance companies", "who is cheapest for me", "is GEICO or Progressive cheaper", "should I switch from State Farm", or asks which carrier to pick. Runs deterministic per-carrier quotes and ranks them with caveats.
version: 0.1.0
---

# Compare Carriers

Help the user shop auto insurance by ranking carriers for their profile using the
`standard-clearing` MCP tools. Results are deterministic estimates computed from
SERFF rate filings.

## When this applies

The user wants a side-by-side of carriers, asks who is cheapest, names two carriers
to compare, or is deciding whether to switch.

## How to run it

1. Gather profile basics (see the `quote-my-car` skill for the field list). State/ZIP
   is essential; the rest improves accuracy.
2. If the user named specific carriers, pass them via the `carriers` argument (carrier
   keys like `geico`, `progressive`, `statefarm`, `allstate`, `libertymutual`,
   `usaa`). Otherwise omit it to compare everything available in that state.
3. Call **`auto_insurance_quote_profile`** for exact tiered prices (minimum / standard
   / premium) per carrier, or **`auto_insurance_quote_range`** for a Monte-Carlo
   spread when key fields are unknown.
4. Optionally call **`auto_insurance_engine_coverage`** first to see which carriers
   have engines for the state and their market rank, so you can frame what's covered.

## Presenting results

- Rank by **standard-tier monthly** (or p50 monthly for ranges), cheapest first.
- Show a compact table: carrier | monthly | notable warnings.
- Call out ties/near-ties honestly — a $3/mo gap is noise given the uncertainty.
- Include per-carrier `warnings` and any `failures` (carriers that couldn't be
  priced for this profile/state) rather than silently dropping them.

## Honesty guardrails

- Do not invent carriers or prices. If the engine returns nothing for a carrier,
  say it couldn't be priced and why.
- USAA is military-affiliated only — flag that if it appears and the user isn't
  eligible.
- If the user's state isn't covered, the tool returns a clear "no coverage yet"
  error — relay it plainly rather than guessing.
