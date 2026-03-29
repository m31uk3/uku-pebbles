**Pebbles UKU Specification v2.3**

**Universal Knowledge Unit – Schema for Sovereign Personal & Interspecies Memory**

**Version:** 0.2.3 (March 2026)
**Status:** Active Draft

**Changelog (v2.1 → v2.3)**
- Formalized pebble-as-descriptor model (AGENTS.md for knowledge work)
- Added 4-layer architecture with compile-time LLM boundary
- Added 4-tier ingestion contract
- Added optional typed edges for consolidation hierarchy
- Atomized emotional_state (Ekman 8) and intent (4 values)
- Corrected file-write rule: RBAC-governed, not actor-locked
- Added Luhmann Test, graph-eligible field registry, and bibliography
- Spec is retrieval-implementation-agnostic; JSONB+GIN feasibility documented inline (WIP)

---

### 1. Introduction & Purpose

Pebbles defines a **schema specification** for capturing lived experience at the moment of creation.

Every Pebble is a **Universal Knowledge Unit (UKU)** — a structured **descriptor** for any human artifact (screenshot, document, photo, conversation, recording, idea). A pebble is not the artifact itself. It is a lightweight Markdown file with YAML frontmatter that makes the artifact discoverable and associable.

**The analogy:** Just as AGENTS.md describes a codebase to an agent without containing the code, a pebble describes an artifact with the lived experiential context of the moment it was captured.

**Core goal:** Create the simplest possible memory layer that humans and agents can use — sovereign, structured, and searchable without LLM calls.

---

### 2. Core Principles

1. **Capture-at-moment** – Experiential metadata recorded immediately, not retrofitted.
2. **Human-first, Agent-ready** – Files remain fully readable/editable in any Markdown editor.
3. **Sovereign & Private** – No third-party services required for core storage or retrieval.
4. **Pebble-as-Descriptor** – A pebble wraps an artifact with context. One pebble = one idea + one artifact reference. Multiple pebbles may reference the same source artifact.
5. **Atomic to a Single Idea** – A meeting produces multiple pebbles, not one. Each captures a distinct thought worthy of remembering.
6. **Fluid Schema** – Any YAML key is valid. Convergence emerges from API-level guardrails during ingestion and curation, not from promotion mechanisms.
7. **Inherent Relationships (Red Strings)** – Any key-value match across pebbles = automatic connection. No manual linking required.
8. **Typed Edges (Progressive Enhancement)** – Optional, explicit, directional relationships for consolidation hierarchy and reasoning chains. Additive — never breaks core red-string functionality.
9. **Minimal Tech** – Files + one index + one optional edges table. Nothing else in the deterministic core.
10. **Conspiracy-Board Mental Model** – Each pebble is a note on the wall. Red strings appear wherever attributes match. Some strings are thicker than others.

---

### 3. Architecture – Four Bounded Layers

| Layer | Name | LLM? | Responsibility |
|-------|------|------|----------------|
| 1 | **Ingestion** | No | Deterministic extraction, normalization, YAML parse, index write |
| 2 | **Curation** | No | Actor-agnostic (human or agent, RBAC-governed). Create edges, consolidate, build L1+ structures. Edit files and index together. |
| 3 | **Query** | No | Pure deterministic retrieval. Red-string matches + optional edge traversals. Returns structured results. |
| 4 | **Inference** | Yes | Separate process. Receives structured Query results only. LLM reasoning, synthesis, suggestions back to Curation via API. |

**The single most important contract:** Layers 1–3 are compile-time LLM-free.

**Graceful degradation:** The system is fully functional without Layer 4 or the typed-edges table.

### 3.1 Ingestion Contract

| Tier | Source | Friction | Examples |
|------|--------|----------|----------|
| 1 | Auto-captured from device/browser | Zero | timestamp, device, source_app, GPS, active_url, file_ref, content_hash |
| 2 | Human moment (mini-tweet + quick-tag) | 3–5 sec | intent, emotional_state, people, topic/tags |
| 3 | Inferred without LLM (high confidence) | Zero | venue_type from GPS, source_type from file extension |
| 4 | LLM-assisted inference (async) | Zero | Optimal attribute assignment using payload content + existing index state |

### 3.2 File Sovereignty

- Pebble `.md` files are the **source of truth**. The index is a derived cache.
- **RBAC governs write access**, not actor type. Any actor (human or agent) with permission can edit files — both YAML frontmatter and Markdown body.
- Enrichments happen via deliberate curation-layer actions that update files and index together.
- The system provides guardrails (hierarchy visibility, suggestion surfaces) to prevent drift — not write locks.

---

### 4. Abstract Data Model

A UKU contains exactly two sections:
- **YAML Frontmatter** – experiential metadata, artifact reference, living fields
- **Body** – human/agent-written summary of the artifact (not the artifact itself)

