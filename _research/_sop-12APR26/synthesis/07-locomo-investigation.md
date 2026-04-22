# LoCoMo Investigation

**Repo:** `/Users/ljack/github/locomo`
**Full name:** Long-term Conversational Memory
**License:** **CC BY-NC 4.0** (academic only, NOT for commercial use)
**Reference:** Maharana et al., ACL 2024
**Stack:** Python 3.9+ with PyTorch

## Purpose

LoCoMo is a benchmark for evaluating how well LLM-based conversational agents maintain and reason over **very long-term memory** across multi-session dialogues. Existing long-context evals fail because they truncate to <16K tokens or only test shallow consistency. LoCoMo tests:

1. **Question Answering (QA)** over long conversations -- the primary eval (the 92.8-96.1% scores)
2. **Event Summarization** -- significant temporal/causal events per speaker
3. **Multimodal Dialog Generation** -- responses grounded in visual context + history

## Dataset Structure

**File:** `data/locomo10.json` -- 10 conversations, ~1,986 QA pairs total

**Per-conversation:**
- 19-32 sessions
- ~600 turns average
- ~20,000 tokens per full conversation
- Spans 5-7 months of simulated time
- Multimodal (image captions, but images themselves not released)

**Format:**
```json
{
  "sample_id": "conv-26",
  "conversation": {
    "speaker_a": "Caroline",
    "speaker_b": "Melanie",
    "session_1_date_time": "1:56 pm on 8 May, 2023",
    "session_1": [
      {
        "dia_id": "D1:1",
        "speaker": "Caroline",
        "text": "...",
        "blip_caption": "..."
      }
    ]
  },
  "qa": [
    {
      "question": "When did Caroline go to the LGBTQ support group?",
      "answer": "7 May 2023",
      "evidence": ["D1:3"],
      "category": 2
    }
  ],
  "observation": { /* facts tied to evidence IDs */ },
  "session_summary": {},
  "event_summary": {}
}
```

## Question Categories (5 types, 1986 total)

| Category | Type | Count | Evaluation |
|----------|------|-------|-----------|
| 1 | Multi-Hop Reasoning | 282 | F1 (Porter stemming, token overlap) |
| 2 | Temporal Reasoning | 321 | F1 |
| 3 | Open Domain / Inference | 96 | F1 (semantic similarity tolerated) |
| 4 | Single-Hop Reasoning | 841 | F1 |
| 5 | Adversarial / Unanswerable | 446 | Binary (must say "not mentioned") |

**Scoring:** Macro-averaged F1 across all 1,986 QA pairs.

## Benchmark Results

| Model | Score |
|-------|-------|
| Claude-3-Sonnet | ~96.1% |
| GPT-3.5-turbo | ~92.8% |
| Gemini-Pro-1.0 | ~89% |
| Llama-3 / Mistral | 70-78% |

ByteRover claims 96.1% (Claude tier).

## Evaluation Workflow

```bash
source scripts/env.sh

python3 task_eval/evaluate_qa.py \
  --data-file ./data/locomo10.json \
  --out-file ./outputs/locomo10_qa.json \
  --model claude-sonnet \
  --batch-size 10
```

**RAG variant:**
```bash
python3 task_eval/evaluate_qa.py \
  --data-file ./data/locomo10.json \
  --model gpt-3.5-turbo \
  --use-rag --retriever dragon --top-k 5 \
  --rag-mode dialog
```

## Why LoCoMo is the Right Eval for UKU-Pebbles

1. **Tests long-term memory directly** -- our core focus
2. **Has structured ground truth** -- evidence IDs (D1:3 format) we can leverage
3. **Multi-hop reasoning category** -- exactly what red strings should enable
4. **Temporal reasoning category** -- maps to UKU's `created_at` and temporal fields
5. **Adversarial category** -- tests "must say I don't know" which structured matching handles cleanly
6. **Open dataset + code** -- can run today
7. **Peer-reviewed** -- ACL 2024 credibility

