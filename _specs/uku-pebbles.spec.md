**Pebbles UKU Specification v0.1**  
**Universal Knowledge Unit – Format-Independent Schema for Sovereign Personal & Interspecies Memory**  
**Version:** 0.1 (March 2026)  
**Status:** Draft – open for collaboration with SAGE & ByteRover  

---

### 1. Introduction & Purpose

**Pebbles** defines a **schema specification** (not a file format) for capturing personal knowledge at the exact moment of creation.  

Every Pebble is a **Universal Knowledge Unit (UKU)** — a single atomic unit of lived experience enriched with:
- raw content
- experiential metadata (intent, context, emotional state)
- interspecies caching signals (how humans vs agents perceive/store it)

**Core goal:** Create sovereign, human-readable, machine-verifiable memory that:
- Never drifts (feeds SAGE’s BFT validators + consensus)
- Is instantly retrievable (feeds ByteRover’s .brv/context-tree)
- Works offline forever (Obsidian-native Markdown default)
- Enables true interspecies shared caching between humans and agents

The spec is **format-independent**. The abstract data model can be serialized as YAML, TOML, JSON, or any future binding.  
**YAML front-matter in Markdown files is the v1 default binding** (one UKU = one `.md` file + optional attached media).

---

### 2. Core Principles (Pebbles Design Tenets)

1. **Capture-at-moment** – All experiential metadata is recorded *at creation time* (not retrofitted).
2. **Human-first, Agent-ready** – Content must remain readable/editable by humans in any Markdown editor.
3. **Sovereign & Private** – No third-party services required for core storage or indexing.
4. **Consensus-ready** – Every UKU can be proposed to a validation layer (SAGE validators).
5. **Living** – Fields like `current_relevance`, `shared_caching_layer_score`, and `related_uku_ids` evolve over time via background agents.
6. **Interoperable** – Direct drop-in to Obsidian, ByteRover .brv trees, SAGE ledger, and future tools.

---

### 3. Abstract Data Model

A UKU contains exactly three top-level sections:
- **Header** – immutable identity & provenance
- **Metadata** – experiential + interspecies context
- **Body** – raw content (Markdown)

---

### 4. YAML Binding v1 (Default – Obsidian-native)

```yaml
---
title: "Short title or first sentence"                  # required
uku_id: "uku-20260321-abcdef"                          # required – stable, unique
created_at: "2026-03-21T02:59:00Z"                     # required – ISO 8601
url: "https://x.com/m31uk3/status/..."                 # optional
source_id: "tweet-1234567890"                          # optional (tweet_id, note_id, etc.)
metrics:                                               # optional – provenance signals
  likes: 42
  retweets: 12
  replies: 8
  views: 1234
  bookmarks: 5

# UKU Ontology
uku_type: experience_capture | insight | problem_statement | proposed_solution | ontology_element
category: foundational | vision | technical | insight | problem

context_elements:                                      # human experiential metadata (filled at capture)
  why_posted: "I was frustrated with agent amnesia again"
  surrounding_activity: "Working on SAGE validators while on a walk"
  emotional_state: "Excited + slightly annoyed"
  intended_next_action: "Build the one-click archive importer"
  current_relevance: "Still 100% relevant – this is the missing schema"

interspecies_cache:                                    # shared human/agent layer
  human_perspective: "This felt like a breakthrough moment"
  agent_perspective: ""                                # auto-filled by SAGE agents
  shared_caching_layer_score: high | medium | low      # auto-scored by consensus

tags:
  - universal-knowledge-unit
  - interspecies-caching
  - agent-memory
  - sovereign

related_uku_ids:                                       # bidirectional links
  - "uku-20260320-123456"
  - "uku-20260318-789012"

status: draft | annotated | published | archived
vector_ready: false                                    # for future local embeddings
confidence: 0.92                                       # added by SAGE validators (0.0–1.0)
decay_factor: 0.85                                     # natural decay (added by SAGE)
---
**Full content here** (Markdown body – tweet text, notes, images, code, etc.)
```

---

### 5. Field Reference & Enums

**uku_type** (required)  
- `experience_capture` – raw moment of lived experience  
- `insight` – distilled learning  
- `problem_statement` – pain point  
- `proposed_solution` – idea/plan  
- `ontology_element` – definition or taxonomy piece  

**category** (required)  
`foundational | vision | technical | insight | problem`

**shared_caching_layer_score**  
`high` (both human & agent cache it permanently) | `medium` | `low` (ephemeral)

**status**  
`draft` (human editing) | `annotated` | `published` | `archived`

**SAGE-added fields** (automatically populated on commit)  
- `agent_perspective`  
- `confidence`  
- `decay_factor`  
- `vector_ready`

---

### 6. Examples

#### Example 1: X Post UKU (auto-generated via importer)
(See your original UKU post for real data)

#### Example 2: Manual Capture (iOS Share Sheet style)
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
  current_relevance: "This is the collab that ships sovereign memory"
interspecies_cache:
  human_perspective: "Feels like the missing piece clicked"
  agent_perspective: ""
  shared_caching_layer_score: high
tags:
  - pebbles
  - sage
  - byterover
  - interspecies
status: draft
---
This feels like perfect timing! 🔥  

You’ve both basically built the runtime infrastructure for the schema spec I’ve been drafting all week...
```

---

### 7. Integration & Next Steps (v0.1)

- **Obsidian** → native (just open the vault)
- **SAGE** → every UKU write → 4 validators + BFT consensus → auto-enrich `agent_perspective`, confidence, decay
- **ByteRover** → direct mapping to `.brv/context-tree` (YAML front-matter already matches)
- **One-click importer** → Twitter Archive Parser + 30-line enrichment script (already built in our thread)

**Next (v0.2 planned)**  
- TOML & JSON bindings  
- Formal JSON Schema + validation library  
- Embedded vector spec  
- MCP standard payload definition
