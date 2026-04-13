# TODO

**Status**: Phase 0 (schema finalization) complete with spec v0.3.0-draft at `_specs/pebbles.spec.md`. Phase 1 (TypeScript reference implementation) is the next major push. For full context, see `.sop/cold-start.md`. For what changed in v0.3, see the spec changelog.

---

## Phase 1 — Core CLI + Schema Validator

The first reference implementation. Single TypeScript monorepo with `packages/{schema, core, cli}`. Postgres indexer is Phase 2.

### Foundation
- [ ] Bun (or pnpm) workspaces monorepo scaffold
- [ ] TypeScript build / lint / test setup
- [ ] ULID library integration (`ulid` or `ulidx`)

### `packages/schema` — schema validator
- [ ] Formal JSON Schema or Zod definition of v0.3 YAML binding
- [ ] Per-field type constraints, array caps, string length limits
- [ ] Unknown field preservation on round-trip (per spec §12.3)
- [ ] Temporal field rule enforcement — full ISO 8601 with timezone required, date-only rejected (§5.1)
- [ ] (label, uid) cross-reference shape validation (§5.2)
- [ ] Tidy data invariant audit (no composite strings; every value atomic)

### `packages/core` — `.pebble` container + parsers
- [ ] EPUB-style zip reader/writer for `.pebble`
- [ ] `pebble.yaml` manifest format
- [ ] `body.md` extraction
- [ ] `artifact/` payload handling
- [ ] `mimetype` prefix file
- [ ] `pebble.md` (Tier 1) Markdown + YAML parser/writer

### `packages/cli` — pebble CLI
- [ ] `pebble create <artifact>` — wrap any file as a pebble
- [ ] `pebble create --note "text"` — pure text pebble
- [ ] `pebble validate <pebble>` — schema check
- [ ] `pebble link A B --type derived_from` — typed edge
- [ ] `pebble export <pebble> --native` — Tier 3 sidecar/XMP export
- [ ] CLI framework (commander.js or oclif)
- [ ] Programmatic API surface for agents (same operations)

### Phase 1 architecture deliverables
- [ ] `_specs/ARCHITECTURE.md` — implementation notes for Q5 (CLI direct, no daemon for v0.1) and Q8 (monorepo structure), plus layer-based conformance examples
- [ ] C4 L1 Context diagram (Mermaid `C4Context`) — canonical "what is Pebbles" artifact for the README
- [ ] C4 L2 Container diagram for v0.1 reference impl (Mermaid `C4Container`)

---

## Phase 1.5 — Spec follow-ups (parallel with Phase 1)

- [ ] Define ontology pebble body format — candidates: YAML-LD, JSON-LD, Mermaid graph. Needed before Phase 1 ontology work.
- [ ] Update synthesis doc 02 (`.sop/synthesis/02-convergence-analysis.md`) to reframe SAGE+ByteRover as integration patterns (Appendix G), not core triad components
- [ ] Update synthesis doc 11 (`.sop/synthesis/11-final-converged-synthesis.md`) similarly
- [ ] Add the remaining ai-pebbles parity fields to spec: `people`, `tools`, `tasks`, `media_refs`, `extraction_provenance`, `consent_snapshot`
- [ ] Define per-field size limits and composite pebble size budget
- [ ] Define `extraction_provenance` model — per-field ML tracking with source enum (user, ml, error, timeout, skipped)

---

## Phase 2 — Postgres JSONB Indexer + Red-String Query Engine

The interference-immune retrieval layer. Demo target: import 10–20 real pebbles from existing Obsidian clippings, run red-string queries.

- [ ] `packages/indexer` package
- [ ] Postgres schema migration from spec §9 (`pebbles` table + GIN index + optional `edges` table)
- [ ] JSONB ingest from pebble files
- [ ] Red-string query engine (compound faceted search via `@>` operator on JSONB)
- [ ] Query DSL: `?who[X]:attribute`, `?when[event:Y]`, `?after[date:Z]`
- [ ] CLI integration: `pebble query "..."`
- [ ] Bulk import: `pebble import <directory>` indexes a folder of `pebble.md` and `.pebble` files
- [ ] Edges table + recursive CTE traversal for typed-edge queries
- [ ] Level derivation from edge topology (per §9.1) at query time
- [ ] Behavioral signal tracking (`access_count`, `reference_count`, `last_accessed_at`)
- [ ] Direct CLI → Postgres connection (no daemon for v0.1, per Q5 ratification)

