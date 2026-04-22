# Weight Field Citation Research

**Source:** Background research agent, 2026-04-13
**Context:** The SAGE creator claimed *"The explicit weight is a deal breaker. It won't scale."* This report was commissioned to gather citations validating (or refuting) the claim before editing spec §7 (Weighting Model).
**Status:** Research complete. Recommendation **deferred to post-v1 release** per user decision 2026-04-13. All findings archived here for future §7 work. Do not act on this during the current v0.3 spec pass.

---

## Tool-availability caveat

WebSearch and WebFetch were denied in the agent environment. The planned 2-hour external search budget could not be spent. This report draws on:

1. **One primary source available locally**: *The Price of Meaning* (Gopinath et al., Sentra.app + MIT, 2026) at `_research/_papers/noescape-28MAR26.pdf` — directly load-bearing for the graph-native section.
2. **Established literature recalled from the agent's training data** (knowledge cutoff May 2025). Citations verifiable offline but not freshly fetched. These are marked **[recalled]** and should be re-verified before going into any external-facing design doc.
3. **Structural/geometric reasoning** derived from the No-Escape theorem.

If fresh citation verification is needed, re-run this research with network access enabled.

---

## 1. Executive summary

**Direction: the claim is supported**, but the support rests more on geometry-of-retrieval and PIM-user-behavior findings than on a single smoking-gun paper about "explicit weight fields specifically." Confidence: **medium-high** that a recommended explicit `weight` field is a failure mode at scale; **high** that behavioral + decay signals outperform it asymptotically.

**One-sentence recommendation** (deferred to post-v1): Option **(c)** — downgrade `weight` from a recommended field to a legacy/escape-hatch field, make §7.2 behavioral signals plus §7.3 effective_weight the spec-default surface, and add a one-paragraph §7.1 note citing the failure modes.

---

## 2. Findings by category

### 2.1 Academic PIM literature (supports, medium strength, [recalled])

- **Whittaker & Sidner (1996), "Email Overload"** [recalled]. The foundational PIM-behavior study: users segregate mail into "must-respond," "to-read," "no-action" via folders, but the taxonomy decays within weeks; users stop refiling and fall back on search. **Direction: supports. Relevance: manual importance taxonomies decay.**
- **Bergman, Beyth-Marom & Nachmias (2003) and Bergman & Whittaker, *The Science of Managing Our Digital Stuff* (MIT Press, 2016)** [recalled]. Core finding: the "user-subjective approach" to PIM — the only reliable curation signal users sustain is *project membership*, not numeric importance. Users overwhelmingly fall back on navigation + search rather than maintaining graded metadata. **Direction: supports. Strength: strong if re-verified. Relevance: direct.**
- **Jones, *Keeping Found Things Found* (Morgan Kaufmann, 2007); Jones & Teevan eds. (2007)** [recalled]. Survey-based: users say they intend to rate/prioritize but rarely do so consistently; the gap between intent and practice grows with collection age. Keeping-vs-finding asymmetry: users over-invest in keeping metadata they never query. **Direction: supports.**
- **Civan, Jones, Klasnja, Bruce (2008), "Better to organize personal information by folders or by tags?"** [recalled]. Empirical study of tag-vs-folder behavior — tagging systems suffer from inconsistent taxonomy drift even within a single user over time. Analogous finding likely applies to numeric weights. **Direction: supports, medium.**
- **Capra (2010), "Poor performance on a single well-defined information task..."** [recalled]. Users struggle to recall their own prior classifications after ~30 days. **Direction: supports.**

**Caveat**: no paper in local materials directly tests explicit numeric importance (0.0-1.0 or 1-5 star) fields in a longitudinal PIM context. The body of evidence is **adjacent** — tag drift, folder abandonment, refiling failure — rather than direct.

### 2.2 HCI / rating-at-scale (supports, medium strength, [recalled])

