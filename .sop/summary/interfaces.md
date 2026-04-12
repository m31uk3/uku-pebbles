# Interfaces and APIs

## Overview

This repository defines interfaces at the specification level. No running API exists yet. The interfaces documented here are from the UKU spec (v0.2.3) and the specified integration surface with SAGE and ByteRover.

## UKU Schema Interface

### File Format
- **Container:** Markdown file with YAML frontmatter
- **Naming:** Not yet specified (ai-pebbles used `{YYYY-MM-DD}_{uuid}.md`)
- **Source of truth:** The `.md` file itself; index is a derived cache
- **Sovereignty:** RBAC-governed writes; any actor (human or agent) with permission can edit

### Required Fields
| Field | Type | Description |
|-------|------|-------------|
| title | string | Short title or first sentence |
| uku_id | string | Unique ID (format: `uku-YYYYMMDD-hexstring`) |
| created_at | ISO 8601 | Capture moment timestamp |
| uku_type | enum | `experience_capture`, `insight`, `problem_statement`, `proposed_solution`, `ontology_element` |
| category | enum | `foundational`, `vision`, `technical`, `insight`, `problem` |

### Optional Fields
| Field | Type | Description |
|-------|------|-------------|
| url | string | Artifact reference (tweet, document, webpage) |
| source_id | string | Artifact identifier (e.g., `tweet-1234567890`) |
| emotional_state | enum | Ekman 8: `joy`, `sadness`, `anger`, `fear`, `surprise`, `disgust`, `trust`, `anticipation` |
| intent | enum | `remember`, `act_on`, `share`, `think_about` |
| context_elements | object | `why_captured` (prose), `surrounding_activity` (prose) |
| location | object | `city` (normalized), `venue_type` (enum: `home`, `office`, `coffee_shop`, `transit`, `outdoor`, `other`) |
| tags | array[string] | User-defined lowercase strings |
| weight | float | Explicit importance (0.0-1.0) |
| status | enum | `draft`, `annotated`, `published`, `archived` |

### Fluid Fields
Any additional YAML key-value pair is valid. The schema is intentionally open-ended. Convergence emerges from API-level guardrails during ingestion/curation, not from schema enforcement.

## Four-Tier Ingestion Interface

| Tier | Source | Friction | Examples |
|------|--------|----------|----------|
| 1 | Auto-captured from device/browser | Zero | timestamp, device, GPS, active_url, file_ref, content_hash |
| 2 | Human moment (mini-tweet + quick-tag) | 3-5 sec | intent, emotional_state, people, tags |
| 3 | Inferred without LLM | Zero | venue_type from GPS, source_type from file extension |
| 4 | LLM-assisted inference (async) | Zero | Optimal attribute assignment using payload + existing index |

## Relationship Interfaces

### Red Strings (Implicit, Symmetric)
Any matching YAML key-value pair across pebbles creates an automatic connection. Computed on-demand from the JSONB+GIN index. Nothing written back to files.

**Graph-eligible fields (high red-string quality):**
| Field | Values | Quality |
|-------|--------|---------|
| uku_type | 5 controlled values | High |
| category | 5 controlled values | High |
| tags | user-defined, lowercase | High |
| emotional_state | Ekman 8 | High |
| intent | 4 controlled values | High |
| status | 4 controlled values | Medium |
| location.city | normalized | Medium |
| location.venue_type | 6 controlled values | Medium |

**Luhmann Test:** A field is graph-eligible if its value is understandable without context. A stranger should know what it means. `emotional_state: joy` passes. `why_captured: "Kevin just replied"` fails.

### Typed Edges (Optional, Explicit, Directional)
Stored in a separate edges table. Created during Curation by actors with RBAC write access.

| Edge Type | Description |
|-----------|-------------|
| derived_from | L1 consolidation -> source L0 pebble(s) |
| contains | L2 MOC -> grouped pebbles |
| supports | Reasoning chain: A reinforces B |
| contradicts | Reasoning chain: A conflicts with B |
| supersedes | Version replacement |

**Progressive enhancement:** System works fully with red strings alone. Typed edges add consolidation hierarchy without breaking core functionality.

## Weighting Interface

Three-layer weighting model:

| Layer | Source | Written to File? |
|-------|--------|-----------------|
| Explicit | `weight` field (0.0-1.0), human-set | Yes |
| Implicit | access_count, update_count, reference_count, last_accessed_at, last_updated_at | No (index only) |
| Effective | Agent-computed combination: explicit + implicit + time decay + pattern signals | No (index only) |

**Pattern weights:** If a category is accessed 10x more, or a tag spans many high-weight pebbles, agents detect and boost/dampen accordingly.

## Consolidation Hierarchy Interface

| Level | Type | Description |
|-------|------|-------------|
| L0 | Raw pebbles | Experience captures, insights, problems |
| L1 | Consolidations | Derived pebbles linking via `derived_from` edge |
| L2 | Maps of Content (MOCs) | Pebbles linked via `contains` edge |
| L3+ | Meta-syntheses | Higher-order structures |

Each higher-order pebble is itself a pebble (same `.md` + YAML format). Hierarchy expressed in edges table, not frontmatter.

## Storage & Indexing Interface

### Recommended: Postgres + JSONB + GIN

**Core table (pebbles):**
| Column | Type | Purpose |
|--------|------|---------|
| uku_id | text PK | Unique identifier |
| file_path | text | Path to source `.md` file |
| yaml_data | JSONB | Parsed YAML frontmatter |
| body_text | text | Markdown body |
| indexed_at | timestamp | When last indexed |
| access_count | integer | Behavioral signal |
| update_count | integer | Behavioral signal |
| reference_count | integer | Behavioral signal |
| last_accessed_at | timestamp | Behavioral signal |
| last_updated_at | timestamp | Behavioral signal |
| effective_weight | float | Agent-computed |

**Edges table (optional):**
| Column | Type | Purpose |
|--------|------|---------|
| source_id | text FK | Source pebble |
| target_id | text FK | Target pebble |
| edge_type | text | Relationship type |
| created_by | text | Actor who created the edge |
| created_at | timestamp | When created |

**GIN index** on `yaml_data` enables sub-millisecond compound faceted search on any YAML field.

**Optional:** `pgvector` column for future semantic search.

## SAGE Integration Interface (Specified but Not Built)

| UKU Operation | SAGE Endpoint | Purpose |
|---------------|--------------|---------|
| Submit UKU for validation | POST /v1/memory/submit | UKU YAML -> SAGE MemoryRecord |
| Receive consensus result | GET /v1/memory/{id} | Validation status + confidence |
| Agent enrichment writeback | Curation layer update | Consensus results -> interspecies_cache |
| Access control check | RBAC gates | Per-domain, per-clearance, with expiry |

### Field Mapping (UKU <-> SAGE)
| UKU Field | SAGE Field | Gap |
|-----------|------------|-----|
| uku_type | memory_type | Different taxonomies, bidirectional mapping needed |
| tags | memory_tags | Compatible |
| status (draft/published) | status (proposed/committed) | Different lifecycles, handoff points needed |
| (missing) | domain_tag | UKU needs this field |
| (missing) | clearance_level | UKU needs this field |
| (missing) | content_hash | UKU needs SHA-256 for SAGE dedup validator |

## ByteRover Integration Interface (Specified but Not Built)

| UKU Operation | ByteRover Component | Purpose |
|---------------|-------------------|---------|
| Query results -> retrieval | ContextEngine.assemble() | Prompt-aware selective retrieval from UKU index |
| Backward recall | .brv/context-tree | State management for associative recall |
