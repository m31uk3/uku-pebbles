# Pebble Templates — Design Discovery (15 APR 2026)

## Origin

While creating the first real Slack pebble, a gap analysis revealed that the spec's Tier 1 ingestion contract references `source_app` and `device` as auto-captured fields (§3.1) but never defines their schema in the YAML binding (§5) or Field Reference (§10). At 6,000 pebbles, queries like "all pebbles from Slack channel X" are impossible without structured source provenance.

## The Problem

The pebble I created had `source_id: "slack-C064EVBE0LR-1776271954.592609"` — a composite string that violates tidy data and fails the Luhmann Test. A stranger can't parse that. The index can't facet on it.

## The Solution: Hierarchical Templates (defuddle-inspired)

Defuddle solves the same problem for web content: each site (YouTube, Reddit, GitHub, etc.) gets a dedicated extractor that knows what structured metadata that source provides. A `BaseExtractor` defines the interface; site-specific extractors implement it.

Pebbles templates follow the same pattern with hierarchical stacking:

```
00-base.json     ← Spec-required fields (ULID, created_at, pebble_type)
01-org.json      ← Org defaults (global-real-estate, BIA team)
10-{app}.json    ← App-specific source provenance (slack, email, web, meeting, terminal)
```

Templates stack via `extends` and numeric priority. Lower numbers apply first. App templates are pattern-matched by `source_app` or `url_pattern`.

### Key Design Decision: `source` as a Structured Block

Instead of flat fields (`source_app`, `source_id`), a single `source` object holds all provenance:

```yaml
source:
  app: slack
  workspace: amzn-fgbs
  channel_id: C064EVBE0LR
  channel_name: kiro-cli-internal-software-builders
  thread_ts: "1776271954.592609"
```

Every subfield is red-string-eligible. `source.app: slack` connects all Slack pebbles. `source.channel_name` connects all pebbles from a channel. JSONB GIN handles this natively.

### Spec Impact

The following should be added to the spec:

1. **§5 YAML Binding** — Add `source` as a top-level structured field with `app` required and app-specific subfields as fluid schema
2. **§10 Field Reference** — Add `source.app` controlled vocabulary: `slack | email | web | screenshot | meeting | terminal | notes | calendar`
3. **§10 Field Reference** — Add `people` array with `{alias, name, role, is_bot}` shape
4. **§10 Field Reference** — Add `device` object with `{os, arch, version}` shape
5. **§3.1 Ingestion Contract** — Reference the template system as the mechanism for Tier 1-3 auto-capture

### Template Location

`~/.pebbles/templates/` — user-level config, read by CLI, skills, hooks, and agents.

### File Naming Convention (codified)

```
{stub}-{ULID}-{DDMMMYY}-{HHMMSS}.md
```

Stored in `_pebbles/{YYYY}/{MM}/{DD}/` hierarchy.

## What This Enables

- At 6,000 pebbles: `source.app: slack` → instant filter to all Slack pebbles
- `source.channel_name: kiro-cli-internal-software-builders` → all pebbles from that channel
- `org: global-real-estate` + `team: BIA` → automatic org context without user effort
- `people[].alias: lujackso` → all pebbles involving a person
- Templates are the ingestion guardrails the spec references but never defines

## Files Created

- `~/.pebbles/templates/00-base.json` — global base
- `~/.pebbles/templates/01-org.json` — org defaults
- `~/.pebbles/templates/10-slack.json` — Slack provenance
- `~/.pebbles/templates/10-email.json` — email provenance
- `~/.pebbles/templates/10-web.json` — web/defuddle provenance
- `~/.pebbles/templates/10-meeting.json` — meeting provenance
- `~/.pebbles/templates/10-terminal.json` — terminal/CLI provenance
- `~/.pebbles/README.md` — template system documentation
