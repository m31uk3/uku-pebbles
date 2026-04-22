**Pebbles Specification v0.3.0-draft**

**Universal Knowledge Unit – Schema for Sovereign Personal & Interspecies Memory**

**Version:** 0.3.0-draft (April 2026)
**Status:** Active Draft
- Added Appendices E (Modality), F (memory_kind / CLS-Zettelkasten lineage), G (Integration Patterns)
- Cross-references between pebbles use (label, uid) object tuple form
- File renamed: `_specs/uku-pebbles.spec.md` → `_specs/pebbles.spec.md`
- §7 (Weighting Model) unchanged from v0.2.3 — pending citation research deferred to post-v1 (see `.sop/synthesis/15-weight-field-citation-research.md`)

---

### 1. Introduction & Purpose

Pebbles defines a **schema specification** for capturing lived experience at the moment of creation.

Every pebble is a **Universal Knowledge Unit (UKU)** — a structured **descriptor** for any human artifact (screenshot, document, photo, conversation, recording, idea). A pebble is not the artifact itself. It is a lightweight Markdown file with YAML frontmatter that makes the artifact discoverable and associable.

"Pebbles" is the brand and the file format. "UKU" is the formal expansion used here once and then dropped — throughout the rest of this document, **pebble** refers to both the file and the underlying structured descriptor.

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
11. **Capture-Immutable, Curation-Editable** – The body and capture metadata of a pebble are immutable post-capture; curator-editable fields (tags, edges, lifecycle, ontology links) are freely refined by the curation layer over time.
12. **Forget by Choice, Not by Geometry** – Pebbles' interference-immune red strings mean retrieval quality does not degrade as the vault grows. The system therefore does not auto-destroy data; lifecycle transitions are visibility controls. Only the user may tombstone or hard-delete.

---

### 3. Architecture – Four Bounded Layers

| Layer | Name | LLM? | Responsibility |
|-------|------|------|----------------|
| 1 | **Ingestion** | No | Deterministic extraction, normalization, YAML parse, index write |
| 2 | **Curation** | No | Actor-agnostic (human or agent, RBAC-governed). Create edges, consolidate, promote, refine tags, manage lifecycle. Edit curator-editable fields and reindex. |
| 3 | **Query** | No | Pure deterministic retrieval. Red-string matches + optional edge traversals. Returns structured results. |
| 4 | **Inference** | Yes | Optional. Separate process. Receives structured Query results only. LLM reasoning, synthesis, suggestions back to Curation via API. |

**The single most important contract:** Layers 1–3 are compile-time LLM-free.

**Graceful degradation:** The system is fully functional without Layer 4 or the typed-edges table.

**Conformance:** An implementation declares the layer subset it supports. There is no separate Reader/Writer/Full taxonomy — the layers an implementation provides *is* its conformance statement. Layer 4 is always optional and is never required for conformance.

#### 3.1 Ingestion Contract

| Tier | Source | Friction | Examples |
|------|--------|----------|----------|
| 1 | Auto-captured from device/browser | Zero | timestamp, device, source_app, GPS, active_url, file_ref, content_hash |
| 2 | Human moment (mini-tweet + quick-tag) | 3–5 sec | intent, emotional_state, modality, people, topic/tags |
| 3 | Inferred without LLM (high confidence) | Zero | venue_type from GPS, source_type from file extension |
| 4 | LLM-assisted inference (async, optional) | Zero | Optimal attribute assignment using payload content + existing index state |

#### 3.2 File Sovereignty

- Pebble `.md` and `.pebble` files are the **source of truth**. The index is a derived cache.
- **RBAC governs write access**, not actor type. Any actor (human or agent) with permission can edit curator-editable fields (see §3.4).
- Enrichments happen via deliberate curation-layer actions that update files and index together.
- The system provides guardrails (hierarchy visibility, suggestion surfaces) to prevent drift — not write locks.

#### 3.3 Lifecycle & Forgetting Policy

Pebbles' interference-immune red strings mean retrieval quality does not degrade as the vault grows. The system therefore **does not auto-destroy data**. Lifecycle transitions are visibility controls and curator-driven state changes, not destructive operations.

| Disposition | Who triggers | What happens | Reversible |
|------------|-------------|--------------|------------|
| **Graduate** (L0 → L1+) | Curator (RBAC) | New permanent pebble created with `derived_from` edge to source. Source untouched. | Yes (additive) |
| **Archive** | System policy OR user | `status: archived`. File and index entry untouched. Hidden from default queries. | Yes (flag flip) |
| **Tombstone** | **User only** | `status: tombstoned`. File untouched. Excluded from all queries unless explicit `include_tombstoned`. | Yes (flag flip) |
| **Hard delete** | **User only** | File removed; index row dropped. | **No** |

**Hard constraint:** the system may transition pebbles to `archived` based on vault policy (age, references, tag exemptions). The system may NEVER auto-tombstone or auto-delete. Tombstone and hard-delete are user-only operations.

**Vault policy** (in `vault.yaml`):

