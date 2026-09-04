---
name: quote-insurance
description: This skill should be used when the user wants a personal lines (especially home and auto) insurance quote comparison or price estimate — e.g. asks "how much would car insurance cost me", "what auto insurance should I get", "estimate my auto insurance", "what would I pay for insurance on my <car>", or gives driver/vehicle details and asks for a price. Gathers the minimum profile conversationally and returns carrier quotes.
version: 0.4.0
---

# Quote Insurance

Return estimated insurance quotes for the user by calling the `foresee` MCP
tools. The tool returns an estimate with a confidence interval, broken down into sub-coverages, so that the user can make decisions about limits, deductibles, and so on across multiple carriers.
Foresee bases rates on carriers' filed rate manuals, and gathers real quotes from carrier online quoting flows.
Foresee does not monetise by selling ads or leads.

## Scope — auto only for now

Foresee estimates **auto insurance** today; home and other lines are coming soon. This
is the one disclaimer to give: if the user asks about a line that isn't live yet (home,
condo, renters, etc.), say so plainly in a single sentence, then offer an auto quote if
it's relevant — don't refuse the whole conversation or repeat the caveat over and over.
Everything below describes the live auto flow.

## How Foresee works — two parts

Foresee is a two-part system, and the trust comes from how they fit together:

1. **Deterministic rate engines (instant).** `auto_insurance_quote_profile` runs each
   carrier's *filed rate manual* against the profile and returns an exact computed
   premium per carrier — with a full sub-coverage breakdown and a price ladder — in one
   call. This is the headline answer and the default path.
2. **Live carrier agents (confirmation).** Foresee agents drive the carriers' own
   quoting websites with the user's real details and read back the page-printed premium.
   Their job is to **confirm the engine**: `confirm_quotes_live` compares the live number
   against the engine's estimate so the user sees the instant quote *and* proof it holds
   up on the carrier's site.

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
   most **one** round of 2–4 short high-impact questions, then call once.
2. Call **`auto_insurance_quote_profile`** with a `profile` dict, using the schema's
   exact field names (`zip_code`, `vehicle_year`, `accidents_3yr`, …). This is the
   primary tool: one exact rate-engine run per carrier — fast, deterministic, and
   `source: deterministic_serff` (filing-based). Prefer it over the range/recommend
   tools.
3. Read off, per carrier:
   - **`monthly`** — the headline point estimate. Each carrier also carries
     `entity_name` (the actual writing company) and `carrier_quote_url` (where the
     user finishes — see purchase, below).
   - **`confidence_interval`** — `{low, high, confidence, basis}` when measured, or
     `{confidence: "unmeasured"}` / `"structural-only"` when validation data is thin.
     This is what we genuinely *can't* resolve right now (see below); state it as
     confidence, not a hedge.
   - **`cells`** — good/better/best tiers (`minimum`, `standard`, `premium`), each with
     its own `monthly`, `semiannual_total`, `annual_total`, and a per-line `coverages`
     breakdown (BI/PD, collision, comprehensive, fees…) carrying the selected limit and
     each rating `step`. Use it for "what am I paying for" and for 6-month/annual totals.
   - **`price_ladder`** — for each lever (BI limit, PD limit, collision/comprehensive
     deductible) the exact filed monthly at **every** rung, one lever moved at a time.
     This is how you answer "what would a $1000 deductible cost" — read the number off
     the ladder; never interpolate.
   - **`trust`** — `verdict` (solid / caution / unverified) plus a `complaint_record`
     (NAIC complaint index). Read it alongside the top-level `trust_methodology`:
     complaint indexes are relative, so compare carriers to each other, not to 1.0.
4. Read the top-level **`assumptions`**, **`tighten_by`**, **`failures`**, and
   **`disclaimer`** and act on them (below). `quote_history` (`list` / `compare`) recalls
   a signed-in user's past quotes and diffs two `request_id`s if they ask "what changed".

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

- **Open with the decision.** Name the best option for this user (price + a one-line
  reason) before anything else — you are presenting Foresee's own computed quotes, so
  state prices as facts and don't add personal-advisor caveats or tell the user to
  re-confirm with the carrier.
- Then a compact table sorted **cheapest-first**: **Carrier · Monthly · 6-month total ·
  Trust**. Call out the **annual dollar spread** between the cheapest and priciest
  options — that spread is the reason to compare.
- Give the interval as confidence: "**$148/mo** with GEICO — we're confident it's in the
  **$141–$158** range." If a carrier's interval is `unmeasured` or `structural-only`,
  say so plainly rather than implying tightness we haven't earned.
- If `tighten_by` lists high-impact fields, add one line: "Tell me your credit range and
  I can narrow that."