---

## Phase 3 — Browser Surface (separate repos, after Phases 1–2)

### `pebble-extract` (fork of `/Users/ljack/github/defuddle`)
- [ ] Fork defuddle to a separate repo at `pebble-extract`
- [ ] Add `src/pebbles/` module (types, generator, attributes, middleware)
- [ ] Hook into `src/node.ts` for YAML injection
- [ ] Tier 3 inference (venue_type from URL, source_type from extractor type)
- [ ] Schema validation against Pebbles spec
- [ ] Upstream-friendly module separation, easy rebase

### `pebble-clipper` (fork of `/Users/ljack/github/obsidian-clipper`)
- [ ] Fork obsidian-clipper to a separate repo at `pebble-clipper`
- [ ] Add Pebbles property types to `property-types-manager.ts`
- [ ] Update `createDefaultTemplate()` with v0.3 fields
- [ ] Tier 2 input UI (emotion picker, intent dropdown, modality toggle)
- [ ] Property compilation hook for validation
- [ ] Cross-browser builds (Chrome, Firefox, Safari)

**Demo target**: Clip a web page from Chrome, see the Pebbles YAML frontmatter populated automatically + ask user for `emotional_state`, `intent`, and `modality` in the popup.

---

## Phase 4 — Eval Framework on LoCoMo

**Critical**: keep this in a SEPARATE repo from the commercial CLI because LoCoMo is CC BY-NC 4.0.

- [ ] Create separate `pebble-eval` repo (CC BY-NC isolation)
- [ ] Annotate 10–20% of LoCoMo QAs (~200 pairs) with red-string templates
- [ ] Build minimal red-string query evaluator in Python (LoCoMo is Python-native)
- [ ] Convert LoCoMo observations to v0.3 pebbles with structured frontmatter
- [ ] 3-way comparison: semantic vs structured (red strings) vs hybrid
- [ ] Per-category breakdown (single-hop, multi-hop, temporal, adversarial, open-domain)
- [ ] **Hypothesis to test**: structured red-string matching ≥85% accuracy on multi-hop QA in <500 tokens vs ~20k tokens for full context

If the hypothesis holds, write up as "Structured Metadata Matching Beats Semantic Retrieval on Long-Term Conversational Memory" — workshop paper, marketing wedge.

---

## Phase 5 — ByteRover Integration (optional, post-Phase-4)

Now explicitly optional per Q13 ratification (SAGE and ByteRover removed from core spec, relocated to non-normative Appendix G).

- [ ] Pebbles Query layer (Phase 2) exposes red-string results in a format ByteRover's RRF can consume (top-K with scores)
- [ ] Optional: Pebbles MCP tool for ByteRover's Memory Swarm
- [ ] Document the integration as one retrieval method in a swarm

This is intentionally minimal because Pebbles is the blueprint, not the product. The community can implement additional integrations directly.

---

## Phase 6 — Community & Adoption (parallel with everything)

- [ ] Publish spec v0.3 announcement (X thread, dev communities)
- [ ] Create `CONTRIBUTING.md` with extension guidelines
- [ ] Example pebbles — curated set showing each `pebble_type` × `memory_kind` × `modality` combination
- [ ] Conformance test suite (layer-based per §3) — fixtures for each implementable layer
- [ ] Validator badge for sites/tools that emit valid pebbles
- [ ] Reference implementations in additional languages (Python, Go, Rust as community contributions)

---

## Deferred to post-v1

### Weighting model rewrite (§7)
See `.sop/synthesis/15-weight-field-citation-research.md`. §7 is unchanged in v0.3.0-draft pending citation research re-verification with network access.

- [ ] Re-run weight-failure-mode citation research with WebSearch enabled (the original session was offline-only)
- [ ] Apply Option (c): downgrade `weight` to optional-legacy, elevate behavioral signals + graph centrality as default surface
- [ ] Add `salience_hint` categorical field (`pin | flag | none`) as a binary capture-moment marker
- [ ] Define pattern-weight detection logic (likely personalized PageRank on the edges table)

