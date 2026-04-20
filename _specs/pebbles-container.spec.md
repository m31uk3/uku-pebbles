# Pebbles Container Format — `.pebble` Zip Specification

**Status:** Placeholder — seeded from `.sop/synthesis/08-container-format-research.md`
**Spec version:** 0.3.0-draft (aligned with `pebbles.spec.md`)
**Date:** 2026-04-20
**Audience:** Implementers of `packages/core` zip reader/writer

---

## TL;DR

A `.pebble` file is a ZIP archive (ISO/IEC 21320-1:2015) containing structured YAML metadata alongside arbitrary binary artifacts. This is the Tier 2 storage format — extending the Tier 1 Markdown pebble to non-text content (screenshots, PDFs, audio, video, documents).

---

## Container Layout

```
mimetype                        # MUST be first entry, MUST be uncompressed (EPUB trick)
pebble.yaml                     # v0.3 UKU frontmatter — same schema as Tier 1 YAML
body.md                         # optional prose (with own YAML frontmatter)
artifact/<original-filename>    # binary payload(s), original filename preserved
META-INF/
  manifest-sha256.txt           # BagIt-style checksums (optional, recommended)
  pebble-version                # spec version declaration
```

---

## MIME Type

`application/vnd.uku.pebble+zip` — follows IANA `+zip` structured syntax suffix convention.

---

## Prior Art

| Format | Container | Year |
|--------|-----------|------|
| EPUB (W3C/IDPF) | ZIP via OCF | 2007 |
| DOCX/XLSX/PPTX (ECMA-376) | ZIP (OOXML) | 2006 |
| ODF | ZIP | 2005 |
| BagIt (RFC 8493) | Directory or tarball | 2008 |
| OCFL (Oxford Common File Layout) | Directory | 2019 |
| Day One (journal app) | ZIP | — |

---

## TODO — Sections to Write

- [ ] `mimetype` entry constraints (byte offset, compression method, no extra field)
- [ ] `pebble.yaml` schema binding (reference §5 of main spec)
- [ ] `artifact/` directory rules (single vs multi-artifact, filename preservation, dedup)
- [ ] `META-INF/manifest-sha256.txt` format (BagIt-compatible checksum manifest)
- [ ] `pebble-version` file format and version negotiation
- [ ] Central directory seek pattern for instant frontmatter access
- [ ] Size limits and compression recommendations per artifact type
- [ ] Round-trip preservation of unknown entries (§12.3 compliance)
- [ ] `pebble export --native` Tier 3 escape hatch (XMP injection, YAML sidecar)
- [ ] Quick Look plugin contract for macOS preview
- [ ] Conformance test fixtures
- [ ] Error handling (corrupt zip, missing mimetype, schema validation failure)

---

## Cross-References

- Main spec: `_specs/pebbles.spec.md` §3 (three-tier model), §12 (versioning)
- Research: `.sop/synthesis/08-container-format-research.md`
- CLI spec: `_specs/pebbles-cli-spec-agent.md` (Component 2: Core)
- TODO.md: Phase 1 → `packages/core` tasks
