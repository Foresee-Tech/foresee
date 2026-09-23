---
# @copy skill.quote-insurance audience=agent
name: quote-insurance
description: This skill should be used when the user wants a personal lines (especially home and auto) insurance quote comparison or price estimate — e.g. asks "how much would car insurance cost me", "what auto insurance should I get", "estimate my auto insurance", "what would I pay for insurance on my <car>", or gives driver/vehicle details and asks for a price. Gathers the minimum profile conversationally and returns carrier quotes, with optional live confirmation from the carriers' own sites.
version: 0.7.2
---

# Quote Insurance

Return estimated insurance quotes for the user by calling the `foresee` MCP tools.
Foresee returns quote estimates - per-carrier monthly point estimates, full sub-coverage detail, and a per-lever price ladder - so that the user can make decisions about limits, deductibles, and so on across multiple carriers.
Foresee does not monetise by selling ads or leads.

## Scope — auto only for now

Foresee quotes the lines and states it currently serves — **California auto is live
today**. This is the one disclaimer to give: if the user asks about a line that isn't
live yet (home, condo, renters, etc.), say so plainly in a single sentence, then offer
an auto quote if it's relevant — once, not repeated over and over.
Everything below describes the live flow.

## How Foresee works — two parts

Foresee is a two-part system, and the trust comes from how they fit together:

1. **Deterministic rate engines (instant).** `quote_insurance` runs each
   carrier's own rating rules against the profile and returns an exact computed
   premium per carrier — with a full sub-coverage breakdown and a price ladder — in one
   call. This is the headline answer and the default path.
2. **Live carrier agents.** Foresee agents drive the carriers' own quoting websites
   with the quoted details and read back the page-printed premium — one tool,
   `live_carrier_quotes`. Where an engine baseline exists, the results carry a
   `confirmation` block comparing the two, so the user sees the instant quote *and*
   proof it holds up on the carrier's site.

Lead with part 1; offer part 2 when the user is ready to act on real numbers.

## When this applies

The user wants to know what insurance would cost them, or gives details
(age, ZIP, car, driving record) and asks for a price/estimate/comparison.

## What to collect

Collect what you can **conversationally — do not demand everything**:

- **State + ZIP code** (most important)
- **Age** or date of birth
- **Vehicle** year / make / model
- **Marital status**, **gender**
- **Driving record**: accidents (last 3 yrs), violations, DUI
- **Credit range** (Excellent / Good / Fair / Poor), **homeowner?**, **currently insured?**
- **Military affiliation** (active / veteran / family / none) — USAA quotes only for
  military-affiliated households, so ask this before quoting; pass it as
  `military_affiliation`.

You do **not** need everything to return a number. Anything you don't provide, Foresee
assumes a sensible default for and tells you exactly what it assumed (see the two kinds
of uncertainty below) — so you can still give a point estimate and then offer to sharpen it.

## How to run it

1. Confirm at least **state/ZIP** and ideally age + vehicle. If the user is vague
   ("just ballpark for a 30-year-old in Austin"), proceed with what you have. Ask at
   most **one** round of 2–4 short high-impact questions, then call once. When the
   user has already given almost all of ZIP, age, vehicle, and driving history,
   call in the first reply — price first, don't ask first.
2. Call **`quote_insurance`** with a `profile` dict, using the schema's
   exact field names: the core carries `zip_code` and `age` (or `dob`), the
   `auto` block carries `vehicles[]` (year/make/model) and `drivers[]`, and
   prior coverage rides `prior_insurance`. This is the
   instant rate-engine tool: one exact rate-engine run per carrier. Pass
   **`lines`** — ONE map naming the line to price, with that line's ask as
   actual numbers on four axes: `lines={"auto": {"bi": "100/300", "pd": 100,
   "coll_deductible": 500, "comp_deductible": 500}}` (`um` / `medpay` optional).
   If the user stated limits or deductibles, use them; otherwise pass that common
   starting point on the **first** call and declare it as an adjustable assumption.
3. The content channel is compact machine text (not JSON): a `Q` header, then `C`
   carrier rows, `L` sub-coverage lines, `F` rating factors, and `D` lever deltas.
   Priced results are keyed per line under `by_line`; structured headlines still
   carry `monthly`, `confidence_interval`, and `carrier_quote_url`. Read off, per carrier:
   - **`monthly`** — the headline point estimate, priced at the selection you
     passed. The `C` row also names the writing company; `carrier_quote_url` is
     where the user finishes (see purchase, below).
   - **`confidence_interval`** — `{low, high, confidence, basis}` when measured, or
     `{confidence: "unmeasured"}` / `"structural-only"` when validation data is thin.
     This is what we genuinely *can't* resolve right now (see below); state it as
     confidence, not a hedge.
   - **Sub-coverage lines (`L`)** — monthly dollars per line (BI/PD, collision,
     comprehensive, UM…) at the selection you passed. Use these for "what am I
     paying for" and for 6-month/annual totals (`monthly × 6` / `× 12`).
   - **`price_ladder` / `D` rows** — for each lever (BI limit, PD limit,
     collision/comprehensive deductible) the exact price at **every**
     rung, one lever moved at a time (`new monthly = monthly + D delta`). This
     is how you answer "what would a $1000 deductible cost" — read the number
     off the ladder; never interpolate. If a rung is missing for a carrier,
     that carrier has no such option.
4. Read the top-level **`assumptions`**, **`tighten_by`**, and **`failures`** and
   act on them (below).

## The two kinds of uncertainty — keep them separate

This is the core of how Foresee talks about confidence. Never blur them.

