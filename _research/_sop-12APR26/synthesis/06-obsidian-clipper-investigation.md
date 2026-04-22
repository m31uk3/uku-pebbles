# Obsidian Clipper Investigation

**Repo:** `/Users/ljack/github/obsidian-clipper`
**Maintainer:** Obsidian (kepano-adjacent)
**License:** MIT (fully forkable)

## Tech Stack

| Aspect | Detail |
|--------|--------|
| Language | TypeScript + SCSS |
| Project Type | Browser extension (Manifest V3) |
| Browsers | Chrome, Brave, Arc, Edge, Firefox, Safari |
| Build | Webpack 5 + ts-loader + esbuild |
| Tests | Vitest |
| Polyfill | webextension-polyfill (cross-browser) |

## Key Dependency: defuddle

```json
"defuddle": "^0.16.0"
```

**obsidian-clipper depends on defuddle as its content extraction engine.** Defuddle does the heavy lifting (article extraction, metadata, Markdown conversion); obsidian-clipper provides the browser UI, template system, and Obsidian vault delivery.

## Architecture

### Entry points
- `src/background.ts` -- Service worker (browser API, tab management)
- `src/content.ts` -- Content script (DOM access, highlights)
- `src/core/popup.ts` -- Main popup UI controller
- `src/core/settings.ts` -- Settings page
- `src/api.ts` -- Programmatic API (environment-agnostic, used by CLI)

### Module structure
```
src/
├── background.ts
├── content.ts
├── core/
│   ├── popup.ts                    # Main clipping logic
│   └── settings.ts
├── managers/
│   ├── template-manager.ts          # Template definitions
│   ├── highlights-manager.ts
│   ├── property-types-manager.ts    # Custom property types
│   └── template-ui.ts
├── utils/
│   ├── content-extractor.ts         # Defuddle integration
│   ├── obsidian-note-creator.ts     # Frontmatter + URI generation
│   ├── template-compiler.ts         # Template variable compilation
│   ├── filters/                     # 100+ filter implementations
│   └── shared.ts                    # generateFrontmatter()
└── api.ts                            # Programmatic API
```

## Default YAML Frontmatter Output

```yaml
---
title: {{title}}
source: {{url}}
author: {{author|split:", "|wikilink|join}}
published: {{published}}
created: {{date}}
description: {{description}}
tags:
  - clippings
---
{{content}}
```

This is **exactly the YAML structure we've been processing in our source documents** (Thread by @ashwingop, "Price of Meaning"). Obsidian-clipper IS the tool generating those `.md` files.

## Property Types Already Supported

- text (default)
- multitext (array with `-` list syntax)
- number
- checkbox
- date / datetime (ISO 8601)

The property type system is already designed for extension. Adding Pebbles property types (Ekman 8 emotion enum, uku_type enum, intent enum) is **a configuration change, not a code change**.

## UI/UX Flow

1. User presses hotkey (Ctrl+Shift+O / Cmd+Shift+O)
2. Popup opens with auto-extracted content
3. Form shows:
   - Note name field
   - Properties section (collapsible metadata fields)
   - Content field (editable Markdown)
   - Vault/path selector
   - Optional interpreter section (AI processing)
4. User submits via:
   - "Add to Obsidian" button (URI scheme)
   - Save to file
   - Copy to clipboard
   - Share

Plus secondary modes:
- Highlighter mode (Alt+Shift+H) -- annotate page
- Reader mode (Alt+Shift+R) -- typography view
- Embedded mode -- side panel

## Fork Strategy for Pebbles

**Verdict: EXCELLENT fork candidate.** The property/template system is already designed for arbitrary metadata.

### Integration points (ranked by effort)

**1. Property Definition Level (easiest)**
File: `src/managers/template-manager.ts`, function `createDefaultTemplate()`, lines 113-132
```typescript
properties: [
  // ... existing properties ...
  { name: 'uku_id', value: '{{date|format:"YYYYMMDD"}}-{{uuid}}' },
  { name: 'uku_type', value: 'experience_capture' },
  { name: 'category', value: 'foundational' },
  { name: 'emotional_state', value: '' },  // user-fillable
  { name: 'intent', value: '' },             // user-fillable
]
```

**2. Variable Compilation Level (medium)**
File: `src/core/popup.ts`, lines 1025-1035
Inject Pebbles attributes into compiled properties before frontmatter generation.

**3. Frontmatter Generation Level (most control)**
File: `src/utils/shared.ts`, function `generateFrontmatter()`, lines 145-215
Wrap or extend to inject Pebbles section.

**4. API Level (cleanest for external use)**
File: `src/api.ts`, function `clip()`, lines 176-260
Post-process `ClipResult` -- no changes needed to browser extension code.

**5. Content Extractor Hook (for Pebbles-specific data)**
File: `src/utils/content-extractor.ts`
Hook between defuddle extraction and template variable building.

## Key Insight: Two-Layer Fork Strategy

Because obsidian-clipper depends on defuddle, we have a choice:

**Option A: Fork only obsidian-clipper.** Keep defuddle as upstream dependency. Inject Pebbles attributes in the clipper layer. Benefit: defuddle stays clean, can update defuddle freely.

**Option B: Fork both.** Defuddle gets the Pebbles attribute generation logic (Tier 3 inference from extractors), clipper gets the UI for Tier 2 user input. Benefit: tighter integration, better leverage of extractor knowledge.

**Recommendation: Option B.** The Tier 3 inference (venue_type, source_type, content classification) belongs in defuddle because that's where the URL patterns and extractor knowledge live. The Tier 2 UI belongs in clipper because that's where the user is.

## Code Flow With Pebbles Hooks

```
[obsidian-clipper popup opens]
        ↓
[defuddle extracts content + metadata]
        ↓ HOOK A: defuddle injects Tier 3 inferences (venue_type, source_type)
        ↓
[obsidian-clipper builds template variables]
        ↓ HOOK B: inject Pebbles defaults (uku_id, uku_type)
        ↓
[user fills Tier 2 properties (intent, emotional_state)]
        ↓ HOOK C: validate against Ekman 8 / 4-intent enums
        ↓
[obsidian-clipper compiles properties to frontmatter]
        ↓
[Obsidian receives via obsidian:// URI]
```

## Why This Matters Strategically

**obsidian-clipper has hundreds of thousands of users.** It's the primary tool Obsidian users employ to clip web content. Forking it gives Pebbles immediate distribution into a user base that already understands YAML frontmatter and is philosophically aligned with "file over app."

If we fork obsidian-clipper as `pebble-clipper` (or similar), we're not building a new market. We're inserting Pebbles into an existing user behavior pattern.

## License

MIT. Copyright (c) 2024 Obsidian. Fully forkable.

## Estimated Effort

**Low.** The property/template system is generic. We're adding new property types and default values, not rewriting the architecture. Expected effort: 100-300 lines for the Pebbles extension layer.
