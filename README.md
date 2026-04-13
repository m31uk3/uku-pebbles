# Pebbles

**The AGENTS.md for knowledge work.**

I believe there's an overlooked yet powerful primitive for capturing human memories. By adding YAML frontmatter (metadata) to the top of Markdown files, we can encode any action's intent (ontology) and significance (meaning) inside a single atomic **Pebble** — a Universal Knowledge Unit (UKU).

Connect pebbles that share matching metadata and you can reconstruct your lived experiences with zero LLM calls — just basic similarity search.

## The Vision

Pebbles is a schema specification for universal knowledge. By weaving pebbles into your everyday tools (web browser, smartphone, notes app, etc.), every "moment" — screenshot, note, tweet, photo, idea — becomes its own atomic UKU.

Each pebble is unique to its moment. It captures not only *what happened* but the lived experiential context: emotional state, surrounding activity, and intent.

A pebble is not the artifact itself — it's a **structured description** that makes any artifact discoverable and associable. Just as AGENTS.md describes a codebase to an agent, a pebble adds the lived experiential context for the artifact it wraps. The body text is a human/agent-written summary. The frontmatter is the experiential index.

Inspired by the insight that "the simplest forms of memory work best," Pebble Piles are the digital equivalent of an evidence board. Every pebble is an item pinned to the wall; every matching YAML key-value pair is a string connecting them.

Because retrieval is interference-immune, Pebbles forgets when you want it to — not when geometry forces it to.

## Architecture

Four clearly bounded layers:

```
  Ingestion ─── Deterministic extraction. Zero LLM.
      │         Parse YAML, normalize, write to index.
      ▼
  Curation ──── Actor-agnostic (human or agent, RBAC-governed).
      │         Create edges, consolidate, build higher-order structures.
      ▼
  Query ──────── Pure deterministic retrieval. Red strings + optional edge traversal.
      │          No LLM. No embeddings. Just SQL.
      ▼
  Inference ──── Optional. Separate process. Receives structured results only.
                 LLM reasoning, synthesis, suggestions.
```

Layers 1–3 are **compile-time LLM-free**. The boundary between deterministic core and inference is the single most important architectural contract.

### Relationships

- **Red strings** — Implicit, symmetric connections from matching YAML key-value pairs. Orthogonal facet axes (`emotional_state`, `intent`, `modality`, `memory_kind`) compound to give 192+ combinations from four fields. Powered by JSONB + GIN index. Sub-millisecond compound faceted search.
- **Ontology governance** (optional) — Every pebble may link to one or more ontology pebbles via `governed_by`, anchoring its claims against ground-truth structures that agents can traverse for fact verification. Inspired by Palantir Foundry's Object Type model.
- **Typed edges** (optional, additive) — Explicit, directional relationships in a lightweight table. Created only during curation. Enables consolidation hierarchy (L0 raw → L1 consolidations → L2 Maps of Content → L3+ meta-syntheses) — operationalizing the Zettelkasten method (Luhmann 1952) and Complementary Learning Systems (McClelland 1995).

The system works fully with red strings alone. Typed edges are a progressive enhancement that never breaks core functionality.

### Ingestion Contract

| Tier | Source | Friction | Examples |
|------|--------|----------|----------|
| 1 | Auto-captured from device/browser | Zero | timestamp, device, GPS, active_url, file_ref, content_hash |
| 2 | Human moment (mini-tweet + quick-tag) | 3–5 seconds | intent, emotional_state, modality, people, tags |
| 3 | Inferred without LLM | Zero | venue_type from GPS, source_type from file extension |
| 4 | LLM-assisted inference (async) | Zero | Optimal attribute assignment using payload + existing index |

### Storage

- **Source of truth**: Plain Markdown + YAML files (sovereign, human-editable, Git versioned)
- **Index**: Postgres + JSONB (single table, single GIN index)
- **Edges**: Optional lightweight table for typed relationships
- **Implementation notes**: Full JSONB + GIN feasibility documented in the spec (WIP)

## v1 Scope

**Capture surfaces:**
- **Chrome extension** — Explicit capture on button click / hotkey. Defuddle-quality content extraction. Quick-tag overlay for the "pebble moment."
- **System-level screenshot override** — Replaces OS default. Auto-generates pebble with Tier 1–3 frontmatter.

**Discovery surfaces:**
- **Obsidian vault** — Pebbles appear as `.md` files with full frontmatter. Native integration.
- **Pebbles dashboard** — Web-based graph view served by the local index. Red strings visualized as connections. Filterable by any attribute.

**Capture UX** — Three modes (user preference):
1. **Silent** — System captures what it can. No UI.
2. **Minimal** — 3 inputs + emoticon picker + location dropdown. Seconds, not minutes.
3. **Full** — All available values surfaced for review/edit.

Collapsible drill-down — start at your level, go deeper when desired.

*Download our beta client for Google Chrome and start pebble-piling today.*

## Full Specification

[`_specs/pebbles.spec.md`](./_specs/pebbles.spec.md)

## Repository Structure

```
├── _specs/          # Pebbles schema specification (v0.3.0-draft)
├── _discussions/    # Raw origin conversations (unedited)
├── _insights/       # Synthesis and analysis
├── _research/       # Architecture, design research, PDD artifacts
└── README.md
```

## License

MIT
