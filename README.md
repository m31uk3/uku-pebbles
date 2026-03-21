# UKU-Pebbles

**Universal Knowledge Units — a format-independent schema for sovereign interspecies memory.**

## The Problem

Every capture tool today stores *what* you saved but discards *how you experienced it*. The surrounding context — why you saved it, what you were doing, how you felt, what you meant to do next — is stripped away the moment you hit save.

Agents have the same problem in reverse. They process your data but have no structured way to share what they learned back into your memory. The result is **agent amnesia**: agents that forget everything between sessions, and humans whose tools can't remember why anything mattered.

There is no standard format for preserving the relationship between information and lived experience — for either species.

## What UKU-Pebbles Is

**A schema specification** that defines a structured data model for personal knowledge enriched with experiential metadata — intent, context, emotional state, and recall associations — captured at the exact moment of creation.

Each unit is a **Universal Knowledge Unit (UKU)**: a single atomic piece of lived experience that both humans and agents can read, write, validate, and retrieve.

The specification is format-independent. YAML front-matter in Markdown is the v1 default binding — one UKU = one `.md` file you can open in any editor or Obsidian vault.

**The spec is the product.**

## How It Works

Every UKU has three sections:

**Header** — Immutable identity and provenance (system-generated, zero user input):
`uku_id`, `created_at`, `uku_type`, `title`, `source`, `content_hash`

**Metadata** — Experiential + interspecies context (human-provided at capture, agent-enriched after validation):
- **Context Elements** — why you captured it, what you were doing, how you felt, what you planned to do next
- **Interspecies Cache** — how the human experienced it, how agents interpret it, and a shared caching score that both species maintain. SAGE validators populate `agent_perspective`, `confidence`, and `decay_factor` through BFT consensus.

**Body** — Raw content in Markdown.

## The Triad

UKU-Pebbles didn't emerge in isolation. Three independent projects converged on the same problem — agent amnesia — from three complementary angles:

| Layer | Project | Role |
|-------|---------|------|
| **Schema** | [Pebbles](https://github.com/m31uk3/ai-pebbles) | Defines the knowledge unit structure |
| **Validation** | SAGE | BFT consensus prevents memory drift |
| **Retrieval** | ByteRover | `.brv/context-tree` for selective state |

This collaboration started with a thread on X (21 Mar 2026) — captured raw in [`_discussions/`](./_discussions/) — where the builders recognized they were solving the same problem from different ends of the stack. No coordination beforehand. Just convergence.

## Origin

This project grew out of [ai-pebbles](https://github.com/m31uk3/ai-pebbles), a solo effort to build a schema for personal knowledge capture with rich experiential metadata. The core insight — that *how you experience something* is as important as *what you captured* — remains foundational.

UKU-Pebbles extends that vision into **interspecies territory**: a shared memory layer where humans and agents co-author, validate, and recall knowledge together. The origin story is preserved unedited in [`_insights/`](./_insights/) and [`_discussions/`](./_discussions/).

## Design Principles

- **Capture-at-moment** — All experiential metadata is recorded at creation time, not retrofitted.
- **Human-first, agent-ready** — Every UKU is a readable Markdown file. Agents enrich, they don't own.
- **Sovereign & private** — Zero API calls by default. All inference runs on-device. No third-party services required for core storage or indexing. SAGE provides vault encryption and access control.
- **Consensus-ready** — Every UKU can be proposed to a validation layer for drift prevention.
- **Ontological data model** — Tags are not strings in an array — they are links to Tag objects. People are not names — they are links to Person objects. This semantic graph is what enables agents, recall, and emergent insight to operate with full understanding.
- **Tidy data invariant** — Every field is independently queryable. No composite prose strings. `emotional_state: "Excited + slightly annoyed"` is a defect; typed emotion enums with confidence and provenance are correct.
- **Pre-attentive attributes** — Auto-suggested metadata must be obviously right or obviously wrong, never ambiguous. We succeed or fail on capture friction.
- **Device-agnostic, device-aware** — The spec is universal — any device can produce a valid UKU. But the richness of experiential metadata varies by device. The spec accommodates both without requiring either.
- **Living** — Fields like `current_relevance` and `shared_caching_layer_score` evolve via background agents.
- **Format-independent** — The data model is abstract; YAML, TOML, JSON are serialization bindings.

## Architecture

```
Human captures UKU (Obsidian / Chrome Extension / Share Sheet)
        │
        ▼
    UKU (.md + YAML front-matter)
    Header + Context Elements + Interspecies Cache + Body
        │
        │ MCP payload
        ▼
    SAGE (Validation Layer)
    4 app validators → BFT consensus → PoE-weighted voting
        │
        ├── Enriched UKU writeback
        │   confidence + decay_factor + agent_perspective
        │
        └── ByteRover (Retrieval Layer)
            .brv/context-tree → ContextEngine.assemble(prompt)
            → selective retrieval → AI agents
```

## Repository Structure

```
├── _specs/          # UKU schema specification
├── _discussions/    # Raw origin conversations (unedited)
├── _insights/       # Synthesis and analysis
├── _research/       # Architecture and component research
└── README.md
```

## Get Involved

This is day one. The spec is draft, the collaboration is live, and the standard is being built in the open.

- Read the spec: [`_specs/uku-pebbles.spec.md`](./_specs/uku-pebbles.spec.md)
- Read the origin thread: [`_discussions/`](./_discussions/)
- Open an issue, propose a change, or build a client.

## License

MIT
