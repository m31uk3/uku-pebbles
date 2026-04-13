# Glossary: Acronyms and Terms

## Retrieval & Search

**BM25** -- Best Matching 25. A bag-of-words ranking function used by search engines to rank documents by relevance to a query. BM25 is term-frequency-based (counts how many times a query term appears in a document) with length normalization. **Does not understand meaning** -- if you search for "doctor" it will not match "physician." This is its strength (interference-immune) and its weakness (low semantic agreement, only 15.5% in the No-Escape paper). BM25 is the gold standard for keyword retrieval and a core component of every hybrid retrieval system.

**Red Strings** -- (UKU coinage) Implicit, symmetric connections between pebbles formed by matching YAML key-value pairs across the corpus. Computed on-demand from the JSONB+GIN index. Nothing is written back to files. Mental model: a conspiracy board where every pebble is a note pinned to the wall and red strings appear wherever attributes match. Equivalent to BM25 in interference-immunity but on **structured controlled-vocabulary fields**, which we hypothesize gives much higher semantic agreement.

**Typed Edges** -- (UKU) Optional, explicit, directional relationships stored in a separate edges table. Created during Curation by humans or agents with RBAC write access. Examples: `derived_from`, `contains`, `supports`, `contradicts`, `supersedes`. Progressive enhancement that never breaks red strings.

**RAG** -- Retrieval-Augmented Generation. The dominant pattern for adding external knowledge to LLMs: retrieve relevant documents using vector similarity, then prepend them to the LLM's prompt. The No-Escape Theorem proves RAG **will always fail** at scale because dense embeddings are subject to interference-driven forgetting and false recall.

**RRF** -- Reciprocal Rank Fusion. A simple, parameter-free method for combining ranked lists from multiple retrievers. Each item gets a score `1/(k + rank)` summed across all retrievers (where k is a small constant, typically 60). RRF is the standard way to fuse heterogeneous retrieval methods (BM25 + vector + graph) into a single ranked result. **Used by ByteRover Memory Swarm** to fuse BM25 + wikilink graph expansion + hybrid vector+keyword retrieval.

**Memory Swarm** -- (ByteRover term) Federated search architecture that fuses multiple retrieval methods (BM25, graph traversal, vector + keyword hybrid) using RRF. The principle: "Each retrieval method has uncorrelated blind spots. The ensemble doesn't eliminate failure, it decorrelates it." This is the practical implementation of "navigating the No-Escape tradeoff frontier."

**HNSW** -- Hierarchical Navigable Small World. A graph-based approximate nearest neighbor (ANN) algorithm widely used in vector search engines (FAISS, pgvector, Milvus, Qdrant). Provides sub-linear search time over millions of vectors. Used inside SAGE for vector similarity search.

**ANN** -- Approximate Nearest Neighbor. Algorithms that find "close enough" matches in high-dimensional space without exhaustive scanning. HNSW, IVF, LSH are the major variants.

**FTS / FTS5** -- Full Text Search / SQLite Full Text Search version 5. SQLite's built-in inverted index implementation. Supports BM25 ranking out of the box. Used as a fallback in ai-pebbles' design when Tantivy exceeds memory budget.

**Tantivy** -- A Rust-based full-text search engine library, similar to Lucene. High performance, embeddable. Specified as the primary search engine in ai-pebbles' design (replaced in UKU by Postgres+JSONB+GIN).

**JSONB** -- Postgres' binary-encoded JSON storage type. Supports indexed lookups (with GIN), partial updates, and rich query operators. The recommended storage layer for UKU's red-string queries.

**GIN** -- Generalized Inverted Index. A Postgres index type optimized for indexing values inside composite types (arrays, JSONB, full-text vectors). Provides sub-millisecond compound faceted search on any JSONB field. The technical foundation for red-string queries.

## Memory & Cognition

**LoCoMo** -- **Long-term Conversational Memory**. A benchmark for evaluating LLM-based conversational agents on multi-session dialogues spanning months of simulated time. Created by Maharana et al., published at ACL 2024. Contains 10 conversations with 1,986 QA pairs across 5 categories (multi-hop reasoning, temporal reasoning, open domain, single-hop, adversarial). Scores: Claude-3-Sonnet ~96.1%, GPT-3.5-turbo ~92.8%. ByteRover claims 96.1%. Licensed CC BY-NC 4.0 (academic only).

**LongMemEval-S** -- A long-term memory evaluation benchmark distinct from LoCoMo. Smaller scale. Often confused with LoCoMo. ByteRover's pure BM25 layer scores 92.8% on LongMemEval-S (different from the 96.1% LoCoMo score).

