# UKU-Pebbles Deep Synthesis — 21 Mar 2026

Full convergence analysis across: ai-pebbles foundation, UKU spec v0.1, SAGE architecture (v5.0.7), ByteRover alignment, and the origin threads.

---

## The Catalyst

Aaron Levie (CEO, Box) posted in Sep 2025: *"Context is king for AI agents... there's going to be a huge premium for individuals, teams, and companies that are able to best design systems to give agents the best context to do their work."*

Six months later, Luke quoted it with the reframe that crystallized UKU: *"We require an interspecies (Agents + Humans) shared caching layer."* The industry thesis was correct — context is the bottleneck — but everyone was solving it from the agent side only. The gap was the human experiential side: why you captured something, how you felt, what you planned to do next. UKU fills that gap by making human experience a first-class data structure that agents can read, validate, and enrich.

## The Organic Convergence

Three independent projects found each other through a public X thread on 21 Mar 2026:

1. **Andy Nguyen (@kevinnguyendn)** posted about his OpenClaw PR #50848 merging — passing user prompts into `ContextEngine.assemble()` to unlock selective retrieval for ByteRover. This solved *how* agents pull context, but not *what format* that context should take.

2. **@l33tdawg** replied with SAGE — a BFT consensus system for agent memory validation. This solved *how* agent memory avoids drift, but not *what structure* the memory should have.

3. **Luke (@m31uk3)** recognized that both had built runtime infrastructure for the schema spec he'd been drafting. Pebbles/UKU was the missing *what* — the structured knowledge unit that both systems needed to operate on.

No prior coordination. Three people solving adjacent problems, converging in a thread. Andy's immediate recognition — *"YAML front-matter in Markdown is exactly how ByteRover structures its .brv/context-tree"* — confirmed structural compatibility without any spec alignment work. That's a strong signal the abstraction is correct.

## SAGE Is Production Infrastructure, Not a Concept

Studying the SAGE codebase reveals it is far more mature than the thread implied:

- **v5.0.7** with 252 files (115 Go, 30 Python, 25 JS)
- **CometBFT v0.38** consensus with 4 in-process validators (sentinel, dedup, quality, consistency)
- **PoE (Proof of Expertise)** weighted voting: `W = exp(0.4·ln(accuracy) + 0.3·ln(domain) + 0.15·ln(recency) + 0.15·ln(corroboration))`
- **Full RBAC** with 4 access gates (direct, domain, org, federation) and 5 clearance levels
- **Vault encryption** (AES-256-GCM + Argon2id) for sovereign memory
- **15+ MCP tools** for agent integration (sage_remember, sage_recall, sage_vote, etc.)
- **Python SDK** (`sage-agent-sdk` on PyPI) with sync/async clients
- **Chrome extension** injecting SAGE tools into browser-based AI interfaces
- **3 deployment modes**: personal (SQLite), multi-agent network (Docker + PostgreSQL), MCP server (stdio)

This changes the integration calculus entirely. The UKU-to-SAGE pipeline maps to real, working APIs — not theoretical endpoints.

## Schema Gap Analysis: UKU v0.1 vs SAGE MemoryRecord

