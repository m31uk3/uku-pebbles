# Pebbles CLI — Design Loop Runtime Seed

**Purpose:** Machine-readable specification for an iterative agent design loop that implements the Pebbles CLI.
**Consumer:** Agent running in loop mode (Kiro CLI, Claude Code, or equivalent)
**Date:** 2026-04-16
**Spec version:** 0.3.0-draft

---

## System Prompt Context

You are implementing the Pebbles CLI — the first reference implementation of the Pebbles schema specification. Pebbles is a sovereign personal memory format: Markdown files with YAML frontmatter that make human artifacts discoverable and associable without LLM calls.

The template system is the shared core. The same templates at `~/.pebbles/templates/` drive three capture surfaces: this CLI, a browser extension (pebble-clipper), and a Kiro skill (pebble-capture). Your implementation must produce identical pebbles to those surfaces for identical inputs.

Implementation language is your choice. The interop contract is the file format (pebble.md, .pebble zip), the template JSON format, and the `~/.pebbles/templates/` directory — not shared code.

---

## Source of Truth

Read these files before starting. They are authoritative. If this document conflicts with the spec, the spec wins.

```
MUST READ (in order):
1. _specs/pebbles.spec.md                                    — the schema spec, v0.3.0-draft
2. .sop/cold-start.md                                        — project state, ratified decisions
3. _discussions/pebble-templates-design-15APR26.md            — template system architecture
4. plugins/pebble-capture/skills/pebble-capture/SKILL.md      — how the Kiro skill uses templates
5. TODO.md                                                    — Phase 1 checklist (your work items)

REFERENCE (read sections as needed):
6. .sop/synthesis/05-defuddle-investigation.md                — browser extension extraction layer
7. .sop/synthesis/06-obsidian-clipper-investigation.md        — browser extension UI layer
8. .sop/synthesis/09-glossary.md                              — term definitions
```

---

## Project State

```yaml
phase: 1
spec_version: 0.3.0-draft
spec_status: frozen_for_phase_1
implementation_status: zero_code_written
implementation_language: builder_choice
template_system: designed_not_implemented
three_surfaces:
  cli: this_implementation
  browser: pebble-clipper (Phase 3, separate repo)
  skill: pebble-capture (exists at plugins/pebble-capture/)
shared_contract:
  templates: ~/.pebbles/templates/*.json
  schema: pebbles.spec.md v0.3 YAML binding
  file_format: pebble.md + .pebble zip
```

---

## Architecture

```
┌─────────────────────────────────────────────┐
│         ~/.pebbles/templates/               │
│                                             │
│  00-base.json   (spec-required fields)      │
│  01-org.json    (org defaults)              │
│  10-slack.json  (Slack source provenance)   │
│  10-email.json  (email source provenance)   │
│  10-web.json    (web/defuddle provenance)   │
│  10-meeting.json                            │
│  10-terminal.json                           │
│                                             │
│  Stacking: base → org → app                 │
│  Lower number = applied first               │
│  Later overrides earlier                    │
└──────────────┬──────────────────────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 ┌──────┐  ┌───────┐  ┌───────┐
 │ CLI  │  │Browser│  │ Kiro  │
 │      │  │Ext.   │  │ Skill │
 └──┬───┘  └───┬───┘  └───┬───┘
    │          │          │
    └──────────┼──────────┘
               ▼
      ┌────────────────┐
      │Schema Validator │
      └────────────────┘
               │
               ▼
      ┌────────────────┐
      │  pebble.md or  │
      │  .pebble zip   │
      └────────────────┘
```

### Three logical components

| Component | Responsibility | Shared? |
|-----------|---------------|---------|
| Schema + Templates | Validate pebbles. Load/stack templates. Apply defaults. | Yes — all surfaces use same templates and rules |
| Core | File I/O: parse/write pebble.md, read/write .pebble zip, generate ULIDs | CLI-specific (browser has its own I/O) |
| CLI | User commands: create, validate, link, export. Programmatic API for agents. | CLI-specific |

---

## Template System Specification

### Template directory

`~/.pebbles/templates/` — user-level config. All surfaces read from here.

### Stacking rules

