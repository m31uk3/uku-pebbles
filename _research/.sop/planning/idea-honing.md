# Idea Honing — UKU Pebbles v2.1

Requirements clarification Q&A for the Pebbles implementation.

---

## Q1: Ingestion — What does "deterministic extraction" mean concretely?

The Ingestion layer says "deterministic, zero-LLM metadata extraction and normalization from any source." But sources vary wildly in structure:

- A tweet has structured API data (author, timestamp, metrics).
- A screenshot has pixels and maybe OCR text.
- A handwritten note photographed on a phone has... almost nothing structured.

**The question:** When a new pebble arrives from a low-structure source (screenshot, photo, voice memo), what happens? Specifically:

(a) Does Ingestion *only* extract what's mechanically present (file metadata, EXIF, timestamp) and leave the rest for the human to fill in via YAML frontmatter?

(b) Or is there an expected "enrichment" step where something (agent? local ML?) adds structured fields — and if so, does that violate the "zero-LLM, deterministic" boundary of Layer 1?

(c) How do you see the capture flow for the hardest case — e.g., you photograph a whiteboard at work? What YAML fields get populated, by whom, and when?

### A1:

Combination of all three, phased:

**v1 (prototype):** Focus on (a) + (b). Ingestion extracts whatever structured/contextual data is immediately and mechanically available from the source — opt-in, device/browser specific. Examples: URL, page title, timestamp, EXIF GPS, browser tab context, clipboard content. Human fills in experiential fields (emotional_state, intent, why_posted) manually via frontmatter. No LLM in the loop.

**v2 (future):** Explore on-device inference / OCR to increase depth and relevance of extracted Markdown and YAML data from low-structure sources (photos, screenshots, whiteboards, voice memos). This stays in the Inference layer — Ingestion boundary remains deterministic.

