<img src="assets/logo.svg" alt="Foresee" width="72">

# Foresee

AI should buy your home and auto insurance. Foresee returns accurate quotes from every carrier as structured objects that agents can reason about.

*"How much would auto insurance cost for a 25 year old driving a 2022 Camry in Sacramento?"*
*"Do I need a high deductible? Which insurer is best for premium coverage?"*
*"Am I eligible for any group discounts?"*

> **Foresee is currently only live with California auto insurance - more states and lines coming soon.** 

## Install

One-click setup — click a button and confirm:

[![Add to Claude](https://img.shields.io/badge/Add_to-Claude-D97757?style=for-the-badge&logo=claude&logoColor=white)](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Foresee&connectorUrl=https%3A%2F%2Fmcp.go-foresee.com%2Fmcp)

[![Add to Cursor](https://img.shields.io/badge/Add_to-Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white)](https://cursor.com/install-mcp?name=foresee&config=eyJ0eXBlIjoiaHR0cCIsInVybCI6Imh0dHBzOi8vbWNwLmdvLWZvcmVzZWUuY29tL21jcCJ9)

Everywhere else, point your client at the MCP endpoint — no API key or sign-up required:

```
https://mcp.go-foresee.com/mcp
```

### ChatGPT

ChatGPT connects to remote MCP servers through **Developer Mode** (available on paid plans). Add it manually:

1. In ChatGPT, open **Settings → Apps & Connectors → Advanced** and turn on **Developer Mode**.
2. Go back to **Apps & Connectors → Create** and fill in:
   - **Name:** `Foresee`
   - **Connector URL:** `https://mcp.go-foresee.com/mcp`
   - **Authentication:** None
3. Save. Foresee's tools now appear in chat.

### Any MCP client

Foresee is a standard streamable-HTTP MCP server, so it works with any MCP-compatible client (VS Code, Windsurf, Zed, Cline, custom agents, etc.). Add this to your client's MCP config:

```json
{
  "mcpServers": {
    "foresee": {
      "type": "http",
      "url": "https://mcp.go-foresee.com/mcp"
    }
  }
}
```