```yaml
lifecycle_policy:
  archive_after_days_unreferenced: 365     # triggered by last_accessed_at
  archive_after_zero_references_days: 180  # triggered by reference_count == 0
  protected_tags: [pinned, important]       # exempt from auto-archive
```

**Per-pebble overrides** (curator-editable, set at capture or revised later):

```yaml
pin: true                          # never auto-archive regardless of policy
archive_at: 2027-01-01T00:00:00Z   # scheduled archival (full ISO 8601)
protected: true                    # requires explicit user action to archive
```

`pin: true` overrides `archive_at`. Both can be set at capture or revised during curation.

#### 3.4 Capture-Immutable vs Curator-Editable Fields

| Class | Fields | Rule |
|-------|--------|------|
| **Capture-Immutable** | `pebble_id`, `created_at`, `body`, `url`, `source_id`, `content_hash`, `device`, `source_app`, `location` (if set at capture) | Never edited after capture. Represents the lived moment. |
| **Curator-Editable** | `pebble_type`, `memory_kind`, `emotional_state`, `intent`, `modality`, `tags`, `topic`, `category`, `governed_by`, `status`, `pin`, `archive_at`, `protected`, all typed edges, every field not in the immutable list | Mutable at any time by the curation layer (RBAC-governed). Triggers reindexing. Not a versioning event. |

**Why partial immutability:** Full L0 immutability would block the feedback loop where fleeting notes benefit from a growing index — tag autocomplete, ontology link proposals, wiki link suggestions, modality refinement. The body and capture metadata represent the lived moment and must be preserved; everything else is curatorial interpretation that should evolve as the vault matures.

---

### 4. Naming & Formats

| Term | Meaning |
|------|---------|
| **Pebble** | The brand, the file format, and the underlying structured descriptor. Used throughout this document. |
| **UKU** | Universal Knowledge Unit. The formal expansion used in §1 only. |
| `pebble.md` | Tier 1 pure-text pebble. Markdown file with YAML frontmatter. |
| `.pebble` | Tier 2 zip container. Wraps an artifact (image, audio, PDF, etc.) plus a `pebble.yaml` manifest and `body.md`. EPUB-style structure. |
| `pebble_id` | Unique identifier. ULID format (26 alphanumeric characters, time-sortable, no prefix). |
| `pebble_short` | Human-friendly secondary key. Last 12 characters of the `pebble_id` (60 bits of randomness). Collision-safe to ~7.7M items per segment (vault/repo/namespace). Regex: `^[0-9A-HJKMNP-TV-Z]{12}$`. Used in inline mentions, filenames, and conversation. The full 26-char `pebble_id` remains the primary key. |

---

### 5. YAML Binding v1 (Default – Obsidian-native)

```yaml
---
title: "Short title or first sentence"                  # required
pebble_id: 01HZJ3K8P7M4R5VYX2W9NQBCDE                   # required – ULID, 26 chars
created_at: 2026-04-13T08:12:00Z                        # required – full ISO 8601 with timezone
url: "https://x.com/..."                                # optional – artifact link
source_id: "tweet-1234567890"                           # optional – artifact identifier
content_hash: "sha256:..."                              # optional – integrity

pebble_type: experience_capture | insight | problem_statement | proposed_solution | reference | ontology
memory_kind: episodic | semantic | procedural
modality: kinetic | non_kinetic
category: foundational | vision | technical | insight | problem

emotional_state: joy                                    # Plutchik 8 Primary
intent: act_on                                          # remember | act_on | share | think_about

governed_by:                                            # 1:many ontology references
  - label: meeting-roster
    uid: 01HZJ3K8P7M4R5VYX2W9NQBCFG
  - label: fiscal-calendar
    uid: 01HZJ3K8P7M4R5VYX2W9NQBCHJ

context_elements:                                       # fleeting / prose (full-text searchable)
  why_captured: "Kevin just replied – this is the exact triad"
  surrounding_activity: "Reading X thread while drinking coffee"

location:
  city: "London"
  venue_type: coffee_shop                               # home | office | coffee_shop | transit | outdoor | other

tags:
  - pebbles
  - architecture
  - interspecies

# Lifecycle (curator-editable)
status: draft                                           # draft | active | annotated | published | archived | tombstoned | superseded
pin: false                                              # never auto-archive if true
archive_at: 2027-01-01T00:00:00Z                        # scheduled archival (optional, full ISO 8601)
protected: false                                        # requires explicit user action to archive

weight: 0.85                                            # optional – legacy. See §7.
---
This feels like perfect timing!

Kevin's reply confirmed the exact triad we've been drafting...
```

#### 5.1 Temporal Field Rules

**All temporal fields MUST use full ISO 8601 timestamps with explicit timezone.** UTC via `Z` suffix is preferred; explicit offsets (`+01:00`, `-05:00`) are permitted.

**Date-only values are invalid.** Parsers MUST reject `2027-01-01` and require `2027-01-01T00:00:00Z`.