### Privacy & consent (port from ai-pebbles doc 16)
- [ ] Trust thresholds, capture filtering, sharing redaction, App Store privacy labels
- [ ] Define `consent_snapshot` semantics — immutable consent state at capture time, per-field sensitivity levels, default-OFF for high-sensitivity
- [ ] Define location precision levels as schema concept (Precise / Neighborhood / City / None)
- [ ] Define sharing redaction rules — what gets stripped on export
- [ ] Per-field consent gating

### Performance budgets
- [ ] Latency budgets per capture step (DOM read, context collection, write, UI feedback) — target <200ms p50, <500ms p99
- [ ] Enrichment latency budget — target <1s p50, <3s p99
- [ ] Chrome extension benchmarks (popup render, capture-to-saved, search response)
- [ ] Study Excalidraw 7-layer compound optimization and McMaster-Carr techniques for capture flow applicability

### Procedural pebble body format
- [ ] Define structured step-sequence body format for `memory_kind: procedural` pebbles (recipes, runbooks, workflows)

### Capture UX
- [ ] Onboarding/activation flow for target demographics (student, corporate employee)
- [ ] Time-to-first-value target for Chrome extension
- [ ] Capture UX parity matrix: Chrome popup/sidebar vs iOS share sheet vs Android
- [ ] Two-phase capture model: Phase 1 (fast write, minimal metadata) → Phase 2 (async enrichment)
- [ ] Pre-attentive attribute guidelines for metadata suggestion display

---

## Platform Context Research (long-term)

- [ ] Android: AppFunctions API gating — can third-party apps call `AppFunctionManager.executeAppFunction()` or is it Gemini-only?
- [ ] Android: Map AppFunction-enabled app categories to capture signals (calendar→temporal, notes→narrative, music→sensory, tasks→intent, email→activity)
- [ ] iOS: Audit equivalents — SiriKit/App Intents, NSUserActivity, Shortcuts, MPNowPlayingInfoCenter, EventKit/Reminders
- [ ] iOS: Identify platform parity gap vs Android
- [ ] Chrome: Current extension context capabilities (tabs, history, bookmarks, Media Session API)
- [ ] Chrome: Track WebMCP (Chrome 146+) — browser equivalent of AppFunctions for structured agent–website interaction
- [ ] Desktop macOS: Accessibility APIs, NSWorkspace, MRMediaRemoteGetNowPlayingInfo
- [ ] Desktop Windows: UI Automation API, SystemMediaTransportControls
- [ ] Define abstract `app_context` node interface for capture-time enrichment
- [ ] Per-signal confidence scoring based on platform mechanism quality (AppFunctions typed return = high; Accessibility scraping = lower)

---

## Parking Lot (v1+)

- 3-tier visualization (macro dashboards, mid-level graphs, micro knowledge graphs)
- Native iOS/Android apps (eventual OS-native integration by Apple/Google)
- TOML and JSON serialization bindings
- MCP standard payload definition for agent interop
- Embedded vector spec for local semantic search
- Knowledge triple extraction from pebble body content
- Time-travel via consensus history (versioned knowledge graph states)
- Pebbles migration tooling for legacy ai-pebbles users
- Post-quantum readiness — monitor ML-DSA-65 for signatures
- Three-protocol stack monitoring: AppFunctions / WebMCP / A2A

---

## Out of scope (delegated, not building)

These are explicitly NOT being built per the v0.3 spec ratification. The spec exposes integration hooks (Appendix G); deployments plug in their own choices.

- **Vector DB** — delegated to ByteRover or community
- **BFT consensus** — delegated to SAGE or community
- **LLM agent runtime** — delegated to SAGE / external MCP servers
- **Encryption / vault** — delegated to SAGE
- **Sync engine** — delegated to SAGE federation
- **Mobile apps** — eventual OS-native integration (Apple, Google)
- **Marketplace / agent catalog** — community-driven via the open spec
- **Subscription / pricing** — Pebbles is the blueprint, not the product
