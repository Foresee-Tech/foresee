---
name: quote-my-car
description: This skill should be used when the user wants an auto/car insurance quote or price estimate — e.g. asks "how much would car insurance cost me", "quote my car", "estimate my auto insurance", "what would I pay for insurance on my <car>", or gives driver/vehicle details and asks for a price. Gathers the minimum profile conversationally and returns per-carrier monthly price ranges.
version: 0.1.0
---

# Quote My Car

Produce an auto-insurance price estimate for the user by calling the
`standard-clearing` MCP tools.

## When this applies

The user wants to know what car insurance would cost them, or gives details
(age, ZIP, car, driving record) and asks for a price/estimate/comparison.

## What to collect

Collect what you can **conversationally — do not demand everything**:

- **State + ZIP code** (most important)
- **Age** or date of birth
- **Vehicle** year / make / model
- **Marital status**, **gender**
- **Driving record**: accidents (last 3 yrs), violations, DUI
- **Credit range** (Excellent / Good / Fair / Poor), **homeowner?**, **currently insured?**

Missing fields are handled automatically; the range tool reports which ones it had to
assume so you can ask follow-ups to narrow the estimate.

## How to run it

1. Confirm at least **state/ZIP** and ideally age + vehicle. If the user is vague
   ("just ballpark for a 30-year-old in Salt Lake City"), proceed with what you have.
2. Call **`auto_insurance_recommend_options`** with a `profile` dict (snake_case or
   camelCase both accepted) for a ranked recommendation, or
   **`auto_insurance_quote_range`** for the full p25/p50/p75 spread per carrier.
   Use `samples: 100` (default) for a stable range; lower (e.g. 20) for a quick pass.
3. Present the **p50 (median) monthly** as the headline number with the **p25–p75
   range**, top 2–3 carriers, and any `warnings`/`caveats` the tools return.
4. If `high_impact_unknown_fields` is non-empty, tell the user which facts would
   tighten the estimate and offer to re-run once they provide them.

## Presenting results

- Lead with a range, never a single false-precision number: "roughly **$120–$180/mo**,
  median ~$145, cheapest looks like GEICO."
- Surface any caveats the tools return verbatim when they affect trust.

## Unsupported states

The tools cover a limited set of states today (beta: Utah). If the user's state
isn't covered, the tool returns a clear error (e.g. *"Standard Clearing doesn't have
rate coverage for WY yet"*). Relay that message plainly — do not guess or fabricate a
number for a state we don't cover.
