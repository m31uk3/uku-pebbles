# Workflows

## Four-Layer Processing Pipeline

```mermaid
sequenceDiagram
    actor User
    participant Capture as Capture Surface
    participant Ingest as Layer 1: Ingestion
    participant Index as Postgres JSONB+GIN
    participant Curate as Layer 2: Curation
    participant Query as Layer 3: Query
    participant Infer as Layer 4: Inference (Optional)

    Note over User,Infer: Deterministic Core (Layers 1-3, zero LLM)

    User->>Capture: Capture moment (screenshot, note, bookmark)
    Capture->>Ingest: Raw artifact + device context

    Note over Ingest: Tier 1: Auto-capture (zero friction)
    Ingest->>Ingest: Extract timestamp, device, GPS, URL, content_hash

    Note over Ingest: Tier 2: Human moment (3-5 sec)
    User->>Ingest: Intent, emotional_state, tags (mini-tweet)

    Note over Ingest: Tier 3: Deterministic inference (zero friction)
    Ingest->>Ingest: venue_type from GPS, source_type from extension

    Ingest->>Index: Write .md file + parse YAML to JSONB

    Note over Curate: Actor-agnostic (human or agent, RBAC-governed)
    Curate->>Index: Create typed edges, build consolidation hierarchy
    Curate->>Curate: Update .md files + index together

    Note over Query: Pure deterministic retrieval
    Query->>Index: Red-string match (JSONB+GIN) + edge traversal
    Index-->>Query: Structured results

    Note over Infer: Optional, separate process
    Query-->>Infer: Structured results only
    Infer->>Infer: LLM reasoning, synthesis, suggestions

    Note over Ingest: Tier 4: LLM-assisted (async, zero friction)
    Infer-->>Curate: Suggested enrichments back to Curation
    Curate->>Index: Apply enrichments (RBAC-governed)
```

### Error Handling
| Scenario | Handling |
|----------|----------|
| YAML parse failure | Reject at ingestion; file not indexed |
| Missing required fields | Reject at ingestion; log validation error |
| Inference layer unavailable | System fully functional on Layers 1-3 only |
| Edge target not found | Cascading delete cleans up orphan edges |
| GIN index corruption | Rebuild from source `.md` files (files are truth) |

---

## Capture Flow (Specified UX)

Three capture modes (user preference):

```mermaid
sequenceDiagram
    actor User
    participant UI as Capture Surface
    participant Ext as Chrome Extension / System Override

    alt Silent Mode
        Ext->>Ext: Auto-capture: timestamp, device, URL, GPS
        Ext->>Ext: Tier 3 inference: venue_type, source_type
        Ext->>Ext: Write .md + index
        Note over User: No UI shown
    else Minimal Mode
        User->>UI: Trigger capture (hotkey / button)
        UI->>User: Show 3 inputs + emoticon picker + location dropdown
        User->>UI: Fill in ~3-5 seconds
        UI->>Ext: Tier 1 + 2 + 3 fields
        Ext->>Ext: Write .md + index
    else Full Mode
        User->>UI: Trigger capture
        UI->>User: Show all available fields for review/edit
        User->>UI: Review, edit, submit
        UI->>Ext: All tier fields
        Ext->>Ext: Write .md + index
    end

    Note over Ext: Tier 4 (async): LLM considers payload + existing index state
    Ext->>Ext: Suggested enrichments queued for Curation
```

**Collapsible drill-down:** Start at user's preferred level, go deeper when desired.

---

## Red-String Query Flow

```mermaid
sequenceDiagram
    actor User
    participant QRY as Query Layer
    participant GIN as JSONB+GIN Index

    User->>QRY: "Show me everything tagged 'pebbles' when I was joyful"
    QRY->>GIN: SELECT * FROM pebbles<br/>WHERE yaml_data @> '{"tags":["pebbles"]}'<br/>AND yaml_data @> '{"emotional_state":"joy"}'
    GIN-->>QRY: Matching pebbles (sub-millisecond)
    QRY->>QRY: Apply weighting (effective_weight sort)
    QRY-->>User: Ranked results with red-string connections highlighted
```

