# Pebbles CLI — Technical Specification

**Audience:** Sr. Software Development Engineer
**Date:** 2026-04-16
**Spec version:** 0.3.0-draft → Phase 1 CLI
**Status:** Seed for design loop run

---

## TL;DR

Build the first reference implementation of the Pebbles schema as a CLI. The template system is the shared core — the same templates drive the CLI, the browser extension (pebble-clipper), and the Kiro skill (pebble-capture). Three logical components: schema+templates (shared), core (file I/O), cli (user surface). No daemon, no server, no Postgres yet — just files in, validated pebbles out.

The spec has been through 42 iterations of research. It is stable at v0.3.0-draft. This doc tells you what to build, not what Pebbles is.

---

## Architecture: Templates Are the Shared Core

The key insight from the template system design (15 APR 2026): the ingestion contract is the same regardless of capture surface. A pebble from Slack should look identical whether captured via CLI, browser extension, or Kiro skill.

```
                    ┌──────────────────────────┐
                    │  ~/.pebbles/templates/    │
                    │                          │
                    │  00-base.json            │
                    │  01-org.json             │
                    │  10-slack.json           │
                    │  10-email.json           │
                    │  10-web.json             │
                    │  10-meeting.json         │
                    │  10-terminal.json        │
                    └──────┬───────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │   CLI    │ │ Browser  │ │  Kiro    │
        │ pebble   │ │ pebble-  │ │ pebble-  │
        │ create   │ │ clipper  │ │ capture  │
        └──────────┘ └──────────┘ └──────────┘
              │            │            │
              └────────────┼────────────┘
                           ▼
                    ┌──────────────────┐
                    │  Schema Validator │
                    │  (shared library) │
                    └──────────────────┘
```

Three surfaces, one template system, one validator. The templates and validator are the shared code. Everything else is surface-specific.

### Template Stacking

Templates stack via `extends` and numeric priority. Lower numbers apply first, later overrides earlier:

```
00-base.json     ← Spec-required fields (ULID, created_at, pebble_type)
01-org.json      ← Org defaults (team, org context)
10-{app}.json    ← App-specific source provenance (slack, email, web, meeting, terminal)
```

App templates are pattern-matched by `source_app` or URL pattern. This is the mechanism for Tier 1–3 auto-capture from the spec's ingestion contract (§3.1).

### The `source` Block

Instead of flat fields, a structured `source` object holds all provenance:

```yaml
source:
  app: slack
  workspace: amzn-fgbs
  channel_id: C064EVBE0LR
  channel_name: kiro-cli-internal-software-builders
  thread_ts: "1776271954.592609"
```

Every subfield is red-string-eligible. `source.app: slack` connects all Slack pebbles. JSONB GIN handles nested objects natively.

---

## What You're Building

### Component 1: Schema + Templates (shared library)

The shared core consumed by all three surfaces.

**Schema validator:**
- Formal type definitions for the v0.3 YAML binding
- Per-field type constraints and controlled vocabulary enforcement
- Temporal field rule: full ISO 8601 with timezone required, date-only rejected (§5.1)
- (label, uid) cross-reference shape validation (§5.2)
- Unknown field preservation on round-trip (§12.3) — non-negotiable for viral adoption
- Structured error reporting (not just pass/fail)

**Template engine:**
- Load templates from `~/.pebbles/templates/`
- Hierarchical stacking: base → org → app (numeric priority)
- URL pattern matching for app template selection
- Template variable interpolation
- Default value application with user-override support

**Language choice is yours.** The spec is a file format — the validator can be written in any language. The constraint: the browser extension (pebble-clipper) and defuddle fork are JavaScript/TypeScript. If you choose a different language for the CLI, the template JSON format and `~/.pebbles/templates/` directory are the shared contract — not shared code. The schema rules are identical regardless of implementation language.

### Component 2: Core (file I/O)

- Read/write `pebble.md` (Tier 1): Markdown + YAML frontmatter parse/serialize
- Read/write `.pebble` (Tier 2): EPUB-style zip container (`mimetype` first entry, uncompressed)
- ULID generation: 26 chars, Crockford Base32, monotonic within same millisecond
- Edge storage: `edges.jsonl` for Phase 1 (one JSON object per line; migrates to Postgres in Phase 2)

### Component 3: CLI (user surface)

```bash
# Create from artifact — template auto-selected by source_app or URL
pebble create screenshot.png --title "Q3 revenue discrepancy" \
  --type experience_capture --emotion surprise --intent act_on \
  --modality kinetic --tags "finance,meeting"

# Create from Slack URL — 10-slack.json template auto-applied
pebble create --url "https://amzn-fgbs.slack.com/archives/C064EVBE0LR/p1776271954592609" \
  --emotion anticipation --intent act_on

# Pure text pebble
pebble create --note "Kevin's reply confirmed the triad" --type insight

# Validate
pebble validate my-pebble.md
pebble validate ./vault/ --recursive

# Link pebbles (typed edge)
pebble link 01HZJ...CDE 01HZJ...FGH --type derived_from

# List templates
pebble templates list

# Export (Phase 3 stub)
pebble export my-screenshot.pebble --native
```

**Programmatic API:** Same operations exposed as functions. This is the surface agents call — must mirror CLI 1:1.

---

## How Templates Connect to Defuddle

The browser extension (pebble-clipper) forks defuddle for content extraction. Defuddle's site-specific extractors (Twitter, YouTube, Reddit, GitHub, etc.) map directly to template-driven source provenance:

