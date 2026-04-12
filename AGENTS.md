# AGENTS.md

AI Coding Assistant Context for uku-pebbles

## Quick Start

This is a **design specification and research repository** for UKU-Pebbles -- a schema for Universal Knowledge Units that makes any human artifact discoverable and associable by encoding experiential context as YAML frontmatter in Markdown files. There is no executable code. All 20 files are Markdown.

**The key idea:** A pebble is not the artifact itself -- it's a **descriptor** that wraps an artifact with lived experiential context (intent, emotional state, surrounding activity). Just as AGENTS.md describes a codebase to an agent, a pebble describes an artifact to both humans and agents.

**The triad:** UKU-Pebbles is one of three projects:
- **UKU-Pebbles** (this repo) -- schema + capture format
- **SAGE** -- BFT consensus validation (prevents memory drift)
- **ByteRover** -- selective retrieval (.brv/context-tree)

**Current phase:** Spec v0.2.3 (Active Draft). No implementation yet.

**Start here:** Read `README.md` for vision, then `_specs/uku-pebbles.spec.md` for the full spec, then `TODO.md` for open work.

## Project Structure

```
uku-pebbles/
├── README.md                          # Vision, architecture overview, v1 scope
├── TODO.md                            # Comprehensive open work items
├── LICENSE                            # Apache 2.0
├── AGENTS.md                          # This file
│
├── _specs/
│   └── uku-pebbles.spec.md           # THE spec: schema, architecture, relationships,
│                                      # weighting, storage, field reference, examples
│
├── _discussions/                      # Raw origin conversations (unedited)
│   ├── uku-pebbles-luke-aaron-box-21MAR26.md    # Levie "context is king" + Luke reframe
│   ├── uku-pebbles-sage-byte-rover-21MAR26.md   # Triad discovery X thread
│   ├── uku-pebbles-plain-summary-21MAR26-093348.md  # Accessible explainer
│   └── self-talk-runway-run-12APR26.md          # Rhetorical situation analysis
│
├── _insights/                         # Synthesis and analysis
│   ├── uku-pebbles-synthesis-21MAR26-081150.md       # Executive: ai-pebbles -> uku evolution
│   ├── uku-pebbles-deep-synthesis-21MAR26-083058.md  # Technical: SAGE gaps, tidy data, HITM
│   └── uku-pebbles-readiness-gap-21MAR26-091233.md   # Strategic: what to keep vs delegate
│
├── _research/
│   ├── sage/                          # SAGE codebase summary (8 docs)
│   │   ├── index.md                   # Primary SAGE context
│   │   ├── architecture.md            # CometBFT, 2-store, ABCI
│   │   ├── components.md              # 13 packages
│   │   ├── data_models.md             # MemoryRecord, 19 tables
│   │   ├── interfaces.md              # 25+ REST, 15+ MCP tools
│   │   ├── workflows.md               # Consensus, voting, vault
│   │   ├── dependencies.md            # Go 1.23, CometBFT, PostgreSQL
│   │   └── review_notes.md            # Findings
│   ├── grok-debate-testing/           # Adversarial design stress-test
│   └── _papers/                       # Empty placeholder
│
├── _dependencies/                     # Empty placeholder
│
├── .claude/                           # Claude Code config
└── .sop/summary/                      # Generated documentation
```

## Key Concepts

### Pebble-as-Descriptor
A pebble wraps an external artifact (screenshot, tweet, PDF) with experiential context. The artifact lives elsewhere; the pebble points to it. Multiple pebbles can reference the same artifact. One pebble = one idea.

### Four-Layer Architecture
```
Ingestion ── Deterministic. Zero LLM. Parse YAML, normalize, index.
Curation ─── Actor-agnostic (human or agent, RBAC). Edges, consolidation.
Query ────── Deterministic. Red strings + edge traversal. No LLM.
Inference ── Optional. Separate. Receives structured results only.
```
Layers 1-3 are compile-time LLM-free. The system works fully without Layer 4.

### Red Strings
Implicit, symmetric connections from matching YAML key-value pairs. Computed on-demand from JSONB+GIN index. Nothing stored. Think conspiracy board: red strings appear wherever attributes match.

### Typed Edges
Optional, explicit, directional relationships. Progressive enhancement that never breaks red strings. Enables consolidation hierarchy: L0 raw -> L1 consolidations -> L2 MOCs -> L3+ meta-syntheses.

### Weighting Model
Three layers: explicit (human-set `weight` field) + implicit (access/update/reference counts, index-only) + effective (agent-computed combination).