**DRM** -- **Deese-Roediger-McDermott paradigm**. A psychological experiment that tests false recall: present a list of words all related to a missing "lure" word (e.g., bed, rest, awake, tired, dream, wake, snooze... lure: SLEEP). Subjects often falsely recall the lure as having been on the list. The No-Escape paper uses DRM to test whether memory systems exhibit false recall, finding that semantic systems do (FA = 0.583 for vector DB) and BM25 does not (FA = 0.000).

**TOT** -- **Tip-of-Tongue states**. The phenomenon where you know you know something but can't quite retrieve it. The No-Escape paper measures TOT rates across architectures: humans ~3.7%, attention memory 21%, parametric memory 69%.

**Ebbinghaus forgetting curve** -- Hermann Ebbinghaus's 1885 finding that memory retention decays exponentially over time. The No-Escape paper shows this curve emerges geometrically from any semantic memory system, with a forgetting exponent `b` in the range 0.3-0.7 for humans and 0.44-0.48 for vector DB and graph memory.

**SPP** -- **Semantic Proximity Property**. Axiom 1 of the No-Escape paper: a memory system has SPP if related concepts have closer representations than unrelated ones. This is what makes semantic retrieval *work* -- and exactly what creates the interference vulnerability the theorem proves.

**Spacing Effect** -- The psychological finding that spaced repetition of material produces better retention than massed repetition. The No-Escape paper shows this effect emerges geometrically: long-spacing produces accuracy 0.90+, massed produces 0.36.

**Complementary Learning Systems (CLS)** -- McClelland, McNaughton & O'Reilly 1995 hypothesis: the brain has a fast hippocampal encoding system + a slow neocortical consolidation system. The two work together to manage the interference-vs-generalisation tradeoff. The No-Escape paper invokes CLS as the model for the recommended architecture: episodic record + semantic reasoning, working together.

**d_eff** -- Effective dimensionality. The number of dimensions actually carrying useful semantic information, regardless of nominal dimensionality. Measured by participation ratio (PR) or Levina-Bickel (LB) estimators. For natural language across all five tested architectures: d_eff ~ 10-158, regardless of nominal dimensionality (which spans 384 to 3,584). This is the key finding driving the No-Escape Theorem.

**No-Escape Theorem** -- Theorem 7 of Gopinath et al., "The Price of Meaning" (arxiv 2603.27116v1, March 2026). Formal proof that any memory system retrieving by semantic similarity will inevitably exhibit forgetting and false recall as memory grows. The only escapes are: (1) abandon semantic retrieval, (2) add an external symbolic verifier or exact episodic record, or (3) make effective dimensionality infinite (impossible for natural language).

## Pebbles-Specific

**UKU** -- **Universal Knowledge Unit**. The atomic data structure of the Pebbles spec. A single pebble is one UKU. Each UKU = one idea + one artifact reference + one experiential context.

**Pebble** -- The colloquial name for a UKU. Also the spec name. A descriptor (Markdown + YAML frontmatter) that wraps an artifact with experiential context. Per the v2.3 spec reframe: a pebble is **not** the artifact itself, it's a structured description of the artifact.

**Pebble Pile** -- A collection of related pebbles, typically grouped via red strings or typed edges. Mental model: a pile of evidence on a desk, with red strings connecting items.

**Tier 1/2/3 Ingestion** -- (UKU) The four-tier ingestion contract:
- **Tier 1**: Auto-captured from device/browser, zero friction (timestamp, GPS, URL, content_hash)
- **Tier 2**: Human moment, 3-5 sec friction (intent, emotional_state, tags)
- **Tier 3**: Deterministic inference, zero friction (venue_type from GPS, source_type from extension)
- **Tier 4**: LLM-assisted inference, async zero friction (attribute assignment using payload + index)

**Layer 1/2/3/4** -- (UKU) The four bounded architectural layers:
- **Layer 1: Ingestion** -- deterministic, zero LLM
- **Layer 2: Curation** -- actor-agnostic (human or agent, RBAC-governed)
- **Layer 3: Query** -- pure deterministic retrieval, red strings + edges
- **Layer 4: Inference** -- optional, separate process, LLM reasoning

**Compile-time LLM boundary** -- (UKU) The architectural contract that Layers 1-3 are LLM-free at compile time. Layer 4 (Inference) is a separate, optional process. The system is fully functional without Layer 4. This is the single most important architectural decision in the UKU spec, and the No-Escape Theorem provides formal mathematical validation for it.

**Luhmann Test** -- (UKU) A field is graph-eligible (suitable for red-string matching) if its value is understandable without context. A stranger should know what it means. `emotional_state: joy` passes. `why_captured: "Kevin just replied"` fails. Named after Niklas Luhmann's Zettelkasten principle of atomic, context-independent notes.

**Tidy Data Invariant** -- (UKU, from Wickham 2014) Every YAML field follows tidy data principles: each variable is its own field, each observation is its own record, each value is a single atomic cell. No composite prose strings.