1. Load all `*.json` files from template directory
2. Sort by numeric prefix ascending: `00-*` before `01-*` before `10-*`
3. Apply in order: each template's fields override previous values
4. App templates (`10-*.json`) are only applied when `source_app` or URL pattern matches

### App template matching

| Pattern | Template |
|---------|----------|
| `*.slack.com/*` | `10-slack.json` |
| Email conversation ID present | `10-email.json` |
| `https://*` (general web) | `10-web.json` |
| Meeting context | `10-meeting.json` |
| Terminal/CLI context | `10-terminal.json` |

### The `source` block

Templates populate a structured `source` object — not flat fields:

```yaml
# 10-slack.json produces:
source:
  app: slack
  workspace: string        # from URL
  channel_id: string       # from URL path
  channel_name: string     # from channel metadata
  thread_ts: string        # from URL

# 10-email.json produces:
source:
  app: email
  provider: string         # outlook, gmail
  subject: string
  from: string
  to: [string]
  conversation_id: string
  message_id: string

# 10-web.json produces:
source:
  app: web
  domain: string
  url: string
  author: string
  published: string        # ISO 8601
```

Every subfield is individually queryable via JSONB GIN. `source.app: slack` is a red string connecting all Slack pebbles.

### `source.app` controlled vocabulary

`slack | email | web | screenshot | meeting | terminal | notes | calendar`

---

## Schema Specification (Machine-Readable Extract)

### Required fields

| Field | Type | Constraint |
|-------|------|-----------|
| `title` | string | min length 1 |
| `pebble_id` | string | ULID: exactly 26 chars, Crockford Base32 `^[0-9A-HJKMNP-TV-Z]{26}$` |
| `created_at` | string | Full ISO 8601 with timezone. REJECT `2027-01-01`. ACCEPT `2027-01-01T00:00:00Z`. |
| `pebble_type` | enum | `experience_capture \| insight \| problem_statement \| proposed_solution \| reference \| ontology` |

### Optional controlled vocabularies

| Field | Values |
|-------|--------|
| `memory_kind` | `episodic \| semantic \| procedural` |
| `modality` | `kinetic \| non_kinetic` |
| `emotional_state` | `joy \| sadness \| anger \| fear \| surprise \| disgust \| trust \| anticipation` |
| `intent` | `remember \| act_on \| share \| think_about` |
| `category` | `foundational \| vision \| technical \| insight \| problem` |
| `status` | `draft \| active \| annotated \| published \| archived \| tombstoned \| superseded` |
| `venue_type` | `home \| office \| coffee_shop \| transit \| outdoor \| other` |
| `source.app` | `slack \| email \| web \| screenshot \| meeting \| terminal \| notes \| calendar` |

### Cross-reference shape

```yaml
governed_by:
  - label: string    # human-readable, diff-friendly hint
    uid: string      # ULID, authoritative
```

### Field mutability classes

**Capture-Immutable (never edit after creation):**
`pebble_id`, `created_at`, `body`, `url`, `source_id`, `content_hash`, `device`, `source_app`, `location` (if set at capture), `source` block

**Curator-Editable (mutable anytime, triggers reindex):**
Everything else: `pebble_type`, `memory_kind`, `emotional_state`, `intent`, `modality`, `tags`, `topic`, `category`, `governed_by`, `status`, `pin`, `archive_at`, `protected`, all typed edges

### Lifecycle states

```
draft → active → annotated → published → archived → tombstoned
                                                         ↓
                                                    (hard delete — user only, irreversible)
```

System MAY auto-archive. System MUST NOT auto-tombstone or auto-delete.

---

## Validation Rules

### Pass criteria for `pebble validate`

```
PASS if:
  ✓ Required fields present and correctly typed
  ✓ pebble_id matches ULID format
  ✓ created_at is full ISO 8601 with timezone (not date-only)
  ✓ All controlled vocabulary values are valid enum members
  ✓ governed_by entries have both label (string) and uid (ULID)
  ✓ source.app (if present) is in controlled vocabulary
  ✓ Unknown YAML keys are preserved (not stripped)

FAIL if:
  ✗ Any required field missing
  ✗ pebble_id is not valid ULID
  ✗ Any temporal field is date-only
  ✗ Controlled vocabulary field has invalid value
  ✗ governed_by entry missing label or uid
```

