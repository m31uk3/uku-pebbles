# Next Session Reading List

**Purpose:** Minimal context required to resume Phase 0 (schema finalization) work or address the 14 open questions in doc 11 section 7.

**Total reading budget:** 9 files (Tier 1 + Tier 2). The rest are reference material to look up as needed.

---

## Tier 1 -- Must read in this order

| # | File | Why |
|---|------|-----|
| 1 | `.sop/synthesis/11-final-converged-synthesis.md` | The roadmap. Phase 0 expanded scope. Section 7 has all 14 open questions. |
| 2 | `.sop/synthesis/13-memory-primitives-decomposition.md` | The new memory work. Forgetting/eviction, procedural memory, CLS reframing. **This is what expanded Phase 0.** |
| 3 | `.sop/synthesis/10-kinetic-vs-non-kinetic.md` | The new facet axis. Need to know the proposed schema change before touching the spec. |
| 4 | `.sop/synthesis/04-pdd-answers.md` | The user's directional answers. Source of truth for "what does Luke want." |
| 5 | `_specs/uku-pebbles.spec.md` | The current v0.2.3 spec. **This is the file we'll be modifying in Phase 0.** |

## Tier 2 -- Strong context

| # | File | Why |
|---|------|-----|
| 6 | `.sop/synthesis/01-no-escape-theorem-summary.md` | The formal mathematical validation. Why UKU's structural choices are correct. |
| 7 | `.sop/synthesis/02-convergence-analysis.md` | How the theorem maps to UKU triad. The structured-metadata hypothesis. |
| 8 | `.sop/synthesis/12-c4-architecture-communication.md` | The C4 deliverable strategy. Phase 1 needs Context + Container diagrams. |
| 9 | `TODO.md` | Already-tracked open work in the repo. Some Phase 0 items may already be there. |

## Tier 3 -- Reference (look up as needed)

| File | When to read |
|------|--------------|
| `.sop/synthesis/09-glossary.md` | Acronyms (RRF, LoCoMo, BM25, DRM, TOT, CLS, SPP, JUMBF, etc.) |
| `.sop/synthesis/05-defuddle-investigation.md` | Only if browser surface comes up |
| `.sop/synthesis/06-obsidian-clipper-investigation.md` | Only if browser surface comes up |
| `.sop/synthesis/07-locomo-investigation.md` | Only if eval methodology comes up |
| `.sop/synthesis/08-container-format-research.md` | Only if Tier 2 storage decisions come up |

## Tier 4 -- Skip unless explicitly asked

- `.sop/synthesis/00-source-matrix.md` -- just source metadata
- `.sop/synthesis/03-pdd-questions.md` -- superseded by doc 04 (the answers)
- `_research/sage/*` -- SAGE is delegated; only relevant if reconsolidation/integration comes up
- `_insights/*` -- origin context, captured in synthesis docs
- `_discussions/*` -- origin context, captured in synthesis docs
- `_research/_papers/noescape-28MAR26.pdf` -- already extracted into doc 01
- `.sop/summary/*` -- codebase structure, useful for orientation but synthesis is more current
- `AGENTS.md`, `README.md` -- public-facing, synthesis has internal-facing context

---

## Key Facts to Keep Top-of-Mind

These are decisions already made. Do NOT re-derive them in the next session.

### Stack
- **TypeScript** for everything (CLI, schema validator, defuddle fork, clipper fork, Postgres indexer)
- **Python** only for eval framework (LoCoMo is Python; CC BY-NC license means eval must be in a separate repo from commercial code)

### Container Format (decided)
- **Tier 1:** `pebble.md` (Markdown + YAML frontmatter) for pure text
- **Tier 2:** `.pebble` (zip envelope, EPUB pattern) for artifacts
- **Tier 3:** native export with `.yaml` sidecar OR embedded XMP for interop

Decisive evidence: Apple Photos, Google Photos, Notion all gave up on header injection. Day One uses zip. EPUB/DOCX/ODF all use zip. **Approach A wins 9-2.** Don't relitigate.

### Forks (decided)
- Fork **defuddle** (TypeScript, MIT, kepano) for Tier 3 inference during extraction
- Fork **obsidian-clipper** (TypeScript, MIT, depends on defuddle) for Tier 2 user input UI
- Two-layer fork strategy: Tier 3 inference belongs in defuddle, Tier 2 UI belongs in clipper

Bonus context: Steph Ango (@kepano) is the author of both AND the "file over app" essay we're philosophically aligned with.

### The Hypothesis to Test
Structured red strings on Ekman 8 emotions + 5 uku_types + 4 intents + 2 modalities sit at a new point on the Pareto frontier above BM25 (which the No-Escape paper measured at 15.5% semantic agreement on unstructured text). Same b=0/FA=0 immunity, much higher semantic agreement because controlled vocabularies encode meaning into the field values themselves.

64+ facet combinations from just 3 fields (8 × 4 × 2). This is testable on LoCoMo.

### Strategic Stance
**Pebbles is the blueprint, not the product.** Don't build what others can build. Moat comes from:
1. Mindful attribute design (precise schema execution, eval-validated)
2. Viral mass adoption (AGENTS.md / SKILLS.md model)

