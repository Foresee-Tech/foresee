<img src="assets/logo.svg" alt="Foresee" width="72">

# Foresee

AI should buy your home and auto insurance. Foresee returns accurate quotes from every carrier as structured objects that agents can reason about.

*"How much would auto insurance cost for a 25 year old driving a 2022 Camry in Sacramento?"*
*"Do I need a high deductible? Which insurer is best for premium coverage?"*
*"Am I eligible for any group discounts?"*

> **Foresee is currently only live with California auto insurance - more states and lines coming soon.** 

## Install

Pick where you want to use Foresee:

[![Add to Claude](https://img.shields.io/badge/Add_to-Claude-D97757?style=for-the-badge&logo=claude&logoColor=white)](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Foresee&connectorUrl=https%3A%2F%2Fforesee-mcp-1026846013023.us-central1.run.app%2Fmcp)
[![Add to ChatGPT](https://img.shields.io/badge/Add_to-ChatGPT-10A37F?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iI2ZmZiI+PHBhdGggZD0iTTIyLjI4MTkgOS44MjExYTUuOTg0NyA1Ljk4NDcgMCAwIDAtLjUxNTctNC45MTA4IDYuMDQ2MiA2LjA0NjIgMCAwIDAtNi41MDk4LTIuOUE2LjA2NTEgNi4wNjUxIDAgMCAwIDQuOTgwNyA0LjE4MThhNS45ODQ3IDUuOTg0NyAwIDAgMC0zLjk5NzcgMi45IDYuMDQ2MiA2LjA0NjIgMCAwIDAgLjc0MjcgNy4wOTY2IDUuOTggNS45OCAwIDAgMCAuNTExIDQuOTEwNyA2LjA1MSA2LjA1MSAwIDAgMCA2LjUxNDYgMi45MDAxQTUuOTg0NyA1Ljk4NDcgMCAwIDAgMTMuMjU5OSAyNGE2LjA1NTcgNi4wNTU3IDAgMCAwIDUuNzcxOC00LjIwNTggNS45ODk0IDUuOTg5NCAwIDAgMCAzLjk5NzctMi45MDAxIDYuMDU1NyA2LjA1NTcgMCAwIDAtLjc0NzUtNy4wNzI5em0tOS4wMjIgMTIuNjA4MWE0LjQ3NTUgNC40NzU1IDAgMCAxLTIuODc2NC0xLjA0MDhsLjE0MTktLjA4MDQgNC43NzgzLTIuNzU4MmEuNzk0OC43OTQ4IDAgMCAwIC4zOTI3LS42ODEzdi02LjczNjlsMi4wMiAxLjE2ODZhLjA3MS4wNzEgMCAwIDEgLjAzOC4wNTJ2NS41ODI2YTQuNTA0IDQuNTA0IDAgMCAxLTQuNDk0NSA0LjQ5NDR6bS05LjY2MDctNC4xMjU0YTQuNDcwOCA0LjQ3MDggMCAwIDEtLjUzNDYtMy4wMTM3bC4xNDIuMDg1MiA0Ljc4MyAyLjc1ODJhLjc3MTIuNzcxMiAwIDAgMCAuNzgwNiAwbDUuODQyOC0zLjM2ODV2Mi4zMzI0YS4wODA0LjA4MDQgMCAwIDEtLjAzMzIuMDYxNUw5Ljc0IDE5Ljk1MDJhNC40OTkyIDQuNDk5MiAwIDAgMS02LjE0MDgtMS42NDY0ek0yLjM0MDggNy44OTU2YTQuNDg1IDQuNDg1IDAgMCAxIDIuMzY1NS0xLjk3MjhWMTEuNmEuNzY2NC43NjY0IDAgMCAwIC4zODc5LjY3NjVsNS44MTQ0IDMuMzU0My0yLjAyMDEgMS4xNjg1YS4wNzU3LjA3NTcgMCAwIDEtLjA3MSAwbC00LjgzMDMtMi43ODY1QTQuNTA0IDQuNTA0IDAgMCAxIDIuMzQwOCA3Ljg3MnptMTYuNTk2MyAzLjg1NThMMTMuMTAzOCA4LjM2NCAxNS4xMTkyIDcuMmEuMDc1Ny4wNzU3IDAgMCAxIC4wNzEgMGw0LjgzMDMgMi43OTEzYTQuNDk0NCA0LjQ5NDQgMCAwIDEtLjY3NjUgOC4xMDQydi01LjY3NzJhLjc5Ljc5IDAgMCAwLS40MDctLjY2N3ptMi4wMTA3LTMuMDIzMWwtLjE0Mi0uMDg1Mi00Ljc3MzUtMi43ODE4YS43NzU5Ljc3NTkgMCAwIDAtLjc4NTQgMEw5LjQwOSA5LjIyOTdWNi44OTc0YS4wNjYyLjA2NjIgMCAwIDEgLjAyODQtLjA2MTVsNC44MzAzLTIuNzg2NmE0LjQ5OTIgNC40OTkyIDAgMCAxIDYuNjgwMiA0LjY2ek04LjMwNjUgMTIuODYzbC0yLjAyLTEuMTYzOGEuMDgwNC4wODA0IDAgMCAxLS4wMzgtLjA1NjdWNi4wNzQyYTQuNDk5MiA0LjQ5OTIgMCAwIDEgNy4zNzU3LTMuNDUzN2wtLjE0Mi4wODA1TDguNzA0IDUuNDU5YS43OTQ4Ljc5NDggMCAwIDAtLjM5MjcuNjgxM3ptMS4wOTc2LTIuMzY1NGwyLjYwMi0xLjQ5OTggMi42MDY5IDEuNDk5OHYyLjk5OTRsLTIuNTk3NCAxLjQ5OTctMi42MDY3LTEuNDk5N3oiLz48L3N2Zz4=)](#chatgpt)
[![Add to Cursor](https://img.shields.io/badge/Add_to-Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white)](https://cursor.com/install-mcp?name=foresee&config=eyJ0eXBlIjoiaHR0cCIsInVybCI6Imh0dHBzOi8vZm9yZXNlZS1tY3AtMTAyNjg0NjAxMzAyMy51cy1jZW50cmFsMS5ydW4uYXBwL21jcCJ9)
[![Add to Claude Code](https://img.shields.io/badge/Add_to-Claude_Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](#claude-code)
[![Any MCP client](https://img.shields.io/badge/Any-MCP_client-6E56CF?style=for-the-badge&logo=modelcontextprotocol&logoColor=white)](#any-mcp-client-coding-agents)

No API key or sign-up required — just connect and start asking. The MCP endpoint is:

```
https://foresee-mcp-1026846013023.us-central1.run.app/mcp
```

---

### Claude (claude.ai)

**Recommended.** Click **[Add to Claude](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Foresee&connectorUrl=https%3A%2F%2Fforesee-mcp-1026846013023.us-central1.run.app%2Fmcp)** above — this opens Claude's *Add custom connector* dialog with Foresee pre-filled. Confirm and you're ready to ask.

### ChatGPT

ChatGPT connects to remote MCP servers through **Developer Mode** (available on paid plans). There's no one-click link, so add it manually:

1. In ChatGPT, open **Settings → Apps & Connectors → Advanced** and turn on **Developer Mode**.
2. Go back to **Apps & Connectors → Create** and fill in:
   - **Name:** `Foresee`
   - **Connector URL:** `https://foresee-mcp-1026846013023.us-central1.run.app/mcp`
   - **Authentication:** None
3. Save. Foresee's tools now appear in chat.

### Cursor

Click **[Add to Cursor](https://cursor.com/install-mcp?name=foresee&config=eyJ0eXBlIjoiaHR0cCIsInVybCI6Imh0dHBzOi8vZm9yZXNlZS1tY3AtMTAyNjg0NjAxMzAyMy51cy1jZW50cmFsMS5ydW4uYXBwL21jcCJ9)** above, then confirm the install in Cursor. That's it — no key to paste.

### Claude Code

Prefer the terminal? Install as a plugin:

```bash
/plugin marketplace add Foresee-Tech/foresee
/plugin install foresee@foresee
```

Enable it and start asking — no API key or sign-up required.

### Any MCP client (coding agents)

Foresee is a standard streamable-HTTP MCP server, so it works with any MCP-compatible client (VS Code, Windsurf, Zed, Cline, custom agents, etc.). Add this to your client's MCP config:

```json
{
  "mcpServers": {
    "foresee": {
      "type": "http",
      "url": "https://foresee-mcp-1026846013023.us-central1.run.app/mcp"
    }
  }
}
```
