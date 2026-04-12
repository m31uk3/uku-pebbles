# Codebase Knowledge Base

## AI Assistant Instructions

This file is the primary context for understanding the uku-pebbles repository. Use it to:
1. Understand the project's purpose, structure, and current phase
2. Find which documentation files contain specific information
3. Navigate to detailed documentation as needed

**Critical context:** This is a design specification and research repository, not a running software application. There are 20 files total, all Markdown. No executable code, no build system, no tests. The `_research/sage/` subdirectory contains a codebase summary of an external system (SAGE) that UKU-Pebbles is designed to interoperate with.

## Quick Reference

| Question Type | Consult |
|--------------|---------|
| What is UKU-Pebbles? How does the triad work? | architecture.md |
| How is the repository organized? | components.md |
| What does the UKU schema define? | data_models.md |
| What are the specified interfaces and layers? | interfaces.md |
| How do capture, curation, and integration work? | workflows.md |
| What external systems does this relate to? | dependencies.md |
| Review gaps and consistency issues | review_notes.md |

## Codebase Overview

**UKU-Pebbles** is a schema specification for Universal Knowledge Units (UKUs) -- structured descriptions that make any human artifact (screenshot, note, tweet, photo) discoverable and associable by encoding intent, emotional state, and experiential context as YAML frontmatter in Markdown files.

The key reframe from its predecessor (ai-pebbles): a pebble is not the artifact itself -- it's a **descriptor** that wraps an artifact with lived experiential context. Just as AGENTS.md describes a codebase to an agent, a pebble describes an artifact to both humans and agents.

UKU-Pebbles is one part of a three-project triad:
- **UKU-Pebbles** (this repo) -- the schema and capture format
- **SAGE** -- BFT consensus validation layer preventing memory drift
- **ByteRover** -- selective retrieval engine (.brv/context-tree)

The triad emerged organically on March 21, 2026 when three independent projects recognized structural compatibility. The spec is at **v0.2.3** (Active Draft). No product code exists yet.

## Table of Contents

### architecture.md
**Purpose:** System architecture of the UKU-Pebbles specification and the triad
**Contains:** Four-layer architecture, triad relationship diagram, design decisions, comparison with ai-pebbles
**Use when:** Understanding what UKU-Pebbles is and how it relates to SAGE and ByteRover

### components.md
**Purpose:** Detailed breakdown of repository content areas
**Contains:** Spec, discussions, insights, research (including SAGE summary), configuration
**Use when:** Finding specific documents or understanding what each directory covers

### interfaces.md
**Purpose:** The UKU schema fields, four-layer boundaries, and integration points
**Contains:** Schema fields, ingestion tiers, red strings, typed edges, weighting model, SAGE/ByteRover integration surface
**Use when:** Understanding what the UKU format defines and how layers interact

### data_models.md
**Purpose:** The UKU entity data model and relationship structures
**Contains:** ER diagram, field semantics, red-string graph-eligible fields, consolidation hierarchy, SAGE MemoryRecord comparison
**Use when:** Working with UKU schema fields, understanding data relationships

### workflows.md
**Purpose:** Key processes -- capture, curation, query, and integration flows
**Contains:** Four-tier ingestion, curation lifecycle, red-string query, SAGE consensus pipeline, research methodology
**Use when:** Understanding how the system is specified to work end-to-end

### dependencies.md
**Purpose:** External systems, tools, and references
**Contains:** SAGE architecture summary, ByteRover relationship, specified tech stack, academic references
**Use when:** Understanding the triad ecosystem and technology choices

### codebase_info.md
**Purpose:** Raw structural analysis output
**Contains:** File counts, directory tree, file type distribution
**Use when:** Quick structural overview

### review_notes.md
**Purpose:** Consistency and completeness review findings
**Contains:** Cross-document issues, documentation gaps, comparison with ai-pebbles
**Use when:** Understanding what needs attention or refinement