### Four-Tier Ingestion
| Tier | Friction | Examples |
|------|----------|----------|
| 1 Auto-capture | Zero | timestamp, device, GPS, URL, content_hash |
| 2 Human moment | 3-5 sec | intent, emotional_state, tags |
| 3 Deterministic | Zero | venue_type from GPS, source_type from extension |
| 4 LLM-assisted | Zero (async) | Attribute assignment using payload + index state |

### UKU Schema (Required Fields)
```yaml
title: "Short title"
uku_id: "uku-YYYYMMDD-hexstring"
created_at: "2026-03-21T08:12:00Z"
uku_type: insight          # experience_capture|insight|problem_statement|proposed_solution|ontology_element
category: vision           # foundational|vision|technical|insight|problem
```

Optional: `url`, `source_id`, `emotional_state` (Ekman 8), `intent` (remember|act_on|share|think_about), `context_elements`, `location`, `tags`, `weight`, `status`

Fluid schema: any additional YAML key is valid.

## Relationship to ai-pebbles

This repo evolved from [ai-pebbles](../ai-pebbles/) (now abandoned). Key differences:

| ai-pebbles | uku-pebbles |
|-----------|-------------|
| Pebble = artifact + metadata | Pebble = descriptor wrapping artifact |
| Monolithic (7+ components) | 4 bounded layers + triad |
| Mixed LLM boundary | Compile-time LLM-free (Layers 1-3) |
| Typed links only | Red strings (implicit) + typed edges (optional) |
| Self-contained | Delegates to SAGE + ByteRover |
| 42 iterations, 16 docs, 271 .py scripts | 1 spec file, focused scope |

**What was kept:** Core thesis, ontological model, tidy data invariant, pre-attentive attributes, Ekman emotions, K-DAG edge taxonomy, privacy principles.

**What was delegated:** Validation (SAGE), retrieval (ByteRover), encryption (SAGE), agent execution (SAGE), sync (SAGE).

**What was dropped:** Consumer app architecture, economics, solo sync/search engines, operability dashboards, 14-month execution plan.

## The Triad

| Project | Responsibility | Status |
|---------|---------------|--------|
| UKU-Pebbles | Schema, capture format, experiential metadata | v0.2.3 spec draft |
| SAGE | BFT consensus, PoE scoring, RBAC, vault encryption | v5.0.7 production |
| ByteRover | Selective retrieval, .brv/context-tree, OpenClaw | Active development |

Integration not yet specified. See TODO.md "Integration" section for open items.

## Known Issues

1. **License discrepancy** -- README says MIT, LICENSE file is Apache 2.0
2. **Version numbering** -- Header says v0.2.3, changelog describes v2.1->v2.3
3. **11 missing fields** from ai-pebbles (people, tools, tasks, consent_snapshot, etc.)
4. **No validation rules** -- Per-field constraints, size limits, conformance levels not yet defined
5. **Tidy data violations** -- `context_elements.emotional_state` and `.intent` are prose, not atomized
6. **SAGE integration protocol** -- Conceptual flow exists, no detailed spec
7. **No performance budgets** -- All latency/memory targets are TODO items

## Working With This Repository

**Understanding the vision:** Read README.md then `_specs/uku-pebbles.spec.md`

**Understanding the triad:** Read `_discussions/uku-pebbles-sage-byte-rover-21MAR26.md` for the origin, then `_insights/uku-pebbles-deep-synthesis-21MAR26-083058.md` for technical analysis

**Understanding what changed from ai-pebbles:** Read `_insights/uku-pebbles-readiness-gap-21MAR26-091233.md`

**Understanding SAGE:** Read `_research/sage/index.md` then the specific area you need

**Understanding design trade-offs:** Read `_research/grok-debate-testing/` for the adversarial stress-test

**Finding open work:** Read TODO.md -- organized by Spec, Integration, Schema Integrity, Community, Research, Platform, Performance, UX

## Gotchas

- This is NOT ai-pebbles. The core model changed (descriptor vs artifact). Don't assume ai-pebbles architecture applies.
- The `_research/sage/` docs are a summary of an external codebase, not part of this project.
- The spec is a single file (`_specs/uku-pebbles.spec.md`), not 16 separate documents like ai-pebbles.
- "Red strings" are the primary relationship mechanism. Don't default to typed edges first.
- The fluid schema means ANY yaml key is valid. Don't reject unknown fields.
- The compile-time LLM boundary is the single most important architectural contract. Layers 1-3 must never depend on Layer 4.
