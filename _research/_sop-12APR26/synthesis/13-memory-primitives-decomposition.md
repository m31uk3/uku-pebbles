# Memory Primitives Decomposition

**Source:** /btw note during synthesis convergence
**Context:** The No-Escape theorem and our convergence analysis focus on retrieval and forgetting. But memory has more primitives than that. Not to mention the different surfaces of memory: **episodic, semantic, and procedural.**

## What This Means for the Spec

Three implications worth surfacing:

### 1. UKU v0.2.3 only handles episodic memory

The current `uku_type` values (`experience_capture`, `insight`, `problem_statement`, `proposed_solution`, `ontology_element`) are all episodic with the partial exception of `ontology_element` which gestures toward semantic. **There's no procedural type. This is a gap.**

| Memory Type | What It Encodes | UKU Coverage |
|-------------|----------------|--------------|
| **Episodic** | Specific events you experienced ("I met Sarah at the cafe yesterday") | Covered: experience_capture, insight, problem_statement, proposed_solution |
| **Semantic** | Facts and concepts ("Sarah is a Stanford grad student") | Partial: ontology_element gestures here |
| **Procedural** | How to do things, skills, sequences ("How I make my morning coffee") | **MISSING** |

Procedural memory deserves its own `uku_type`. Skills, recipes, runbooks, workflows are all procedural -- and they're a huge category of personal knowledge that the current spec cannot represent cleanly.

### 2. The consolidation hierarchy IS the episodic→semantic transition

The synthesis (doc 02) already noted that L0→L1→L2→L3+ maps to compression in the No-Escape paper's Solution 4 sense. **But it should be reframed more precisely:**

- **L0 = episodic memory** -- raw pebbles, specific events, full detail
- **L1, L2 = consolidation gradient** -- partial abstraction, themed grouping
- **L3+ = semantic memory** -- abstracted concepts, generalized knowledge

This is **exactly the Complementary Learning Systems (CLS) hypothesis operationalized**. McClelland, McNaughton & O'Reilly 1995: fast hippocampal encoding (episodic) + slow neocortical consolidation (semantic). The brain doesn't pick one or the other; it uses both, and the consolidation gradient between them is what makes memory work.

UKU's L0→L3+ hierarchy isn't just a compression scheme. **It's a CLS implementation.** This reframing matters because it tells us:
- What L1-L2 nodes should look like (partial abstractions, not aggregations)
- How agents should walk the gradient (start specific, generalize as needed)
- Why the spec needs explicit consolidation policies, not just "create edges when desired"

### 3. Forgetting/eviction is missing entirely from the spec

UKU has no story for:
- **How pebbles age out** -- do they decay automatically?
- **Whether they decay, are archived, or get evicted** -- one-way deletion vs reversible archive vs hard eviction
- **Who decides** -- the user, an agent, time-based policy, importance-weighted
- **Whether forgetting is destructive or reversible** -- can you un-forget?

The No-Escape theorem says forgetting is inevitable for semantic systems -- but **UKU's red strings are immune to that specific failure mode** (b=0, FA=0). So UKU has the unusual property of being able to **make forgetting an explicit design choice rather than an inevitable consequence.**

**That's a design surface the spec hasn't claimed yet.** And it's a major one. Every memory system has to handle forgetting; UKU's structural advantage means we get to choose *what kind* of forgetting we want.

## The Reframe

The synthesis Doc 02 maps the triad (UKU + SAGE + ByteRover) onto the No-Escape Theorem's Exit 2 components. **But it should be expanded to map onto the memory primitives decomposition:**

| Primitive | Triad Owner | Status |
|-----------|------------|--------|
| **Encoding** | UKU schema (frontmatter design) | Spec'd, **needs procedural surface** |
| **Storage** | UKU files + Postgres index | Spec'd |
| **Retrieval/Search** | UKU red strings + ByteRover Memory Swarm | Spec'd, this is where the synthesis focuses |
| **Forgetting/Eviction** | **Unowned** | **Gap** |
| **Consolidation** | UKU L0->L3+ hierarchy | Spec'd but **not framed as CLS** |
| **Reconsolidation** | SAGE consensus updates? | **Unclear** |

**Forgetting/eviction and reconsolidation are the two biggest open primitives.** They deserve their own synthesis docs. **Procedural memory deserves a `uku_type`.**