Red strings are computed at query time. No precomputed link table needed for implicit connections.

---

## Curation Workflow

```mermaid
sequenceDiagram
    actor Actor as Human or Agent (RBAC-governed)
    participant Files as Markdown Files
    participant Index as Postgres Index
    participant Edges as Edges Table

    Note over Actor,Edges: Any actor with RBAC write permission

    alt Edit existing pebble
        Actor->>Files: Modify YAML frontmatter or body
        Actor->>Index: Re-index modified file
    else Create typed edge
        Actor->>Edges: INSERT (source, target, type, actor, timestamp)
    else Build consolidation
        Actor->>Files: Create new L1/L2/L3 pebble (.md file)
        Actor->>Edges: Create derived_from or contains edges
        Actor->>Index: Index new pebble
    end
```

**Key principle:** Files and index are always updated together during curation. Enrichments are deliberate actions, not background side effects.

---

## SAGE Integration Pipeline (Specified, Not Built)

```mermaid
sequenceDiagram
    participant UKU as UKU Pebble
    participant MCP as SAGE MCP Tool
    participant BFT as CometBFT Consensus
    participant VAL as 4 Validators
    participant POE as PoE Scoring
    participant WB as Writeback

    UKU->>MCP: sage_remember (UKU YAML content)
    MCP->>BFT: Submit as MemoryRecord
    BFT->>VAL: Pre-validate (sentinel, dedup, quality, consistency)
    VAL-->>BFT: 3/4 quorum reached

    BFT->>POE: PoE weighted voting
    POE-->>BFT: Confidence score + validator rationales

    BFT-->>MCP: Consensus result (validated/challenged)
    MCP-->>WB: Enriched data (confidence, decay, agent_perspective)
    WB->>UKU: Update interspecies_cache in frontmatter

    Note over WB,UKU: Writeback model TBD:<br/>modify in-place vs. create enriched version
```

### Open Integration Questions (from TODO.md)
- UKU-to-SAGE submission pipeline: UKU YAML -> MCP sage_remember -> consensus -> enriched writeback
- Writeback model: modify original `.md` in-place or create enriched version?
- Type mapping: uku_type <-> SAGE memory_type bidirectional
- Status lifecycle handoff: draft/published -> proposed/committed
- Consent reconciliation: UKU consent model <-> SAGE access grants

---

## Research & Design Methodology

```mermaid
sequenceDiagram
    actor Luke as Luke Jackson
    participant AI as ai-pebbles (42 iterations)
    participant Thread as X Thread (Mar 21)
    participant Triad as Triad Discovery
    participant UKU as uku-pebbles

    Luke->>AI: Found ai-pebbles: 16 docs, 271 verification scripts
    Note over AI: Requirements clarification + detailed design

    Luke->>Thread: Post "interspecies shared caching layer" thesis
    Thread->>Thread: Andy (ByteRover) + l33tdawg (SAGE) respond
    Thread->>Triad: Three projects recognize structural compatibility

    Triad->>UKU: Fork concept: delegate validation + retrieval
    UKU->>UKU: Reframe: pebble-as-descriptor, 4-layer arch
    UKU->>UKU: Grok adversarial debate -> design implications
    UKU->>UKU: PDD requirements clarification (10 questions)
    UKU->>UKU: Spec v2.1 -> v2.2 -> v2.3
```

### Evolution Arc
1. **ai-pebbles** -- Solo monolithic specification (schema + app + sync + search + agents + economics)
2. **Triad discovery** -- SAGE and ByteRover solve validation, retrieval, and encryption
3. **uku-pebbles** -- Focused specification (schema + capture format + integration contracts)
4. **Grok debate** -- Adversarial stress-testing produces pebble-as-descriptor, compile-time LLM boundary
5. **v2.3** -- Current: atomized fields, 4-layer architecture, 4-tier ingestion, weighting model
