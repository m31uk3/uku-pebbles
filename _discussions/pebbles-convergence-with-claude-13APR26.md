

drop all instances of uku_ simplify to pebble_

uku is a explainer pebble is universal and our core brand

  Q3. Should ontology_element be at the same level as other uku_types
  
  ontology is core to everything and should be another type relative to our 3 way alignment 
  
  The three-way alignment

  ┌─────────┬───────────────────────────────────────┬─────────────────────────────────────────┬────────────────────────────────────────────────────────┐
  │  UKU    │         Doc 02 (compression)          │              Doc 13 (CLS)               │              Zettelkasten (practitioner)               │
  │  Level  │                                       │                                         │                                                        │
  ├─────────┼───────────────────────────────────────┼─────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ L0      │ Individual memories, zero compression │ Episodic — raw, hippocampal-fast, full  │ Fleeting notes — temporary, "no context," captured     │
  │         │                                       │ detail                                  │ without understanding                                  │
  ├─────────┼───────────────────────────────────────┼─────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ L1      │ Large clusters, preserve detail       │ Consolidation gradient, partial         │ Permanent (atomic) notes — one big idea, own words,    │
  │         │                                       │ abstraction                             │ linked, self-contained                                 │
  ├─────────┼───────────────────────────────────────┼─────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ L2      │ Medium clusters, moderate             │ Consolidation gradient, themed grouping │ MOCs (Maps of Content) — organizational layer grouping │
  │         │ compression, thematic                 │                                         │  permanent notes                                       │
  ├─────────┼───────────────────────────────────────┼─────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ L3+     │ Small clusters, high-level patterns,  │ Semantic — abstracted concepts,         │ Structural/index notes (implicit in article; Luhmann   │
  │         │ max compression                       │ generalized knowledge                   │ called them Hauptzettel)                               │
  └─────────┴───────────────────────────────────────┴─────────────────────────────────────────┴────────────────────────────────────────────────────────┘
  
  ontologies are the source truth or anchor of a system. this is either provided at time of creation via some human/agent linking or post creation curation. there should be strong precedent for this with Palantir and their Maven systems being heavily integrated to ontologies 
  
  the intention with this is there should be a direct 1:Many link from a pebble to any relevant ontologies which govern it. think of it as the pebble making a claim and the ground truth validation is a graph object ontology that an agent can traverse to verify facts
  
  e.g. in a meeting; statement made by X; Y highlights moment + statement against A,B,C ontologies for async validation and further analysis 

  Q14. consolidation_level: user-set or computed from edges
  
  unclear what is happening here. edges match organically based on pebbles having matching attribute values. this feels like an index concern why is it even part of the pebbles yaml?
  
  
Q7. Conformance levels Reader / Writer / Full

unclear what you mean here. it feels like this is over complicating the personas 

Four clearly bounded layers:

```
  Ingestion ─── Deterministic extraction. Zero LLM.
      │         Parse YAML, normalize, write to index.
      ▼
  Curation ──── Actor-agnostic (human or agent, RBAC-governed).
      │         Create edges, consolidate, build higher-order structures.
      ▼
  Query ──────── Pure deterministic retrieval. Red strings + optional edge traversal.
      │          No LLM. No embeddings. Just SQL.
      ▼
  Inference ──── Optional. Separate process. Receives structured results only.
                 LLM reasoning, synthesis, suggestions.
```


  Q6. Schema versioning (semver, compat matrix, migration determinism)

similar to Q7 it feels like there's some guidance somewhere that curation is not allowed to update yaml attributes and trigger reindexing to improve quality and cleanliness of relationships/tag values

  Spec impact: Add §12 "Versioning & Migration" with the semver rules, compat matrix template, and unknown-field preservation rule.
  
  please revaluate and explain
  
  
Q11. Forgetting granularity — per-pebble vs per-vault

overall direction looks good; however guidance from SAGE creator 

The explicit weight is a deal breaker
It won't scale

One way I think it could work with sage
Pebbles as the capture/export format (human creates/edits MD files -> watcher ingests to index or SAGE). SAGE as the agent runtime that governs, persists, and orchestrates across sessions/agents. 

The KV links become one reliable edge type in SAGE’s broader memory graph.
1:09 AM
1:09 AM
Basically SAGE can act as the governed runtime layer on top of Pebbles:
1.) Ingest UKUs while preserving all inherent red strings as strong graph edges
2.) Add validation, signing, confidence, decay/reinforcement, and semantic layering
3.) Give agents reliable longitudinal memory via MCP without ever touching your source files
4.) CEREBRUM can visualize the conspiracy board with usage-weighted connections
1:12 AM
  
      minimum_effective_weight: 0.1            # never auto-archive above this
      
condider SAGE input as directional and should not expand scope but should influence schema based on verifiable claims such as weight being a failure mode; we must validate with citations

  Q12. Reversibility storage — shadow vault vs flagged tombstones
  
  no shadow vault. where did that idea even come from?
  
Q13. Reconsolidation model — new pebble version vs in-place modification

ahh here's the culprit 

  Recommendation: New pebble version on all reconsolidation. L0 is immutable. SAGE only operates on L1+. Add status: superseded as a new lifecycle state.
  
  irrelevant to SAGE or anything else front matter must be editable in Curation ──── Actor-agnostic (human or agent, RBAC-governed).
  
  that is the effective librarian that makes curation possible. agree the content of the pebble / user inputs should be immutable however edges and their ability to be converged / curated by agents needs to be possible 
  
SAGE needs to be completely removed as a core depencency just as ByteRover they are enhancements not core dependencies 

SAGE is an asset / tool call during curation and potentially during inference 

validate the pros / cons of having fleeting notes L0's being immutable; there needs to be some feedback loop which informs the attribute tags / wiki links / edges such that during creation it is constantly using the most current index (e.g. from L1+ Permanent/Literature/MOCs etc.)

  - Trigger: curator promotes a fleeting note to a permanent note
    
    make this clear that promotes consist of creating a new permanent note that links back to the raw fleeting note. the objective being considstent sense making of fleeting notes ; substantiated by ontologies and other permanent / literature notes / citations 
    
    this is a key opportunity to lean into any obsidian in line citations and markdown elements as permanent notes will always be markdown whereas fleeting notes (raw) are by definition wrappers/pointers  for any content type 

  L0 is immutable. SAGE consensus cannot vote on lived experience. The user was there, SAGE was not. This is the cleanest UKU/SAGE boundary: SAGE operates on
   abstractions, never on raw episodes.
   
   sounds like you're clarifying that SAGE is a tool call asset for curation so less of a boundary and more of a user manual for the pebbles blueprint



## Round 2


  pebble_id: pebble-20260413-a1b2c3 - this should be a alphanumeric uid shouldn't waste space with pebble- prefix
  
  same for this
  
    governed_by:
    - pebble-ontology-finance-ledger     # ground-truth revenue data
    - pebble-ontology-meeting-roster     # who X is, their role
    - pebble-ontology-fiscal-calendar    # what "Q3" means
      
should point to text plus uid so has redundancey in the event of renames uid is constant 


ensure this gets renamed   └── _specs/uku-pebbles.spec.md to pebbles.spec.md

i like this concept of pre specifiying expiry 

  archive_at: 2027-01-01 # scheduled archival (user-set)
  
  this gives the user/agent more power at creation
  
  