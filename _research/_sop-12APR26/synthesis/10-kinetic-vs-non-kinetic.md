# Kinetic vs Non-Kinetic Red Strings

## The Concept

A new facet axis for UKU red strings: distinguishing **kinetic** attributes (actions, observable behavior) from **non-kinetic** attributes (thoughts, internal states). This delineation is a powerful search space reducer because users can easily infer or recall during query: **"was it an action or a thought?"**

## Why This Is Powerful

### Cognitive accessibility
When a user tries to recall a past pebble, the first thing they almost always know is **whether something happened or whether they thought about it**. This is one of the most reliably remembered features of any moment.

- "Did I actually meet with her, or was I just planning to?"
- "Did I send the email, or was I drafting it?"
- "Did I read the paper, or was I considering reading it?"

The kinetic/non-kinetic distinction maps to a binary that humans intuitively partition memories by. If we encode it as a top-level facet, we cut the search space roughly in half on every query.

### Independent of all other facets
Critically, kinetic vs non-kinetic is **orthogonal** to:
- emotional_state (you can be joyful while thinking OR while acting)
- intent (you can intend to act, OR intend to think)
- category (any category can be kinetic or non-kinetic)
- uku_type (any type can be either)

This makes it a pure additional axis -- it doesn't conflict with existing facets, it multiplies their resolving power.

## Mapping to UKU Schema

### Option A: New top-level field
```yaml
modality: kinetic   # or non_kinetic
```

### Option B: Subfield of intent
```yaml
intent:
  value: act_on
  modality: kinetic
```

### Option C: Bound to uku_type
- `experience_capture` defaults kinetic
- `insight` defaults non-kinetic
- `problem_statement` defaults non-kinetic
- `proposed_solution` defaults non-kinetic
- `ontology_element` defaults non-kinetic

**Recommendation: Option A** -- new top-level field. Maximum query power, minimum coupling. Users and agents can override defaults.

## Controlled Vocabulary

Two-value enum:

| Value | Definition | Examples |
|-------|------------|----------|
| `kinetic` | Action occurred, observable behavior, externally verifiable | Sent email, met with person, took screenshot, walked into building, made payment |
| `non_kinetic` | Thought, plan, observation, internal state, not yet acted on | Idea, draft, intent, observation, hypothesis, draft email, proposed solution |

Edge case: `mixed` for moments that contain both ("I had this thought while walking" -- the walking is kinetic, the thought is non-kinetic). Recommendation: **don't add a third value**. Force atomization -- create two separate pebbles, one kinetic and one non-kinetic, linked via `co-occurred_with` typed edge.

## Mapping to Cognitive Science Research

This concept is well-grounded in cognitive psychology and embodied cognition research, which the No-Escape paper does not address:

### Episodic vs Semantic Memory (Tulving 1972)
Tulving's foundational distinction:
- **Episodic memory**: events you experienced (kinetic, in our terms)
- **Semantic memory**: facts and concepts (non-kinetic, in our terms)

These are stored differently in the brain (medial temporal lobe vs neocortex). The No-Escape paper invokes Complementary Learning Systems (CLS) which uses this same distinction. **Kinetic/non-kinetic is the ML-tractable proxy for episodic/semantic.**

### Mirror Neurons & Action Encoding
Rizzolatti's mirror neuron research shows that observing actions activates the same neural circuits as performing them. Actions have a distinctive neural signature that thoughts don't. This means kinetic events are physiologically more memorable -- the brain literally allocates different machinery to them.

**Implication for UKU:** kinetic pebbles will have higher recall rates and tighter clustering than non-kinetic pebbles. We should expect kinetic red strings to be more useful for query disambiguation.

### Embodied Cognition
The Embodied Cognition framework (Lakoff, Johnson, Varela) holds that cognition is grounded in bodily action. The kinetic/non-kinetic distinction maps directly to this -- kinetic experiences have a body-anchored "where, when, with whom" that non-kinetic experiences lack.

### Verb Aspect in Linguistics
Linguistically, languages distinguish:
- **Telic events** (have an endpoint, completed actions) -- kinetic
- **Atelic states** (ongoing, no endpoint) -- non-kinetic
- **Achievements vs accomplishments** (Vendler 1957)

Many languages encode this in verb morphology (Slavic perfective/imperfective, English progressive vs simple). **The fact that human languages evolved to mark this distinction suggests it's cognitively load-bearing.** UKU encoding it as a facet aligns with how humans naturally segment experience.

### Action Database Research
Cognitive load and action recognition research (Schank, Wilensky) developed the concept of **scripts** (sequences of actions) vs **plans** (intended sequences). Scripts are kinetic; plans are non-kinetic. AI systems built on this distinction (early NLP planning systems) handled action queries fundamentally differently from plan queries.

## Why This Matters for the No-Escape Tradeoff

Recall the No-Escape paper's key finding: BM25 achieves b=0, FA=0 but only 15.5% semantic agreement because it's matching arbitrary tokens.

UKU's hypothesis is that red strings on **structured, controlled vocabularies** sit at a new point on the Pareto frontier with much higher semantic agreement. The kinetic/non-kinetic facet **doubles down on this hypothesis**:

- It's a binary controlled vocabulary (only 2 values, maximum interference immunity)
- It's high semantic value (cognitively load-bearing, queryable by humans intuitively)
- It cuts search space by ~50% on every query
- It's independent of all other facets (compounds the resolving power)

In Pareto frontier terms: **adding kinetic/non-kinetic moves UKU red strings further toward the ideal corner** (high immunity + high usefulness) than any other single field we could add.

## Query Disambiguation Power

Example query: "Show me times I felt frustrated about the project"

| Filter | Result count (hypothetical) |
|--------|----------------------------|
| `emotional_state: anger` | 50 pebbles |
| `+ tags: project` | 25 pebbles |
| `+ modality: kinetic` (frustrated *while doing* something) | 12 pebbles |
| `+ modality: non_kinetic` (frustrated *thinking about* something) | 13 pebbles |

The kinetic split immediately tells the user which 50% of results to look at, **without needing to scan content**. This is the kind of disambiguation power that makes structured metadata matching dramatically better than BM25 on unstructured text.

## Open Research Questions

1. **Is `mixed` truly avoidable?** Some moments genuinely mix action and thought. Can we always atomize?
2. **Should `kinetic` be further subdivided?** (physical action, communication, transaction, observation)
3. **How do agents reliably infer modality at capture time?** (Tier 3 inference from URL patterns? Tier 2 user input?)
4. **What's the inter-annotator agreement on kinetic/non-kinetic for ambiguous cases?**
5. **Does the kinetic/non-kinetic split improve eval scores on LoCoMo when we test it?**

## Implementation Priority

**v0.2 spec change.** Add `modality: enum [kinetic, non_kinetic]` as an optional Tier 2 field. Test empirically against LoCoMo to validate the hypothesis before promoting to a recommended field.

If the empirical result is strong (>5% improvement in multi-hop accuracy when filtered by modality), promote it to a recommended field in v0.3.

## Connection to Wider UKU Vocabulary

This becomes the third "killer attribute" alongside the existing two:

| Attribute | Vocabulary | Resolving Power |
|-----------|------------|-----------------|
| **emotional_state** | Ekman 8 (Plutchik basis) | 8-way split |
| **intent** | remember/act_on/share/think_about | 4-way split |
| **modality** (NEW) | kinetic/non_kinetic | 2-way split |

Combined: 8 × 4 × 2 = 64 distinct facet combinations from just 3 fields. Each combination is a tiny, sharply-defined slice of the user's pebble space. **This is the structured-metadata advantage made concrete.**
