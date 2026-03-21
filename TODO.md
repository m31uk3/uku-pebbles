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
- [ ] Add missing fields from Pebble Schema Spec: `people`, `tools`, `tasks`, `location`, `media_refs`, `extraction_provenance`, `consent_snapshot`, `source_app`
- [ ] Port validation rules from Pebble Schema Spec — per-field type constraints, array caps, string length limits
- [ ] Add unknown field preservation rule — clients must round-trip unknown YAML keys without data loss
- [ ] Define conformance levels: Level 1 (Reader), Level 2 (Writer), Level 3 (Full)
- [ ] Define schema versioning — semver rules, compatibility matrix, migration determinism
- [ ] Define per-field size limits and composite UKU size budget
- [ ] Define enum extensibility rule — clients must preserve unknown enum values

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
- [ ] Determine writeback model — does SAGE enrichment modify the original UKU `.md` in-place or create a new enriched version?
- [ ] Reconcile UKU consent model with SAGE's existing access grants (per-domain, per-clearance, with expiry)
- [ ] Chrome extension interaction model with SAGE's existing Chrome extension — integrate vs. standalone

## Schema Integrity

- [ ] Audit all fields against tidy data invariant (no composite strings, every value atomic)
- [ ] Define ontological object type registry: UKU, Person, Tag, Tool, Location, Narrative
- [ ] Define typed link vocabulary with direction, cardinality, provenance — adopt K-DAG edge taxonomy (supports, contradicts, qualifies, supersedes, breadcrumb_next, part_of, derived_from, tension, gap)
- [ ] Confidence score calibration — thresholds per signal type
- [ ] Consent model: per-field gating for `interspecies_cache` and `context_elements`
- [ ] Fix tidy data violation in `context_elements.emotional_state` — currently composite prose, needs atomic decomposition (align with ai-pebbles CBT emotion vocabulary using `{value, confidence, provenance}` triples)
- [ ] Atomize `context_elements.intent` — replace prose with typed enum: `remember`, `act_on`, `share`, `think_about`
- [ ] Atomize `context_elements.emotional_state` — replace prose with typed enum from Ekman's 8 basic emotions
- [ ] Define knowledge triple extraction from UKU body content — maps to SAGE `knowledge_triples` (subject/predicate/object RDF-style)
- [ ] Define field-level read/write permissions — which fields are human-only, agent-writable, system-computed
- [ ] Define action type registry: capture, tag, link, archive, merge, agent_converge, consent_withdraw
- [ ] Define shared property set reused across object types: confidence, provenance, created_at, updated_at
- [ ] Define ontological extension mechanism — how third parties extend the UKU schema with new types and fields
- [ ] Define `extraction_provenance` model — per-field ML tracking with source enum (user, ml, error, timeout, skipped)
- [ ] Define `consent_snapshot` semantics — immutable consent state at capture time, per-field sensitivity levels, default values (high-sensitivity = OFF)
- [ ] Define location precision levels as schema concept: Precise / Neighborhood / City / None
- [ ] Define sharing redaction rules — what gets stripped when a UKU is exported or shared

## Community & Adoption

- [ ] Publish spec v0.1 announcement (X thread, dev communities)
- [ ] Create CONTRIBUTING.md with schema extension guidelines
- [ ] Example UKUs — curated set showing each `uku_type` in practice, including student and corporate employee scenarios
- [ ] Validator CLI — command-line tool to check a `.md` file against the spec
- [ ] Reference implementation — minimal Python/TS library for reading/writing UKUs
- [ ] Conformance test suite — Level 1/2/3 test fixtures for implementers

## Research (Carried from ai-pebbles)

- [ ] Agent system design — how agents read, write, and propose UKU changes
- [ ] NAI inference engine — on-device context DAG for capture-time enrichment
- [ ] Bidirectional context engine — forward (suggestion) is UKU/NAI; backward (recall) is ByteRover
- [ ] "Human in the mesh" concept — consent as standing policy, not per-action gate
- [ ] Map each UKU field to mesh presence — which fields make the human visible to agents (passive read vs active trigger)

## Platform Context Research

- [ ] Android: AppFunctions API gating — can third-party apps call `AppFunctionManager.executeAppFunction()` or is it Gemini-only?
- [ ] Android: Map AppFunction-enabled app categories to NAI DAG signals (calendar→temporal, notes→narrative, music→sensory, tasks→intent, email→activity)
- [ ] iOS: Audit equivalents — SiriKit/App Intents, NSUserActivity, Shortcuts, MPNowPlayingInfoCenter, EventKit/Reminders
- [ ] iOS: Identify platform parity gap — which Android AppFunctions signals iOS cannot provide
- [ ] Chrome: Current extension context capabilities (tabs, history, bookmarks, Media Session API, cross-extension messaging limitations)
- [ ] Chrome: Track WebMCP (Chrome 146+) — browser equivalent of AppFunctions for structured agent-website interaction
- [ ] Desktop: macOS accessibility APIs, NSWorkspace, MRMediaRemoteGetNowPlayingInfo
- [ ] Desktop: Windows UI Automation API, SystemMediaTransportControls
- [ ] Define abstract `app_context` node interface for the NAI DAG: current_media, current_calendar_event, active_task, recent_note, active_app
- [ ] Per-signal confidence scoring based on platform mechanism quality (AppFunctions typed return = high; Accessibility scraping = lower; absent = null)
- [ ] Per-field consent gating of app_context signals per platform

## Performance

- [ ] Define latency budgets per capture step: DOM read, context collection, NAI inference, write, UI feedback (<200ms p50, <500ms p99)
- [ ] Define enrichment latency budget: metadata extraction (<1s p50, <3s p99)
- [ ] Account for SAGE consensus latency in the end-to-end pipeline budget
- [ ] Benchmark targets for the Chrome extension: popup render, capture-to-saved, search response
- [ ] Study Excalidraw 7-layer compound optimization and McMaster-Carr techniques for capture flow applicability

## Capture UX

- [ ] Onboarding/activation flow for target demographics (student, corporate employee)
- [ ] Time-to-first-value target for Chrome extension
- [ ] Capture UX parity matrix: Chrome popup/sidebar vs iOS share sheet vs Android
- [ ] Two-phase capture model spec: Phase 1 (fast write, minimal metadata) → Phase 2 (async enrichment)
- [ ] Pre-attentive attribute guidelines for metadata suggestion display (auto-populate / suggest / discard thresholds)

## Parking Lot (v1+)

- Level 3 natural language recall via LLM delegation (note: ByteRover agents may already enable this)
- 3-tier visualization (macro dashboards, mid-level graphs, micro knowledge graphs)
- iOS and Android native apps
- User-provided agents (WASM sandbox) — likely a SAGE responsibility
- Team/family shared vaults — likely a SAGE responsibility (federation + multi-agent deployment exists)
- Pebbles-to-UKU migration tooling for ai-pebbles users
- Post-quantum readiness — AES-256 provides 128-bit PQ security; monitor ML-DSA-65 for signatures
- Three-protocol stack monitoring: AppFunctions / WebMCP / A2A for UKU compatibility
- Time-travel via SAGE consensus history — version-aware knowledge graph states
