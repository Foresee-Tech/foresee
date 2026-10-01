<!-- @copy plugin.cursor.readme audience=human -->
# Foresee for Cursor

Foresee enables AI to shop for home and auto insurance.
Foresee returns accurate quote estimates from every insurance carrier, so that your AI can help you make the right decision for you and your finances.
Foresee provides full, free and detailed quote information across the entire market - from household names like State Farm, Progressive, and Allstate, down to niche and regional carriers that might be a fit for you.

Beyond instant estimates, Foresee agents can complete the carriers' own online
quote flows and read back the page-printed premium, so the estimate comes with
proof it holds up on the carrier's site. Live submissions run only with the
user's explicit, in-chat consent, and no sign-in is needed.

## Install

Open **Cursor Settings → Plugins**, search for **Foresee** and click **Install**,
or run `/add-plugin foresee` in chat.

## MCP

```json
{
  "mcpServers": {
    "foresee": {
      "type": "http",
      "url": "https://cursor.go-foresee.com/mcp"
    }
  }
}
```

No sign-in, API key or configuration: the server is open to anonymous callers.
It serves the same tools as `agents.go-foresee.com`, with every result written
out in full on the content channel, the one Cursor's model reads.

## What agents can do

| Tool | What it does |
| --- | --- |
| `quote_insurance` | Instant quote estimates from every supported carrier, with a sub-coverage breakdown and a price ladder per carrier |
| `live_carrier_quotes` | Completes the carriers' own quote flows and reads back the page premium, after the user consents in chat |

## Skills

- **quote-insurance**: gathers the minimum profile and returns carrier quotes.
- **compare-carriers**: compares carriers for the user's profile.
- **explain-coverage**: explains limits and deductibles and what changing them costs.

Full docs: https://go-foresee.com/docs
