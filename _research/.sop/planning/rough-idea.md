# UKU Pebbles: Functional & Non-Functional Requirements

## 1. Functional Requirements

### Core Primitive – The Pebble (UKU)

Every Pebble is an atomic Universal Knowledge Unit: a Markdown file containing YAML frontmatter (metadata) plus optional body text.

The system deterministically extracts, normalizes, and stores the YAML hierarchy for every Pebble.

A fluid schema mechanism allows new fields to start as fleeting (prose, full-text searchable only) and graduate to permanent/graph-eligible status after meeting frequency, convergence, and approval criteria.

### Relationship Model

**Red strings:** Implicit, symmetric, attribute-based connections created by exact matching on permanent YAML key-value pairs. Powered by a single JSONB column and GIN index for compound, sub-millisecond faceted search.

**Typed edges (optional and additive):** Explicit, directional, typed relationships stored in a lightweight table. Edges are created only during curation (by humans or agents) and support multi-hop traversal via standard SQL.

The system works fully with red strings alone; typed edges are a progressive enhancement that never breaks core functionality.

### Architecture

Four clearly bounded layers:

1. **Ingestion:** Deterministic, zero-LLM metadata extraction and normalization from any source (browser, phone, notes app, Obsidian, screenshots, tweets, photos, etc.).
2. **Curation:** Actor-agnostic interface shared by humans and agents for creating edges, performing consolidations, and building higher-order structures.
3. **Query:** Pure deterministic retrieval returning structured results (red-string matches + typed-edge traversals).
4. **Inference:** Optional separate process that receives only structured Query results and applies LLM reasoning or synthesis.

### Higher-Order Structures

Level-0 raw Pebbles → Level-1 consolidations → Level-2 Maps of Content (MOCs) → Level-3+ meta-syntheses, all linked explicitly via typed edges when desired.

### Everyday Use

- Seamless ingestion from everyday tools via YAML frontmatter.
- "Pebble Piles" / evidence-board experience: red strings visually connect matching metadata; typed edges add labeled, directional connections.
- Zero LLM required for basic retrieval and similarity search.

### Graceful Degradation

The system remains fully functional if Inference or the typed-edges table is unavailable.

## 2. Non-Functional Requirements

### Simplicity & Minimum Components

- Single Postgres instance with one primary table (JSONB + GIN index) and one optional edges table.
- No graph database, no vector store, and no additional services required in the deterministic core.
- Layers 1–3 are guaranteed LLM-free at compile time.

### Performance & Scale

- Sub-millisecond red-string queries and ≤5-hop traversals at personal scale (<100k Pebbles).
- Linear scaling with pebble count; index maintenance is automatic and low-cost.

### Reliability & Auditability

- All core operations are deterministic, transactional, and auditable.
- Human vs. agent actions are clearly distinguished.

### Extensibility

- Fluid schema graduation for new permanent fields.
- Typed edges can be added later without refactoring the core.
- Semantic features (embeddings) are confined to the optional Inference layer.

### User Experience & Vision Alignment

- Realizes the pitch: "zero LLM calls — just basic similarity search" for core use.
- Preserves the conspiracy-board / pebble-pile metaphor through red strings + optional labeled edges.
- Works natively with existing Markdown/Obsidian workflows.

### Security & Privacy

- Designed local-first and personal-scale (Postgres runs on laptop or Raspberry Pi).
- Full user control over data; no external calls required for core functionality.

## Appendix

### Luhmann Test

A field is permanent (graph-eligible, red-string eligible) if its value is understandable without the context in which it was written. A stranger should be able to read the value and know what it means.

### Ekman 8 (for emotional_state)

Controlled vocabulary used to atomize the emotional_state field into permanent/graph-eligible values:

`joy`, `sadness`, `anger`, `fear`, `surprise`, `disgust`, `trust`, `anticipation`

### Graph-Eligible Fields

Fields whose values pass the Luhmann Test and are therefore eligible for red-string matching and/or typed edges:

- `uku_type` — experience_capture, insight, problem_statement, proposed_solution, ontology_element
- `category` — foundational, vision, technical, insight, problem
- `status` — draft, annotated, published, archived
- `tags` — user-defined, lowercase
- `emotional_state` — atomized to Ekman 8
- `intent` / `intended_next_action` — atomized to: remember, act_on, share, think_about
- `location.city` — normalized
- `location.venue_type` — controlled vocabulary: home, office, coffee_shop, transit, outdoor, other

## Bibliography

- Mikey O'Brien. "Brain.md." Rho repository. https://github.com/mikeyobrien/rho/blob/main/docs/brain.md
- Obsidian Rocks. "Getting Started with Zettelkasten in Obsidian." https://obsidian.rocks/getting-started-with-zettelkasten-in-obsidian/
- UKU Pebbles RQ1 + RQ2 Analysis Artifact (27 MAR 2026). Internal design document.
