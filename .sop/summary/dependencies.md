# Dependencies

## Repository Tooling

This repository has no runtime dependencies. All 20 files are Markdown documents.

### AI Assistant Tooling
| Tool | Configuration | Purpose |
|------|--------------|---------|
| Claude Code | `.claude/settings.local.json` | AI-assisted design with Python execution and SAGE codebase access |

The Claude Code config permits `find` commands targeting `/Users/ljack/github/resources/code/sage/` -- indicating active cross-referencing with the SAGE source code during design work.

## Triad Ecosystem

UKU-Pebbles is designed to interoperate with two external systems:

### SAGE (Sovereign Agent Governed Experience)
**Role in triad:** Consensus validation layer -- prevents memory drift, provides confidence scoring
**Maturity:** Production infrastructure (v5.0.7, 252 files, Go 1.23)
**Source:** External repository (summarized in `_research/sage/`)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Consensus | CometBFT v0.38 (BFT) | Multi-agent transaction validation |
| Validators | 4 in-process (sentinel, dedup, quality, consistency) | Pre-filter noise before consensus |
| Scoring | PoE (Proof of Expertise) | Weighted voting by accuracy + domain + recency |
| Storage | BadgerDB (on-chain) + PostgreSQL/pgvector (off-chain) | Two-store architecture |
| Encryption | AES-256-GCM + Argon2id KDF | Vault encryption |
| Identity | Ed25519 keypairs | Agent + human authentication |
| Access | RBAC (4 gates, 5 clearance levels) | Fail-secure access control |
| API | 25+ REST endpoints + 15+ MCP tools | Integration surface |
| Deployment | Personal (SQLite), Multi-agent (Docker+PostgreSQL), MCP server | 3 modes |

### ByteRover
**Role in triad:** Selective retrieval engine -- prompt-aware context assembly
**Maturity:** Active development (OpenClaw PR #50848 merged as of March 2026)
**Source:** External (no local codebase summary available)

| Component | Purpose |
|-----------|---------|
| ContextEngine.assemble() | Selective, prompt-aware retrieval |
| .brv/context-tree | State management for context |
| OpenClaw | Open-source contribution framework |

### What Each Triad Member Owns

| Concern | Owner | ai-pebbles Equivalent |
|---------|-------|----------------------|
| Schema + capture format | UKU-Pebbles | Pebble Schema Spec |
| Experiential metadata | UKU-Pebbles | NAI engine + enrichment |
| Memory validation | SAGE | 44 invariants + TLA+ (never built) |
| Confidence scoring | SAGE (PoE) | Local ML confidence |
| Agent identity | SAGE (Ed25519) | ML-DSA-65 signing (planned) |
| Encryption | SAGE (AES-256-GCM) | Custom vault encryption |
| Access control | SAGE (RBAC) | Custom consent model |
| Agent execution | SAGE (MCP tools) | WASM sandbox |
| Search/retrieval | ByteRover | Tantivy + SQLite FTS5 |
| Backward recall | ByteRover | Bidirectional context engine |
| Vector embeddings | SAGE (nomic-embed-text + HNSW) | Custom pipeline (planned) |

## Specified Technology Stack (Not Yet Implemented)

### Storage & Indexing
| Technology | Purpose | Specified In |
|-----------|---------|--------------|
| Postgres | Relational database for index | Spec: Storage & Indexing |
| JSONB | Parsed YAML frontmatter storage | Spec: Storage & Indexing |
| GIN index | Sub-millisecond compound faceted search | Spec: Storage & Indexing |
| pgvector | Optional future semantic search | Spec: Storage & Indexing |

### Capture Surfaces (Planned)
| Surface | Mechanism | Specified In |
|---------|-----------|--------------|
| Chrome extension | Manifest V3, Defuddle content extraction | README: v1 Scope |
| System screenshot override | Replaces OS default | README: v1 Scope |
| Obsidian vault | Native `.md` file integration | README: v1 Scope |
| Pebbles dashboard | Web-based graph view via daemon | README: v1 Scope |

## Academic / Industry References

The spec includes a bibliography (Appendix D). Key sources:

| Category | Sources | Used For |
|----------|---------|----------|
| Psychology | Ekman (1992) basic emotions | `emotional_state` vocabulary |
| Knowledge Management | Luhmann's Zettelkasten | Atomicity principle, Luhmann Test |
| Data Architecture | Wickham (2014) tidy data | Tidy data invariant |
| PKM | Obsidian, Notion, Roam | Competitive context, file sovereignty |
| Agent Infrastructure | MCP (Model Context Protocol) | Agent interop standard |

Full bibliography: `_specs/uku-pebbles.spec.md` Appendix D