**Design implication:** The Ingestion/Inference boundary is enforced by *when* enrichment happens, not *whether* it happens. Ingestion is synchronous and deterministic (extract what's there). Inference is async and optional (add what can be inferred). Both write to the same pebble file, but Ingestion runs first and Inference never blocks capture.

---

## Q2: YAML Frontmatter at Scale — Will it hold?

The entire system rests on YAML frontmatter as the source of truth. Let's stress-test that assumption.

As a user accumulates pebbles and the schema matures (more graph-eligible fields, location blocks, Ekman emotions, intent enums), individual frontmatter blocks could grow. Consider a well-populated pebble:

```yaml
---
title: "..."
uku_id: "..."
created_at: "..."
url: "..."
source_id: "..."
uku_type: insight
category: technical
emotional_state: anticipation
intent: act_on
tags: [pebbles, architecture, postgres]
location:
  city: "London"
  venue_type: coffee_shop
context_elements:
  why_posted: "..."
  surrounding_activity: "..."
  intended_next_action: "..."
weight: 0.8
status: draft
---
```

That's ~20 lines of YAML before body content. With fluid schema graduation adding more fields over time, this grows.

**The question:** At what point does frontmatter size become friction for the human editing experience in Obsidian? Do you see a practical ceiling — say 30 fields max — or is the expectation that most pebbles will only have 5-10 fields populated, with the full schema being the theoretical maximum?

### A2:

Frontmatter display is configurable — collapse to show only essential attributes by default, with a max of N visible lines at all times. Full frontmatter exists in the file but the editing UX keeps it tight.

YAML's key function is not human reading — it's enabling **automatic, organic linking** by matching attribute values across pebbles (red strings).

**Future vision:** Frontmatter becomes a search surface / quick-link interface. Each attribute value shows a count of matching pebbles — a fast path to find all related pebbles in one dimension. E.g., clicking `emotional_state: anticipation` shows "12 pebbles" as a link.

**Design implication:** No practical ceiling on schema size because humans don't need to see all fields. The file is the source of truth; the display is a view. This means:
- v1: Obsidian's native frontmatter collapse handles this adequately
- v2+: Custom rendering could turn frontmatter into an interactive search surface
- The full schema lives in the file regardless of what's displayed

---

## Q3: The Ingestion/Curation Boundary — Who can write to the file?

The spec says "agents never modify source Markdown files directly" — all enrichment goes to the JSONB index only. But the 4-layer architecture has Curation as "actor-agnostic" (humans and agents share it), and Ingestion writes the initial file.

This creates a tension. Consider these scenarios:

(a) **Ingestion creates the pebble** with whatever YAML it can extract deterministically. Human later opens it in Obsidian, adds `emotional_state: joy`, saves. The watcher picks up the change and re-indexes. Clean — human writes to file, system reads from file.

(b) **An agent during Curation** wants to add a typed edge between two pebbles. The edge goes into the edges table (not the file). Clean — agent writes to DB, not file.

(c) **An agent during Curation** discovers that 15 pebbles about the same topic should be consolidated into a Level-1 synthesis. Does the agent *create a new pebble file* (a new .md with its own frontmatter)? Or does it only create index-level structures?

**The question:** Is the file-sovereignty rule absolute ("only humans write .md files") or is it "only humans *modify existing* .md files, but agents can *create new* .md files for consolidations/MOCs"?

### A3:

The "agents never modify source Markdown files directly" rule is **wrong and needs revision**. The actual design:

**Write access is RBAC-governed, not actor-governed.** Any actor (human or agent) with write permission can edit pebble files — both YAML frontmatter and Markdown body. If an actor lacks write access, they request it. This is a distinct question from system design.

**Curation includes file editing.** A curation task (e.g., enriching a whiteboard photo capture) could include adding exposition to the body, extending YAML attributes, with or without LLM assistance. This is a legitimate write operation.

**Edges are additive for all L0+ pebbles** per the design — typed edges get created during curation regardless of level.

**API design principle:** Robust endpoints exist for:
- **Creating/editing YAML attributes** — exposing the full current state of all YAML hierarchies and values (to avoid fragmentation, redundancy, and drift). When a user/agent adds or changes frontmatter, they can see all existing attribute hierarchies.
- **Creating edges** — same principle, with intelligent edge suggestions based on existing graph state.
- **Creating L0+ pebbles** — with intelligent edge suggestions surfaced to the user, similar to Obsidian's existing search/link functionality.

**Revised sovereignty rule:** Files are the source of truth. RBAC governs who can write. The system provides guardrails (hierarchy visibility, suggestion surfaces) to prevent drift — not write locks.

---

## Q4: Fluid Schema Graduation — What are the concrete criteria?

The spec says fields start as "fleeting" (prose, full-text searchable only) and graduate to "permanent" (graph-eligible, red-string eligible) after meeting "frequency, convergence, and approval criteria." The Luhmann Test provides the qualitative bar.

But the mechanics matter for implementation. Consider: a user starts putting `mood: focused` in their frontmatter. After 30 pebbles, the system notices this recurring field.

**The question:** What does graduation actually look like in v1?

(a) Is it purely manual? The system surfaces "hey, `mood` appeared 30 times — want to promote it?" and the human decides.

(b) Is there an automatic threshold? E.g., field appears in N pebbles with M distinct values → auto-promoted to permanent.

(c) When a field graduates, what changes mechanically? Does the GIN index already cover it (since it's in JSONB regardless), and graduation just means "we now treat it as red-string eligible in queries"? Or is there a schema registry that explicitly lists permanent fields?

### A4:

No promotion-based schema. The schema is fluid — JSONB + GIN indexes everything regardless. Convergence and coherence are driven through **API-level guardrails** during Ingestion and Curation:

- Endpoints expose the full current state of all YAML hierarchies and values
- When adding/changing frontmatter, users/agents see existing attribute hierarchies (preventing fragmentation, redundancy, and drift)
- Same principle applies to creating L0+ pebbles — intelligent suggestions surface existing patterns

**Design implication:** The Luhmann Test is a *design-time heuristic* for which fields to include in the initial graph-eligible set, not a runtime promotion mechanism. The GIN index already covers every field. "Graph-eligible" is a spec-level declaration about which fields produce meaningful red strings, not an index-level distinction.

---

## Q5: The 4 Layer Boundaries — Sanity Check

Let's stress-test each boundary with concrete scenarios to ensure they hold under real usage:

### Boundary 1→2 (Ingestion → Curation)
- Ingestion writes the initial pebble file + JSONB row. It never creates edges or consolidations.
- Curation reads from the index and creates edges, consolidations, and L1+ pebbles.
- **Boundary contract:** Ingestion is write-once-per-capture (deterministic). Curation is iterative (actor-driven).

### Boundary 2→3 (Curation → Query)
- Curation writes to files, JSONB, and the edges table.
- Query only reads from JSONB (via GIN) and edges (via recursive CTEs).
- **Boundary contract:** Query never writes. Query never parses YAML. Query never calls LLMs.

### Boundary 3→4 (Query → Inference)
- Query returns structured JSON results (pebble metadata + edge traversals).
- Inference receives these results and applies LLM reasoning.
- **Boundary contract:** Inference never touches the database directly. It can suggest new edges/pebbles back through the Curation API.

### Cross-boundary scenario: Agent enriches a whiteboard photo
1. **Ingestion** creates pebble with EXIF data, timestamp, file path. Writes JSONB.
2. **Curation** (agent with write RBAC): adds OCR text to body, adds `category: technical`, creates `derived_from` edge to the meeting note pebble. Writes to file + edges table.
3. **Query** returns this pebble when someone searches `category: technical` red strings.
4. **Inference** (optional): synthesizes the whiteboard content with related pebbles into a summary.

All boundaries hold. Each layer does exactly one thing.

---

## Key Takeaways from Grok RQ1 + RQ2 Design Sessions

Distilled from the comprehensive design convergence sessions:

1. **JSONB + GIN is non-negotiable for red strings.** B-trees are uni-dimensional; GIN is N-dimensional (inverted index across all key-path + value pairs). FTS5 + multi-pass intersection is a hack that breaks at scale and violates Query layer purity.

2. **The `@>` containment operator is the NoSQL equivalent of compound SQL WHERE clauses.** One operator, one GIN scan, arbitrary facets — this is the minimal viable query component.

3. **Typed edges (lightweight edges table + recursive CTEs) are additive, not foundational.** The system works 100% without them. They enable consolidation hierarchy (derived_from, contains) and multi-hop reasoning that pure red strings cannot express.

4. **File sovereignty = files are truth + RBAC governs access.** Not "humans-only write locks." Any actor with permission can edit files and create pebbles.

5. **No promotion-based schema.** GIN indexes everything. Convergence comes from API-level guardrails (hierarchy visibility, suggestion surfaces), not field promotion mechanisms.

6. **Layers 1–3 are compile-time LLM-free.** This is the single most important architectural contract. Inference is a separate process that receives structured results only.

7. **Personal scale (<100k pebbles, <100k edges) keeps everything sub-millisecond.** Recursive CTEs for 3–5 hop traversals are well within Postgres's capabilities at this scale.

---

## Q6: Pebble-as-Descriptor — The AGENTS.md Analogy

Parallel research surfaced a key architectural insight: pebbles are not self-contained artifacts. They are **metadata wrappers / descriptors** that point to external payloads.

The analogy: just as AGENTS.md is a lightweight, human-readable index that makes a codebase navigable by agents without parsing every file, a pebble makes a life artifact findable via deterministic search without storing the artifact itself.

**The distinction:**
- **The pebble file** = description (YAML frontmatter + optional body text pointing to or summarizing the artifact)
- **The artifact** = the actual screenshot, PDF, audio, video, document, or conversation that lives elsewhere (filesystem, cloud drive, app)

The body text is a human/agent-written summary, not the content itself. The pebble "wraps" the artifact via filename, link, or content hash — just as AGENTS.md explains the codebase within which it resides, a pebble adds the lived experiential context for the artifact it links to.

**The question:** Does this pebble-as-descriptor model change anything about the required YAML fields? Specifically — should there be a formalized `artifact_ref` block (file path, URL, content hash) as a required or strongly-recommended field, or is `url` + `source_id` sufficient?

### A6:

Defer `artifact_ref` design to the detailed design phase. Both approaches have advantages. The intent is clear regardless of field structure:

**A pebble must be atomic to a single idea and a single artifact.**

Multiple pebbles can point to the same source artifact. Example: a meeting could produce 5 pebbles — each pointing to the same recording/transcript but capturing a distinct idea, concern, or follow-up. The meeting notes file itself is not a pebble. Each *significant thought* from that meeting is.

**The differentiator:** A pebble exists because a human deemed something worthy of remembering. This is a deliberate act of capture — not passive note-taking. It requires a behavioral shift: from "save the file" to "what from this moment matters enough to encode?"

**Design implication:** Atomicity is enforced by intent, not by file structure. One pebble = one idea + one artifact reference + the lived context of that moment. The many-to-one relationship (multiple pebbles → same source artifact) is a first-class pattern, not an edge case.

---

## RESEARCH NEEDED: Write Conflicts & Git-Based Concurrency

**Context:** The original "watcher" concept (filesystem daemon syncing files → JSONB) was removed as a separate component. Ingestion handles JSONB creation and GIN updates directly. The same applies to edits — any file modification triggers re-ingestion into JSONB.

**Open problem:** Since pebble files are the source of truth and multiple actors (humans + agents) may have RBAC write access, we need the simplest possible write-lock mechanism for concurrent file access.

**Candidate approach:** Build on top of a **git repository**. In this model:
- Write conflicts become **merge conflicts** (a well-understood, tooled problem)
- Git provides a natural audit trail (who changed what, when)
- Obsidian already has git plugin support
- Agents would commit changes via standard git workflow

**Status:** Needs further research. Key questions:
- Is git-based concurrency sufficient for personal-scale multi-actor writes?
- What is the merge conflict resolution strategy (last-write-wins? human-arbitrated?)
- Does git add unacceptable latency to the Ingestion → JSONB pipeline?
- How does this interact with Obsidian's file-save behavior?

**For v1 prototype:** Acceptable to use simple file-level locking or single-writer assumption. Git-based concurrency is a v2 research topic.

---

## Q7: Edge Type Vocabulary — How constrained?

The edges table has a controlled `edge_type` column. The Grok sessions mentioned several types: `supports`, `contradicts`, `derived_from`, `contains`, `supersedes`. But the vocabulary isn't finalized.

Two tensions:

1. **Too few types** and edges lose expressiveness — everything becomes a generic "related" link (the same context rot Pebbles exists to solve).
2. **Too many types** and agents/humans face decision fatigue at curation time, plus the vocabulary fragments across users.

**The question:** For v1, what is the minimum edge type set that enables the consolidation hierarchy (L0→L1→L2) and basic reasoning chains, without over-engineering?

### A7:

Defer to detailed design. The edge type vocabulary requires deep consideration of YAML + JSONB + GIN trade-offs vs. something more sophisticated for typed relationships.

**However — this is distinct from the core value proposition.** Pebbles is the **AGENTS.md of knowledge work**: a lightweight, human-readable descriptor layer that makes any content/artifact type findable, contextual, and connectable. That value exists with red strings alone. Typed edges are a progressive enhancement for reasoning — important but not foundational to the pitch or the v1 experience.

---

## Q8: The Chrome Extension — What does "capture" mean concretely?

The pitch ends with *"Download our beta client for Google Chrome and start pebble-piling today."* The Chrome extension is the v1 beachhead capture surface.

When a user clicks the extension on a webpage, what actually happens?

(a) Does it create a `.md` file locally (written to an Obsidian vault directory)? Or does it POST to a local API that handles file creation + JSONB ingestion?

(b) What fields get auto-populated from the browser context? (URL, page title, timestamp are obvious — what about tab group name, selected text, open tab count, time-on-page?)

(c) What does the user see? A popup with pre-filled YAML fields they can edit before saving? A minimal "one-click capture" that saves immediately and lets them enrich later? Both as modes?

### A8:

**(a) Daemon model.** The extension hands off to a running Pebbles process (daemon) that handles file creation + JSONB ingestion + GIN update as a single atomic operation. The extension is a thin capture surface; the daemon is the engine. This is a v1 architectural requirement — not just a file write.

**(b) Everything available, intelligently filtered.** The extension captures all available browser/device context, but what gets included is governed by **pebble templates** — configurable per device, application, and user privacy preferences. Templates ensure maximum value without overstepping privacy boundaries. Design inspiration: Defuddle's approach to stripping noise from webpages to capture only target content. The template system should be a highlighted design component — it's where intelligent system-level intuition lives.

**(c) Three capture modes (user preference):**

1. **Silent** — System captures whatever it can via template. No UI. Pebble created immediately.
2. **Minimal** — 3 input fields + emoticon picker (Ekman 8) + location dropdown (GPS-populated). Seconds, not minutes.
3. **Full** — All available values surfaced for review/edit.

Interface is a **collapsible drill-down** — user starts at their preferred level and can go deeper when desired. Each level expands into the next.

**Core UX tenet:** Find the perfect balance between value-add from precise context attributes vs. effort to add them. The capture experience must be **seconds, not minutes**. Friction kills adoption.

---

## Q9: The Daemon — What is the minimum viable backend?

A8 established that a running Pebbles daemon handles the pipeline: receive capture request → create `.md` file → parse YAML → write JSONB → update GIN. The Chrome extension is just a thin client.

But this daemon also needs to serve the Query layer (red-string searches, edge traversals) and the Curation layer (create edges, suggest attribute hierarchies, surface intelligent suggestions).

**The question:** For v1, is the daemon a single process exposing a local REST API (thin HTTP server over Postgres), or something else? And what is the minimum set of endpoints that makes the Chrome extension + Obsidian workflow functional?

### A9:

Generally correct — refine during design. Single local daemon process exposing a REST API over Postgres.

**Key v1 requirements for the daemon:**
- Optimal extraction for all browser-based content
- Complete feature parity with Obsidian Web Clipper / Defuddle for content extraction quality
- Endpoint design deferred to detailed design phase

**Design implication:** The daemon is not just a CRUD wrapper around Postgres. It must include intelligent content extraction (Defuddle-quality noise removal, template-driven field population) as part of the Ingestion layer. The extraction pipeline is a first-class component, not an afterthought.

---

## Q10: What does "success" look like for v1?

We've clarified the architecture, the capture UX, the relationship model, and the layer boundaries. Before we move to design, let's lock the v1 success criteria.

**The question:** If v1 ships and works perfectly, what can a user actually do end-to-end? Concretely — what is the demo scenario that proves Pebbles works?

For example: "I install the Chrome extension, capture 20 pebbles over a week from X threads, articles, and meeting notes. I open Obsidian and can see red-string connections I never manually created. I search for `emotional_state: anticipation` and find the 4 moments where I was excited about something — across completely different topics."

Is that the v1 story? Or is it something more/less ambitious?

### A10:

Yes — that example is exactly the v1 story. Two discovery surfaces:

1. **Obsidian-native integration** — red-string connections surface directly in the user's existing vault workflow. Pebbles captured via Chrome extension appear as `.md` files in the vault with full frontmatter. Search/discovery happens through Obsidian's existing tools + the new red-string dimension.

2. **Pebbles dashboard / graph view** — a dedicated UI (web-based, served by the daemon) that visualizes the pebble pile as a conspiracy board. Red strings rendered as connections between nodes. Filterable by any graph-eligible attribute. Shows clusters, patterns, and dimensions that don't exist in any current tool.

**v1 success criteria:**
- Chrome extension → capture 20+ pebbles from diverse sources (X, articles, meetings, notes)
- Red strings automatically surface connections the user never manually created
- Search by any graph-eligible field (emotional_state, intent, category, tags, location) returns cross-topic matches
- Both surfaces (Obsidian vault + Pebbles dashboard) show the same truth
- Zero LLM calls required for any of the above

**The v1 value proposition in one sentence:** "A search/discovery surface that didn't exist before — connections across your life's artifacts based on how you experienced them, not just what they contain."

---
