# Cold Start — Resuming Pebbles Spec Work

**Last updated:** 2026-04-13 (after spec v0.3.0-draft landed)
**Purpose:** Single entry point for a fresh agent picking up the Pebbles project. Read this file first, then read the files it points to in the order specified. This file supersedes `.sop/synthesis/14-next-session-reading-list.md` (which served the previous session and is now historical).

---

## Where the project is now

Pebbles is a sovereign personal memory schema, designed as the **blueprint, not the product**, for capturing lived experience and making it queryable without LLM calls. The current spec is **v0.3.0-draft** at `_specs/pebbles.spec.md`. It was rewritten on 2026-04-13 to incorporate ratified answers to 14 open questions.

**Phase 0 (schema finalization) is essentially complete.** The next phase is the TypeScript reference implementation (Phase 1: CLI + schema validator + .pebble zip reader/writer). No code has been written yet for v0.3 — only the spec.

The user is **Luke Jackson** (m31uk3 on GitHub), the spec author. They prefer terse, high-confidence collaboration and will push back hard on hedging, premature abstraction, scope creep, or unrequested work. When in doubt, propose decisively rather than presenting options.

---

## Files to read in order

### Tier 1 — Mandatory, in this order

| # | Path | Why |
|---|------|-----|
| 1 | `_specs/pebbles.spec.md` | The current spec, v0.3.0-draft. **Source of truth.** Read in full. |
| 2 | `.sop/cold-start.md` | This file. You're already reading it. |
| 3 | `.sop/synthesis/15-weight-field-citation-research.md` | Citation research on the `weight` field. §7 of the spec is still v0.2.3 form pending this work; do not touch §7 without re-reading this. |
| 4 | `.sop/synthesis/11-final-converged-synthesis.md` | The overall roadmap and Phase 0–6 plan. Section 7 has the original 14 open questions (now all ratified). |
| 5 | `.sop/synthesis/13-memory-primitives-decomposition.md` | Memory primitives (episodic / semantic / procedural), forgetting/eviction, CLS reframing. Drove much of the v0.3 expansion. |

### Tier 2 — Strong context

| # | Path | Why |
|---|------|-----|
| 6 | `.sop/synthesis/10-kinetic-vs-non-kinetic.md` | The `modality` axis. |
| 7 | `.sop/synthesis/04-pdd-answers.md` | The user's directional answers from the original PDD round. |
| 8 | `.sop/synthesis/01-no-escape-theorem-summary.md` | The mathematical validation. Why Pebbles' structural choices are correct. |
| 9 | `.sop/synthesis/02-convergence-analysis.md` | How the No-Escape theorem maps to the architecture. **STALE NOTE: still references the SAGE+ByteRover triad framing — that has been reframed in v0.3 to "Pebbles + optional runtime integrations." See the deferred-work table below.** |
| 10 | `.sop/synthesis/12-c4-architecture-communication.md` | C4 diagram strategy for Phase 1 deliverables. |

### Tier 3 — Reference (look up only when needed)

| Path | When to read |
|------|--------------|
| `.sop/synthesis/09-glossary.md` | Acronyms (RRF, LoCoMo, BM25, DRM, TOT, CLS, SPP, JUMBF, etc.) |
| `.sop/synthesis/05-defuddle-investigation.md` | Only if browser surface comes up |
| `.sop/synthesis/06-obsidian-clipper-investigation.md` | Only if browser surface comes up |
| `.sop/synthesis/07-locomo-investigation.md` | Only if eval methodology comes up |
| `.sop/synthesis/08-container-format-research.md` | Only if Tier 2 storage decisions come up |
| `_research/_papers/noescape-28MAR26.pdf` | The Gopinath et al. paper. Doc 01 has everything needed; only re-read if you need a primary source quote. |
| `_discussions/pebbles-convergence-with-claude-13APR26.md` | The session transcript that produced v0.3 — useful if you want to understand *why* a decision was made. |

### Tier 4 — Skip unless explicitly asked