### Round-trip test

```
1. Parse pebble.md with unknown keys (e.g., custom_field: "hello")
2. Serialize back to YAML
3. Assert: custom_field is present and unchanged
4. Assert: field ordering is preserved (best effort)
```

### Template stacking test

```
1. Load 00-base.json (sets pebble_type: experience_capture)
2. Load 01-org.json (sets org: "my-org", team: "my-team")
3. Load 10-slack.json (sets source.app: slack, memory_kind: episodic)
4. Assert: final merged result has all three layers applied
5. Assert: 10-slack.json values override 00-base.json where they conflict
```

---

## Test Fixtures

### Golden pebble (from spec §13, extended with source block)

```yaml
---
title: "SAGE + ByteRover alignment moment"
pebble_id: 01HZJ3K8P7M4R5VYX2W9NQBCDE
created_at: 2026-03-21T08:12:00Z
url: "https://x.com/kevinnguyendn/status/2035366573192753648"
source_id: "tweet-1234567890"
pebble_type: insight
memory_kind: semantic
modality: non_kinetic
category: vision
emotional_state: joy
intent: act_on
source:
  app: web
  domain: x.com
  url: "https://x.com/kevinnguyendn/status/2035366573192753648"
  author: kevinnguyendn
governed_by:
  - label: pebbles-roadmap
    uid: 01HZJ3K8P7M4R5VYX2W9NQBCFG
  - label: triad-architecture
    uid: 01HZJ3K8P7M4R5VYX2W9NQBCHJ
context_elements:
  why_captured: "Kevin just replied – this is the exact triad"
  surrounding_activity: "Reading X thread while drinking coffee"
location:
  city: "kuala lumpur"
  venue_type: coffee_shop
tags:
  - pebbles
  - sage
  - byterover
  - interspecies
status: draft
weight: 0.85
---
This feels like perfect timing!

You've both basically built the runtime infrastructure for the schema spec
I've been drafting all week...
```

### Invalid pebble (should fail validation)

```yaml
---
title: ""
pebble_id: not-a-ulid
created_at: 2026-03-21
pebble_type: invalid_type
emotional_state: happy
source:
  app: tiktok
governed_by:
  - label: missing-uid
---
Body text.
```

Expected errors:
- `title`: empty string
- `pebble_id`: not ULID format
- `created_at`: date-only, missing time and timezone
- `pebble_type`: not in controlled vocabulary
- `emotional_state`: "happy" not in Plutchik 8 (should be "joy")
- `source.app`: "tiktok" not in controlled vocabulary
- `governed_by[0]`: missing `uid` field

### Slack pebble (template-driven)

```yaml
---
title: "Collaborator offers CLI design loop run"
pebble_id: 01JSGK8P7M4R5VYX2W9NQBCXY
created_at: 2026-04-16T20:37:49Z
pebble_type: experience_capture
memory_kind: episodic
modality: kinetic
emotional_state: anticipation
intent: act_on
source:
  app: slack
  workspace: example-workspace
  channel_id: D0A7A4RBY7Q
  channel_name: "DM with collaborator"
  thread_ts: "1776371869.891609"
people:
  - alias: jdoe
    name: Jane Doe
    role: Sr. Software Dev Engineer
    is_bot: false
tags:
  - pebbles
  - cli
  - design-loop
status: active
---
"You need a cli design research loop run?"

Collaborator volunteered to run their iterative agent design loop on the Pebbles CLI.
```

---

## Typed Edges (Phase 1 Storage)

Phase 1 stores edges in `edges.jsonl` (one JSON object per line). Phase 2 migrates to Postgres.

```jsonl
{"source_id":"01HZJ...CDE","target_id":"01HZJ...FGH","edge_type":"derived_from","created_by":"user","created_at":"2026-04-16T14:00:00Z"}
```

Valid edge types: `derived_from`, `contains`, `governed_by`, `supports`, `contradicts`, `supersedes`, `co_occurred_with`

---

## File Naming Convention

```
{stub≤20}-{ULID}-{DDMMMYY}-{HHMMSS}.md
```

Stored in `{vault_path}/_pebbles/{YYYY}/{MM}/{DD}/` hierarchy.

