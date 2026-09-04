---
name: compare-carriers
description: This skill should be used when the user wants to compare auto-insurance carriers or shop around — e.g. "compare car insurance companies", "who is cheapest for me", "is GEICO or Progressive cheaper", "should I switch from State Farm", or asks which carrier to pick. Ranks per-carrier point estimates and reasons about the coverage ladder across carriers.
version: 0.4.0
---

# Compare Carriers

Help the user shop auto insurance by ranking carriers for their profile using the
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
3. Call **`auto_insurance_quote_profile`** for the point estimate per carrier. Each
   carrier comes back with `monthly`, a `confidence_interval`, a `cells` breakdown
   (good/better/best tiers, each with `monthly` + `semiannual_total` + `annual_total`),
   a `price_ladder` (exact filed monthly at every rung of each lever), a `trust` block
   (`verdict` + NAIC complaint index), `carrier_quote_url`, and (where loaded)
   `coverage_options`. There is no separate serviceability tool: the quote tool
   self-gates on state (an uncovered state returns a clear error naming the live states)
   and its response carries top-level `assumptions`, `tighten_by`, and `failures`.
4. If the response includes **`dispatched_agents`**, more carriers are being quoted live
   by Foresee agents completing the carriers' own quote flows. Mention them, and after a
   minute or two call **`check_agent_quotes`** with the `dispatch_id` to fold the results
   into the comparison — call out anything now cheaper than the previous best. An agent
   may report a carrier `declined`; that's a real answer, relay it.
5. When the user wants proven numbers or is ready to buy, offer a live confirmation:
   **`confirm_quotes_live`** drives the carrier's real site and compares the page premium
   against the engine estimate (collect the `confirmation` block via `check_agent_quotes`).
   This requires consent — see the `quote-insurance` skill for the exact disclosure and
   the verbatim `user_authorization` requirement.

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
  monthly at every filed rung of each lever, so "who's cheapest at a $1000 deductible?"
  is a direct read across carriers — no extra calls, no interpolation.
- **Re-price an explicit combined selection** when the user pins several levers at once:
  pass `coverage_selection` (e.g. `{"bi": "100/300", "coll_deductible": 1000,
  "comp_deductible": 1000}`) and every carrier re-prices at that exact rung. Compare the
  resulting `monthly` values.
- This is how you surface statements like *"Liberty Mutual is cheapest at a low
  deductible, but you want a high one, so GEICO wins for you."*
- **Snapping.** Carriers have different filed ladders. When a requested rung doesn't
  exist for a carrier, the cell reports what it was `snapped_to` — keep comparisons
  honest by noting when two carriers were priced at slightly different rungs.
- Use `coverage_options` (when present) to stay on each carrier's filed ladder rather
  than requesting a level that doesn't exist.

## The one hard rule: never invent a price

Rank, filter, and pivot only over numbers Foresee returned — every `monthly`, `cells`,
and `price_ladder` value IS an exact re-rate. **Do not** compute a premium by
multiplying `steps` factors, interpolate a deductible we didn't price, or synthesize a
carrier's number from another's. If you want a cell we didn't return (another carrier,
another coverage selection), call the tool again — the server prices it. This is what
keeps "every number is validated" true.

## Honesty guardrails

- Do not invent carriers or prices. If a carrier returns nothing, say it couldn't be
  priced and why.
- USAA is military-affiliated only — flag that if it appears and the user isn't
  eligible.
- The instant quote is a filing-based estimate, **not a bindable quote**; when the user
  wants to buy, hand off to the carrier. Prefer a live walk's `handoff_url` when present
  (signed-in users only — it drops them into the already-filled browser session; warn
  them not to share the link, it holds their details); otherwise use the carrier's
  `carrier_quote_url`. See the `quote-insurance` skill for the full hand-off detail.
- If the user's state isn't covered, the tool returns a clear "no coverage yet"
  error — relay it plainly rather than guessing.