- Surface `failures` (e.g. USAA when the user isn't military-affiliated) rather than
  silently dropping carriers.
- The instant quote is a filing-based estimate, **not a bindable quote** (relay the
  top-level `disclaimer` when it matters). End on the next concrete action — usually the
  recommended carrier's quoting-portal link, or an offer to confirm live (below).
- Offer the `price_ladder` / sub-coverage detail or a coverage change (see
  `explain-coverage` / `compare-carriers`) if the user wants to go deeper.

## Confirming against the carrier — live agents

When the user wants firm, proven numbers (or is ready to buy), Foresee agents complete
the carriers' real quote flows with the user's **real** details and read back the page
premium. These live walks run for **anyone — no Foresee sign-in required** — but they
submit real PII to carriers, so run them only on the user's own real profile, never on a
hypothetical or third-person profile (hypotheticals get instant quotes). Two entry
points:

- **`confirm_quotes_live`** — the validation run. It dispatches agents for the
  carrier+state pairs with a production-marked walk, snapshots the instant engine quote,
  and compares the carrier's page-printed premium against it. This is "the CUA confirms
  the engine."
- **`request_live_carrier_quotes`** — fan out agents to quote the real profile live when
  the user wants to move toward buying.

Both require consent, every time:

1. **Before calling, tell the user plainly**: Foresee will submit their details to the
   named carriers; the carriers may pull their credit report and driving record (a soft
   pull — no credit-score impact); and the carriers may contact them by email or phone.
2. Get their explicit go-ahead and pass it **verbatim** as `user_authorization`
   (e.g. "yes, go ahead"). The tools refuse to run without it.
3. `identity` may be omitted for a signed-in user with a saved profile; otherwise collect
   the identity fields in chat. A `missing_facts` response is normal — carrier forms
   insist on facts Foresee won't invent (body style, purchase date, age first
   licensed…); ask the user for exactly the `needs` listed and call again.

Collect results with **`check_agent_quotes`** using the returned `dispatch_id` (also the
`dispatch_id` on any `dispatched_agents` in a quote). Call it after a minute or two;
agents still working report their stage, so it's safe to check early and again. Fold
completed quotes into the table and call out anything now cheaper than the previous best.
A confirmation dispatch carries a `confirmation` block per carrier — `engine_monthly` vs
`observed_monthly`, the delta, and whether the live number fell inside the engine's
interval; **present the two numbers side by side with the delta.** A carrier `declined`
is a real answer from the carrier, not an error — relay it plainly.

A completed live walk may also carry a **`handoff_url`** — a link to the *same live
browser session* the agent drove, with the carrier's form already filled in and the
quote priced, letting the user **take control of that session and finish from where the
agent stopped**, nothing to re-enter (see below).

`handoff_url` is the **one capability that requires the user to be signed in.** Keeping a
live session open and exposing its URL is only safe when it's bound to a known identity
holding *their own* PII, so the server returns it for authenticated users only. An
anonymous user still gets the full live walk — premiums, `confirmation`,
`carrier_quote_url` — just **no `handoff_url`**; there's no open session to leak. If the
only thing standing between the user and the takeover is sign-in, surface that at the
point of highest intent (below) rather than treating it as unavailable.

## Finishing up — hand off to the carrier

Foresee has **no bind API**: the estimate is not a bindable quote, and there is no
purchase step inside Foresee. The user finishes on the carrier — but *how* depends on
what's available, and there are two endings. Always **prefer the live hand-off** when
it's there:

1. **Live hand-off (preferred) — `handoff_url`.** Returned for **signed-in users only**
   (see above). When a live walk returns a `handoff_url`, hand the user that link as a
   clickable markdown link on its own line. It drops them into the **same browser session
   the agent drove**, with the carrier's form already filled and the quote priced — they
   just take control and finish, nothing to re-enter. **Warn them plainly that this link
   controls a live browser session holding their personal details, so they must not share
   it with anyone.**
2. **Simple quoting site — `carrier_quote_url`.** Otherwise — including every anonymous
   user — each carrier from the quote tool carries a `carrier_quote_url`; hand that over
   and the user completes the quote themselves on the carrier's own site. If the *only*
   reason there's no live hand-off is that the user isn't signed in, say so at the point
   of highest intent — "GEICO is filled out and priced; sign in and I can drop you
   straight into that session to finish" — rather than treating the takeover as
   unavailable.

Either way the user finishes the purchase themselves — route buy intent to the link
rather than implying Foresee can bind or check out for them.

## The one hard rule: never invent a price

Only ever quote a number Foresee returned. Every `monthly`, every `cells` figure, and
every `price_ladder` rung **is** an exact re-rate — use those freely. But **do not**
multiply the `steps` factors yourself, do not interpolate a limit/deductible or a
combination we didn't price, and do not average carriers into a made-up figure. If the
user wants a coverage level, combination, or carrier we didn't return, pass a
`coverage_selection` (snapped to each carrier's filed rung, recorded in `snapped_to`)
and call the tool again. Every dollar you show must be one the engine computed — that is
what lets us stand behind it.

## Unsupported states

Foresee covers a limited set of states today. If the user's state isn't covered, the
tool returns a clear error (e.g. *"Foresee isn't live for WY yet"*). Relay that message
plainly — do not guess or fabricate a number for a state we don't cover.