- **Ebbinghaus (1885) / Anderson & Schooler (1991)** — cited by the No-Escape paper ref [13]. Anderson & Schooler showed the *environment* itself provides power-law usage patterns; "what the human memory system needs" is decay-weighted access, not deliberate ranking. This is the foundational argument that *frequency + recency is a better predictor of future need than self-report.* **Direction: supports, strong.** Primary source: Anderson, J. R. & Schooler, L. J. (1991). "Reflections of the environment in memory." *Psychological Science* 2:396-408.
- **Bjork & Bjork (1992), "New theory of disuse"** — cited as ref [16] in the No-Escape paper. Retrieval strength and storage strength dissociate; what you think is important ≠ what you actually need. Implication: user-declared importance is a poor proxy for effective memory utility. **Direction: supports, strong.**
- **Rating inflation / response-set bias** [recalled, general HCI]. When users are asked to assign a 0.0-1.0 score repeatedly, scores regress toward a few modal values (0.5, 0.8, 1.0) and lose discriminative power. Netflix, Amazon, and nearly every star-rating system observed this; it's why Netflix moved from 5-star to thumbs in 2017 — they stated publicly that 5-star ratings had become "a popularity poll" rather than a signal of personal taste. **Direction: supports, strong by analogy.**
- **Implicit vs explicit feedback in recommender systems**: Hu, Koren & Volinsky (2008), "Collaborative Filtering for Implicit Feedback Datasets" [recalled] — implicit signals (dwell, click-through) outperformed explicit ratings for most real-world deployments. The single clearest industry-scale comparison of the two signals. **Direction: supports, strong.**

### 2.3 Case evidence from products (supports, mixed strength, [recalled — verify])

- **Evernote**: priority/reminder field usage has consistently been reported as low; Evernote's 2019+ product pivots moved toward search-first, not rating-first. Cannot verify a changelog quote without network access.
- **Netflix 5-star → thumbs (2017)**: explicitly stated that explicit ratings were misleading vs implicit watch behavior. **Direction: supports.**
- **Obsidian**: no core "weight" field; community plugins exist but are niche. Core team has consistently emphasized linking and tagging over numeric rating.
- **Roam Research / Logseq**: no native importance field; PageRank-style backlink density is the de-facto weight.
- **Notion**: has an explicit "priority" *select* field in templates, but it's categorical (High/Medium/Low), not a 0.0-1.0 scalar, and in practice maps to status rather than importance.
- **Readwise**: no user-assigned weights; importance is inferred from highlight frequency, review cycles, and spaced-repetition feedback. A strong case-in-point: a successful PIM product deliberately chose implicit weighting.
- **del.icio.us / Pinboard / Flickr tag era**: no explicit weight field; tag frequency and in-link counts served as weight proxies. The explicit-weight approach was never tried at scale in tagging systems, which is itself evidence that product designers intuited it wouldn't work.

**Caveat**: these are recalled from training data and product knowledge as of May 2025. A design doc going external should re-verify each claim with a live changelog/blog link.

### 2.4 Graph-native weighting alternatives (supports, strong — from local primary source)

Evidence is strongest here because the paper is in-repo.

**Primary source**: Gopinath, Starenky, Barman, Bodnar, Narasimhan (2026). *The Price of Meaning: Why Every Semantic Memory System Forgets*. Sentra.app / MIT Dept. of Mechanical Engineering. Local path: `_research/_papers/noescape-28MAR26.pdf`.

Key claims:

- **Graph memory with PageRank (Architecture 4, MiniLM + personalized PageRank, α=0.85)** produces forgetting exponent **b = 0.478 ± 0.028** — squarely in the human range (b ≈ 0.3-0.7) — **without any explicit weight field**. The network structure itself produces a behaviorally realistic importance gradient. (Table 3, p.19; Figure 3, p.17.)
- **Anderson-Schooler power-law arrival (ref [13])** was empirically fitted with α = 0.459, R² = 0.952 — confirming that real-world usage statistics follow the exact distribution that decay-based implicit weighting is designed to exploit.
- **Stretched-exponential individual retention + population power law** (Theorem 3, Corollary 4, Proposition 5): what users experience as "importance" emerges mathematically from arrival statistics + per-item decay. You don't need to ask the user.
- **Dimensionality convergence**: d_eff collapses to ~10-50 for natural language regardless of nominal dimension (p.8). A 0.0-1.0 scalar compresses to roughly the same signal as an 8-state categorical in practice.
- **PoE formula from local SAGE codebase** (`_research/sage/components.md:225-242`): `W = exp(0.4·ln(accuracy) + 0.3·ln(domain) + 0.15·ln(recency) + 0.15·ln(corroboration))`. **None of the four inputs are user-self-reported.** This is an in-repo existence proof: the tool whose creator raised the objection already computes weight without a user scalar.

