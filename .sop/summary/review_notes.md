# Review Notes

## Consistency Check

### Terminology Consistency
1. **"Pebble" vs "UKU"** -- The spec and README use both terms interchangeably. The spec title is "UKU-Pebbles" and fields use `uku_id`, `uku_type`, but the README headline is "Pebbles" and the mental model references "pebble-piling." This is consistent enough (UKU is the formal name, pebble is the colloquial name) but should be explicit about the convention.

2. **Version numbering** -- The spec file says `v0.2.3` in the header, but the changelog describes evolution from `v2.1 → v2.3`. The TODO header says `v0.2`. These should be reconciled. Is the version 0.2.3 or 2.3?

3. **License discrepancy** -- README says "MIT" but the LICENSE file is Apache 2.0. These contradict each other.

### Cross-Reference Validity
1. **README references `_specs/uku-pebbles.spec.md`** -- Correct, file exists.
2. **README repository structure** -- Accurate. Lists _specs, _discussions, _insights, _research.
3. **TODO.md references to ai-pebbles** -- Multiple TODO items reference concepts from ai-pebbles (Pebble Schema Spec, CBT emotion vocabulary, K-DAG edge taxonomy). These are valid cross-project references but the ai-pebbles repo is described as "abandoned" -- the TODO items should clarify they're porting concepts, not depending on that codebase.

### Internal Consistency
1. **Emotional state atomization** -- The spec already defines `emotional_state` as Ekman 8 enum at the top level. But `context_elements` still allows freeform prose for emotional state. TODO.md correctly flags this as a tidy data violation to fix.

2. **The spec says "Fluid Schema" (any YAML key valid)** while also defining controlled vocabularies. These coexist correctly (controlled vocabularies are recommendations, not enforcement), but the spec could be clearer about which fields are strictly validated vs. recommended.

3. **Red strings are "computed on-demand"** -- Consistent across spec, README, and insights. No documents claim red strings are pre-computed or stored.

## Completeness Check

### Well-Documented Areas
- UKU schema fields and semantics (spec)
- 4-layer architecture with LLM boundary (spec + README)
- 4-tier ingestion contract (spec + README)
- Red string mechanism and graph-eligible fields (spec)
- Typed edges and consolidation hierarchy (spec)
- Weighting model (spec)
- Triad relationship and strategic positioning (insights)
- SAGE architecture (research/sage/ -- 8 comprehensive docs)
- Design evolution from ai-pebbles (readiness gap analysis)
- Adversarial design validation (Grok debate)

### Documentation Gaps

1. **No implementation code** -- Same as ai-pebbles: pure design/research repository. No product code, tests, CI/CD, or build system. By design.

2. **Missing UKU fields** -- The readiness gap analysis identifies 11 fields that exist in ai-pebbles but are absent from UKU v0.2.3: `people`, `tools`, `tasks`, `location` (full GPS), `media_refs`, `extraction_provenance`, `consent_snapshot`, `source_app`, `content_hash`, `clearance_level`, `domain_tag`. These are tracked in TODO.md.

3. **No validation rules** -- ai-pebbles had per-field type constraints, array caps, string length limits. UKU has none yet. TODO.md tracks this.

4. **No conformance levels** -- ai-pebbles spec defined Level 1 (Reader), Level 2 (Writer), Level 3 (Full). UKU has none yet.

5. **No schema versioning rules** -- Semver, compatibility matrix, migration determinism are all TODO items.

6. **SAGE integration pipeline not specified** -- The readiness gap analysis describes the conceptual flow (UKU -> MCP -> consensus -> enriched writeback) but no detailed protocol spec exists. Open questions: writeback model (in-place vs new version), type mapping, status lifecycle handoff.

7. **ByteRover integration not specified** -- ByteRover is referenced as the retrieval layer but no integration spec exists. The `.brv/context-tree` mapping to UKU fields is a TODO item.