Affected fields: `created_at`, `updated_at`, `last_accessed_at`, `last_updated_at`, `status_changed_at`, `archive_at`, and any future temporal fields.

**Rationale**: date-only values are ambiguous across timezones and break scheduling determinism for `archive_at`. Parser contract is simpler with one format. Maps cleanly to Postgres `TIMESTAMPTZ`.

#### 5.2 Cross-Reference Format

All pebble→pebble references in YAML (`governed_by`, and typed-edge references when stored in frontmatter) use the **(label, uid) object tuple** form:

```yaml
governed_by:
  - label: morning-standup
    uid: 01HZJ3K8P7M4R5VYX2W9NQBCFG
```

**Resolution rule**: `uid` is authoritative. The `label` is a human-readable diff-friendly hint. If a referenced pebble's label changes, the `uid` still resolves and the index surfaces a label-drift warning for curator repair. The edge never breaks.

---

### 6. Relationship Model

#### 6.1 Red Strings (Implicit, Symmetric)

Any key-value match in the YAML frontmatter between two pebbles = an automatic connection.

**Examples:**
- Same `emotional_state: joy`
- Same `pebble_type: insight` + `category: vision`
- Same `modality: kinetic`
- Same `memory_kind: procedural`
- Shared tag
- Same `location.venue_type: coffee_shop`
- Same `governed_by` ontology
- Any fluid field you add tomorrow

Red strings are computed on-demand from the index. Nothing is written back to files.

**Field combinations** like `pebble_type × memory_kind × modality` produce 64+ orthogonal facets from just 3 fields. Each combination is a tiny, sharply-defined slice of the vault — the structured-metadata advantage in concrete form.

#### 6.2 Typed Edges (Optional, Explicit, Directional)

Stored in a lightweight edges table. Created only during Curation (by humans or agents with RBAC write access).

**Purpose:** Enable consolidation hierarchy, ontology governance, and reasoning chains that red strings cannot express.

| Edge type | Direction | Use |
|-----------|-----------|-----|
| `derived_from` | new → source | Promotion (L1 created from L0); literature notes citing source pebbles |
| `contains` | parent → child | L2 MOC grouping L1 pebbles; L3+ structural notes containing L2 MOCs |
| `governed_by` | claim → ontology | Pebble references ontology pebble for fact verification (also surfaced as a YAML field on every pebble; see §11) |
| `supports` / `contradicts` | A → B | Reasoning chains |
| `supersedes` | new → old | Version replacement |
| `co_occurred_with` | A ↔ B | Atomic events split into kinetic + non-kinetic pebbles |

The system works fully without this table. Typed edges are a progressive enhancement.

#### 6.3 Promotion

Promotion is the curation operation that walks a pebble up the consolidation gradient (L0 fleeting → L1 permanent → L2 MOC → L3+ structural). It is grounded in two converging traditions:

