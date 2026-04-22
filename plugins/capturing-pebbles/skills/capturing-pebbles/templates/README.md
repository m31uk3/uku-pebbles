# Pebbles Templates

Hierarchical template system for pebble creation. Inspired by [defuddle](https://github.com/nicepkg/defuddle)'s extractor pattern — each source app gets a dedicated template that knows how to extract maximum structured context. See `.sop/synthesis/05-defuddle-investigation.md` for the design lineage.

## Standard Install Path

`~/.pebbles/templates/` is the standard config location on all systems (macOS, Linux, cloud desktops, AgentSpaces). All consumers — CLI, skills, hooks, agents — read from this path.

## Available vs Installed

Templates in this directory are the **available** set — everything the skill ships with.

At install time, only `.sys.json` (system default) templates are copied to `~/.pebbles/templates/`. User templates (`.user.json`) are opt-in — the user copies what they need.

| Suffix | Meaning | Installed by default |
|--------|---------|---------------------|
| `.sys.json` | System template — ships with skill, installed automatically | Yes |
| `.user.json` | User/content-type template — available, not installed by default | No |

### Install behavior

1. Check if `~/.pebbles/templates/` exists
2. If not, create it and copy all `.sys.json` files
3. If it exists, only copy `.sys.json` files that are missing (never overwrite)
4. User copies `.user.json` templates manually when needed

## Template Hierarchy

Templates stack via `extends` and the `name` field. The `name` field is the stacking key — filenames are for humans.

```
base.sys.json              ← Always. Spec-required fields (ULID, created_at, pebble_type).
  └── org.sys.json         ← Always. Org + team defaults.
        ├── slack.sys.json         ← source_app=slack
        ├── email.sys.json         ← source_app=email
        ├── web.sys.json           ← source_app=web
        ├── meeting.sys.json       ← source_app=meeting
        ├── terminal.sys.json      ← source_app=terminal
        └── known-issue.user.json  ← pebble_type=problem_statement + tags contain "known-issue"
```

### Two matching axes

- **Source-type** (`.sys.json`): matched by `source_app` or `url_pattern` — where the content came from
- **Content-type** (`.user.json`): matched by `pebble_type` + `tags` — what kind of knowledge it is

A pebble can stack both: a known issue discovered in Slack applies `org` → `slack` → `known-issue`.

## Zettelkasten Mapping

Templates enforce structured metadata at capture time — the L0 layer of the consolidation hierarchy:

| Level | Zettelkasten | Pebbles | Template role |
|-------|-------------|---------|---------------|
| L0 | Fleeting notes | Raw episodic pebbles | Templates populate frontmatter |
| L0.5 | **Literature notes** | **Reference pebbles** (`pebble_type: reference`) | web.sys.json defaults to this |
| L1 | Permanent notes | Consolidated insights | Promoted from L0 via curation |
| L2 | Maps of Content | Synthesis/ontology pebbles | Agent or human authored |
| L3+ | Meta-syntheses | Cross-domain abstractions | — |

## Resolution Order

1. Load `base.sys.json` (always)
2. Walk `extends` chain: `base` → `org` → app/content-specific
3. Match source-type template by `source_app` or `url_pattern`
4. Match content-type template by `pebble_type` + `tags`
5. Merge: later templates override earlier defaults; `required` fields accumulate
6. User-provided values override all defaults

## Adding a New Template

1. Create `{name}.user.json` in this directory
2. Set `match` criteria (source_app, url_pattern, pebble_type, tags_contain)
3. Set `extends: "org"` (or `"base"` if no org context needed)
4. Define fields in `required`, `defaults`, `optional` sections
5. Add `body_template` array for the Markdown scaffold
6. Copy to `~/.pebbles/templates/` to activate

## Design Principles

1. **Defuddle-inspired**: one template per source app, pattern-matched
2. **Hierarchical stacking**: base → org → app/content (like CSS specificity)
3. **Source provenance is structured**: never composite strings, always Luhmann-passing
4. **Fluid schema preserved**: templates define known fields; unknown fields pass through
5. **Org context is automatic**: team, org injected without user effort
6. **Available ≠ installed**: skill ships all templates; user activates what they need