## Why This Matters Before Code

This is the kind of decomposition that would strengthen the v0.3 synthesis considerably -- and **probably needs to land before any code gets written**, because the storage layer's schema needs to support whatever forgetting and reconsolidation policies we choose.

Specifically:
- If pebbles can be forgotten/evicted, the schema needs an `evicted_at` or `archived_at` field
- If forgetting is reversible, we need a separate "tombstone" or "shadow" storage tier
- If consolidation walks a gradient, we need explicit `consolidation_level: int` field
- If procedural memory exists, the body format may need step-sequence semantics
- If reconsolidation happens via SAGE consensus, we need a `last_reconsolidated_at` field

**These are schema decisions, not implementation decisions.** They have to be made before the storage layer is built, or we'll have to migrate everything later.

## Proposed Additions to UKU Spec

### New uku_type values
```yaml
uku_type:
  - experience_capture    # episodic - existing
  - insight              # episodic/semantic boundary - existing
  - problem_statement    # episodic - existing
  - proposed_solution    # episodic - existing
  - ontology_element     # semantic - existing
  - procedural           # NEW: procedural memory
  - skill                # NEW: learned capability
  - reference            # NEW: pure semantic (no episodic anchor)
```

Actually, simpler: add a separate `memory_kind` field that is orthogonal to `uku_type`:

```yaml
memory_kind: episodic   # episodic | semantic | procedural
```

This keeps `uku_type` for the user's intent ("what kind of thing is this?") and adds `memory_kind` for the cognitive science classification ("how should this be retrieved and consolidated?").

### New lifecycle fields
```yaml
# Existing
created_at: 2026-04-12T10:00:00Z
updated_at: 2026-04-12T10:00:00Z

# Proposed
last_accessed_at: 2026-04-12T15:30:00Z   # for importance weighting
consolidation_level: 0                    # 0=raw, 1=consolidated, 2=MOC, 3+=meta
status: active                            # active | archived | evicted | tombstoned
status_reason: ""                         # why this status (user choice, policy, age)
status_changed_at: 2026-04-12T16:00:00Z
reversible: true                          # can this status be undone?
```

### New forgetting policy
This isn't a per-pebble field, it's a vault-level policy:

```yaml
# In vault.yaml or .pebble-config
forgetting_policy:
  default_action: archive   # archive | evict | tombstone | never
  age_threshold: 365d       # archive after X days unused
  importance_floor: 0.1     # protect pebbles with effective_weight > X
  user_override: true       # allow per-pebble pin/protect
```

## Connection to the Forgetting Curve

The No-Escape paper's Figure 2 shows forgetting curves across architectures. UKU's structural immunity (b=0) means **we don't have a forgetting curve we're stuck with**. We have a forgetting curve we get to design.

This is a remarkable position. Every other memory system the paper tested is *constrained* by the geometry to forget a certain way. UKU is the only one that can choose.

The choice we make becomes part of the spec's value proposition: **"Pebbles forgets when you want it to, not when geometry forces it to."**

## Action Items

- [ ] Add `memory_kind` field to UKU schema (episodic/semantic/procedural)
- [ ] Add `procedural` related uku_types or accept `memory_kind` as the discriminator
- [ ] Add lifecycle fields (status, reversible, consolidation_level, last_accessed_at)
- [ ] Define vault-level forgetting policy structure
- [ ] Write synthesis doc on reconsolidation (SAGE integration)
- [ ] Reframe consolidation hierarchy (L0->L3+) as CLS implementation in the spec
- [ ] Add forgetting design choice as a top-level value proposition
- [ ] Update Phase 0 (schema finalization) to include all of the above before code starts

## Open Questions

1. Should `memory_kind` be a new field or should we extend `uku_type`?
2. Is procedural memory really distinct enough to warrant its own type, or is it just `experience_capture` with step semantics in the body?
3. Should forgetting be per-pebble (each pebble decides) or per-vault (vault policy)?
4. Does reversibility need a separate "shadow vault" or can tombstones live in the main vault with a flag?
5. How does SAGE consensus interact with reconsolidation? (When consensus updates a fact, does it create a new pebble version or modify in place?)
6. Should consolidation_level be set by the user or computed from edges?
