# Standard Clearing (ChatGPT + Codex)

Auto-insurance quote estimates for ChatGPT and Codex. Ask in plain English — e.g.
*"how much would car insurance cost for a 2020 Honda Civic in Salt Lake City?"* — and
get per-carrier monthly price estimates, or compare carriers.

This is the ChatGPT/Codex counterpart of the Claude plugin in this same repo
([`plugins/standard-clearing/`](../standard-clearing)). Both connect to the same
hosted MCP server — no separate backend to deploy.

- **Beta:** Utah only. Estimates, not bindable quotes.
- **MCP server:** `https://standard-clearing-mcp-1026846013023.us-central1.run.app/mcp`
- **Auth:** OAuth 2.1 (email one-time code). No API key to paste.

## What's in the package

```
plugins/standard-clearing-chatgpt/
├── .codex-plugin/plugin.json   # plugin manifest (identity + interface metadata)
├── .mcp.json                   # points at the hosted MCP server (streamable HTTP)
├── .app.json.example           # optional: ChatGPT developer-mode connector template
└── skills/
    ├── quote-my-car/           # "how much would insurance cost me?"
    ├── compare-carriers/       # "who's cheapest / should I switch?"
    └── explain-coverage/       # "what does 100/300/100 mean?"
```

The four MCP tools the skills call: `auto_insurance_engine_coverage`,
`auto_insurance_quote_profile`, `auto_insurance_quote_range`,
`auto_insurance_recommend_options`.

## Install & test (Codex CLI)

The Codex marketplace lives at the repo root (`.agents/plugins/marketplace.json`).
Add this repo as a local marketplace, then install:

```bash
codex plugin marketplace add .
codex plugin marketplace list
```

Then open the ChatGPT desktop app → Plugins Directory → **Standard Clearing**
marketplace → install **standard-clearing**. On first use you'll complete the OAuth
email one-time-code flow. Start a new chat and ask a quote question.

## Install & test (ChatGPT developer mode)

For a hosted remote MCP server, ChatGPT connects through a registered developer-mode
app:

1. ChatGPT → Settings → **Security and login** → turn on **Developer mode**.
2. Settings → **Plugins** → **+** → enter the MCP server URL
   `https://standard-clearing-mcp-1026846013023.us-central1.run.app/mcp` and create
   the connection. Complete the OAuth sign-in (email one-time code).
3. Copy the app ID from the browser URL (starts with `plugin_asdk_app`).
4. Copy `.app.json.example` to `.app.json`, replace the placeholder with your
   `plugin_asdk_app...` ID, and add `"apps": "./.app.json"` to
   `.codex-plugin/plugin.json`.
5. Refresh ChatGPT and install the plugin from your local marketplace.

The bundled `.mcp.json` is enough for Codex CLI and for surfaces that consume a remote
MCP server directly; the `.app.json` route is only needed where ChatGPT requires a
pre-registered connector.

## Publish

To list in the universal ChatGPT + Codex directory, submit through the OpenAI plugin
submission portal. Provide `interface.privacyPolicyURL` and
`interface.termsOfServiceURL` (absolute `https://` URLs) at submission time.