| Dimension | UKU v0.1 | SAGE MemoryRecord | Gap |
|-----------|----------|-------------------|-----|
| **Type system** | `uku_type`: experience_capture, insight, problem_statement, proposed_solution, ontology_element | `memory_type`: fact, observation, inference, task | Different taxonomies — need bidirectional mapping |
| **Classification** | `category`: foundational, vision, technical, insight, problem | `domain_tag`: free-form string (infrastructure, research, etc.) | UKU has no domain_tag; SAGE has no category. Both needed. |
| **Confidence** | `confidence`: 0.0–1.0 | `confidence_score`: 0.0–1.0 | 1:1 match |
| **Links** | `related_uku_ids`: flat list of IDs (untyped) | `memory_links`: source_id, target_id, link_type + `knowledge_triples`: subject, predicate, object | UKU links are untyped — loses edge semantics (ironic given Pebbles' own design principle that untyped links are a defect) |
| **Privacy** | Sovereignty as a principle, no field-level expression | `clearance_level`: 0–4 (Public to TopSecret) | UKU needs clearance_level to operationalize its sovereignty principle |
| **Integrity** | No content hash | `content_hash`: SHA-256 | UKU should add content_hash — enables dedup and tamper detection |
| **Decay** | `decay_factor`: referenced but undefined | Epoch-based scoring with PoE recalculation | SAGE's scoring engine can power UKU's decay semantics |
| **Status** | draft, annotated, published, archived | proposed, validated, committed, challenged, deprecated | Different lifecycles — UKU is authoring; SAGE is consensus. Both needed. |
| **Agent enrichment** | `interspecies_cache.agent_perspective`: empty string awaiting agent fill | Validators produce vote rationales, PoE weights, confidence adjustments | Direct mapping: SAGE consensus output → agent_perspective + confidence + decay_factor |
| **Embeddings** | `vector_ready`: boolean flag | 768-dim nomic-embed-text via Ollama + HNSW indexing | UKU defers to SAGE for actual vector infrastructure |

## The Integration Pipeline (Emerging)

```
Human captures UKU (Obsidian / Chrome ext / share sheet)
    │
    ├── UKU written as .md with YAML front-matter
    │   (header + context_elements + interspecies_cache + body)
    │
    ├── SHA-256 content_hash computed
    │
    └── MCP payload → sage_remember(content, domain, type, confidence)
            │
            ├── 4 app validators (sentinel, dedup, quality, consistency)
            │   └── 3/4 quorum required
            │
            ├── CometBFT BFT consensus
            │   └── PoE-weighted voting (2/3 weighted quorum)
            │
            └── Enriched UKU writeback:
                ├── interspecies_cache.agent_perspective ← validator rationales
                ├── confidence ← consensus confidence_score
                ├── decay_factor ← PoE epoch scoring
                ├── vector_ready ← true (embedding generated)
                └── status: draft → published (post-consensus)

ByteRover indexes enriched UKU into .brv/context-tree
    └── Agents query via ContextEngine.assemble(prompt)
        └── Selective retrieval based on user's actual request
```

## Tidy Data Violation

The ai-pebbles design principles state: *"No composite prose strings. `time_context: '10:23 AM, Tuesday'` is a defect."* Yet UKU v0.1's `context_elements.emotional_state: "Excited + slightly annoyed"` is exactly that — a composite prose string. This needs atomic decomposition in v0.2, possibly using ai-pebbles' planned CBT emotion vocabulary with `{value, confidence, provenance}` triples.

## "Human in the Mesh" Meets SAGE RBAC

The ai-pebbles TODO introduced "human in the mesh" — the idea that humans are ambient nodes in an agent fabric, not sequential gates. SAGE's architecture validates this operationally:

- **Identity**: Ed25519 keypairs. A human emitting UKUs through a capture tool has a cryptographic identity just like any SAGE agent.
- **Clearance**: SAGE's 5-level system (Public → TopSecret) maps to UKU's sovereignty principle. The human sets clearance per-UKU, agents respect it through RBAC gates.
- **Presence**: A human who continuously captures UKUs is a node that agents route through. SAGE's domain_tag system means agents with expertise in relevant domains see and validate the human's knowledge. The human doesn't approve agent actions — they radiate structured context.
- **Consent**: SAGE's access grants (per-domain, per-clearance, with expiry) are already the "standing policy" model that HITM requires, not per-action approval.

## What This Means

The UKU spec is not just a schema. With SAGE as the validation layer and ByteRover as the retrieval layer, it becomes the **data contract for interspecies memory**. The human writes UKUs. Agents validate, enrich, and retrieve them. Both species operate on the same structured units with full provenance, consensus integrity, and cryptographic identity.

The fact that all three components exist independently, are structurally compatible (YAML front-matter in Markdown), and converged organically suggests the abstraction is sound. What remains is the integration engineering — type mapping, pipeline wiring, and resolving the schema gaps identified above.

---

## Appendix A: System Architecture

A human captures a moment. That moment becomes a UKU — a structured Markdown file with experiential metadata. SAGE validates it through BFT consensus so it never drifts. ByteRover indexes it for selective retrieval so agents only pull what's relevant. The result: sovereign memory that both species share, trust, and build on.

```
┌─────────────────────────────────────────────────────────────────┐
│                        HUMAN CAPTURES                          │
│         (Obsidian / Chrome Extension / iOS Share Sheet)         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     UKU (.md + YAML)                            │
│                                                                 │
│  ┌─────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │   Header     │  │  Context Elements │  │ Interspecies Cache│  │
│  │             │  │                  │  │                   │  │
│  │ uku_id      │  │ why_captured     │  │ human_perspective │  │
│  │ created_at  │  │ activity         │  │ agent_perspective │◄─┼── SAGE writes back
│  │ uku_type    │  │ emotional_state  │  │ caching_score     │◄─┼── SAGE writes back
│  │ content_hash│  │ intended_next    │  │                   │  │
│  └─────────────┘  └──────────────────┘  └───────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Body (Markdown — the raw content)                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    MCP payload
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SAGE (Validation Layer)                       │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  App Validators (3/4 quorum)                           │     │
│  │  sentinel ─ dedup ─ quality ─ consistency              │     │
│  └────────────────────────┬───────────────────────────────┘     │
│                           │                                     │
│                           ▼                                     │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  CometBFT Consensus (2/3 weighted quorum)              │     │
│  │  PoE-weighted voting + collusion detection              │     │
│  └────────────────────────┬───────────────────────────────┘     │
│                           │                                     │
│               confidence + decay_factor                         │
│               + agent_perspective                               │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
               ┌────────────┴────────────┐
               │                         │
               ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────────────┐
│   Enriched UKU Writeback │  │  ByteRover (Retrieval Layer)     │
│                          │  │                                  │
│  confidence ← consensus  │  │  .brv/context-tree               │
│  decay      ← PoE epoch  │  │  (YAML front-matter = native)   │
│  agent_perspective ←     │  │                                  │
│    validator rationales   │  │  ContextEngine.assemble(prompt)  │
│  vector_ready ← true     │  │  → selective retrieval           │
│  status: published       │  │  → only relevant UKUs returned   │
└──────────────────────────┘  └──────────────┬───────────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │      AI AGENTS               │
                              │  (Claude / ChatGPT / etc.)   │
                              │                              │
                              │  Query with intent →         │
                              │  ← Receive relevant UKUs     │
                              │  ← Full experiential context │
                              └──────────────────────────────┘
```
