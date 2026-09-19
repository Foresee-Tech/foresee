---
# @copy skill.compare-carriers audience=agent
name: compare-carriers
description: This skill should be used when the user wants to compare personal lines insurance carriers, shop around, or find the right insurance — e.g. "compare car insurance companies", "who is cheapest for me", "is GEICO or Progressive cheaper", "should I switch from State Farm".
version: 0.6.0
---

# Compare Carriers

Help the user shop for insurance by ranking carriers for their profile using the
`foresee` MCP tools, and — when it matters — reasoning about *how the coverage is set
up*, because the cheapest carrier changes with the coverage selection.

## When this applies

The user wants a side-by-side of carriers, asks who is cheapest, names two carriers
to compare, is deciding whether to switch, or wants to trade coverage against price.

## How to run it

1. Gather profile basics (see the `quote-insurance` skill for the field list). State/ZIP
   is essential; the rest improves accuracy.
2. If the user named specific carriers, pass them via the `carriers` argument (carrier
   keys like `geico`, `progressive`, `statefarm`, `allstate`, `mercury`, `kemper`,
   `csaa`, `farmers`, `usaa`). Otherwise omit it to compare everything available in
   that state.
3. Call **`quote_insurance`** for the instant per-carrier estimate.
   Pass **`coverage_selection`** as actual numbers (`bi`, `pd`,
   `coll_deductible`, `comp_deductible`). If the user didn't specify limits, pass
   the common starting point (`"100/300"`, `100`, `500`, `500`) on the first call
   and declare it. Each carrier comes back with `monthly`, a `confidence_interval`,
   sub-coverage `L` lines at that selection, `D` / `price_ladder` deltas for every
   rung of each lever, a `trust` verdict, and `carrier_quote_url`. An
   uncovered state returns a clear error naming the live states. The response
   carries top-level `assumptions`, `tighten_by`, and `failures`.
4. When the user wants proven numbers or is ready to buy, offer live quotes:
   **`live_carrier_quotes`** drives the carriers' real sites and reads back the
   page-printed premium; where an engine baseline exists the results carry a
   `confirmation` block comparing it against the engine estimate. The tool is
   idempotent — re-call it with the same arguments to collect progress and results,
   and an already-walked profile returns its existing results without re-submitting.
   Commissioning requires consent — see the `quote-insurance` skill for the exact
   disclosure and the verbatim `user_authorization` requirement. Fold completed
   quotes into the comparison and call out anything now cheaper than the previous
   best; a carrier `declined` is a real answer, relay it.

## Presenting results

- **Rank by the point-estimate `monthly`**, cheapest first.
- Show a compact table: **Carrier · Monthly · 6-month total · Trust** (plus the
  confidence interval when it matters). Call out the annual dollar spread between the
  cheapest and priciest options — that spread is the reason to compare.
- **Ties within the interval are noise.** If two carriers' point estimates fall inside
  each other's `confidence_interval`, say they're effectively tied rather than
  declaring a $3/mo "winner".
- Read `trust.verdict` (solid / caution / unverified) against the top-level
  `trust_methodology`: complaint indexes are relative, so compare carriers to each
  other, not to 1.0.
- Include any `failures` (carriers that couldn't be priced for this profile/state)
  rather than silently dropping them.

## Reasoning about the coverage ladder across carriers

The ranking can flip depending on how coverage is set. A carrier that's cheapest at a
$500 collision deductible may not be cheapest at $1000, and limits behave the same way.
This is a real lever — use it when the user cares about a specific coverage level or
wants to trade coverage for price.

- **Read the `price_ladder` first.** Each carrier's ladder already gives the exact
  monthly at every rung of each lever, so "who's cheapest at a $1000 deductible?"
  is a direct read across carriers — no extra calls, no interpolation.
- **Re-price an explicit combined selection** when the user pins several levers at once:
  pass `coverage_selection` (e.g. `{"bi": "100/300", "coll_deductible": 1000,
  "comp_deductible": 1000}`) and every carrier re-prices at that exact rung. Compare the
  resulting `monthly` values.
- This is how you surface statements like *"Liberty Mutual is cheapest at a low
  deductible, but you want a high one, so GEICO wins for you."*
- **Missing rungs.** Carriers have different ladders. If a requested rung
  isn't in that carrier's `D` / `price_ladder`, the filing has no such option —
  say so rather than interpolating or implying they were priced at the same rung.
- Stay on each carrier's ladder (`D` / `price_ladder` rungs) rather than
  requesting a level that doesn't exist.

## The one hard rule: never invent a price

Rank, filter, and pivot only over numbers Foresee returned — every `monthly`, `L`
line, and `price_ladder` / `D` value IS an exact re-rate. **Do not** compute a
premium by multiplying `F` factors, interpolate a deductible we didn't price, or
synthesize a carrier's number from another's. If you want a selection we didn't
return (another carrier, another coverage combination), call the tool again — the
server prices it. This is what keeps "every number is validated" true.

## Honesty guardrails

- Do not invent carriers or prices. If a carrier returns nothing, say it couldn't be
  priced and why.
- USAA is military-affiliated only — flag that if it appears and the user isn't
  eligible.
- The instant quote is a filing-based estimate, **not a bindable quote**; when the user
  wants to buy, hand off to the carrier with its `carrier_quote_url`. See the
  `quote-insurance` skill for the full hand-off detail.
- If the user's state isn't covered, the tool returns a clear "no coverage yet"
  error — relay it plainly rather than guessing.