**Pebble-as-Descriptor** -- (UKU v2.3) The architectural reframe: a pebble is not the artifact itself, but a descriptor that wraps an artifact with experiential context. Just as AGENTS.md describes a codebase to an agent, a pebble describes an artifact to humans and agents.

## Triad & Ecosystem

**SAGE** -- **Sovereign Agent Governed Experience**. Production memory infrastructure for AI agents, built by @l33tdawg. Uses CometBFT BFT consensus, PoE weighted voting, RBAC with 4 gates and 5 clearance levels, AES-256-GCM vault encryption. Provides the "external symbolic verifier" component of the No-Escape theorem's recommended Exit 2 architecture.

**ByteRover** -- Memory infrastructure for AI agents, built by Andy Nguyen (@kevinnguyendn). Uses Memory Swarm federated retrieval (BM25 + wikilink graph + hybrid vector+keyword, fused with RRF) over markdown files in a hierarchical Context Tree. Achieves 96.1% on LoCoMo. Provides the semantic reasoning layer component of the triad.

**OpenClaw** -- ByteRover's open-source contribution framework. PR #50848 introduced ContextEngine.assemble() for selective, prompt-aware context retrieval.

**.brv/context-tree** -- ByteRover's hierarchical knowledge storage format. Markdown files in a tree structure, queried by the ContextEngine.

**MCP** -- **Model Context Protocol**. Anthropic's open standard for connecting LLMs to external tools and data sources. Allows tools like ByteRover, SAGE, and (eventually) UKU to expose typed function calls that any LLM client can invoke.

**Triad** -- (UKU coinage) The three-project ecosystem: UKU-Pebbles (schema + capture) + SAGE (consensus validation) + ByteRover (selective retrieval). Together they implement the No-Escape Theorem's Exit 2 architecture: exact episodic record + external symbolic verifier + semantic reasoning layer.

## Standards & Formats

**YAML** -- YAML Ain't Markup Language. Human-readable data serialization standard. UKU uses YAML as the v1 binding for pebble frontmatter. Strict subset of JSON since YAML 1.2 (2009).

**XMP** -- **Extensible Metadata Platform**. ISO 16684-1:2012 (now with JSON-LD serialization since ISO 16684-3:2021). Adobe's standard for embedding metadata in files via custom XML namespaces. Supported in PDF, JPEG, PNG, HEIC, MP4, WAV, DOCX, HTML, SVG, and others. Considered as a backup approach for Pebbles header injection but rejected as primary because of inconsistent preservation across tools and platforms.

**JUMBF** -- **JPEG Universal Metadata Box Format**. ISO/IEC 19566-5:2023. Generic "box of metadata" container that can hold XML, JSON, CBOR, embedded files, or UUIDs. Used by C2PA.

**C2PA** -- **Coalition for Content Provenance and Authenticity**. Cryptographically-signed metadata embedded in 20+ file formats via JUMBF. Backed by Adobe, Microsoft, Intel, BBC, NYT, Leica, Sony, Nikon. Operationally proven existence proof for header injection at scale.

**EPUB** -- The W3C/IDPF e-book format. A ZIP file containing OPF metadata + content. The architectural pattern UKU adopts for `.pebble` bundles.

**OOXML** -- **Office Open XML** (ECMA-376 / ISO 29500). The DOCX/XLSX/PPTX format. Internally a ZIP archive with custom XML parts. Same architectural pattern as EPUB and the proposed `.pebble`.

**BagIt** -- **RFC 8493**, IETF, Library of Congress packaging format. Directory-based: bagit.txt declaration, bag-info.txt metadata, manifest-sha512.txt checksums, data/ payload. The cleanest existing spec for "metadata + arbitrary files."

**OCFL** -- **Oxford Common File Layout** v1.1. Adds versioning to the BagIt model. JSON inventory is content-addressable by SHA-512. Used by Fedora, Stanford, Oxford for digital preservation.

**Frictionless Data Package** -- Open standard for data publishing. `datapackage.json` + a `resources` array. Same shape as a Pebble manifest.

## File Format Tactics

**Sidecar file** -- A separate file placed alongside an artifact to hold metadata (e.g., `image.jpg` + `image.jpg.json`). Google Photos Takeout uses this. Risk: separation when files are moved independently.

**Container format** -- A file format that wraps other content (e.g., ZIP, TAR, MKV). Pebbles' `.pebble` is a container format using ZIP.

**Magic bytes** -- The first few bytes of a file that identify its format (e.g., `PK\x03\x04` for ZIP, `%PDF` for PDF). Pebbles `.pebble` files inherit the ZIP magic bytes (PK header).

**Manifest** -- A structured file inside a container that describes the container's contents. `pebble.yaml` is the manifest of a `.pebble` bundle. `META-INF/container.xml` is the manifest of an EPUB.