The artifact (screenshot, PDF, recording, webpage) lives elsewhere. The pebble points to it.

---

### 5. YAML Binding v1 (Default – Obsidian-native)

```yaml
---
title: "Short title or first sentence"                  # required
uku_id: "uku-20260321-abcdef"                          # required – unique
created_at: "2026-03-21T02:59:00Z"                     # required – ISO 8601
url: "https://x.com/..."                               # optional – artifact link
source_id: "tweet-1234567890"                          # optional – artifact identifier

uku_type: experience_capture | insight | problem_statement | proposed_solution | ontology_element
category: foundational | vision | technical | insight | problem

emotional_state: joy                                    # Ekman 8 controlled vocabulary
intent: act_on                                          # 4 values: remember, act_on, share, think_about

context_elements:                                       # fleeting / prose (full-text searchable)
  why_captured: "Kevin just replied – this is the exact triad"
  surrounding_activity: "Reading X thread while drinking coffee"

location:
  city: "London"                                        # normalized
  venue_type: coffee_shop                               # controlled: home, office, coffee_shop, transit, outdoor, other

tags:
  - pebbles
  - architecture
  - interspecies

weight: 0.85                                            # optional – human-assigned importance (0.0–1.0)

status: draft | annotated | published | archived
---
This feels like perfect timing!

Kevin's reply confirmed the exact triad we've been drafting...
```

---

### 6. Relationship Model

#### 6.1 Red Strings (Implicit, Symmetric)

Any key-value match in the YAML frontmatter between two pebbles = an automatic connection.

**Examples:**
- Same `emotional_state: joy`
- Same `uku_type: insight` + `category: vision`
- Shared tag
- Same `location.venue_type: coffee_shop`
- Any fluid field you add tomorrow

Red strings are computed on-demand from the index. Nothing is written back to files.

#### 6.2 Typed Edges (Optional, Explicit, Directional)

Stored in a lightweight edges table. Created only during Curation (by humans or agents with RBAC write access).

**Purpose:** Enable consolidation hierarchy and reasoning chains that red strings cannot express.

- `derived_from` — Level-1 consolidation → source Level-0 pebble(s)
- `contains` — Level-2 MOC → grouped pebbles
- `supports` / `contradicts` — reasoning chains
- `supersedes` — version replacement

The system works fully without this table. Typed edges are a progressive enhancement.

---

### 7. Weighting Model

Three layers of signal:

#### 7.1 Explicit Weight (in the file)

Optional `weight` field (0.0–1.0). The human saying "this matters."

#### 7.2 Implicit Signals (in the index only)

Behavioral signals tracked in the index, **never written back to files**:

| Signal | What it captures |
|--------|-----------------|
| `access_count` | Times opened/viewed/queried |
| `update_count` | Times the source file was modified |
| `reference_count` | Times appeared in a red-string result |
| `last_accessed_at` | Most recent access timestamp |
| `last_updated_at` | Most recent file modification |

#### 7.3 Effective Weight (agent-computed)

Agents combine explicit weight + implicit signals + time decay + cross-pebble pattern signals into `effective_weight` in the index. Formula is implementation-specific.

**Pattern weights:** A category accessed 10x more, a tag across many high-weight pebbles, an emotional_state that correlates with revisits — agents detect these and boost/dampen accordingly. Some red strings are thicker than others.

---

### 8. Higher-Order Structures

Level-0 raw Pebbles → Level-1 consolidations → Level-2 Maps of Content (MOCs) → Level-3+ meta-syntheses.

Higher-order pebbles are themselves pebbles (same `.md` + YAML format). They link to their sources via typed edges (`derived_from`, `contains`). The hierarchy is expressed in the edges table, not in file frontmatter.

---

### 9. Storage & Indexing (Implementation – WIP)

**Recommended implementation: Postgres + JSONB + GIN**

- Markdown files = source of truth
- Ingestion parses YAML and writes to a `yaml_data` JSONB column
- One GIN index enables sub-millisecond compound faceted search on any field
- Optional `pgvector` column for future semantic search
- Optional edges table for typed relationships with recursive CTE traversal

**Minimal schema:**

```sql
CREATE TABLE pebbles (
    uku_id           TEXT PRIMARY KEY,
    file_path        TEXT NOT NULL UNIQUE,
    yaml_data        JSONB NOT NULL,
    body_text        TEXT,
    indexed_at       TIMESTAMPTZ DEFAULT now(),

    -- Implicit behavioral signals (never written back to files)
    access_count     INTEGER DEFAULT 0,
    update_count     INTEGER DEFAULT 0,
    reference_count  INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMPTZ,
    last_updated_at  TIMESTAMPTZ,

    -- Agent-computed effective weight
    effective_weight REAL
);

CREATE INDEX idx_pebbles_yaml ON pebbles USING GIN (yaml_data);
CREATE INDEX idx_pebbles_weight ON pebbles (effective_weight DESC NULLS LAST);

-- Optional: typed edges for consolidation hierarchy
CREATE TABLE edges (
    source_id   TEXT NOT NULL REFERENCES pebbles(uku_id) ON DELETE CASCADE,
    target_id   TEXT NOT NULL REFERENCES pebbles(uku_id) ON DELETE CASCADE,
    edge_type   TEXT NOT NULL,
    created_by  TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (source_id, target_id, edge_type)
);

CREATE INDEX idx_edges_source ON edges(source_id);
CREATE INDEX idx_edges_target ON edges(target_id);
```

