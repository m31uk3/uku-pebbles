# UKU-Pebbles

**Universal Knowledge Units (UKUs) — Pebbles**
Sovereign, human-first memory units for interspecies collaboration.

## The Vision

Pebbles turn every capture (screenshot, note, tweet, photo, idea) into an atomic **Universal Knowledge Unit (UKU)** — a Markdown file with rich **YAML frontmatter** that records *what* happened *and* the lived context (emotional state, surrounding activity, intent, categories, etc.).

Inspired directly by the insight that "the simplest forms of memory work best with current LLMs" (Obsidian vaults + metadata for multi-dimensional search), Pebbles are the conspiracy board made real: every pebble is a note on the wall, and **every matching YAML key-value pair is an automatic red string**.

## v2.1 Architecture (Minimal & Optimal)

- **Source of Truth**: Plain Markdown + YAML files (sovereign, human-editable in Obsidian, Git versioned — forever)
- **Schema**: Fluid + lightweight taxonomy (new fields welcome; agents discover patterns)
- **Indexing Layer**: Postgres + JSONB (single table, single GIN index — classic NoSQL patterns)
- **Relationships**: Inherent "red strings" — any key-value match across pebbles creates an automatic, on-demand connection (no `related_uku_ids`, no manual tagging)
- **Weighting**: Explicit human priority in files + implicit behavioral signals (access, updates, references) in the index — some strings are thicker than others
- **Mental Model**: The classic evidence/conspiracy board — strings appear wherever attributes match

This is the smallest functional system possible: vault + one DB container + tiny watcher. No Neo4j. No extra plugins. No complexity.

Full specification: [`_specs/uku-pebbles.spec.md`](./_specs/uku-pebbles.spec.md)

## Quick Start

1. Clone the repo and open the vault in Obsidian.
2. Capture pebbles as normal Markdown + YAML.
3. Run the tiny Postgres watcher — instant indexing and automatic red strings.

Built in public for the interspecies-memory community.

## Repository Structure

```
├── _specs/          # UKU schema specification (v2.1)
├── _discussions/    # Raw origin conversations (unedited)
├── _insights/       # Synthesis and analysis
├── _research/       # Architecture and component research
└── README.md
```

## License

MIT
