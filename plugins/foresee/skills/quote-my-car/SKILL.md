---
name: quote-my-car
description: This skill should be used when the user wants an auto/car insurance quote or price estimate — e.g. asks "how much would car insurance cost me", "quote my car", "estimate my auto insurance", "what would I pay for insurance on my <car>", or gives driver/vehicle details and asks for a price. Gathers the minimum profile conversationally and returns a per-carrier monthly point estimate with a confidence interval.
version: 0.2.0
---

# Quote My Car

Produce an auto-insurance price estimate for the user by calling the `foresee` MCP
tools. The goal is a **confident point estimate per carrier** — a single monthly
number the user can act on — plus an honest confidence interval. Foresee prices from
the carriers' own filed rate manuals, so the number is a real computed premium, not a
marketing lead.

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

You do **not** need everything to return a number. Anything you don't provide, Foresee
assumes a sensible default for and tells you exactly what it assumed (see the two kinds
of uncertainty below) — so you can still give a point estimate and then offer to sharpen it.

## How to run it

1. Confirm at least **state/ZIP** and ideally age + vehicle. If the user is vague
   ("just ballpark for a 30-year-old in Austin"), proceed with what you have.
2. Call **`auto_insurance_quote_profile`** with a `profile` dict (snake_case or
   camelCase both accepted). This is the primary tool: one exact rate-engine run per
   carrier — fast, and deterministic given the profile.
3. Read off, per carrier:
   - **`monthly`** — the headline point estimate.
   - **`confidence_interval`** — `{low, high, confidence, basis}`. This is what we
     genuinely *can't* resolve right now (see below). State it as confidence.
   - **`cells`** — the sub-coverage breakdown (BI, PD, collision, comprehensive,
     UM/UIM…), each with its own monthly figure and the selected limit/deductible.
     Use it when the user asks "what am I paying for" or wants to change coverage.
4. Read the response's top-level **`assumptions`** and **`tighten_by`** and act on them
   (below).

## The two kinds of uncertainty — keep them separate

This is the core of how Foresee talks about confidence. Never blur them.

- **Confidence interval = irreducible.** "We think it's between $141 and $158 and we
  can't do better than that right now." This is proprietary carrier math we can't see
  (e.g. an insurer's internal tier/placement) plus our measured engine-vs-reality
  error. Report it as confidence, **not** as a hedge, and **do not widen it** because
  the profile was incomplete.
- **`assumptions` / `tighten_by` = reducible.** "If you also tell us your credit tier,
  we'll sharpen the number." These are fields the user didn't give, so Foresee assumed
  them. Still give the point estimate; then, if `tighten_by` is non-empty, tell the
  user which one or two facts would tighten it most and offer to re-run.

So: incomplete profile → **point estimate + name the assumptions**, never a refusal and
never a widened CI.

## Presenting results

- **Lead with the point estimate**, then the interval as confidence:
  "About **$148/mo** with GEICO — we're confident it's in the **$141–$158** range."
- If the interval is labeled `unmeasured` or `provisional` (thin/no validation data
  for that carrier/state yet), say so plainly rather than implying tightness we haven't
  earned.
- If `tighten_by` lists high-impact fields, add one line: "Tell me your credit range
  and I can narrow that."
- Offer the sub-coverage breakdown or a coverage change (see `explain-coverage` /
  `compare-carriers`) if the user wants detail.

## The one hard rule: never invent a price

Only ever quote a number Foresee returned. **Do not** multiply the factors in `steps`
yourself, do not interpolate a limit/deductible we didn't price, and do not average
carriers into a made-up figure. If the user wants a coverage level or carrier we didn't
return, call the tool again for it. Every dollar you show must be one the engine
computed — that is what lets us stand behind it.

## Unsupported states

Foresee covers a limited set of states today. If the user's state isn't covered, the
tool returns a clear error (e.g. *"Foresee isn't live for WY yet"*). Relay that message
plainly — do not guess or fabricate a number for a state we don't cover.
