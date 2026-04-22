# Defuddle Investigation

**Repo:** `/Users/ljack/github/defuddle`
**Author:** Steph Ango (@kepano) -- creator of Obsidian
**License:** MIT (fully forkable)

## Tech Stack

| Aspect | Detail |
|--------|--------|
| Language | TypeScript (ES2020+) |
| Runtime | Node.js v14+ AND Browser (works with JSDOM, linkedom, happy-dom) |
| Build | Webpack 5 + ts-loader + Vitest |
| Hard deps | Just `commander` (for CLI) |
| Optional deps | linkedom, mathml-to-latex, temml, turndown |

## Project Type

Hybrid library + CLI tool. Three export bundles:
- `dist/index.js` -- Browser bundle (~150KB, no deps)
- `dist/index.full.js` -- With Markdown + math (~250KB)
- `dist/node.js` -- Node.js async API (~200KB)
- `dist/cli.js` -- Compiled CLI executable

Also published as npm package and runs as Cloudflare Worker (`defuddle.md` API).

## Purpose

Content extraction from web pages -- removes clutter, extracts main article. Comparable to Mozilla Readability but more forgiving with better metadata extraction. Capabilities:
- Cleans HTML (removes nav, sidebars, ads, comments)
- Extracts metadata (title, author, date, description, favicon, image, language)
- Standardizes elements (footnotes, code blocks, headings, math, callouts)
- Optional Markdown conversion via Turndown.js
- Site-specific extractors for: X/Twitter, YouTube, Reddit, GitHub, ChatGPT, Claude, Gemini, Grok, Substack, HackerNews

## Core Architecture

### Main entry points
- Browser: `src/index.ts`
- Full bundle: `src/index.full.ts` (with Markdown + math)
- Node: `src/node.ts` (async, accepts any DOM)
- CLI: `src/cli.ts`

### Core modules
| Module | Lines | Purpose |
|--------|-------|---------|
| `src/defuddle.ts` | 1500+ | Main parsing pipeline |
| `src/standardize.ts` | 1200+ | HTML normalization |
| `src/markdown.ts` | 700+ | HTML-to-Markdown via Turndown |
| `src/metadata.ts` | -- | Schema.org, meta tags, OpenGraph |
| `src/extractor-registry.ts` | -- | Plugin architecture for site-specific extractors |
| `src/extractors/` | 18 files | Site-specific parsers |

### Extractor plugin pattern
```typescript
ExtractorRegistry.register({
  patterns: ['twitter.com', /x\.com\/.*/],
  extractor: TwitterExtractor
});
```

## DefuddleResponse Output Format

```typescript
{
  content: string;           // HTML or Markdown
  contentMarkdown?: string;  // Optional separate version

  // Already extracts what UKU needs:
  title: string;
  author: string;
  site: string;
  domain: string;
  favicon: string;
  image: string;
  description: string;
  published: string;
  language: string;          // BCP 47

  // Extras
  wordCount: number;
  parseTime: number;
  schemaOrgData: any;        // Raw schema.org JSON-LD
  metaTags?: MetaTagItem[];
  extractorType?: string;
  variables?: Record<string, string>;  // Custom variables hook
}
```

## Fork Strategy for Pebbles YAML Injection

**Verdict: EXCELLENT fork candidate.** Defuddle already extracts most of what UKU needs.

### Best integration point
`src/node.ts` -- wrap the Defuddle call:

```typescript
import { Defuddle as DefuddleBase } from './defuddle';
import { injectPebblesYAML } from './pebbles';

export async function Defuddle(
  input: Document | string,
  url?: string,
  options?: DefuddleOptions & PebblesOptions
): Promise<DefuddleResponse> {
  const result = await DefuddleBase(...);
  if (options?.addPebbles) {
    result.content = injectPebblesYAML(result, options);
  }
  return result;
}
```

### Proposed fork module structure
```
src/pebbles/
├── types.ts           # PebblesYAML interface
├── generator.ts       # YAML frontmatter generation
├── attributes.ts      # Pebbles attribute mapping (defuddle metadata -> UKU schema)
└── middleware.ts      # Injection middleware
```

**Estimated effort:** 200-400 lines of TypeScript to fully integrate Pebbles YAML injection while maintaining upstream compatibility.

## Why Fork Instead of Wrap

1. **Tier 3 inference benefits from being inside the pipeline** -- venue_type from URL patterns, source_type from extractor type, all feasible during defuddle's existing pipeline
2. **The `variables` system already exists** -- Pebbles attributes can flow through this
3. **Site-specific extractors map perfectly to source-aware pebble enrichment** -- a Twitter extractor knows it's a tweet, a YouTube extractor knows it's a video
4. **Upstream rebase is easy** -- clean module separation means we can pull defuddle updates without conflicts

## Strategic Note

Steph Ango (@kepano) is also the author of obsidian-clipper AND the "file over app" essay we read as inspiration. The same author owns both the content extraction layer AND the philosophical positioning we're aligning with. This is a remarkable convergence -- forking defuddle is structurally aligned with the same vision that informed UKU.
