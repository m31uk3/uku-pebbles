# C4 Architecture Communication

**Source:** /btw note during synthesis convergence
**Reference:** https://c4model.com/introduction

## Why This Matters for Convergence

### 1. It enforces the compile-time LLM boundary visually
A C4 container diagram makes the Layer 1-3 deterministic core vs Layer 4 inference separation impossible to fudge. The boundary becomes a literal box on a diagram, not a paragraph in a spec.

### 2. It clarifies the "blueprint vs product" tension
The user said Pebbles is the blueprint, not the product. C4's Context level is exactly where you draw the line: the system is the Pebbles spec + reference implementations; everything else (ByteRover, future OS implementations, third-party clients) is an external actor in the context diagram. **This makes the open-spec strategy concrete.**

### 3. It scales communication for viral adoption
The user's UVP #2 is "rapid mass market adoption similar to AGENTS.md and SKILLS.md." C4 diagrams are the single best artifact for getting external implementers to understand your system in 60 seconds. AGENTS.md became popular because it was instantly graspable; **a one-page C4 Context diagram for Pebbles would do the same for the architecture.**

### 4. It surfaces integration endpoint decisions
The unresolved Q4 question -- "should UKU expose an MCP/REST/CLI endpoint or leave it open for community implementations?" -- becomes much easier to answer when you draw the L2 container diagram. You can literally see whether ByteRover sits inside the Pebbles system boundary or outside it as an external consumer. The user's strong preference (open spec, infinite endpoints) maps to "outside the boundary" -- and a C4 diagram makes that contract explicit.

### 5. It pairs naturally with the No-Escape architecture
The paper's Exit 2 (exact episodic record + external semantic verifier) is fundamentally a containers diagram: two distinct containers with a contract between them. **C4 is the right notation for expressing that separation.**

## Where to Apply It in the Synthesis

When the final converged synthesis is written, three C4 diagrams would land hard:

### Diagram 1: Context Diagram (L1)
Pebbles (the spec + reference impl) at the center; humans, agents, ByteRover, SAGE, OS integrations, clipper/defuddle forks as actors. **Makes the open-blueprint strategy visually undeniable.**

```
[Human users]                    [AI agents]
     |                                |
     v                                v
+----------------------------------------+
|                                        |
|     PEBBLES (spec + reference impl)    |
|                                        |
+----------------------------------------+
     ^         ^         ^         ^
     |         |         |         |
[ByteRover] [SAGE]  [OS native]  [3rd party
 swarm]    consensus  integrations  clients]
```

### Diagram 2: Container Diagram for v0.1 Reference Implementation (L2)
CLI, file format, JSONB+GIN index, query engine. **Shows the minimum viable demonstration as a discrete, buildable thing.**

```
+-------------------------------------------+
|         PEBBLES v0.1 reference            |
|                                           |
|  +----------+      +-------------------+  |
|  |   CLI    |----->| Schema validator  |  |
|  +----------+      +-------------------+  |
|       |                     |             |
|       v                     v             |
|  +------------------------------------+   |
|  |   Pebble file format (.md/.pebble) |   |
|  +------------------------------------+   |
|                     |                     |
|                     v                     |
|  +------------------------------------+   |
|  |   Postgres + JSONB + GIN index    |   |
|  +------------------------------------+   |
|                     |                     |
|                     v                     |
|  +------------------------------------+   |
|  |   Red-string query engine          |   |
|  +------------------------------------+   |
+-------------------------------------------+
```

### Diagram 3: Container Diagram for the Triad Runtime (L2)
Pebbles container (exact episodic) + ByteRover container (semantic swarm) + SAGE container (consensus verifier), with the contracts between them. **This is the empirical realization of the No-Escape theorem's Exit 2.**

```
+--------------------+    +--------------------+    +--------------------+
|                    |    |                    |    |                    |
|     PEBBLES        |    |    BYTEROVER       |    |       SAGE         |
|  exact episodic    |<-->|  semantic swarm    |<-->|  consensus         |
|  record            |    |  BM25+graph+vector |    |  verifier          |
|  (b=0, FA=0)       |    |  RRF fusion        |    |  BFT + PoE         |
|                    |    |                    |    |                    |
+--------------------+    +--------------------+    +--------------------+
       ^                          ^                          ^
       |                          |                          |
       +---red-string queries-----+                          |
                                  +------MCP / REST----------+
       +-----submit pebbles for consensus--------------------+
```

The L3 component diagrams can wait until we're actually writing code for the v0.1 CLI. The L4 code level can stay implicit unless we hit a part of the system complex enough to warrant it.

## One Caution

C4 is a communication tool, not a design methodology. **Don't let it become bureaucracy.** Simon Brown's own guidance: produce only the diagrams that answer questions someone is actually asking. For Pebbles right now, the Context and Container levels are doing real work; the Component and Code levels would be premature.

## Recommendation

Add a section titled "Architecture Communication via C4" to the final synthesis that commits to producing the **Context diagram and v0.1 Container diagram as part of the first deliverable**, alongside the working CLI. This gives external implementers (and Andy at ByteRover) a one-page artifact they can grok in seconds -- which is exactly what AGENTS.md-style viral adoption requires.

## Action Items

- [ ] Produce L1 Context diagram as part of Phase 1 deliverable
- [ ] Produce L2 Container diagram for v0.1 reference impl as part of Phase 1 deliverable
- [ ] Produce L2 Container diagram for triad runtime alongside ByteRover integration in Phase 5
- [ ] Use Mermaid `C4Context` and `C4Container` notation for portability (renders in GitHub, Obsidian, most Markdown viewers)
- [ ] Treat the Context diagram as the canonical "what is Pebbles" artifact for the README
