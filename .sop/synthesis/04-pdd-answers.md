# PDD Answers: v0.1 Infrastructure Direction

**Date:** 2026-04-12
**Status:** Answered, awaiting investigation results

---

## A1: First Tangible Demo

**Answer: Option C (Both) -- but reframed**

The CLI is the primary tool. The "importer" framing was wrong -- this is not import, it's **active interception**. The browser surface integration must be done via forks of:
- `/Users/ljack/github/defuddle`
- `/Users/ljack/github/obsidian-clipper`

**Design question:** During design we must decide how best to intercept these to introduce additional YAML attributes per the Pebbles spec. Could this be done by a simple fork?

**The CLI MUST be standalone** and implement Pebbles for all non-browser surfaces:
- Screenshots
- Images
- Documents
- Any artifact

This also enables agents to have a simple interface for creating pebbles for any artifact.

---

## A2: Stack Decision -- Driven by Dependencies

**Answer:** No integration friction with anyone for proof of concept. Language choice **must be driven by the dependency on clipper and/or defuddle**.

**Action required:** Investigate both codebases and confirm:
- Are both required, or only one?
- What language makes the most sense for Pebbles YAML attribute insertion?

**Plus a critical container format question:**

**Option A: Hybrid envelope** -- zip/tar.gz approach that envelops/compresses the artifact yet still allows instant access to the YAML frontmatter. Hybrid that keeps everything together.

**Option B: MIME/file header injection** -- "Cute things" with file headers for full backward compatibility. Needs research: is it possible to reliably store YAML/JSON in file headers?

Both options need evaluation.

---

## A3: Structured Metadata Hypothesis -- YES, Test It

**Answer: Yes.** "Red strings on Ekman 8 emotions, 5 uku_types, and 4 intents could score significantly higher while maintaining b=0, FA=0."

**Plus a new dimension to evaluate:** kinetic vs non-kinetic red strings.

**Concept:** Some attributes are kinetic (actions), others are non-kinetic (thoughts/states). This delineation could be a powerful search space reducer because users can easily infer/recall during query: "was it an action or a thought?"

**Action required:** Evaluate any research that touched on this kinetic vs non-kinetic distinction. This will be a powerful axis for facet-based query.

---

## A4: ByteRover Integration & The Bigger Picture

**Answer: Yes, exactly stems from Andy's post.**

> "the design principle behind what we're shipping with ByteRover's Memory Swarm federated search across BM25, wikilink graph expansion, and hybrid vector+keyword, fused with RRF. Each retrieval method has uncorrelated blind spots. BM25 misses paraphrases, embeddings miss exact terms, graph traversal misses unlinked knowledge. The ensemble doesn't eliminate failure, it decorrelates it."

### Action items
- **Fully clarify all acronyms** (RRF, LoCoMo, BM25, RAG, etc.) in an appendix glossary
- **Investigate** `/Users/ljack/github/defuddle` and `/Users/ljack/github/locomo`
- **Evaluations will be a HUGE aspect of pebbles** as validated by the No-Escape paper
- **Copy the paper** to `/Users/ljack/Library/Mobile Documents/iCloud~md~obsidian/Documents/m31uk3/_m31uk3/uku-pebbles/_research/_papers`

### Reframing the implementation question

The original Q4 framing was unclear. The clearer question is:

**If pebbles is the schema AND the ingestion tooling (CLI + fork of clipper/defuddle), then we need to think carefully about the integration end points for ByteRover and anyone else.**

This is fundamentally a question of: **converting non-pebblized content into pebblized content** and exposing that function as an endpoint (MCP, CLI, API).

### The Two Sources of Pebbles' UVP

This is NOT going to be Pebbles' moat or stickiness. The true UVP comes from two things:

1. **Mindful attributes** (8 emotions, 5 uku_types, 4 intents -- these need finalization) and precise execution of the schema, which unlocks new measurable performance provable via evals like LoCoMo.

2. **Rapid mass market adoption** similar to AGENTS.md and SKILLS.md.

### Strategic Insight

As soon as critical mass is reached in market attention/adoption, there will be a million new endpoints that can implement/create pebbles -- in the same way that there are infinite ways to create Skills and Agents .mds.

**Pebbles intends to be the blueprint for the future, not the product itself.**

The organic ingestion push (CLI + clipper/defuddle forks) is a stepping stone. Long term it will be replaced by native implementation in OS/device owners (macOS, Android, iOS) replacing the feckless functionality that exists today.

### Inspiration

> "If you want your writing to still be readable on a computer from the 2060s or 2160s, it's important that your notes can be read on a computer from the 1960s.
>
> You should want the files you create to be durable, not only for posterity, but also for your future self. You never know when you might want to go back to something you created years or decades ago. Don't lock your data into a format you can't retrieve."

-- @kepano, "File over app"
Source: `/Users/ljack/Library/Mobile Documents/iCloud~md~obsidian/Documents/m31uk3/Clippings/Thread by @kepano - File over app.md`

### LOE / Opportunity Cost Decision

We need to consider all of this to determine the opportunity / LOE costs of building the integration endpoint functionality vs leaving it open. **As long as the spec is open, the community can implement it directly into systems like ByteRover or anything else.**

This is distinct from our organic ingestion push.

### Andy contact status

Brief contact via X.com messages. Totally possible to reach out to him again, but want to have something valuable to offer for free first (e.g. working demo).

**Zero concern that he takes it for himself.** Multiple parallel "ponies" being worked with to release pebbles into the wild. Crude analogy: multiple "infection" vectors to maximize likelihood of pebbles going viral and gaining mass market adoption.

---

## A5: v0.1 Scope -- Two Killer Features in Parallel

**Answer:** Direction correct, minus the chrome extension limit.

We're solving for **two key killer features in parallel**:

### Killer Feature 1: Near-Zero Friction Ingestion
Covers both browser surface AND CLI:
- User invocation via agent
- Autonomous agent invocation
- Browser intercept via clipper/defuddle forks
- Standalone CLI for all non-browser artifacts

### Killer Feature 2: Schema Validation via Powerful Facets
Proving the schema and well-designed researched attributes of pebbles maximize on user empathy such that they create powerful facets with which users and agents can:
- Significantly reduce search spaces
- Effortlessly create links between pebbles

**Mental model:** Google Maps location history, but for knowledge work.

---

## Open Questions Generated By These Answers

1. What language are defuddle and obsidian-clipper written in? (drives stack choice)
2. Can we fork them simply, or do we need a different intercept strategy?
3. Are both required, or only one? (defuddle does extraction, clipper does the UI?)
4. Is reliable YAML/JSON injection into file headers possible? Which formats support it?
5. What does the LoCoMo eval methodology look like? (drives our eval framework)
6. What research exists on kinetic vs non-kinetic attribute distinctions?
7. How do AGENTS.md and SKILLS.md achieve their viral adoption? (the marketing moat)
8. What's the right finalized vocabulary for the 8 emotions, 5 uku_types, 4 intents?