- `.sop/synthesis/00-source-matrix.md` — source metadata only
- `.sop/synthesis/03-pdd-questions.md` — superseded by doc 04 (the answers)
- `.sop/synthesis/14-next-session-reading-list.md` — historical, served the previous session only
- `_research/sage/*` — SAGE is non-normative (Appendix G); only relevant if integration patterns come up
- `_insights/*`, `_discussions/*` (other dates) — origin context, captured in synthesis docs
- `.sop/summary/*` — codebase structure, useful for orientation but synthesis is more current
- `AGENTS.md`, `README.md` — public-facing, this file has internal-facing context

---

## What's been ratified — DO NOT re-litigate

The user explicitly ratified all 14 open questions on 2026-04-13. Summary:

| # | Question | Decision |
|---|----------|----------|
| 1 | emotion vocabulary | Plutchik 8 Primary (8 values unchanged from v0.2.3, label corrected from "Ekman 8") |
| 2 | modality placement | Top-level field |
| 3 | ontology_element | Promoted to first-class `pebble_type: ontology` + `governed_by` 1:many link |
| 4 | `.pebble` vs `.uku` | `.pebble` for file; UKU is the explainer expansion only |
| 5 | CLI vs daemon | Direct CLI for v0.1–0.2; daemon reconsidered in Phase 3 if browser fork needs a local endpoint |
| 6 | schema versioning | Wire format only; curation freely edits curator-editable fields without versioning events |
| 7 | conformance | Layer-based (no Reader/Writer/Full taxonomy) |
| 8 | monorepo | Monorepo for Phase 0–2; defuddle/clipper/eval forks are separate repos |
| 9 | memory_kind | New orthogonal field, separate axis from `pebble_type` |
| 10 | procedural distinctness | `memory_kind: procedural` value (not a `pebble_type` value) |
| 11 | forgetting granularity | Vault defaults + per-pebble overrides; system never auto-tombstones or auto-deletes |
| 12 | reversibility storage | Flagged tombstones in same vault; shadow vault rejected |
| 13 | reconsolidation | Capture-immutable + curator-editable field classes; SAGE/ByteRover removed from core spec |
| 14 | consolidation_level | Removed from YAML; derived from edge topology at query time |

**Plus format decisions:**
- **ULID** for `pebble_id` (26 alphanumeric chars, time-sortable, no prefix). Crockford Base32 — no I/L/O/U.
- **(label, uid) object tuple** for all pebble→pebble cross-references
- **Full ISO 8601 with timezone** for all temporal fields (date-only values invalid)
- **`archive_at`** preserved as a curator-editable scheduling primitive
- Spec file renamed: `_specs/uku-pebbles.spec.md` → `_specs/pebbles.spec.md`
- Synthesis file `.sop/synthesis/15-weight-field-citation-research.md` archives the deferred §7 research

---

## What's deferred — don't start without explicit user confirmation

| Item | Where | Status |
|------|-------|--------|
| §7 Weighting Model rewrite | `_specs/pebbles.spec.md` §7 | Deferred post-v1. The full recommendation is in `.sop/synthesis/15-weight-field-citation-research.md` (Option (c): downgrade `weight` to optional-legacy, elevate behavioral signals + graph centrality, add `salience_hint` categorical). The research was conducted offline (no network); citations marked `[recalled]` need re-verification. |
| Synthesis doc 02 / 11 revision | `.sop/synthesis/02-convergence-analysis.md`, `.sop/synthesis/11-final-converged-synthesis.md` | Both still reference the SAGE+ByteRover "triad" framing. Per Q13 ratification, this should be reframed as "Pebbles + optional runtime integrations." Non-blocking; not done yet. |
| `ARCHITECTURE.md` | does not exist yet | Should hold Q5 (CLI direct) + Q8 (monorepo structure) and other implementation notes that don't belong in the spec. Non-blocking. |
| Phase 1 implementation | `packages/` (does not exist yet) | TypeScript reference implementation. Schema validator, CLI, .pebble zip I/O. Sequenced after spec is locked. |

---

## What NOT to do