**Example red-string query:**

```sql
SELECT b.uku_id, b.yaml_data->>'title'
FROM pebbles a, pebbles b
WHERE a.uku_id = 'uku-20260321-abcdef'
  AND a.uku_id != b.uku_id
  AND a.yaml_data @> b.yaml_data->'emotional_state';
```

---

### 10. Field Reference

**uku_type** (required)
- `experience_capture` – raw moment of lived experience
- `insight` – distilled learning
- `problem_statement` – pain point
- `proposed_solution` – idea/plan
- `ontology_element` – definition or taxonomy piece

**category** (required)
`foundational | vision | technical | insight | problem`

**emotional_state** (graph-eligible, Ekman 8)
`joy | sadness | anger | fear | surprise | disgust | trust | anticipation`

**intent** (graph-eligible)
`remember | act_on | share | think_about`

**location.venue_type** (graph-eligible)
`home | office | coffee_shop | transit | outdoor | other`

**weight** (optional)
Human-assigned importance, 0.0–1.0.

**status**
`draft | annotated | published | archived`

**Fluid fields** — any additional YAML key is valid. The schema is intentionally open.

---

### 11. Example Pebble

```yaml
---
title: "SAGE + ByteRover alignment moment"
uku_id: "uku-20260321-2035366573192753648"
created_at: "2026-03-21T08:12:00Z"
url: "https://x.com/kevinnguyendn/status/2035366573192753648"
uku_type: insight
category: vision
emotional_state: joy
intent: act_on
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
weight: 0.85
status: draft
---
This feels like perfect timing!

You've both basically built the runtime infrastructure for the schema spec
I've been drafting all week...
```

**Red strings this pebble automatically creates:**
- Every other pebble with `emotional_state: joy`
- Every other pebble with `intent: act_on`
- Every other pebble with `uku_type: insight` and `category: vision`
- Every other pebble tagged `pebbles`, `sage`, `byterover`, or `interspecies`
- Every other pebble at `venue_type: coffee_shop`
- No manual linking required. The wall does the work.

**Weighting in action:**
- Human assigned `weight: 0.85` — this pebble matters
- If the human keeps opening it, `access_count` rises in the index
- If it appears in many red-string results, `reference_count` climbs
- Agents combine all signals into `effective_weight`
- If `vision` is consistently high-weight, agents boost all vision pebbles (pattern weight)

---

### Appendix A: Luhmann Test

A field is **permanent** (graph-eligible, red-string eligible) if its value is understandable without the context in which it was written. A stranger should be able to read the value and know what it means.

- `emotional_state: joy` — passes (stranger understands "joy")
- `why_captured: "Kevin just replied"` — fails (stranger doesn't know Kevin)

### Appendix B: Ekman 8 (emotional_state)

Controlled vocabulary for the `emotional_state` field:

`joy`, `sadness`, `anger`, `fear`, `surprise`, `disgust`, `trust`, `anticipation`

### Appendix C: Graph-Eligible Fields

Fields whose values pass the Luhmann Test:

| Field | Values | Red-string quality |
|-------|--------|--------------------|
| `uku_type` | 5 controlled values | High — clusters by artifact nature |
| `category` | 5 controlled values | High — clusters by domain |
| `status` | 4 controlled values | Medium — lifecycle tracking |
| `tags` | user-defined, lowercase | High — primary association surface |
| `emotional_state` | Ekman 8 | High — experiential clustering |
| `intent` | 4 controlled values | High — action-oriented clustering |
| `location.city` | normalized | Medium — geographic clustering |
| `location.venue_type` | 6 controlled values | Medium — situational clustering |

### Appendix D: Bibliography

- Mikey O'Brien. "Brain.md." Rho repository. https://github.com/mikeyobrien/rho/blob/main/docs/brain.md
- Obsidian Rocks. "Getting Started with Zettelkasten in Obsidian." https://obsidian.rocks/getting-started-with-zettelkasten-in-obsidian/
- UKU Pebbles RQ1 + RQ2 Analysis Artifact (27 MAR 2026). Internal design document.
- UKU Pebbles Grok Adversarial Debate (29 MAR 2026). Internal design stress test.
