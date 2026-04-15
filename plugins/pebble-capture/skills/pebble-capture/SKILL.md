---
name: pebble-capture
description: Capture episodic memories as Pebbles (Universal Knowledge Units). Use when the user says "save this as a pebble", "capture this", "pebble this", "remember this", mentions pebbles, UKU, episodic memory, or wants to persist a Slack message, email, meeting note, web page, or terminal session as structured knowledge. Applies hierarchical templates from ~/.pebbles/templates/ to maximize context capture with minimal friction.
---

# Pebble Capture

Create spec-compliant Pebbles (v0.3) from any source — Slack threads, emails, meetings, web pages, terminal sessions. Templates auto-populate structured YAML frontmatter for maximum red-string discoverability.

## Parameters

- **source_url** (optional): URL of the artifact (Slack permalink, email link, web page). Used to match app template.
- **source_app** (optional): Override app detection. Values: `slack | email | web | meeting | terminal | notes | calendar`
- **vault_path** (optional, default: from `~/.pebbles/config.json` or auto-detect Obsidian vault): Where to write the pebble.
- **pebble_type** (optional, default: from template): `experience_capture | insight | problem_statement | proposed_solution | reference | ontology`
- **emotional_state** (optional): Plutchik 8 Primary: `joy | sadness | anger | fear | surprise | disgust | trust | anticipation`
- **intent** (optional): `remember | act_on | share | think_about`
- **tags** (optional): Comma-separated tags.

**Constraints:**
- If source_url provided, auto-detect source_app from URL pattern
- If neither source_url nor source_app, ask user what they're capturing
- Always generate ULID for pebble_id
- All timestamps must be full ISO 8601 with timezone (Z preferred)
- Never use date-only values

## Step 1: Detect Source & Load Templates

1. Read `~/.pebbles/templates/00-base.json` (always)
2. Read `~/.pebbles/templates/01-org.json` (always)
3. Match app template by `source_app` or URL pattern:
   - `*.slack.com/*` → `10-slack.json`
   - Email conversation ID → `10-email.json`
   - `https://*` (general web) → `10-web.json`
   - Meeting context → `10-meeting.json`
   - Terminal/CLI → `10-terminal.json`
4. Stack templates: base → org → app (later overrides earlier defaults)
5. Determine vault path and create `_pebbles/{YYYY}/{MM}/{DD}/` directory

## Step 2: Extract Source Provenance

Based on matched template, extract structured `source` block.

### For Slack (`10-slack.json`):
1. Parse URL: `https://{workspace}.slack.com/archives/{channel_id}/p{ts}`
2. Use Slack MCP tools (`get_thread`, `get_channel`) to fetch:
   - `source.workspace` from URL
   - `source.channel_id` from URL path
   - `source.channel_name` from channel metadata
   - `source.thread_ts` from URL
   - `people[]` from message user objects (alias, name, role, is_bot)
3. Capture full thread content for the body

### For Email (`10-email.json`):
1. Use email MCP tools (`email_read`) to fetch:
   - `source.subject`, `source.from`, `source.to`, `source.cc`
   - `source.conversation_id`, `source.message_id`
   - `source.provider` (outlook)
   - `people[]` from participants
2. Capture email body as markdown for the pebble body

### For Web (`10-web.json`):
1. Fetch page content (defuddle extraction path when available)
2. Extract: `source.domain`, `source.url`, `source.author`, `source.published`
3. Capture extracted content for the body

### For Meeting (`10-meeting.json`):
1. Use calendar MCP tools to fetch event metadata
2. Extract: `source.title`, `source.start_time`, `source.end_time`, `source.organizer`
3. `people[]` from attendees
4. User provides meeting notes as body

### For Terminal (`10-terminal.json`):
1. Auto-detect: `source.shell` from `$SHELL`, `source.working_dir` from `$PWD`
2. `source.hostname` from system
3. `device` block from system info
4. User provides command/output as body

## Step 3: Generate Pebble YAML

1. Generate ULID for `pebble_id` (26 alphanumeric chars, time-sortable)
2. Set `created_at` to current time in ISO 8601 with Z
3. Apply template defaults for `pebble_type`, `memory_kind`, `modality`
4. Ask user for Tier 2 fields if not provided:
   - `emotional_state` (Plutchik 8 picker)
   - `intent` (remember / act_on / share / think_about)
   - `tags` (suggest from existing vault tags if available)
5. Set `org` and `team` from org template
6. Set `status: active`

## Step 4: Generate Filename & Write

1. Generate stub from title (≤20 chars, lowercase, hyphenated)
2. Format: `{stub}-{ULID}-{DDMMMYY}-{HHMMSS}.md`
3. Create directory: `{vault_path}/_pebbles/{YYYY}/{MM}/{DD}/`
4. Write pebble file with YAML frontmatter + body
5. Confirm to user with:
   - File path
   - Red strings this pebble creates (list matching fields)
   - Suggested `governed_by` ontology links if relevant

## Step 5: Post-Capture (Optional)

If user wants to refine:
- Add `governed_by` ontology links
- Adjust tags based on existing vault vocabulary
- Set `pin: true` or `archive_at` for lifecycle control
- Add `context_elements.why_captured` if not already set

## References

- Pebbles Spec v0.3: `references/pebbles-spec-summary.md`
- Template System: `~/.pebbles/README.md`
- Templates: `~/.pebbles/templates/*.json`

## Troubleshooting

**No template matched:** Falls back to base + org. All fields are manual Tier 2 input.

**Slack MCP not available:** Ask user to paste the message content. Extract what you can from the URL.

**ULID generation fails:** Use Python: `import time,random; t=int(time.time()*1000); chars='0123456789ABCDEFGHJKMNPQRSTVWXYZ'; enc=''.join(chars[(t>>(45-5*i))&31] for i in range(10)); rand=''.join(random.choice(chars) for _ in range(16)); print(enc+rand)`

**Vault path unknown:** Check for Obsidian vaults at `~/shared/Obsidian/` or ask user.
