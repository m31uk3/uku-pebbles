# PDD Requirements Clarification: UKU-Pebbles Infrastructure

**Status:** Open -- awaiting answers
**Date:** 2026-04-12
**Context:** The No-Escape theorem convergence analysis (02-convergence-analysis.md) validates UKU's architecture and identifies a clear implementation path. These questions resolve design decisions needed before writing code.

---

## Q1: First Tangible Demo -- What Should It Be?

The convergence analysis shows the interference-immune foundation (files + JSONB+GIN + red strings) is the highest-value first build. Three options:

**Option A: CLI tool** -- `pebble create`, `pebble query`, `pebble link`. Creates `.md` files with YAML frontmatter, indexes to Postgres JSONB, runs red-string queries. Pure Layers 1-3. No LLM needed.

**Option B: Obsidian importer** -- Takes existing Obsidian Clippings (like the source docs processed in this synthesis) and converts them to UKU pebbles with structured frontmatter. Demonstrates the capture-to-query loop on real data.

**Option C: Both** -- CLI as the core, importer as the first ingestion surface.

**Why it matters:** Determines whether we build capture-first or query-first. The theorem says the exact episodic record is the foundation -- but which direction do we prove it from?

**Answer:**

---

## Q2: Language and Stack

The spec recommends Postgres + JSONB + GIN. For the first implementation:

- **Python** -- Fast to prototype, rich ecosystem, likely compatible with ByteRover
- **Go** -- SAGE is Go, could share patterns and integration surface
- **TypeScript** -- If the Chrome extension is the first real capture surface
- **Rust** -- ai-pebbles specified this, but may be premature for a proof-of-concept

**Why it matters:** Determines integration friction with ByteRover (retrieval) and SAGE (validation). Also determines iteration speed.

**Answer:**

---

## Q3: The "Structured Metadata" Hypothesis -- Should We Test It?

The convergence analysis identifies that red strings on controlled vocabularies might occupy a new, untested point on the Pareto frontier. The No-Escape paper tested BM25 on unstructured text and measured 15.5% semantic agreement. Red strings on Ekman 8 emotions, 5 uku_types, and 4 intents could score significantly higher while maintaining b=0, FA=0.

This is empirically testable using the paper's methodology (measure forgetting exponent b, false alarm rate FA, and semantic retrieval agreement). A positive result would be a publishable finding that validates the UKU architecture with hard numbers.

**Why it matters:** Would produce external validation and potentially a paper. But adds scope. Do we want to build measurement alongside implementation, or ship first and measure later?

**Answer:**

---

## Q4: ByteRover Integration Surface

Andy's Memory Swarm uses BM25 + wikilink graph expansion + hybrid vector+keyword, fused with RRF. UKU's Query layer needs to expose an interface that ByteRover can consume. Two approaches:

**Option A: UKU exposes a standard API** (REST or MCP) that ByteRover calls as one retrieval method in its swarm.

**Option B: UKU provides its red-string results as a BM25-equivalent input** to ByteRover's RRF fusion pipeline directly.

**Why it matters:** Determines the integration architecture. Option A is cleaner (loose coupling). Option B is tighter but may produce better RRF fusion results since red strings and BM25 have different characteristics.

**Sub-question:** Have you discussed integration mechanics with Andy? Is there a preferred protocol (REST, MCP, direct library call)?

**Answer:**

---

## Q5: Scope Boundary for v0.1 Implementation

Given the convergence analysis, suggested minimum viable demonstration:

1. UKU file parser (read/write Markdown + YAML frontmatter)
2. Postgres JSONB indexer (parse YAML to JSONB, maintain GIN index)
3. Red-string query engine (compound faceted search via GIN)
4. CLI for create/query/link operations
5. Import 10-20 real pebbles from existing Obsidian clippings
6. Demo: show red-string connections emerging from structured metadata

**Explicitly out of scope for v0.1:**
- SAGE integration
- ByteRover integration
- Tier 4 (LLM-assisted) ingestion
- Chrome extension
- Typed edges / consolidation hierarchy
- Weighting model (effective weight computation)

**Why it matters:** Defines what "done" looks like for the first build. Everything listed as out-of-scope becomes v0.2+.

**Answer:**

---

## Dependencies Between Questions

```
Q2 (stack) ──── blocks ──── Q1 (demo type)
                                │
Q4 (ByteRover) ── informs ── Q5 (scope)
                                │
Q3 (hypothesis) ── informs ── Q5 (scope)
```

Q2 is the most blocking -- stack choice affects everything downstream.
