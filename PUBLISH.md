# Publishing to the public `Dagulf795/standard-clearing` repo

This directory (`standard-clearing-marketplace/`) is the **exact payload** for the
public distribution repo. It's kept here (inside the private `quoting` monorepo) so
the plugin is co-developed with the backend, then published out to a public repo —
which is required because Claude community-marketplace sources must be **public git**
and `quoting` is private/proprietary.

## One-time: create the empty public repo

Create `https://github.com/Dagulf795/standard-clearing` on GitHub (public, empty — no
README/license, we provide those).

## Option A — publish with history (git subtree, recommended)

From the **root of the `quoting` repo**:

```bash
# Split this subdirectory into a standalone branch with its own history
git subtree split --prefix=standard-clearing-marketplace -b sc-publish

# Push that branch to the public repo's main
git push git@github.com:Dagulf795/standard-clearing.git sc-publish:main

# Clean up the local split branch
git branch -D sc-publish
```

Re-run the same three commands to publish updates (subtree split is idempotent).

## Option B — publish a flat snapshot (no history)

```bash
tmp=$(mktemp -d)
cp -r standard-clearing-marketplace/. "$tmp"
cd "$tmp"
git init -b main
git add .
git commit -m "Standard Clearing plugin marketplace"
git remote add origin git@github.com:Dagulf795/standard-clearing.git
git push -u origin main
```

## After publishing — verify end to end

```bash
/plugin marketplace add Dagulf795/standard-clearing
/plugin install standard-clearing@standard-clearing
# enable, paste beta key: informationwantstobefree
```

## Community submission (Phase 6)

Once the hosted MCP endpoint is live and the public repo is up, submit via
`platform.claude.com/plugins/submit` (individual-author path). On approval the plugin
is pinned to a commit SHA and synced nightly into `anthropics/claude-plugins-community`.
