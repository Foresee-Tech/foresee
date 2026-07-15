# Standard Clearing — Claude plugin marketplace

Public distribution repo for the **Standard Clearing** auto-insurance quoting plugin
for Claude Code. This repo is a **thin client**: it contains only the plugin manifest,
MCP configuration, and skills. It ships **no proprietary rate data** — quotes are
computed server-side by a hosted MCP endpoint.

> This directory is the self-contained payload for the public repo
> `Dagulf795/standard-clearing`. It lives inside the private `quoting` monorepo during
> development and is published out via `PUBLISH.md`.

## Install

```bash
/plugin marketplace add Dagulf795/standard-clearing
/plugin install standard-clearing@standard-clearing
```

On enable, Claude Code prompts for an API key (beta key: `informationwantstobefree`).

## What's here

```
.claude-plugin/marketplace.json      # marketplace catalog (lists the plugin)
plugins/standard-clearing/           # the plugin itself
  ├── .claude-plugin/plugin.json
  ├── .mcp.json                      # remote HTTP MCP + Bearer ${user_config.api_key}
  ├── skills/                        # quote-my-car, compare-carriers, explain-coverage
  ├── README.md
  └── LICENSE
```

See `plugins/standard-clearing/README.md` for plugin details and local development.

## Validate

```bash
claude plugin validate ./plugins/standard-clearing --strict
claude plugin validate .        # marketplace catalog
```

## License

MIT — see `LICENSE`.
