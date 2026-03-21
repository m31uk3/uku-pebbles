# UKU-Pebbles Readiness & Gap Analysis — 21 Mar 2026

Cross-referencing 18 autoresearch documents (pebble.v42), 10 PDD planning artifacts (.sop/planning), and ai-pebbles README/TODO against uku-pebbles current state.

---

## Readiness Verdict

**The triad is structurally sound. The gap is spec maturity.**

The three-project convergence (Schema / Validation / Retrieval) is validated at every level — the core thesis holds, the middleware positioning is durable, and SAGE is production infrastructure (not a concept). But UKU spec v0.1 is a sketch compared to the mature Pebble Schema Spec it descends from. Closing this gap is the critical path.

---

## I. What the Triad Resolves

The original ai-pebbles planned to build everything solo: schema + inference engine + sync engine + search engine + agent runtime + vault + capture clients. Under the triad:

| Concern | Solo Plan (ai-pebbles) | Triad Resolution |
|---------|----------------------|------------------|
| Memory drift prevention | LWW sync + per-device manifests | SAGE BFT consensus (CometBFT v0.38) |
| Confidence scoring | Local ML inference | SAGE PoE-weighted voting |
| Agent identity | ML-DSA-65 signing | SAGE Ed25519 keypairs |
| Encryption at rest | Custom vault | SAGE AES-256-GCM + Argon2id |
| Access control | Custom consent model | SAGE RBAC (4 gates, 5 clearance levels) |
| Agent execution | WASM sandbox | SAGE MCP tools (15+) |
| Search & retrieval | Tantivy/FTS5 | ByteRover .brv/context-tree |
| Backward recall | Bidirectional engine | ByteRover ContextEngine.assemble() |
| Vector embeddings | Custom pipeline | SAGE 768-dim nomic-embed-text + HNSW |

**Everything above is now someone else's job.** UKU can focus exclusively on what only it can do: the schema, the capture experience, and the experiential metadata model.

---

## II. What UKU Must Own

### A. Schema Specification (Critical Gap)

UKU spec v0.1 is missing significant structure that the mature Pebble Schema Spec (v1.0.0, 42 iterations) already defined:

| Aspect | Pebble Schema Spec | UKU v0.1 | Gap |
|--------|-------------------|----------|-----|
| Validation rules | Per-field with precise limits | None | Must port |
| Unknown field preservation | Formal rule (Section 4) | Not specified | Must add |
| Conformance levels | 3 levels (Reader/Writer/Full) | Not specified | Must define |
| Schema versioning | Full semver with compat matrix | Not specified | Must define |
| Experience layer | Typed enums: 4 intents, 8 emotions | Prose in `context_elements` | Must atomize |
| Fields | ~20 (people, tools, tasks, location, media_refs, extraction_provenance, consent_snapshot) | ~15 | Must add missing fields |
| Size limits | Per-field and composite | None | Must define |
| Enum extensibility | Formal rule (preserve unknowns) | Not specified | Must add |

### B. Capture UX Contract

Any UKU client must fulfill:
- **Latency**: <200ms p50, <500ms p99 for capture-to-saved
- **Two-phase model**: Phase 1 fast write with minimal metadata; Phase 2 async enrichment
- **Pre-attentive attributes**: Auto-suggested metadata is obviously right or obviously wrong
- **Enrichment idempotency**: `extraction_provenance == null` triggers enrichment

### C. NAI Inference Engine

On-device context DAG for capture-time enrichment. Platform-abstracted `app_context` nodes:
- Android: AppFunctions (richest — calendar, notes, music, tasks, email)
- iOS: SiriKit/App Intents, EventKit, MPNowPlayingInfoCenter, Shortcuts
- Chrome: tabs, history, bookmarks, Media Session API
- Desktop: Accessibility APIs, NSWorkspace, UI Automation

### D. Privacy & Consent Model

- Per-field sensitivity classification (personal data, derived personal data, special category data)
- Default consent values (high-sensitivity = OFF)
- `consent_snapshot` field (immutable consent state at capture time)
- Location precision levels (Precise / Neighborhood / City / None)
- Sharing redaction rules (what gets stripped in different export contexts)

---

## III. What's Now Irrelevant in ai-pebbles

### Entire Sections Superseded

- **Consumer app architecture** — Vault Core, Write Serializer, Event Bus, Platform Bridge, Chrome Extension Architecture internals
- **Economics & monetization** — freemium model, $4.99/month pricing, RevenueCat, break-even analysis, referral programs
- **Solo sync engine** — HLC, device registry, per-device manifests, LWW conflict resolution, tombstone lifecycle
- **Solo search engine** — Tantivy/FTS5, search index schema, co-occurrence tables
- **Operability** — Storage Dashboard, Sync Status UX, Agent Monitoring, Debug Mode (all consumer app features)
- **Reliability implementation** — failure mode tables, degradation modes, circuit breakers (per-implementation concerns)
- **Build vs Buy** — UniFFI, Wasmtime pinning, platform traits (code-sharing decisions for a solo app)
- **14-month phased execution** — iOS build timeline, paywall timing, user-count transition triggers

