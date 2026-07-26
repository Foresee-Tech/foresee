# Standard Clearing

Auto-insurance quote estimates in your AI assistant. Ask in plain English — e.g.
*"how much would car insurance cost for a 2022 Camry in NY?"* — and get per-carrier
monthly price estimates. Both plugins connect to the **same hosted MCP server**; there
is no separate backend per client.

## Claude

```bash
/plugin marketplace add Dagulf795/standard-clearing
/plugin install standard-clearing@standard-clearing
```

On enable, Claude prompts for an API key. Package:
[`plugins/standard-clearing/`](plugins/standard-clearing).

## ChatGPT + Codex

```bash
codex plugin marketplace add .
codex plugin marketplace list
```

Then install **standard-clearing** from the ChatGPT desktop Plugins Directory and
complete the OAuth email one-time-code sign-in on first use. Package:
[`plugins/standard-clearing-chatgpt/`](plugins/standard-clearing-chatgpt) — see its
README for the full install/test/publish guide. The Codex marketplace manifest lives
at [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json).

| | Claude | ChatGPT / Codex |
|---|---|---|
| Manifest | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` |
| Marketplace | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` |
| MCP config | `.mcp.json` (bearer `${user_config.api_key}`) | `.mcp.json` (remote HTTP) |
| Auth | OAuth (web) or shared key (Desktop/Code) | OAuth 2.1 via ChatGPT connector |
| Skills | quote-my-car, compare-carriers, explain-coverage | identical (same MCP tools) |
| Backend | `standard-clearing-mcp` on Cloud Run | **same** `standard-clearing-mcp` on Cloud Run |

**Beta:** Utah only. Estimates, not bindable quotes.