Example: `alex-cli-loop-01JSGK8P7M4R5VYX2W9NQBCXY-16APR26-203749.md`

---

## Iteration Protocol

```
1. READ    — Check TODO.md for next uncompleted Phase 1 item
2. PLAN    — Identify files to create/modify, dependencies
3. BUILD   — Implement the item
4. TEST    — Run tests in the affected component
5. VERIFY  — Validate golden pebble + template stacking test + round-trip test
6. COMMIT  — Stage, commit with descriptive message
7. UPDATE  — Mark item complete in TODO.md
8. REPEAT  — Go to step 1
```

### Iteration ordering (dependency graph)

```
1. Project scaffold (build system, directory structure)
2. Schema validator (type definitions, controlled vocabularies, temporal rules)
3. Template engine (loader, stacking, URL pattern matching)
4. Core: pebble.md parser/writer + ULID generation
5. Core: .pebble zip reader/writer
6. CLI: create command (with template auto-selection)
7. CLI: validate command
8. CLI: link command + edges.jsonl
9. CLI: templates list command
10. CLI: programmatic API surface
11. Integration test: 5 pebbles from different sources, all template-driven
```

---

## Hard Constraints

```
MUST:
  - All components work offline (zero network calls)
  - Unknown YAML keys round-trip without data loss
  - Temporal fields reject date-only values
  - ULID generation is monotonic within same millisecond
  - .pebble zip has mimetype as first uncompressed entry
  - Programmatic API mirrors CLI commands 1:1
  - Templates load from ~/.pebbles/templates/
  - Template stacking is deterministic (numeric prefix ordering)
  - source block is structured (not flat fields)
  - All tests pass before committing

MUST NOT:
  - Import any LLM SDK or embedding library
  - Modify _specs/pebbles.spec.md
  - Add a daemon, server, or HTTP endpoint
  - Auto-tombstone or auto-delete pebbles
  - Strip unknown YAML keys during parse/serialize
  - Use date-only values in any temporal field
  - Hardcode source provenance — it comes from templates
```

---

## Completion Criteria

Phase 1 is complete when:

```
[ ] Project builds and all tests pass
[ ] Schema validator accepts golden pebble from spec §13
[ ] Schema validator rejects invalid pebble fixture with correct errors
[ ] Template engine loads and stacks 00-base → 01-org → 10-slack correctly
[ ] pebble create --url <slack_url> auto-selects 10-slack.json template
[ ] pebble create --note "text" --type insight produces valid pebble.md
[ ] pebble validate accepts/rejects correctly
[ ] pebble link writes to edges.jsonl
[ ] Round-trip test: parse → serialize → parse produces identical output
[ ] 5 real pebbles from different sources (slack, web, terminal, note, meeting)
[ ] All 5 used correct app template automatically
[ ] Programmatic API: createPebble(), validatePebble(), linkPebbles() all work
```

---

## Context Window Management

This document is ~450 lines. The spec is ~900 lines. Together they fit in a single context load.

If context degrades (canary: agent stops following constraints), start a new session with:
1. This file (the seed)
2. `_specs/pebbles.spec.md` §1–§6
3. `_discussions/pebble-templates-design-15APR26.md`
4. `TODO.md`

Do not load the full spec on every iteration — load §5 (YAML binding) and §10 (field reference) as needed.

---

## Provenance

This seed was generated from:
- Pebbles spec v0.3.0-draft (`_specs/pebbles.spec.md`)
- Template system design (`_discussions/pebble-templates-design-15APR26.md`)
- Pebble-capture skill (`plugins/pebble-capture/skills/pebble-capture/SKILL.md`)
- Defuddle investigation (`.sop/synthesis/05-defuddle-investigation.md`)
- Obsidian-clipper investigation (`.sop/synthesis/06-obsidian-clipper-investigation.md`)
- 42-iteration research artifact (design loop output, March 2026)
- No-Escape Theorem synthesis (`nova-memory/no-escape-nova-pebbles-deep-research.md`)
- Git log: 28 commits through v0.3.0-draft + pebble-capture skill
- Slack persona analysis: 256 messages across #amazon-builder-genai-power-users, #kiro-cli-internal-software-builders
