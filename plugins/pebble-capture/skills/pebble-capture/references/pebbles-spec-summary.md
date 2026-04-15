# Pebbles Spec v0.3 — Quick Reference for Skill

## Required Fields
- `title`: string, ≤120 chars
- `pebble_id`: ULID, 26 alphanumeric (Crockford Base32, no I/L/O/U)
- `created_at`: ISO 8601 with timezone (Z preferred). Date-only INVALID.
- `pebble_type`: `experience_capture | insight | problem_statement | proposed_solution | reference | ontology`

## Controlled Vocabularies
- `memory_kind`: `episodic | semantic | procedural`
- `modality`: `kinetic | non_kinetic`
- `category`: `foundational | vision | technical | insight | problem`
- `emotional_state` (Plutchik 8): `joy | sadness | anger | fear | surprise | disgust | trust | anticipation`
- `intent`: `remember | act_on | share | think_about`
- `status`: `draft | active | annotated | published | archived | tombstoned | superseded`
- `location.venue_type`: `home | office | coffee_shop | transit | outdoor | other`

## Field Classes
- **Capture-Immutable**: `pebble_id`, `created_at`, body, `url`, `source_id`, `content_hash`, `device`, `source_app`, `location` (if set at capture)
- **Curator-Editable**: `pebble_type`, `memory_kind`, `emotional_state`, `intent`, `modality`, `tags`, `topic`, `category`, `governed_by`, `status`, `pin`, `archive_at`, `protected`, all typed edges

## Cross-References
Use (label, uid) tuple: `governed_by: [{label: "name", uid: "ULID"}]`

## File Naming
`{stub≤20}-{ULID}-{DDMMMYY}-{HHMMSS}.md` in `_pebbles/{YYYY}/{MM}/{DD}/`

## Red Strings
Any matching YAML key-value pair = automatic connection. No manual linking needed.