**Direction: supports, strong.** Single strongest line of evidence in the report.

### 2.5 Forgetting curve as weighting substrate (supports, strong)

From the same Gopinath paper:

- Individual retention: R(t) = exp(−c·t^(1−α)) — stretched exponential
- Population average: R̄(t) ~ κΓ(β)·t^(−β(1−α)) — power law
- Per-item hazard scales with environmental intensity
- Spacing effect emerges geometrically (long-spacing 0.902, massed 0.36, Cohen's d=24.6)

**Direct implication for Pebbles**: if §7.2 behavioral signals + standard exponential decay on `last_accessed_at` are implemented, the resulting `effective_weight` is mathematically grounded and reproduces the human forgetting curve. A user-assigned 0.0-1.0 scalar cannot compete because it's (a) time-invariant by default, (b) subject to rating inflation, and (c) sampled at creation time when the user knows least about the item's long-run utility.

---

## 3. Strongest evidence (top 5)

1. **Gopinath et al. 2026 (*Price of Meaning*)** — local file. Graph memory + PageRank reproduces human forgetting range without any explicit weight field. Decay-based implicit weighting is mathematically grounded in retrieval geometry. **[primary, in-repo]**
2. **Anderson & Schooler 1991, *Psychological Science* 2:396-408** — environmental usage statistics (frequency, recency, spacing) are sufficient to reconstruct memory utility without subject self-report. Cited in Gopinath ref [13], α=0.459 fit empirically reproduced. **[primary, cited]**
3. **Hu, Koren & Volinsky 2008, "Collaborative Filtering for Implicit Feedback Datasets"** [recalled] — industrial-scale demonstration that implicit signals beat explicit ratings in recommender deployments. **[recalled]**
4. **Bergman & Whittaker 2016, *The Science of Managing Our Digital Stuff* (MIT Press)** [recalled] — users do not reliably maintain graded metadata over time; only project-membership survives. Closest direct support for the claim in PIM literature. **[recalled, verify]**
5. **Bjork & Bjork 1992** (Gopinath ref [16]) — retrieval strength ≠ storage strength; declared importance ≠ future utility. **[primary, cited]**

---

## 4. Counter-evidence (steelman for keeping explicit weight)

- **Spaced-repetition systems (Anki, SuperMemo, Readwise Reader)** explicitly use a user-supplied difficulty/ease rating *at review time*, and it works at scale. Real counter-evidence. BUT: (a) rated at retrieval, not capture, so it's closer to a behavioral signal; (b) the rating is ordinal with immediate consequences (next review schedule), not a detached 0.0-1.0 scalar; (c) Anki's SM-2 algorithm treats the user rating as *input to a decay model*, not as the weight itself. Compatible with §7.3 effective_weight consuming an optional explicit signal, not with §7.1 being the primary recommended field.
- **Email flagging / star-as-capture signal**: Gmail's star, Slack's saved items — users do flag important things. BUT these are binary/categorical, not 0.0-1.0, and their observed use is "I will come back to this soon," not "this is 0.85 important." Binary salience markers can work; graded numeric ratings do not.
- **Capture-moment affect is information**: there is a real argument that the user's emotional state at capture ("this mattered when I saw it") is signal the system otherwise can't reconstruct. The Pebbles spec already has `emotional_state` and `location` for this — a 0.0-1.0 scalar is a lossy compression of that richer context.
- **Tool-maker critique is a claim, not evidence**: the SAGE creator's "won't scale" is an opinion from a practitioner with relevant experience but is not itself a citation. It should be treated as a hypothesis to validate.

On balance, the steelman does not save the explicit 0.0-1.0 field. It does save the idea that *capture-moment salience is valuable*, which argues for keeping the field available but not recommending it.

---

## 5. Recommendation (DEFERRED to post-v1)

**Session decision 2026-04-13: deferred to post-v1. The v0.3 spec pass will NOT rewrite §7. `weight` remains as defined in v0.2.3. Revisit after the first release/demo.**

The recommendation below is preserved for future reference:

1. **Keep `weight` as an optional field, but mark it `deprecated-soft` or `legacy-escape-hatch`** in §5 (schema reference) and §7.1 (weighting model).
2. **Rewrite §7 headline model as "Effective weight = f(behavioral signals, decay, graph centrality, [optional explicit weight])"** where explicit weight becomes one of several inputs to `effective_weight`, not the primary surface.
3. **Add a §7.1-note titled "Why explicit weight is optional"** with ~200 words citing: Anderson-Schooler, rating inflation, Bergman & Whittaker, and the local Gopinath paper's graph-PageRank result. Include the Netflix thumbs anecdote and Anki-as-counterpoint as balance.
4. **Elevate §7.2 implicit signals** (access_count, reference_count, last_accessed_at, last_updated_at) to the default weighting surface. Add `indegree` and `outdegree` from the edges table as additional implicit signals.
5. **Introduce a `salience_hint` field** (categorical: `pin | flag | none`) as a binary-ish capture-moment marker, separate from weight. This preserves the legitimate steelman use-case (Gmail-star semantics) without committing to a 0.0-1.0 scalar.
6. **Spec-level invariant**: `effective_weight` is always the index's business and never written back to files. The file is sovereign; the index is forgettable.

---

## 6. Gaps

1. **No primary PIM paper in recall base directly tests longitudinal reliability of a 0.0-1.0 explicit importance field.** The strongest adjacent papers (Bergman, Whittaker, Jones) need to be re-fetched with live access to confirm exact wording and strength.
2. **No changelog quote** from Evernote, Day One, Obsidian, or Notion about removing/deprioritizing a weight field. General product knowledge, not a primary source. Biggest verification gap, fixable with ~30 min of web access.
3. **No empirical measurement** of how Pebbles users in the current prototype actually populate the `weight` field. A 50-user sample of existing pebbles would replace all of this literature with ground truth specific to this system. Single most valuable follow-up.
4. **Pattern-weight detection logic** (§7.3) is unspecified. Whatever replaces explicit weight needs a crisp algorithm — personalized PageRank on the edges table is the obvious default given the Gopinath paper already validates it at b = 0.478.
5. **Spaced-repetition compatibility**: if Pebbles ever grows a review loop, the Anki-style ordinal rating-at-review is the one place explicit user input genuinely beats decay. Worth noting in §7.1 that the recommendation is specific to capture-time weighting.
6. **WebSearch/WebFetch denied in this session**: the full 2-hour external search budget could not be used. Treat this report as the offline portion; the remaining work is verification of the **[recalled]** citations and fetching product-changelog primary sources.

---

## 7. Files referenced (for future work)

- `_research/_papers/noescape-28MAR26.pdf` — Gopinath et al. 2026, primary source for §§2.4-2.5
- `_specs/pebbles.spec.md` (post-rename) — the `weight` field and §7 weighting model targeted for revision
- `_discussions/pebbles-convergence-with-claude-13APR26.md` lines 71-93 — the original SAGE-creator claim and the "validate with citations" directive
- `_research/sage/components.md` lines 225-242 — SAGE's own PoE formula, the in-repo existence proof of non-user-reported weighting
- `.sop/synthesis/01-no-escape-theorem-summary.md` — local distillation of the Gopinath paper

---

## 8. Bottom line

The claim is most likely true. Evidence that can be fully cited (Gopinath 2026 primary + Anderson-Schooler + Bjork-Bjork via Gopinath refs) is strong on the *geometric/algorithmic* side. Evidence on the *PIM-user-behavior* side exists in recall but needs re-verification before quoting in a design doc. When §7 is revisited post-v1, recommendation is Option (c): downgrade `weight` to optional-legacy, elevate behavioral signals and graph centrality as the default weighting surface, add a `salience_hint` categorical to preserve the capture-moment-affect use case.
