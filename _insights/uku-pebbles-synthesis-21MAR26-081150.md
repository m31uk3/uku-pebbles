# UKU-Pebbles Synthesis

## ai-pebbles (Foundation)

A schema specification for capturing personal knowledge enriched with experiential metadata (intent, emotional state, device context, recall associations) at the moment of capture. Follows an ontological data model with three tiers (Required, Enrichment, Relations), uses a privacy-first on-device inference engine (NAI), and targets a Chrome extension as the v0 client. Status: requirements clarification done, detailed design pending, with extensive open questions around agents, sync, platform APIs, and the "human in the mesh" concept.

## uku-pebbles (Evolution / Collaboration Fork)

### Spec (uku-pebbles.spec.md)

Reframes each Pebble as a **Universal Knowledge Unit (UKU)** — same core philosophy but now explicitly designed for **interspecies shared caching** (human + agent memory). Adds an `interspecies_cache` block (human_perspective, agent_perspective, shared_caching_layer_score) and integrates with two external systems:

- **SAGE** — BFT consensus validators that auto-enrich UKUs with confidence scores, decay factors, and agent perspectives (prevents "memory drift")
- **ByteRover** — `.brv/context-tree` for selective retrieval/state management

### Discussion (21 Mar 2026 X Thread)

Captured thread between @m31uk3 (Luke Jackson), @kevinnguyendn (Andy Nguyen / ByteRover), and @l33tdawg (SAGE). Andy's OpenClaw PR enabled prompt-aware context assembly; he recognized Pebbles as the missing schema layer. The three projects attack "agent amnesia" from complementary angles:

- **Schema** — Pebbles (UKU spec)
- **Validation** — SAGE (BFT consensus)
- **Retrieval** — ByteRover (.brv/context-tree)

Group agreed to collaborate on a sovereign agent memory standard.

## Significance

The UKU spec represents Pebbles evolving from a personal knowledge capture tool into a foundational **interspecies memory standard** — a schema that lets both humans and AI agents share, validate, and retrieve knowledge units with full provenance, consensus integrity, and experiential context. The three-project triad (Pebbles/SAGE/ByteRover) covers the full stack needed to make this work.