8. **Capture UX not specified** -- README describes three modes (Silent/Minimal/Full) and two surfaces (Chrome extension, system screenshot override). No wireframes, latency budgets, or detailed UX flows exist.

9. **Performance budgets absent** -- ai-pebbles had detailed latency budgets (<200ms capture, <100ms search, 150MB memory). UKU has none; all performance items are in TODO.

10. **Privacy and consent model absent** -- ai-pebbles had doc 16 (Privacy Design) with trust thresholds, capture filtering, sharing redaction, App Store privacy labels. UKU has "Sovereign & Private" as a principle but no specification.

11. **NAI inference engine not ported** -- ai-pebbles defined a DAG of 7 context signals with per-signal confidence scoring. UKU's Tier 3 ingestion references deterministic inference but doesn't define the signal DAG.

12. **_papers/ directory empty** -- Placeholder with no content.

13. **_dependencies/ directory empty** -- Placeholder with no content.

### What ai-pebbles Had That UKU Deliberately Dropped

The readiness gap analysis explicitly identifies these as **delegated to triad partners, not missing:**
- Consumer app architecture (Vault Core, Write Serializer, Event Bus)
- Economics & monetization
- Solo sync engine (HLC, LWW, device manifests)
- Solo search engine (Tantivy, FTS5)
- Operability (dashboards, monitoring)
- Reliability implementation (failure modes, degradation)
- Build vs Buy decisions (UniFFI, Wasmtime)
- 14-month phased execution plan

This is a strategic scope reduction, not an oversight.

## Cross-Repository Comparison: ai-pebbles vs uku-pebbles

| Dimension | ai-pebbles | uku-pebbles |
|-----------|-----------|-------------|
| Files | 331 (271 .py + 59 .md) | 20 (19 .md + 1 license) |
| Spec iterations | 42 (v0, v19, v42) | 3 (v2.1, v2.2, v2.3) |
| Spec documents | 16 numbered + design.md + references.md | 1 comprehensive spec file |
| Verification scripts | 271 Python files | None |
| Core model | Pebble = artifact + metadata | Pebble = descriptor wrapping artifact |
| Architecture | Monolithic (7+ components) | 4 bounded layers + triad delegation |
| LLM stance | "Zero custom ML in v1" but mixed in pipeline | Compile-time LLM boundary (Layers 1-3 pure) |
| Relationships | Typed ontological links only | Red strings (implicit) + typed edges (progressive) |
| External systems | Self-contained | Triad: SAGE (validation) + ByteRover (retrieval) |
| Schema maturity | Very high (44 invariants, TLA+ roadmap) | Early (missing validation rules, conformance levels, versioning) |
| Research depth | 7 deep research docs + 6 human docs | 3 insight docs + 4 discussion docs + SAGE summary + Grok debate |
| Strategic positioning | "App-first, format-second" | "AGENTS.md for knowledge work" |

## Recommendations

1. **Fix the license discrepancy** -- README says MIT, LICENSE file is Apache 2.0. Pick one.
2. **Reconcile version numbering** -- Is it v0.2.3 or v2.3? The changelog suggests 2.x lineage but the header says 0.2.3.
3. **Port validation rules from ai-pebbles** -- The readiness gap analysis's #1 priority. Per-field constraints, size limits, unknown field preservation.
4. **Add the 11 missing fields** -- Priority order from readiness gap: source_app, content_hash, extraction_provenance, consent_snapshot, people, then others.
5. **Specify the SAGE integration protocol** -- The conceptual flow exists; needs a detailed spec with field mapping, lifecycle handoff, and writeback model.
6. **Define conformance levels** -- Level 1 (Reader), Level 2 (Writer), Level 3 (Full) as planned in TODO.
7. **Add performance budgets** -- At minimum, capture latency and query latency targets.
8. **Consider porting the privacy design** -- ai-pebbles doc 16 had trust thresholds, capture filtering, consent snapshots, sharing redaction. UKU's "Sovereign & Private" principle needs operational specification.