- **Don't re-derive any of the 14 ratified answers.** They are locked.
- **Don't add SAGE or ByteRover as required dependencies.** They are non-normative integration patterns (Appendix G). The spec is sovereign.
- **Don't add `consolidation_level` back to the YAML.** It is derived at query time from edge topology (§9.1).
- **Don't touch `weight` or §7 in v1.** That work is deferred and tracked in synthesis doc 15.
- **Don't propose a Reader/Writer/Full conformance taxonomy.** Conformance is layer-based per §3.
- **Don't propose a shadow vault for tombstones.** Flagged tombstones in the same vault is the decision.
- **Don't auto-delete or auto-tombstone anything.** The system can only auto-archive. Tombstone and hard-delete are user-only operations.
- **Don't add date-only temporal values.** All timestamps are full ISO 8601 with timezone (`Z` preferred).
- **Don't use `uku-` or `uku_` prefixes for new identifiers.** The brand is `pebble`. UKU is the formal expansion used once in §1 only.
- **Don't propose building things that are explicitly out of scope** (vector DB, BFT consensus, agent runtime, encryption, sync engine, mobile app, marketplace).

---

## Sanity check

After reading Tier 1 + Tier 2, you should be able to answer YES to all of these:

- [ ] Can you name the four bounded layers of Pebbles and identify the LLM boundary?
- [ ] Do you know what the No-Escape Theorem proves and what Exit 2 is?
- [ ] Can you list the 6 `pebble_type` values and the 3 `memory_kind` values?
- [ ] Do you know the difference between capture-immutable and curator-editable fields?
- [ ] Can you describe the L0 → L1 promotion operation in Zettelkasten terms (atomic, Luhmann, own words, linked)?
- [ ] Do you know why §7 is deferred and where the deferred research lives?
- [ ] Can you explain why ULID was chosen over UUID v7?
- [ ] Do you know which language the implementation will be written in (and why)?
- [ ] Can you name what is explicitly NOT being built?
- [ ] Do you know the difference between a fleeting pebble (wrapper for any artifact) and a permanent pebble (markdown-native body)?
- [ ] Can you name two things the user has pushed back on hardest in this project (hedging, scope creep, premature abstraction, restating what they already know)?

If any answer is no, re-read the relevant Tier 1 file.

---

## How to start the conversation

Once you've read Tier 1 + Tier 2 and passed the sanity check, ask the user which mode they want to start in:

- **(A) Phase 1 implementation** — TypeScript reference impl: schema validator, CLI, `.pebble` zip I/O. This is the obvious next step.
- **(B) Synthesis revision** — update docs 02 and 11 to reflect SAGE/ByteRover as integration patterns, not core triad components.
- **(C) `ARCHITECTURE.md` write-up** — capture Q5 (CLI direct) + Q8 (monorepo structure) and other implementation notes.
- **(D) Citation re-verification** — re-run the deferred §7 weight research with network access enabled.
- **(E) Something the user names** — they may have a fresh direction.

**Default to asking unless context makes it obvious.** Do not just start working on (A) without confirmation.

---

## File locations (so you don't have to grep)

- **Repo root**: `/Users/ljack/github/m31uk3/uku-pebbles`
- **Spec**: `_specs/pebbles.spec.md`
- **Cold start**: `.sop/cold-start.md` (this file)
- **Synthesis**: `.sop/synthesis/`
- **Codebase summary**: `.sop/summary/`
- **Research papers**: `_research/_papers/`
- **Discussions**: `_discussions/`
- **Insights**: `_insights/`

External repos (referenced but not in this repo):
- defuddle: `/Users/ljack/github/defuddle`
- obsidian-clipper: `/Users/ljack/github/obsidian-clipper`
- locomo: `/Users/ljack/github/locomo`
- (deprecated) ai-pebbles: `/Users/ljack/github/m31uk3/ai-pebbles`

---

## Maintenance rule

**Update this file in place rather than creating a new one.** A single canonical entry point is more valuable than a chain of "next session" docs. When the project state changes meaningfully (new spec version, new phase, ratified decisions), bump this file and reference it in the commit message so future agents reading `git log` find it immediately.
