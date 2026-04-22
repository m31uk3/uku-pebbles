---
title: "Pebble Template: 10-known-issue.json — Structured Known-Issue Capture"
pebble_id: 01KPQ8RVZM4KXWN3BFHJ6T2P9A
created_at: 2026-04-21T12:15:00-07:00
pebble_type: proposed_solution
memory_kind: semantic
modality: kinetic
org: global-real-estate
team: Business Innovation and AI (BIA)
source:
  app: terminal
  shell: zsh
  working_dir: /Users/lujackso/_workspaces/github/uku-pebbles
  tool: kiro-cli
tags:
  - pebbles
  - template
  - known-issue
  - primitive
  - problem-statement
  - triage
status: active
people:
  - alias: lujackso
    name: Luke Jackson
    role: author
pin: true
protected: true
---

## Problem

The Pebbles template hierarchy (00-base → 01-org → 10-{app}) covers source provenance but has no template for issue-type pebbles. Known issues — bugs, outages, gotchas, failure modes — need structured metadata beyond what `pebble_type: problem_statement` provides. Without it, triage queries like "all critical unresolved issues affecting kiro-cli" require full-text search instead of faceted red-string matching.

## Primitive

`10-known-issue.json` extends the base + org templates with 12 issue-specific fields. Six are controlled-vocabulary enums (red-string eligible), two are booleans (red-string eligible), and four are prose/datetime (search-only). The template auto-applies when `pebble_type: problem_statement` and `tags` contain `known-issue`.

## Template Location

```
~/.pebbles/templates/10-known-issue.json
```

Stacking order: `00-base.json` → `01-org.json` → `10-known-issue.json`

## Field Reference

### Red-string eligible (controlled vocabulary — graph fields)

| Field | Type | Values | Purpose |
|-------|------|--------|---------|
| `severity` | enum | `critical \| high \| medium \| low` | Triage priority |
| `environment` | enum | `production \| staging \| development \| all` | Where it manifests |
| `reproducibility` | enum | `always \| intermittent \| once \| unknown` | Reproduction confidence |
| `resolution_status` | enum | `investigating \| workaround_only \| fix_in_progress \| resolved` | Current state |
| `workaround_available` | boolean | `true \| false` | Highest-value triage signal |
| `root_cause_known` | boolean | `true \| false` | Investigation completeness |
| `affected_systems` | array[string] | controlled list | Systems/tools affected |

### Search-only (prose/datetime — context fields)

| Field | Type | Purpose |
|-------|------|---------|
| `impact_scope` | string | Who/what is affected (prose) |
| `discovered_at` | datetime | When first observed (may differ from `created_at`) |
| `discovered_by` | array[{alias, name, role}] | Who reported it |
| `workaround_summary` | string | One-line workaround |
| `resolved_at` | datetime | When resolved (null until then) |
| `related_tickets` | array[string] | SIM/ticket IDs |

### Design Decisions

1. `discovered_at` vs `created_at` — the pebble may be created days after the issue was first observed. Conflating these loses timeline accuracy.

2. `workaround_available` as a top-level boolean — this is the single highest-value field for a reader scanning known issues. It answers "can I unblock myself right now?" before reading anything else.

3. `pin: true` by default — known issues should never auto-archive while active. The lifecycle policy exemption is deliberate.

4. `impact_scope` is prose (not red-string eligible) because impact descriptions are inherently unique. `affected_systems` is the controlled counterpart for graph queries.

5. `severity` uses 4 values, not 5 — aligns with standard triage (P1-P4). "Informational" issues are just pebbles with `pebble_type: insight`.

## Body Template

```markdown
## Symptom
<!-- What the user/system observes. One paragraph. No interpretation. -->

## Impact
<!-- Who is affected, how many, what can't they do. Quantify. -->

## Reproduction Steps
1.

## Workaround
<!-- If workaround_available: true — exact steps. If false: "None known." -->

## Root Cause
<!-- If root_cause_known: true — explain. If false: "Under investigation." -->

## Timeline
| Date | Event |
|------|-------|

## References
```

## Example Pebble (Fully Populated)

```yaml
---
title: "Kiro CLI symlink target broken on macOS — templates not found"
pebble_id: 01KPQ9EXAMPLE00000000000
created_at: 2026-04-21T12:00:00-07:00
pebble_type: problem_statement
memory_kind: episodic
modality: kinetic
category: problem
emotional_state: anger
intent: act_on
status: active
pin: true
severity: medium
impact_scope: "Any macOS user whose $HOME is /Users/ — the symlink targets /home/"
affected_systems:
  - kiro-cli
  - pebble-capture
environment: development
reproducibility: always
discovered_at: 2026-04-21T12:00:00-07:00
discovered_by:
  - alias: lujackso
    name: Luke Jackson
    role: reporter
workaround_available: true
workaround_summary: "Create templates directly at ~/.pebbles/templates/ instead of relying on the repo symlink"
resolution_status: workaround_only
root_cause_known: true
related_tickets: []
org: global-real-estate
team: "Business Innovation and AI (BIA)"
source:
  app: terminal
  shell: zsh
  working_dir: /Users/lujackso/_workspaces/github/uku-pebbles
  tool: kiro-cli
people:
  - alias: lujackso
    name: Luke Jackson
    role: author
tags:
  - known-issue
  - kiro-cli
  - symlink
  - macos
---
```

## Relationship to Template Hierarchy

This is the first non-source-provenance template in the `10-` tier. The existing `10-{app}.json` templates match by `source.app` or URL pattern. `10-known-issue.json` matches by `pebble_type` + `tags`, establishing a second matching axis: content-type templates alongside source-type templates.

This pattern extends to future content-type templates (e.g., `10-decision-record.json`, `10-retrospective.json`) without conflicting with source-type templates — a pebble can stack both `10-slack.json` (source) and `10-known-issue.json` (content) if the issue was discovered in Slack.

## Provenance

- Pebbles spec v0.3.0-draft (`uku-pebbles/_specs/pebbles.spec.md`)
- Template system design (`uku-pebbles/_discussions/pebble-templates-design-15APR26.md`)
- Pebble-capture skill (`uku-pebbles/plugins/pebble-capture/skills/pebble-capture/SKILL.md`)
- Fleeting vs permanent field distinction (`_insights/memory-systems-intersectional-insights-26MAR26.md`)
