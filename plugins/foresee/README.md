# Foresee

Insurance quote estimates for ChatGPT, Codex, Claude, and any MCP client. Ask
in plain English — e.g. *"how much would car insurance cost for a 2022 Camry
in Sacramento?"* — and get a per-carrier monthly point estimate with a
confidence interval and full sub-coverage detail, or compare carriers.

> **Auto only for now.** Foresee estimates auto insurance today — home and other lines are coming soon.

Instant quotes need no sign-in. Live carrier confirmation prompts the host's
OAuth flow (email code) the first time you run it.

## Install

```bash
/plugin marketplace add Foresee-Tech/foresee
/plugin install foresee@foresee
```

Enable it and start asking — no API key required. Instant quotes work anonymously; the
live carrier-confirmation tools require signing in.

Or point any MCP client at:

```
https://mcp.go-foresee.com/mcp
```