What we're NOT building: vector DB, BFT consensus, agent runtime, encryption, sync engine, mobile app, marketplace. All delegated to SAGE/ByteRover or community.

### Phase 0 Expanded Scope
Phase 0 was originally 1 week of vocabulary finalization. It's now ~2 weeks because the memory primitives /btw insight (doc 13) added schema decisions that **must land before any storage code** or we'll have to migrate later:

- `memory_kind` field (episodic/semantic/procedural)
- Procedural memory surface (new uku_types or memory_kind discriminator)
- Lifecycle fields (status, reversible, consolidation_level, last_accessed_at)
- Vault-level forgetting policy structure
- Reframe consolidation hierarchy as CLS implementation
- Reconsolidation model (SAGE consensus boundary)

### The 14 Open Questions (from doc 11 section 7)

The user said: *"address the open questions first"* may be the right move before starting Phase 0 schema work itself. The questions split into 4 categories:

**Vocabulary / schema (Q1, 2, 3, 9, 10, 14)**
1. Ekman 8 vs Plutchik's wheel for emotional_state
2. Modality field placement (top-level vs sub of intent)
3. Should ontology_element be at the same level as other uku_types
9. memory_kind as new field vs extending uku_type
10. Is procedural distinct enough to warrant its own type
14. consolidation_level: user-set or computed from edges

**Naming / branding (Q4)**
4. `.pebble` extension vs `.uku`

**Architecture (Q5, 7, 8)**
5. CLI direct-to-Postgres vs daemon pattern
7. Conformance levels: Reader / Writer / Full
8. Monorepo vs separate repos

**Lifecycle / forgetting (Q6, 11, 12, 13)**
6. Schema versioning (semver, compat matrix, migration determinism)
11. Forgetting granularity: per-pebble vs per-vault
12. Reversibility storage: shadow vault vs flagged tombstones
13. Reconsolidation model: new pebble version vs in-place modification

---

## Recommended Starting Pattern

```
Read Tier 1 (5 files) ............ ~10 min orient
Read Tier 2 (4 files) ............ ~10 min context
Look up Tier 3 only as needed
Skip Tier 4 unless asked
```

After reading: **ask the user which mode they want to start in**:
- (A) Address open questions first (Q1-Q14, batch them by category)
- (B) Start Phase 0 schema work (modify `_specs/uku-pebbles.spec.md` directly)
- (C) Both in parallel (resolve schema-related questions while writing the spec changes)

The user already flagged option A as a possibility: *"address the open questions first"*. Default to asking which mode unless context makes it obvious.

---

## What NOT to Do at Session Start

- **Don't re-read the No-Escape paper.** Doc 01 has everything needed.
- **Don't re-investigate defuddle/clipper/locomo.** Docs 05/06/07 have full reports.
- **Don't relitigate the container format decision.** It's settled in doc 08.
- **Don't ask the original 5 PDD questions again.** Doc 04 has the answers.
- **Don't re-derive the stack choice.** TypeScript is decided.
- **Don't suggest building things that are explicitly out of scope** (vector DB, BFT, encryption, sync, mobile, marketplace).

---

## File Locations (so the agent doesn't have to grep)

- Repo root: `/Users/ljack/github/m31uk3/uku-pebbles`
- Spec: `/Users/ljack/github/m31uk3/uku-pebbles/_specs/uku-pebbles.spec.md`
- Synthesis: `/Users/ljack/github/m31uk3/uku-pebbles/.sop/synthesis/`
- Codebase summary: `/Users/ljack/github/m31uk3/uku-pebbles/.sop/summary/`
- Research: `/Users/ljack/github/m31uk3/uku-pebbles/_research/`
- Discussions: `/Users/ljack/github/m31uk3/uku-pebbles/_discussions/`
- Insights: `/Users/ljack/github/m31uk3/uku-pebbles/_insights/`

External repos (not in uku-pebbles, but referenced):
- defuddle: `/Users/ljack/github/defuddle`
- obsidian-clipper: `/Users/ljack/github/obsidian-clipper`
- locomo: `/Users/ljack/github/locomo`
- (deprecated) ai-pebbles: `/Users/ljack/github/m31uk3/ai-pebbles`

---

## Sanity Check

After reading Tier 1 + Tier 2, the next-session agent should be able to answer YES to all of these:

- [ ] Can I name the four bounded layers of UKU and their LLM boundary?
- [ ] Do I know what the No-Escape Theorem proves and what Exit 2 is?
- [ ] Can I name the three triad components and their roles?
- [ ] Do I know which fields are in v0.2.3 and which are proposed additions?
- [ ] Can I list the 14 open questions and group them by category?
- [ ] Do I know why Phase 0 expanded from 1 week to ~2 weeks?
- [ ] Can I explain the structured-metadata hypothesis in one paragraph?
- [ ] Do I know which language we're using and why?
- [ ] Can I name what we're explicitly NOT building?
- [ ] Do I know the difference between Tier 1, Tier 2, and Tier 3 storage?

If any answer is no, re-read the relevant Tier 1 doc.