- **Zettelkasten** (Luhmann 1952): fleeting notes are refactored into permanent atomic notes written in the curator's own words, linked to other permanent notes.
- **Complementary Learning Systems** (McClelland, McNaughton & O'Reilly 1995): fast hippocampal episodic encoding plus slow neocortical semantic consolidation, with a gradient between them.

Both predict the same four-level structure. See Appendix F.

**Promotion creates a new permanent pebble** that links back to the source fleeting pebble via a `derived_from` edge. The source fleeting pebble is **untouched by the promotion itself** — its body and capture metadata remain as captured, while its curator-editable fields may continue to evolve independently.

**Graduation criteria** (Zettelkasten rules) for L0 → L1 promotion:

1. **Atomic** — one big idea per permanent pebble (Principle 5)
2. **Luhmann Test passing** — body understandable without context (Appendix A)
3. **Own words** — body re-expressed by the curator, not copied
4. **Linked** — at least one outbound typed edge (`derived_from` to source, plus any `governed_by` ontology links and supporting `derived_from` edges to other permanent notes)

**Substantiation**: a permanent pebble's value is in its body and its links. The body should make consistent sense of the fleeting source(s) and be substantiated by:
- `governed_by` → relevant ontology pebbles (ground truth anchoring)
- Additional `derived_from` edges → other permanent/literature notes that inform the sense-making
- In-body markdown citations (Obsidian-compatible inline citation syntax)

**Pebble shape distinction**:
- **Fleeting pebble** = wrapper/pointer for any content type. Body is a brief note *about* an external artifact. Value is in YAML + pointer + capture metadata. Can be `pebble.md` (pure text) or `.pebble` (zip wrapping an artifact).
- **Permanent pebble** = markdown-native. Body IS the content, written by the curator. Markdown formatting, wiki links, inline citations all apply. Always `pebble.md`.

The fleeting/permanent distinction is not declared via a flag — it is derivable from edge topology and content source at query time. See §9.1.

---

### 7. Weighting Model

> **STATUS:** This section is unchanged from v0.2.3. A citation-research-driven rewrite is queued for post-v1 release. See `.sop/synthesis/15-weight-field-citation-research.md` for the deferred recommendation (Option (c): downgrade `weight` to optional-legacy, elevate behavioral signals + graph centrality as default, add `salience_hint` categorical).

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

### 8. Higher-Order Structures (CLS / Zettelkasten Hierarchy)

Pebbles' consolidation hierarchy is the operationalization of **Complementary Learning Systems** (McClelland 1995) as the **Zettelkasten workflow** (Luhmann 1952), encoded in structured YAML.

| Level | CLS | Zettelkasten | Pebble shape |
|-------|-----|--------------|--------------|
| **L0** | Episodic — raw, hippocampal-fast, full detail | Fleeting note — temporary capture, often without context | Wrapper/pointer; body is a brief note about an artifact |
| **L1** | Consolidation gradient — partial abstraction | Permanent (atomic) note — own words, linked, self-contained | Markdown-native; body IS the content |
| **L2** | Consolidation gradient — themed grouping | Map of Content (MOC) | Markdown-native; body explains the grouping |
| **L3+** | Semantic — abstracted concepts, generalized knowledge | Structural / Hauptzettel | Markdown-native; body presents the abstraction |

Higher-order pebbles are themselves pebbles (same `pebble.md` + YAML format). They link to their sources via typed edges (`derived_from`, `contains`). The hierarchy is expressed in the edges table, not in file frontmatter.

**Level is derived at query time** from edge topology — the YAML does not declare it. See §9.1.

That a paper-based 1950s note-taking system and a 1995 cognitive science hypothesis independently arrived at the same four-level structure is structural confirmation that the gradient is load-bearing, not a metaphor. Pebbles is the operationalization of both as a structured YAML format. See Appendix F for the dual-precedent argument.

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
    pebble_id        TEXT PRIMARY KEY,         -- ULID (26 chars)
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

-- Optional: typed edges for consolidation hierarchy and ontology governance
CREATE TABLE edges (
    source_id   TEXT NOT NULL REFERENCES pebbles(pebble_id) ON DELETE CASCADE,
    target_id   TEXT NOT NULL REFERENCES pebbles(pebble_id) ON DELETE CASCADE,
    edge_type   TEXT NOT NULL,
    created_by  TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (source_id, target_id, edge_type)
);

CREATE INDEX idx_edges_source ON edges(source_id);
CREATE INDEX idx_edges_target ON edges(target_id);
CREATE INDEX idx_edges_type ON edges(edge_type);
```

**Example red-string query:**

```sql
SELECT b.pebble_id, b.yaml_data->>'title'
FROM pebbles a, pebbles b
WHERE a.pebble_id = '01HZJ3K8P7M4R5VYX2W9NQBCDE'
  AND a.pebble_id != b.pebble_id
  AND a.yaml_data @> b.yaml_data->'emotional_state';
```

#### 9.1 Level Derivation from Edge Topology

`consolidation_level` is **not** a YAML field. It is derived at query time from the edge graph:

| Derived level | Condition |
|---------------|-----------|
| **L0 fleeting** | No incoming `derived_from` edges; often has `url`/`source_id`/artifact pointer |
| **L1 permanent** | Has outbound `derived_from` edges pointing at L0 sources |
| **L2 MOC** | Has outbound `contains` edges pointing at L1 pebbles |
| **L3+ structural** | Has outbound `contains` edges pointing at L2+ pebbles |

A query that needs level information runs a single CTE on the edges table. The YAML stays minimal; the index does the bookkeeping.

#### 9.2 Index Mutability vs File Sovereignty

The index may freely add, remove, or recompute derived columns (`access_count`, `effective_weight`, derived levels, label-drift warnings). The source files are sovereign — the index is a rebuildable cache. If the index disagrees with a file, the file wins.

---

### 10. Field Reference

#### 10.1 Required

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Short title or first sentence |
| `pebble_id` | string (ULID) | Unique identifier, 26 alphanumeric chars, no prefix |
| `created_at` | string (ISO 8601) | Capture moment, full timestamp with timezone |
| `pebble_type` | enum | See §10.2 |

#### 10.2 pebble_type (controlled vocabulary)

| Value | Meaning |
|-------|---------|
| `experience_capture` | Raw moment of lived experience |
| `insight` | Distilled learning |
| `problem_statement` | Pain point, friction, gap |
| `proposed_solution` | Idea, plan, candidate fix |
| `reference` | Definition, citation, taxonomy entry |
| `ontology` | First-class ground truth anchor; structured agent-traversable body. See §11. |

#### 10.3 memory_kind (controlled vocabulary, orthogonal to pebble_type)

| Value | Meaning |
|-------|---------|
| `episodic` | Specific events, full detail, anchored in time and place |
| `semantic` | Facts and concepts, generalized, time-independent |
| `procedural` | Sequences, steps, skills, "how to do X" |

**Default mapping for capture-time inference**:

| pebble_type | default memory_kind |
|-------------|---------------------|
| `experience_capture` | `episodic` |
| `insight` | `semantic` (overridable) |
| `problem_statement` | `episodic` |
| `proposed_solution` | `episodic` (may promote to `procedural` if step-structured) |
| `reference` | `semantic` |
| `ontology` | `semantic` |

#### 10.4 modality (controlled vocabulary, top-level)

| Value | Meaning |
|-------|---------|
| `kinetic` | Action occurred, observable behavior, externally verifiable |
| `non_kinetic` | Thought, plan, observation, internal state, not yet acted on |

See Appendix E.

#### 10.5 category (controlled vocabulary)

`foundational | vision | technical | insight | problem`

#### 10.6 emotional_state (Plutchik 8 Primary)

`joy | sadness | anger | fear | surprise | disgust | trust | anticipation`

See Appendix B.

#### 10.7 intent (controlled vocabulary)

`remember | act_on | share | think_about`

#### 10.8 governed_by (1:many ontology references)

```yaml
governed_by:
  - label: <human-readable label>
    uid: <ULID of the ontology pebble>
```

See §11.

#### 10.9 location.venue_type (controlled vocabulary)

`home | office | coffee_shop | transit | outdoor | other`

#### 10.10 status (lifecycle)

`draft | active | annotated | published | archived | tombstoned | superseded`

#### 10.11 Lifecycle fields (curator-editable)

| Field | Type | Description |
|-------|------|-------------|
| `pin` | bool | Never auto-archive regardless of policy |
| `archive_at` | ISO 8601 | Scheduled archival timestamp (full timestamp required) |
| `protected` | bool | Requires explicit user action to archive |
| `status_changed_at` | ISO 8601 | Last lifecycle transition timestamp |
| `status_reason` | string | Why this status (curator note) |

#### 10.12 weight (optional, legacy)

Optional human-assigned importance, 0.0–1.0. See §7. Deferred for review post-v1 (see `.sop/synthesis/15-weight-field-citation-research.md`).

#### 10.13 Fluid fields

Any additional YAML key is valid. Implementations MUST round-trip unknown keys without data loss. See §12.3.

---

### 11. Ontology Governance

Pebbles makes claims. **Ontologies are the ground truth that validates them.** Every pebble may link to one or more ontology pebbles via `governed_by`, and an agent walking those links can verify the pebble's assertions against the ontology's internal structure.

**Mental model** (Palantir Foundry parallel):

| Pebbles | Foundry |
|---------|---------|
| Pebble (any type) | Data instance / row |
| `pebble_type: ontology` | Object Type definition |
| `governed_by` link | Instance-of relationship |
| Agent ontology walk | Foundry Object Type traversal |

An ontology pebble has the same `pebble.md` shape as any other pebble, but its body is a **structured, agent-traversable representation** of a domain (a roster, a taxonomy, a calendar, a ledger, a policy). Format candidates for the body are deferred to Phase 1 (YAML-LD, JSON-LD, or Mermaid graph).

**Linking mechanics**:
- `governed_by` is a top-level field on every pebble that needs ontological grounding
- It is curator-editable (can be added at capture time or post-creation)
- It is red-string-eligible — pebbles sharing an ontology are automatically connected
- It is also surfaced as a typed edge (`governed_by`) in the edges table for graph traversal

**Example** (meeting capture with ontology validation):

```yaml
---
pebble_id: 01HZJ3K8P7M4R5VYX2W9NQBCDE
created_at: 2026-04-13T14:32:00Z
pebble_type: experience_capture
memory_kind: episodic
modality: kinetic
emotional_state: surprise
governed_by:
  - label: finance-ledger
    uid: 01HZJ3K8P7M4R5VYX2W9NQBCFG
  - label: meeting-roster
    uid: 01HZJ3K8P7M4R5VYX2W9NQBCHJ
  - label: fiscal-calendar
    uid: 01HZJ3K8P7M4R5VYX2W9NQBCJK
---
X claimed Q3 revenue was $12M — Finance ledger shows $9.4M.
```

An agent walking `governed_by` can verify the claim against `finance-ledger` (does the ledger show $12M or $9.4M for Q3?), confirm X's authority via `meeting-roster` (is X the right person to make this claim?), and resolve "Q3" against `fiscal-calendar` (which dates does Q3 cover?). All asynchronously. Without an LLM if the ontology pebbles are structured enough.

**Provenance and trust**: ontology pebbles are themselves pebbles, so they have the same lifecycle, edge, and curation properties. An ontology pebble can be `governed_by` a higher-level meta-ontology if the implementer wants a ground-truth-of-ground-truths layer. The spec does not mandate this; one level of governance is sufficient for v0.3.

---

### 12. Versioning, Migration & Curation Rights

#### 12.1 Curation Rights

The curation layer (Layer 2) is **explicitly empowered to edit any curator-editable field in a pebble's YAML, and to add or remove typed edges, at any time, subject to RBAC permissions.** This is a curation operation. It is **not** a schema versioning event. Reindexing is triggered automatically by the indexer.

> Editing a field is a curation operation, not a schema migration. A curator refining tags on a fleeting pebble in spec v0.3 is a v0.3 operation, not a v0.2 → v0.3 migration event.

#### 12.2 Schema Versioning (Wire Format)

Schema versioning governs **wire format compatibility between producers and consumers** of pebbles. It does not govern individual pebble mutability.

| Bump | Trigger |
|------|---------|
| **MAJOR** | Spec-breaking — removed fields, renamed fields, removed enum values, tightened constraints |
| **MINOR** | Additive — new fields, new enum values, new optional constraints |
| **PATCH** | Documentation, typos, clarifications, no schema impact |

#### 12.3 Unknown Field Preservation

**All implementations at every layer MUST round-trip unknown YAML keys without data loss.** This is the single most important rule for viral adoption: a writer at spec v0.4 can emit fields a v0.3 reader doesn't understand, and the reader must preserve them on write-back.

A v0.3 reader that strips unknown keys on save is non-conforming.

#### 12.4 Migration Determinism

Migration only runs on a **MAJOR** version bump. Migrations live in a numbered `migrations/` directory, are pure deterministic transformations, and are never LLM-assisted.

Example: v0.2 → v0.3 migration includes:
- `uku_id` → `pebble_id` (rename)
- `uku_type: ontology_element` → `pebble_type: ontology`
- `uku_type` → `pebble_type` (rename)
- Drop `consolidation_level` from YAML if present (now derived)
- Convert any date-only temporal values to full ISO 8601 with `T00:00:00Z`

#### 12.5 Compatibility Matrix

| Writer | Reader v0.2 | Reader v0.3 | Reader v1.0 |
|--------|-------------|-------------|-------------|
| v0.2 | full | lossy-read with migrate-on-load | migrate |
| v0.3 | error | full | lossy-read |
| v1.0 | error | error | full |

- **full**: reader and writer on same version
- **lossy-read**: newer reader sees older pebble, doesn't error, may miss new derived fields
- **migrate**: deterministic upgrade before read

---

### 13. Example Pebble

```yaml
---
title: "SAGE + ByteRover alignment moment"
pebble_id: 01HZJ3K8P7M4R5VYX2W9NQBCDE
created_at: 2026-03-21T08:12:00Z
url: "https://x.com/kevinnguyendn/status/2035366573192753648"

pebble_type: insight
memory_kind: semantic
modality: non_kinetic
category: vision

emotional_state: joy
intent: act_on

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

**Red strings this pebble automatically creates:**
- Every other pebble with `emotional_state: joy`
- Every other pebble with `intent: act_on`
- Every other pebble with `pebble_type: insight` and `category: vision`
- Every other pebble with `modality: non_kinetic`
- Every other pebble with `memory_kind: semantic`
- Every other pebble tagged `pebbles`, `sage`, `byterover`, or `interspecies`
- Every other pebble at `venue_type: coffee_shop`
- Every other pebble `governed_by` `pebbles-roadmap` or `triad-architecture`
- No manual linking required. The wall does the work.

**Curation can subsequently**:
- Refine tags as the vocabulary converges
- Add `governed_by` ontology links as new ontology pebbles are created
- Promote to a permanent pebble via §6.3, creating a new L1 markdown-native pebble with `derived_from` edge back to this one
- Update `status`, set `archive_at`, or mark `pin: true`

The body, `created_at`, `url`, and `pebble_id` remain capture-immutable.

---

### Appendix A: Luhmann Test

A field is **permanent** (graph-eligible, red-string eligible) if its value is understandable without the context in which it was written. A stranger should be able to read the value and know what it means.

- `emotional_state: joy` — passes (stranger understands "joy")
- `why_captured: "Kevin just replied"` — fails (stranger doesn't know Kevin)

The test is adopted from the Zettelkasten method (Luhmann 1952). The same test governs L0 → L1 promotion (see §6.3): a fleeting pebble graduates to permanent only when its body content can be re-expressed in own-words form that a stranger can understand.

---

### Appendix B: Plutchik 8 Primary (emotional_state)

Controlled vocabulary for the `emotional_state` field:

`joy`, `sadness`, `anger`, `fear`, `surprise`, `disgust`, `trust`, `anticipation`

Source: Plutchik, R. (1980). *Emotion: A Psychoevolutionary Synthesis*. New York: Harper & Row. The 8-emotion primary set is the inner ring of Plutchik's wheel of emotions.

**Note**: prior versions of this spec labeled this set "Ekman 8." That label was incorrect. Ekman's canonical set is 6 emotions (anger, disgust, fear, happiness, sadness, surprise) and adds contempt as a seventh. The 8-value vocabulary used here — which adds `trust` and `anticipation` — is Plutchik's primary set, not Ekman's. The vocabulary is unchanged; only the label is corrected.

The fuller Plutchik wheel includes 8 secondary emotions and intensity gradients (24 total values), which is **not** adopted here. 8 primary values gives 3 bits of entropy per pebble — the sweet spot between resolving power and capture-time cognitive load. More granularity would break interference immunity (narrower buckets, noisier matches) and break human classification reliability.

---

### Appendix C: Graph-Eligible Fields

Fields whose values pass the Luhmann Test:

| Field | Values | Red-string quality |
|-------|--------|--------------------|
| `pebble_type` | 6 controlled values | High — clusters by descriptor nature |
| `memory_kind` | 3 controlled values | High — clusters by cognitive classification |
| `modality` | 2 controlled values | High — kinetic/non-kinetic 50% split |
| `category` | 5 controlled values | High — clusters by domain |
| `status` | 7 controlled values | Medium — lifecycle tracking |
| `tags` | user-defined, lowercase | High — primary association surface |
| `emotional_state` | Plutchik 8 Primary | High — experiential clustering |
| `intent` | 4 controlled values | High — action-oriented clustering |
| `governed_by` | references to ontology pebbles | High — ground truth anchoring |
| `location.city` | normalized | Medium — geographic clustering |
| `location.venue_type` | 6 controlled values | Medium — situational clustering |

---

### Appendix D: Bibliography

- Anderson, J. R. & Schooler, L. J. (1991). "Reflections of the environment in memory." *Psychological Science* 2:396–408.
- Bjork, R. A. & Bjork, E. L. (1992). "A new theory of disuse and an old theory of stimulus fluctuation." In Healy, A. F. (ed.) *From Learning Processes to Cognitive Processes*.
- Brown, S. *The C4 Model for Visualising Software Architecture*. https://c4model.com/
- Ekman, P. (1992). "An argument for basic emotions." *Cognition and Emotion* 6(3-4):169-200. (For comparison; Pebbles uses Plutchik, not Ekman.)
- Gopinath, S., Starenky, K., Barman, V., Bodnar, A., Narasimhan, K. (2026). *The Price of Meaning: Why Every Semantic Memory System Forgets*. arXiv 2603.27116v1. Local copy: `_research/_papers/noescape-28MAR26.pdf`.
- Kepano (Steph Ango). *File over app*. https://stephango.com/file-over-app
- Luhmann, N. (1952–1997). The Zettelkasten slip-box method, documented across his published reflections on note-taking practice.
- McClelland, J. L., McNaughton, B. L. & O'Reilly, R. C. (1995). "Why there are complementary learning systems in the hippocampus and neocortex." *Psychological Review* 102(3):419–457.
- O'Brien, M. *Brain.md*. Rho repository. https://github.com/mikeyobrien/rho/blob/main/docs/brain.md
- Obsidian Rocks. *Getting Started with Zettelkasten in Obsidian*. https://obsidian.rocks/getting-started-with-zettelkasten-in-obsidian/
- Palantir Foundry Ontology (concept reference). https://www.palantir.com/docs/foundry/ontology/overview/
- Plutchik, R. (1980). *Emotion: A Psychoevolutionary Synthesis*. New York: Harper & Row.
- Tulving, E. (1972). "Episodic and semantic memory." In Tulving, E. & Donaldson, W. (eds.) *Organization of Memory*.
- ULID Specification. https://github.com/ulid/spec
- Pebbles RQ1 + RQ2 Analysis Artifact (27 MAR 2026). Internal design document.
- Pebbles Grok Adversarial Debate (29 MAR 2026). Internal design stress test.

---

### Appendix E: Modality Vocabulary

The `modality` field encodes whether a pebble represents an action (kinetic) or a thought/internal state (non-kinetic). It is a top-level field, orthogonal to `intent`, `pebble_type`, and `memory_kind`.

| Value | Definition | Examples |
|-------|------------|----------|
| `kinetic` | Action occurred, observable behavior, externally verifiable | Sent email, met with person, took screenshot, walked into building, made payment |
| `non_kinetic` | Thought, plan, observation, internal state, not yet acted on | Idea, draft, intent, observation, hypothesis, draft email, proposed solution |

**Edge case**: `mixed` is **not** a permitted value. Moments that contain both action and thought ("I had this thought while walking") should be atomized into two separate pebbles (one kinetic, one non-kinetic) linked via a `co_occurred_with` typed edge.

**Why a binary**: a 2-way split cuts query space ~50% on every modality-filtered query, with maximum interference immunity (only 2 buckets) and effortless human classification (any user can answer "was it an action or a thought?" in under a second).

**Cognitive grounding**:
- **Episodic vs Semantic memory** (Tulving 1972) — kinetic events are typically episodic; non-kinetic thoughts are typically semantic. The CLS hypothesis (McClelland 1995) operationalizes this same split.
- **Mirror neurons** (Rizzolatti) — observed actions activate distinct neural circuits, suggesting kinetic events have a physiologically privileged encoding.
- **Telic/atelic verb aspect** (Vendler 1957) — many languages mark this distinction in verb morphology, suggesting it is cognitively load-bearing.

---

### Appendix F: memory_kind — CLS / Zettelkasten Lineage

The `memory_kind` field encodes the cognitive classification of how a pebble should be retrieved and consolidated. It is orthogonal to `pebble_type` (which encodes user framing).

| Value | Encoding | Retrieval | Consolidation |
|-------|----------|-----------|---------------|
| `episodic` | Specific events, full detail, anchored in time/place | "When did I…", "What happened when…" | Walks the L0 → L1 → L2 → L3+ gradient over time |
| `semantic` | Facts, concepts, generalized | "What is…", "Define…" | Born at L1 or above; abstracted, time-independent |
| `procedural` | Sequences, steps, skills | "How do I…" | Resists L3+ abstraction; recipes stay concrete |

#### Dual lineage

Pebbles' four-level consolidation hierarchy (L0 → L3+) appears independently in two traditions, 43 years apart:

- **Complementary Learning Systems** (McClelland, McNaughton & O'Reilly 1995): the brain uses fast hippocampal episodic encoding *and* slow neocortical semantic consolidation, with a gradient between them. Episodic memories are gradually abstracted into semantic knowledge by repeated reactivation.
- **Zettelkasten** (Luhmann 1952): fleeting notes (raw captures) are refactored into permanent atomic notes (own words, linked, self-contained), grouped into Maps of Content, and synthesized into structural notes. The same four levels.

| L | CLS | Zettelkasten | Pebble |
|---|-----|--------------|--------|
| L0 | Episodic, raw, hippocampal | Fleeting note (no context, temporary) | Wrapper for any artifact |
| L1 | Consolidation gradient (partial abstraction) | Permanent atomic note (own words, linked) | Markdown-native, `derived_from` L0 |
| L2 | Consolidation gradient (themed grouping) | Map of Content | Markdown-native, `contains` L1 |
| L3+ | Semantic, abstracted, generalized | Structural note (Hauptzettel) | Markdown-native, `contains` L2+ |

That a paper-based 1950s note-taking system and a 1995 cognitive science hypothesis independently arrived at the same four-level structure is structural confirmation that the gradient is load-bearing, not a metaphor. Pebbles is the operationalization of both as a structured YAML format.

#### Promotion semantics

See §6.3 for the four graduation criteria (atomic, Luhmann Test passing, own words, linked) that govern L0 → L1 promotion. The "own words" rule is where Zettelkasten contributes the explicit reconsolidation primitive that CLS as a hypothesis does not provide.

---

### Appendix G: Integration Patterns (Non-Normative)

This appendix describes **optional** integrations between Pebbles and external runtime systems. **None of these are required for conformance.** Pebbles is a sovereign, self-contained spec; the integrations below are example tool calls that a Curation or Inference layer implementation may invoke.

#### G.1 SAGE — consensus validation, signing, BFT

**What SAGE provides**:
- Byzantine Fault Tolerant consensus across a swarm of validator agents
- Proof-of-Expertise weighted voting (accuracy, domain expertise, recency, corroboration)
- Cryptographic provenance via Ed25519 keypairs
- Contradiction detection via dedicated validators

**Where Pebbles can invoke it**:
- During **Curation** (Layer 2) as a tool call — e.g., "validate this `governed_by` ontology link against consensus" or "have validators check this claim's consistency with the rest of the vault"
- During **Inference** (Layer 4) as a tool call — e.g., "does this proposed insight contradict consensus-held facts?"

**What Pebbles does NOT inherit from SAGE**: encryption, key management, RBAC enforcement, federation. These remain SAGE concerns; Pebbles' RBAC is independent.

SAGE is a runtime; Pebbles is a file format. They compose cleanly when both are present, and Pebbles works fully without SAGE.

#### G.2 ByteRover — semantic swarm retrieval

**What ByteRover provides**:
- Memory Swarm fusing BM25 + wikilink graph expansion + hybrid vector+keyword retrieval
- Reciprocal Rank Fusion (RRF) of decorrelated retrieval methods
- Strong empirical results on long-term conversational memory benchmarks

**Where Pebbles can invoke it**:
- During **Inference** (Layer 4) as a tool call — e.g., "expand this red-string query with semantic reasoning across the index"
- ByteRover consumes Pebbles' Query layer output as one of its retrieval methods

**What Pebbles does NOT inherit from ByteRover**: a vector database, an embedding model, RRF logic. These remain ByteRover concerns. Pebbles provides interference-immune red-string retrieval as one decorrelated method that ByteRover (or any other swarm) can fuse with its own.

#### G.3 Other Integration Patterns

The Curation and Inference layers may invoke any tool. SAGE and ByteRover are named here as concrete examples, not as a recommended set. Other patterns (knowledge graph backends, vector stores, agent frameworks, LLM tool servers) compose the same way: as tool calls from Curation or Inference, never as core dependencies.

The **No-Escape Theorem** (Gopinath et al. 2026; see Appendix D) proves that the only principled architecture for long-term semantic memory is "exact episodic record + external symbolic verifier + semantic reasoning layer." Pebbles implements the exact episodic record. The other two components are reachable via Curation (verifier) and Inference (semantic reasoning) tool calls. Different deployments will plug in different tools to fill those roles.