### Specific TODO Items Superseded

- Autoresearch tooling evaluation (process concern, already settled)
- Agent loop implementation (process concern)
- Vault schema migration from 14-doc spec (internal ai-pebbles concern)
- Sync delta size impact analysis (SAGE's concern)
- Extension-to-extension communication with Claude (SAGE's Chrome extension handles this)

---

## IV. PDD Questions — Validity Under the Triad

| # | Question | Original Answer | Triad Status |
|---|----------|----------------|-------------|
| Q1 | Spec or app? | Standalone specification | **STRENGTHENED** — three projects all treat the schema as foundational. "The schema IS the platform." |
| Q2 | What format? | Schema-first, YAML v1 binding | **VALID** — SAGE may need binary binding for consensus wire format; YAML remains human-facing default |
| Q3 | What fields? | 7 signals, CBT core, NAI DAG | **VALID, EXTENDED** — fields carry forward; SAGE validates provenance; ByteRover indexes for retrieval |
| Q4 | v0 schema? | Three-tier (required/enrichment/relations) | **VALID** — Tier 1 = SAGE must-validate; Tier 2 = ByteRover indexes; Tier 3 = both consume |
| Q5 | How recall? | Bidirectional engine, Level 3 deferred | **TRANSFORMED** — ByteRover IS the recall engine. Level 3 no longer deferred. |

---

## V. Strategic Positioning (Middleware Trap Analysis)

The ai-pebbles research identified four durable positions for surviving the AI middleware trap. The triad occupies all four simultaneously:

| Durable Position | Triad Mapping |
|-----------------|---------------|
| Proprietary context others can't rationally replicate | UKU: personal experiential context users can't/shouldn't hand to platforms |
| Infrastructure agents call | ByteRover: context-tree IS the infrastructure agents call |
| Deep workflow ownership | Triad collectively: accumulated UKUs + validated links + indexed context-tree = switching cost |
| Trust/verification layer | SAGE: BFT consensus is exactly the audit/verify/enforce layer |

No single competitor occupies all four. This is the structural advantage.

---

## VI. Key Carry-Forward Insights

### From Thesis Validation (01)
- The thesis is **strengthened**: "no standardized format coupling information with personal experience" now extends to "no interspecies format."
- The competitive gap remains: 15+ products analyzed, none have schema + consensus + selective retrieval.

### From K-DAG Research (04)
- Typed links with edge taxonomy (supports, contradicts, qualifies, supersedes, breadcrumb_next, part_of, derived_from, tension, gap) — must be adopted by UKU, validated by SAGE, traversed by ByteRover.
- "Context rot preferentially destroys edges while preserving nodes" — SAGE exists to prevent this at runtime.

### From Iceberg Introspection (05)
- "It's a specification, not a server" — the Iceberg parallel validates the triad architecture perfectly.
- Time-travel via consensus history — SAGE's consensus log inherently provides versioned states.

### From Agent Envelopment Thesis (07)
- Phase 2 (agents as surface) means apps dissolve into structured data + capabilities. The triad IS the Phase 2 infrastructure.
- "The schema's value APPRECIATES as agents get more capable" — compound return thesis for the triad.

### From AppFunctions/Middleware Research (06)
- AppFunctions validates the on-device/local-first thesis — Google built an entire framework for on-device agent-app communication.
- Three-protocol stack (AppFunctions / WebMCP / A2A) should be monitored for UKU compatibility.

---

## VII. Top Actions — Priority Ordered

1. **Mature the spec** — Port validation rules, conformance levels, versioning, unknown field preservation, and size limits from Pebble Schema Spec into UKU spec v0.2
2. **Atomize context_elements** — Replace prose fields with typed enums: `intent` (4 values: remember, act_on, share, think_about), `emotion` (8 values from Ekman), using `{value, confidence, provenance}` triples
3. **Add missing fields** — `people`, `tools`, `tasks`, `location`, `media_refs`, `extraction_provenance`, `consent_snapshot`, `source_app`
4. **Define field-level permissions** — which fields are human-only, agent-writable, or system-computed
5. **Reconcile type systems** — `uku_type` ↔ SAGE `memory_type` bidirectional mapping
6. **Upgrade links** — typed links with K-DAG edge taxonomy, replacing untyped `related_uku_ids`
7. **Define the pipeline** — UKU capture → MCP → SAGE consensus → enriched writeback (in-place or new version?)
8. **Expand platform context research** — Android AppFunctions, iOS equivalents, WebMCP tracking, platform parity matrix
9. **Add design principles to README** — ontological data model, tidy data invariant, pre-attentive attributes, device-agnostic/device-aware
10. **Define performance budgets** — <200ms capture, <1s enrichment, consensus latency accounting
