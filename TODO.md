# TODO

## Spec (v0.2)

- [ ] Formal JSON Schema + validation library for UKU YAML binding
- [ ] TOML and JSON serialization bindings
- [ ] Define full `uku_type` taxonomy with community input
- [ ] Embedded vector spec for local semantic search
- [ ] MCP standard payload definition for agent interop
- [ ] Specify `interspecies_cache` scoring algorithm and update lifecycle
- [ ] Define `decay_factor` semantics — who sets it, how it's recalculated, what triggers archival
- [ ] Add `content_hash` (SHA-256) as required header field — enables SAGE dedup validator and content integrity
- [ ] Add `clearance_level` field (0–4) — operationalizes sovereignty principle, mirrors SAGE's privacy tiers
- [ ] Add `domain_tag` field — enables SAGE domain-based access control and PoE expertise scoring

## Integration

- [ ] SAGE validator wiring — define the UKU commit/consensus flow
- [ ] ByteRover `.brv/context-tree` mapping — confirm field-level compatibility
- [ ] Obsidian plugin for native UKU creation and browsing
- [ ] One-click importer for Twitter/X archive (enrichment script exists in ai-pebbles)
- [ ] Chrome extension capture surface (carried from ai-pebbles v0 plan)
- [ ] Reconcile `uku_type` with SAGE `memory_type` — define bidirectional mapping (experience_capture/insight/problem_statement/proposed_solution/ontology_element vs fact/observation/inference/task)
- [ ] Define UKU-to-SAGE submission pipeline — UKU YAML → MCP `sage_remember` → consensus → enriched UKU writeback
- [ ] Specify SAGE agent_perspective writeback — how consensus results (validator rationales, PoE weights) flow back into `interspecies_cache.agent_perspective`
- [ ] Upgrade `related_uku_ids` to typed links — align with SAGE `memory_links` (link_type, direction) and `knowledge_triples` (subject/predicate/object)
- [ ] Map UKU `status` lifecycle (draft→published) to SAGE `status` lifecycle (proposed→committed) — define handoff points

## Schema Integrity

- [ ] Audit all fields against tidy data invariant (no composite strings, every value atomic)
- [ ] Define ontological object type registry: UKU, Person, Tag, Tool, Location, Narrative
- [ ] Define typed link vocabulary with direction, cardinality, provenance
- [ ] Confidence score calibration — thresholds per signal type
- [ ] Consent model: per-field gating for `interspecies_cache` and `context_elements`
- [ ] Fix tidy data violation in `context_elements.emotional_state` — currently composite prose, needs atomic decomposition (align with ai-pebbles CBT emotion vocabulary using `{value, confidence, provenance}` triples)
- [ ] Define knowledge triple extraction from UKU body content — maps to SAGE `knowledge_triples` (subject/predicate/object RDF-style)

## Community & Adoption

- [ ] Publish spec v0.1 announcement (X thread, dev communities)
- [ ] Create CONTRIBUTING.md with schema extension guidelines
- [ ] Example UKUs — curated set showing each `uku_type` in practice
- [ ] Validator CLI — command-line tool to check a `.md` file against the spec
- [ ] Reference implementation — minimal Python/TS library for reading/writing UKUs

## Research (Carried from ai-pebbles)

- [ ] Agent system design — how agents read, write, and propose UKU changes
- [ ] NAI inference engine — on-device context DAG for capture-time enrichment
- [ ] Bidirectional context engine — forward (suggestion) and backward (recall)
- [ ] Platform API audit — Chrome, iOS, Android, desktop context signal availability
- [ ] "Human in the mesh" concept — consent as standing policy, not per-action gate
- [ ] Cross-platform `app_context` abstraction for the NAI DAG

## Parking Lot (v1+)

- Level 3 natural language recall via LLM delegation
- 3-tier visualization (macro dashboards, mid-level graphs, micro knowledge graphs)
- iOS and Android native apps
- User-provided agents (WASM sandbox)
- Team/family shared vaults
- Pebbles-to-UKU migration tooling for ai-pebbles users