- **Confidence interval = irreducible.** "We think it's between $141 and $158 and we
  can't do better than that right now." This is proprietary carrier math we can't see
  (e.g. an insurer's internal tier/placement) plus our measured engine-vs-reality
  error. Report it as confidence, **not** as a hedge, and **do not widen it** because
  the profile was incomplete.
- **`assumptions` / `tighten_by` = reducible.** "If you also tell us your credit score,
  we'll sharpen the number." These are fields the user didn't give, so Foresee assumed
  them. Still give the point estimate; then, if `tighten_by` is non-empty, tell the
  user which one or two facts would tighten it most and offer to re-run.

So: incomplete profile → **point estimate + name the assumptions**, never a widened CI.

## Presenting results

- **Open with the decision.** Name the best option for this user (price + a one-line
  reason) before anything else — you are presenting Foresee's own computed quotes, so
  state prices as facts.
- Then a compact table sorted **cheapest-first**: **Carrier · Monthly · 6-month
  total**. Call out the **annual dollar spread** between the cheapest and priciest
  options — that spread is the reason to compare.
- Give the interval as confidence: "**$148/mo** with GEICO — we're confident it's in the
  **$141–$158** range." If a carrier's interval is `unmeasured` or `structural-only`,
  say so plainly rather than implying tightness we haven't earned.
- If `tighten_by` lists high-impact fields, add one line: "Tell me your credit score and
  I can narrow that."
- Surface `failures` (e.g. USAA when the user isn't military-affiliated) rather than
  silently dropping carriers.
- The instant quote is a computed estimate, **not a bindable quote**. End on the
  next concrete action — usually the recommended carrier's quoting-portal link, or
  an offer to confirm live (below).
- Offer the `price_ladder` / sub-coverage detail or a coverage change (see
  `explain-coverage` / `compare-carriers`) if the user wants to go deeper.

## Live quotes from the carrier's own site — agents

When the user wants firm, proven numbers (or is ready to buy), Foresee agents complete
the carriers' real quote flows and read back the page premium. Hypothetical or synthetic
profiles are fine: someone exploring "what would a driver like this pay" can fan out
live agents just like someone quoting their own details. When the details ARE the
user's real PII, the consent disclosure below is what makes the submission theirs to
authorize.

- **`live_carrier_quotes`** — the live-walk tool. IDEMPOTENT, keyed on profile +
  the ask. `lines` names the lines to walk: `{"auto": {...the ask...}}`,
  `{"home": null}`, or several at once — `{"auto": {...}, "renters": {...}}`
  commissions bundled walks: each carrier that writes all the named lines is
  driven through its own multi-line quote flow and reports per-line premiums
  plus the carrier's own bundle total; a carrier writing only some of them is
  walked for those alone. Walks cover the lines and states Foresee currently
  serves (California auto today), so a single-line auto walk is the common
  case. An auto or renters walk's ask is required (the same axes as the
  instant tool); without it the tool answers with the selection-required
  message — ask the user, then call again; a home walk takes `{"home": null}`
  — the carrier's own form prices its package.
  The first call commissions the walks; calling again with the SAME arguments
  collects progress and results instead of re-submitting. A profile that has
  already been walked returns those results — the carriers are never asked twice.
  **No sign-in or account is required.** The one hard gate is the user's own
  consent, captured in-band: a call without a verbatim `user_authorization` is
  refused with `authorization_required` — relay the disclosure, get the
  go-ahead, and call again. Never invent a live premium.

Commissioning requires consent:

1. **Before the first call, tell the user plainly**: Foresee will submit their details
   to the named carriers; the carriers may obtain their credit-based insurance score
   (a soft pull — no credit-score impact); and the carriers may contact them by email
   or phone.
2. Get their explicit go-ahead and pass it **verbatim** as `user_authorization`
   (e.g. "yes, go ahead"). That affirmation is stored as the durable consent record
   for the dispatch.
3. Collect the `identity` fields in chat (name, DOB, street address, email — never an
   SSN, which no carrier flow needs; a driver's-license number only when a
   carrier's form asks for it, handled like the name and address).
   A `missing_facts` response is normal — carrier forms
   insist on facts Foresee won't invent (body style, purchase date, age first
   licensed…); ask the user for exactly the `needs` listed and call again.

Collect results by re-calling `live_carrier_quotes` with the same arguments after a
minute or two; agents still working report their stage, so it's safe to check early and
again. Fold completed quotes into the table and call out anything now cheaper than the
previous best. An envelope with an engine baseline carries a `confirmation` block per
carrier — `engine_monthly` vs `observed_monthly`, the delta, and whether the live number
fell inside the engine's interval; **present the two numbers side by side with the
delta.** A carrier `declined` is a real answer from the carrier, not an error — relay
it plainly.

## Finishing up — hand off to the carrier

Foresee has **no bind API**: the estimate is not a bindable quote, and there is no
purchase step inside Foresee. Each carrier from the quote tool carries a
**`carrier_quote_url`** — when the user is ready to act, hand over the recommended
carrier's link as a clickable markdown link on its own line, and they finish the quote
themselves on the carrier's own site. This is the finish path for everyone. Route buy
intent to that link rather than implying Foresee can bind or check out for them.

## The one hard rule: never invent a price

Only ever quote a number Foresee returned. Every `monthly`, every `L` line, and
every `price_ladder` / `D` rung **is** an exact re-rate — use those freely. But
**do not** multiply the `F` factors yourself, do not interpolate a limit/deductible
or a combination we didn't price, and do not average carriers into a made-up figure.
If the user wants a coverage combination or carrier we didn't return, re-call the
tool with the new ask in `lines`. Every dollar you show must be one the
engine computed — that is what lets us stand behind it.

## Unsupported states

Foresee covers a limited set of states today. If the user's state isn't covered, the
tool returns a clear error (e.g. *"Foresee isn't live for WY yet"*). Relay that message
plainly — do not guess or fabricate a number for a state we don't cover.
