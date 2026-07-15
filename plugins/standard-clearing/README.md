# Standard Clearing — Auto Insurance Quotes (Claude plugin)

Deterministic auto-insurance price estimates inside Claude. Ask for a car-insurance
quote or compare carriers; the plugin gathers a driver/vehicle profile and returns
per-carrier monthly price ranges computed from published **SERFF rate filings**.

## How it works

The plugin is a **thin client**. It ships only an MCP configuration + skills and
connects over HTTP to a hosted Standard Clearing MCP endpoint. All proprietary rate
data (VIN symbol tables, filing factors, thousands of SERFF filings) stays on the
server and is never downloaded to your machine.

```
Claude Code ──HTTP (Bearer key)──▶ https://api.quoting.dev/mcp ──▶ SERFF rate engines
```

## Tools

| Tool | Purpose |
|------|---------|
| `auto_insurance_engine_coverage` | Which carriers/tiers are modeled for a state |
| `auto_insurance_quote_profile`   | Exact tiered quotes for a structured profile |
| `auto_insurance_quote_range`     | Monte-Carlo p25/p50/p75 over unknown fields |
| `auto_insurance_recommend_options` | Ranked recommendation + uncertainty caveats |

## Skills

- `/standard-clearing:quote-my-car` — get an estimate conversationally
- `/standard-clearing:compare-carriers` — rank carriers / shop around
- `/standard-clearing:explain-coverage` — understand limits, deductibles, tiers

(Skills are also model-invoked: just ask "how much would car insurance cost me?")

## Install

```bash
# From the marketplace
/plugin marketplace add Dagulf795/standard-clearing
/plugin install standard-clearing@standard-clearing
```

On enable, Claude Code prompts for your **API key** (stored securely). During the
beta the key is:

```
informationwantstobefree
```

The plugin ships **disabled by default** (`defaultEnabled: false`) because it calls
an external service — opt in when ready.

### Local development (no install)

```bash
claude --plugin-dir ./plugins/standard-clearing
claude plugin validate ./plugins/standard-clearing --strict
```

Point the plugin at a local server by editing `.mcp.json`'s `url` to
`http://localhost:8009/mcp` and running the hosted MCP endpoint locally (from the
main quoting repo): `cd backend && uv run uvicorn src.quote_advisor.mcp_http:app --port 8009`.

## Coverage

The engines cover a limited set of states today. For states we don't cover yet, the
tools return a clear "no coverage yet" error rather than a made-up number. The skills
also surface per-carrier caveats (e.g. a carrier unpriced for a profile).

## License

MIT — see `LICENSE`.