```
User clicks capture in browser
        ↓
defuddle extracts content + metadata (Tier 1 auto-capture)
        ↓
pebble-clipper matches URL → loads 10-web.json template
        ↓
Template populates source block from defuddle metadata
        ↓
User fills Tier 2 fields (emotion, intent) in popup
        ↓
Schema validator checks the result
        ↓
pebble.md written to vault
```

The CLI does the same flow without defuddle — it reads the artifact directly and applies the matched template. The Kiro skill does the same flow using MCP tools for source extraction. Three paths, same template contract, same validator.

---

## Decisions Already Made (Don't Re-litigate)

Ratified 2026-04-13. Full list in `.sop/cold-start.md`.

| Decision | Rationale |
|----------|-----------|
| ULID for pebble_id | Time-sortable, no prefix, Crockford Base32 |
| Plutchik 8 (not Ekman) | 3 bits entropy, sweet spot for capture-time cognitive load |
| Direct CLI, no daemon | Phase 1–2 simplicity; daemon reconsidered Phase 3 |
| Layer-based conformance | No Reader/Writer/Full taxonomy |
| consolidation_level derived | Not in YAML; computed from edge topology at query time |
| Capture-immutable + curator-editable | Body and capture metadata frozen; tags/edges/lifecycle freely edited |
| System never auto-tombstones | Archive yes (policy-driven); tombstone/delete = user only |
| Templates at `~/.pebbles/templates/` | User-level config, shared across all surfaces |
| `source` as structured block | Not flat fields; every subfield red-string-eligible |

---

## What's NOT in Phase 1

- Postgres indexer / red-string query engine (Phase 2)
- Browser extension / pebble-clipper / defuddle fork (Phase 3)
- LoCoMo eval framework (Phase 4)
- §7 weighting model rewrite (post-v1)
- SAGE/ByteRover integration (non-normative, Appendix G)

---

## Assumptions (ASM-)

ASM-001: No network calls in any component — fully offline, sovereign
ASM-002: Edge storage is `edges.jsonl` in Phase 1; migrates to Postgres in Phase 2
ASM-003: The spec at `_specs/pebbles.spec.md` is frozen for Phase 1
ASM-004: Template JSON format is the shared contract between CLI, browser extension, and skill
ASM-005: Implementation language is the builder's choice — the file format and template directory are the interop layer

## Constraints (CON-)

CON-001: Zero LLM dependency in Layers 1–3 — the single most important architectural contract
CON-002: Unknown YAML keys must round-trip without data loss (§12.3)
CON-003: All temporal fields require full ISO 8601 with timezone — reject date-only
CON-004: `.pebble` zip must have `mimetype` as first uncompressed entry
CON-005: Templates at `~/.pebbles/templates/` — all surfaces read from the same directory
CON-006: `source` block is structured, not flat — every subfield must be individually queryable

## Requirements (REQ-)

REQ-001: `pebble create` produces a valid `pebble.md` or `.pebble` from any input artifact
REQ-002: `pebble create --url <slack_url>` auto-selects `10-slack.json` template and populates `source` block
REQ-003: `pebble validate` returns structured errors with field paths, not just pass/fail
REQ-004: Programmatic API mirrors CLI 1:1 — agents call the same functions
REQ-005: Schema validator is a standalone component — usable without core or CLI
REQ-006: Template stacking is deterministic: base → org → app, numeric priority, later overrides earlier
REQ-007: Default templates ship with the CLI; user templates in `~/.pebbles/templates/` override defaults

## Invariants (INV-)

INV-001: Files are source of truth — any future index is a derived, rebuildable cache
INV-002: One pebble = one idea + one artifact reference (atomic to a single idea)
INV-003: Red strings are computed, never stored — matching YAML key-values = automatic connection
INV-004: Capture-immutable fields never change after creation
INV-005: The template system is the ingestion contract — all surfaces produce identical pebbles for identical inputs

---

## How to Run the Design Loop

Your approach: initial condition → differential function → integrate in a loop.

**Initial condition:** This spec + `_specs/pebbles.spec.md` + `.sop/cold-start.md` + `_discussions/pebble-templates-design-15APR26.md`

**Differential function per iteration:**
1. Pick the next unimplemented item from Phase 1 in `TODO.md`
2. Implement it
3. Run `pebble validate` against the example pebble in spec §13
4. Check: does the round-trip preserve unknown keys?
5. Check: does template stacking produce correct output?
6. Update `TODO.md`, commit

**Integration test:** Create 5 real pebbles from different sources (Slack, web, terminal, note, meeting). Validate all. Verify each used the correct app template. Link two with `derived_from`. If all pass, Phase 1 is done.

---

## References

| Doc | Path | What it gives you |
|-----|------|-------------------|
| The spec | `_specs/pebbles.spec.md` | Source of truth for schema, architecture, field reference |
| Cold start | `.sop/cold-start.md` | Reading order, ratified decisions, deferred items |
| Templates design | `_discussions/pebble-templates-design-15APR26.md` | Template system architecture, `source` block design |
| Pebble-capture skill | `plugins/pebble-capture/skills/pebble-capture/SKILL.md` | How the Kiro skill uses templates |
| Defuddle investigation | `.sop/synthesis/05-defuddle-investigation.md` | Fork strategy, integration points |
| Clipper investigation | `.sop/synthesis/06-obsidian-clipper-investigation.md` | Browser extension architecture |
| TODO | `TODO.md` | Phase 1 checklist |
| No-Escape summary | `.sop/synthesis/01-no-escape-theorem-summary.md` | Why red strings work (b=0, FA=0) |

---
