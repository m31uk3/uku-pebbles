**Pebbles UKU Specification v2.1**

**Universal Knowledge Unit – Format-Independent Schema for Sovereign Personal & Interspecies Memory**

**Version:** 0.2.1 (March 2026)
**Status:** Active Draft – Locked for Minimalism

**Changelog (v2.0 → v2.1)**
- Completely removed `related_uku_ids` and all explicit link fields
- Redefined relationships as inherent key-value matches ("red strings") computed on-demand via JSONB
- Added conspiracy-board / evidence-wall mental model as the canonical north star
- Further stripped to the absolute minimal tech stack that works
- Incorporated universal validation from practitioner consensus: simplest Obsidian + metadata memory is what actually works for LLMs/agents

---

### 1. Introduction & Purpose

Pebbles defines a **minimal schema specification** for capturing lived experience at the moment of creation.

Every Pebble is a **Universal Knowledge Unit (UKU)** — one atomic, sovereign Markdown file with YAML frontmatter that holds both the raw content *and* rich experiential metadata.

**Core goal:** Create the simplest possible memory layer that current LLMs and agents can actually use without distraction or over-engineering.

This spec is deliberately the smallest functional system: plain files + one lightweight index. It follows the proven insight that "simplest forms of memory work best" — Obsidian vaults with metadata for searching across any dimensions.

---

### 2. Core Principles (Pebbles Design Tenets)

1. **Capture-at-moment** – Experiential metadata recorded immediately.
2. **Human-first, Agent-ready** – Files remain fully readable/editable in any Markdown editor.
3. **Sovereign & Private** – No third-party services required.
4. **Methodical, not noisy** – No random dumps; structure emerges from metadata.
5. **Fluid Schema** – New YAML keys are always allowed. Agents discover repeated patterns.
6. **Inherent Relationships** – Any key-value match = automatic red string (no manual fields needed).
7. **Minimal Tech** – Vault + Postgres JSONB + tiny watcher. Nothing else.
8. **Conspiracy-Board Mental Model** – Each pebble is a note on the wall. Strings appear wherever attributes match.

---

### 3. Abstract Data Model

A UKU contains exactly two sections:
- **YAML Frontmatter** – experiential metadata + living fields
- **Body** – raw Markdown content

No explicit relationship fields. Connections are inherent to the data.

---

### 4. YAML Binding v1 (Default – Obsidian-native)

```yaml
---
title: "Short title or first sentence"                  # required
uku_id: "uku-20260321-abcdef"                          # required – unique
created_at: "2026-03-21T02:59:00Z"                     # required – ISO 8601
url: "https://x.com/..."                               # optional
source_id: "tweet-1234567890"                          # optional

uku_type: experience_capture | insight | problem_statement | proposed_solution | ontology_element
category: foundational | vision | technical | insight | problem

context_elements:                                      # lived experience
  why_posted: "I was frustrated with agent amnesia again"
  surrounding_activity: "Working on SAGE validators while on a walk"
  emotional_state: "Excited + slightly annoyed"
  intended_next_action: "Build the one-click archive importer"

tags:
  - universal-knowledge-unit
  - interspecies-caching
  - agent-memory

# New fields always allowed (fluid)
# interspecies_caching_signal: "high"

status: draft | annotated | published | archived
---
**Full content here** (Markdown body – text, images, code, etc.)
```

---

### 5. Relationship Model – "Red Strings" (v2.1)

There are no `related_uku_ids` or explicit link fields in the files.

**Rule:** Any key-value match in the YAML frontmatter between two pebbles = a direct, inherent relationship.

**Examples of automatic red strings:**
- Same `emotional_state`
- Same `uku_type` + `category`
- Shared tag
- Any brand-new field you invent tomorrow

These strings are computed on-demand by the Postgres JSONB index. No data is ever written back into your Markdown files.

---

### 6. Storage & Indexing Layer (The Minimal "Wall")

**Single recommendation (v2.1): Postgres + JSONB**

- Markdown files = single source of truth
- Tiny watcher parses changed files into one `yaml_data` JSONB column
- One GIN index on the entire document enables instant "any key-value match" queries
- Optional `pgvector` column for semantic search if desired
- Agents query the index directly for red strings, relevance, decay, etc.

**Minimal schema:**

```sql
CREATE TABLE pebbles (
    uku_id       TEXT PRIMARY KEY,
    file_path    TEXT NOT NULL UNIQUE,
    yaml_data    JSONB NOT NULL,
    body_text    TEXT,
    indexed_at   TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_pebbles_yaml ON pebbles USING GIN (yaml_data);
```

**Example red-string query** — find all pebbles sharing any value with a given pebble:

```sql
-- Find pebbles with the same emotional_state
SELECT b.uku_id, b.yaml_data->>'title'
FROM pebbles a, pebbles b
WHERE a.uku_id = 'uku-20260321-abcdef'
  AND a.uku_id != b.uku_id
  AND a.yaml_data->'context_elements'->>'emotional_state'
    = b.yaml_data->'context_elements'->>'emotional_state';

-- Find pebbles sharing any tag
SELECT b.uku_id, b.yaml_data->>'title'
FROM pebbles a, pebbles b
WHERE a.uku_id = 'uku-20260321-abcdef'
  AND a.uku_id != b.uku_id
  AND a.yaml_data->'tags' ?| ARRAY(
      SELECT jsonb_array_elements_text(a.yaml_data->'tags')
  );
```

This is the conspiracy board made digital: infinite scale, perfect memory, zero ceremony.

---

### 7. Background Agents Role

Agents are responsible for:
- Enriching living fields (`current_relevance`, `decay_factor`, etc.)
- Keeping the JSONB index in sync
- Querying red strings for context
- Suggesting taxonomy extensions when new patterns appear

Agents **never** modify the source Markdown files directly. All enrichment is written to the JSONB index only, preserving file sovereignty.

---

### 8. Field Reference

**uku_type** (required)
- `experience_capture` – raw moment of lived experience
- `insight` – distilled learning
- `problem_statement` – pain point
- `proposed_solution` – idea/plan
- `ontology_element` – definition or taxonomy piece

**category** (required)
`foundational | vision | technical | insight | problem`

**status**
`draft` (human editing) | `annotated` | `published` | `archived`

**Fluid fields** — any additional YAML key is valid. The schema is intentionally open. Agents discover repeated patterns and may suggest promoting frequent ad-hoc fields into the lightweight taxonomy.

---

### 9. Example Pebble

```yaml
---
title: "SAGE + ByteRover alignment moment"
uku_id: "uku-20260321-2035366573192753648"
created_at: "2026-03-21T08:12:00Z"
uku_type: insight
category: vision
context_elements:
  why_posted: "Kevin just replied – this is the exact triad"
  surrounding_activity: "Reading X thread while drinking coffee"
  emotional_state: "Energized"
  intended_next_action: "Generate full spec v0.1 and DM"
tags:
  - pebbles
  - sage
  - byterover
  - interspecies
status: draft
---
This feels like perfect timing!

You've both basically built the runtime infrastructure for the schema spec
I've been drafting all week...
```

**Red strings this pebble automatically creates:**
- Every other pebble with `emotional_state: "Energized"`
- Every other pebble with `uku_type: insight` and `category: vision`
- Every other pebble tagged `pebbles`, `sage`, `byterover`, or `interspecies`
- No manual linking required. The wall does the work.