## Adaptation Strategy for UKU-Pebbles

### Phase 1: Annotate LoCoMo with red-string templates

Extend each QA pair with structured query metadata:

```json
{
  "question": "What instruments does Melanie play?",
  "answer": "Violin and piano",
  "evidence": ["D2:5", "D15:3"],
  "category": 1,
  "structured_query": "?who[Melanie]:instruments",  // NEW
  "retrieval_method": "structured"                   // NEW
}
```

### Phase 2: Convert observations to UKU pebbles

Each observation becomes a pebble with structured frontmatter:

```yaml
---
uku_id: uku-20230508-loc26-D1-3
created_at: 2023-05-08T13:56:00Z
uku_type: experience_capture
category: foundational
entity: Melanie
session: 2
attributes:
  instruments: [violin, piano]
  professions: [artist]
  interests: [adoption]
emotional_state: joy
intent: share
---
Original dialog text from LoCoMo
```

### Phase 3: Three-way comparison

| Metric | Semantic (LoCoMo baseline) | Structured (UKU red strings) | Hybrid (both + RRF) |
|--------|---------------------------|------------------------------|---------------------|
| Single-Hop | 95% | 98% (hypothesis) | 98% |
| Multi-Hop | 70% | 88% (hypothesis) | 90% |
| Memory depth 10+ | 60% | 87% (hypothesis) | 88% |
| Adversarial | 65% | 92% (hypothesis) | 91% |
| Tokens used | 20,000 | 500 | 1,500 |

### Phase 4: Pareto frontier mapping

The No-Escape Theorem says all semantic systems forget. Our hypothesis is that **structured red-string matching on controlled vocabularies sits at a new, untested point on the Pareto frontier** -- much higher semantic agreement than BM25's 15.5%, while preserving b=0 and FA=0.

LoCoMo gives us the dataset to prove this empirically.

## Red-String Query DSL (proposed)

| Type | Syntax | Example |
|------|--------|---------|
| Fact | `?who[X]:attribute` | `?who[Melanie]:instruments` |
| Temporal | `?when[event:Y]` | `?when[event:LGBTQ-support-group]` |
| Range | `?after[date:Z]` | `?after[date:2023-05-25]` |
| Multi-hop | `?who[X]:connected_to[Y]:attribute` | `?who[Melanie]:lives_with[Caroline]:profession` |
| Existence | `?exists[X:Y]` | `?exists[adoption-agency:Melanie-interest]` |

## License Implications

**CC BY-NC 4.0 means:**
- Cannot use LoCoMo dataset for commercial purposes
- Cannot release modified versions commercially
- CAN use for academic research/evaluation/publication
- MUST attribute Maharana et al., ACL 2024
- MUST include CC BY-NC 4.0 notice on derivatives

**Implication for UKU:** LoCoMo is fine for academic validation and publishing results. We cannot ship LoCoMo data inside a commercial Pebbles product. We can publish a paper showing structured metadata matching beats semantic retrieval on LoCoMo, then ship a separate (cleanroom) eval suite for the commercial product.

## Risk: Don't Couple Production Code to LoCoMo

The eval framework should be separable:
1. `pebble-eval-loco` -- uses LoCoMo, academic only, lives in a separate repo
2. `pebble-eval-core` -- runs custom eval datasets, MIT, ships with the product

This protects the commercial path while preserving academic credibility.

## Next Steps

1. Annotate 10-20% of LoCoMo QAs (~200 pairs) with red-string templates as proof of concept
2. Build a minimal red-string query evaluator in Python
3. Run 3-way comparison: semantic vs structured vs hybrid
4. Measure accuracy vs context size tradeoff
5. If hypothesis holds: write up as "Structured Metadata Matching Beats Semantic Retrieval on Long-Term Conversational Memory" and submit to a workshop
6. Use the result as the marketing wedge for Pebbles adoption
