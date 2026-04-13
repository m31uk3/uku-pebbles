# Container Format Research: Zip Envelope vs Header Injection

**Question:** How should Pebbles bundle YAML frontmatter with arbitrary file artifacts (PDFs, images, screenshots, documents, audio, video)?

**Verdict:** **Approach A (zip container) wins decisively.** 9 categories vs 2.

## Approach A: `.pebble` = ZIP Archive

A `.pebble` file is a ZIP archive containing:
```
mimetype                   # uncompressed, first entry: "application/vnd.uku.pebble+zip"
pebble.yaml                # the structured UKU frontmatter
body.md                    # optional prose description (with own YAML frontmatter)
artifact/<original>        # the binary file(s), original filename preserved
META-INF/
  manifest-sha256.txt      # BagIt-style checksums (optional)
  pebble-version           # spec version declaration
```

This mirrors EPUB's Open Container Format (OCF) exactly.

### Prior Art (decisive evidence)

| Format | Container | Manifest | Year |
|--------|-----------|----------|------|
| **EPUB** (W3C/IDPF) | ZIP via OCF spec | META-INF/container.xml + OPF | 2007 |
| **DOCX/XLSX/PPTX** (ECMA-376/ISO 29500) | ZIP (OOXML) | [Content_Types].xml + customXml/ | 2006 |
| **ODF** | ZIP | META-INF/manifest.xml | 2005 |
| **BagIt** (RFC 8493, Library of Congress) | Directory or tarball | bagit.txt + manifest-sha512.txt | 2008 |
| **OCFL** (Oxford Common File Layout) | Directory | inventory.json (content-addressable) | 2019 |
| **PDF/A-3** (ISO 19005-3) | PDF (acts as container) | /AF array + AFRelationship | 2012 |
| **Frictionless Data Package** | Directory or zip | datapackage.json | 2017 |
| **WebDataset** (ML training) | Tar shards | .json sidecar per sample basename | 2021 |
| **C2PA Content Credentials** | JUMBF box (ISO 19566-5) | Cryptographic manifest with assertions | 2022 |
| **Day One** (journal app) | ZIP | Journal.json + photos/ + videos/ | -- |

**EPUB, DOCX, ODF -- three of the most widely deployed document formats on Earth -- all chose "zip + manifest" for this exact problem.** That's the strongest signal we have.

### Strengths
- **Universal** -- same logic for PDFs, JPEGs, screenshots, MP4s, audio, raw, DOCX, plain text
- **Instant frontmatter access without unpacking the binary** -- ZIP's central directory is at the END of the file. Reader does `seek(SIZE-65557)`, finds central dir, reads `pebble.yaml`. Never touches the binary payload. This is exactly how EPUB scans 5,000-book libraries in milliseconds.
- **File-over-app durable** -- ZIP (1989) + UTF-8 (1992) + YAML 1.2 (strict JSON subset since 2009). All open, royalty-free, ISO-standardized (ISO/IEC 21320-1:2015 for ZIP). Closest digital formats get to "carved in stone."
- **Survives copy/paste, email, AirDrop** -- one file, one bundle. No risk of YAML separation from artifact.
- **Tamper-evident by extension** -- BagIt-style checksums or OCFL content addressing for free.
- **Body.md slot is free** -- the existing UKU Markdown+YAML toolchain works on it.
- **Custom MIME type is trivial** -- `application/vnd.uku.pebble+zip` follows IANA `+zip` convention used by `epub+zip`.
- **Inspectable with stock tools** -- `unzip`, `zipinfo`, Finder Quick Look, `zipgrep`. Archaeologist test passes.

### Weaknesses
- **Not a "real" image/PDF/video** -- a `.pebble` containing a JPEG is not itself a JPEG. Can't drag into Photoshop without unwrapping.
- **Filesystem dedup slightly worse** -- a pebble around `cat.jpg` is a different blob from `cat.jpg`.
- **Slightly larger** -- ZIP central directory overhead (~100 bytes per file).
- **Native preview needs Quick Look extension** -- one-time engineering cost.
- **Two-tier knowledge** -- spec authors must define internal layout (one-time work).

## Approach B: Header / In-File Injection

Inject YAML/JSON into existing file format headers.

### Per-format feasibility

| Format | Mechanism | Custom YAML feasible? | Lossy on copy? | Stock OS searchable? | Verdict |
|--------|-----------|----------------------|----------------|---------------------|---------|
| **PDF** | XMP metadata stream | YES (custom XMP namespaces) | Mostly preserved; some "Save As" drops | Yes | Strong |
| **JPEG** | XMP packet (APP1) or JUMBF (APP11) | YES | **STRIPPED by Instagram, Facebook, Imgur, X, WhatsApp**; lost on clipboard | Limited | Workable but fragile |
| **PNG** | iTXt chunk + custom keyword | YES | Survives most editors; lost on re-encoding/screenshots/clipboard | Yes | Strong for PNG |
| **HEIC/HEIF** | XMP/EXIF boxes | YES | OK on Apple; spotty cross-platform | Apple yes | Apple-only |
| **MP3** | ID3v2 TXXX user-defined frames | YES | Most players preserve | Yes | Workable |
| **MP4/M4A/MOV** | udta atom; uuid box | Partial | **AVFileTypeMPEG4 silently DROPS** non-standard atoms | Inconsistent | **WEAK** |
| **WAV/AIFF** | XMP via specific chunk | YES | Often stripped by audio editors | Limited | Weak |
| **DOCX/XLSX/PPTX** | Custom XML parts | YES (already a zip!) | Preserved | Yes | Strong |
| **HTML** | meta tags or JSON-LD | YES | Survives | Yes | Strong |
| **SVG** | XMP in metadata element | YES | Often stripped by minifiers | Mostly | OK |
| **Markdown** | YAML frontmatter | YES (existing UKU) | Survives anything | Yes | Best for text |
| **Plain .txt** | None without breaking format | NO | -- | -- | Not feasible |
| **Raw binary** | None | NO | -- | -- | Not feasible |

### Strengths
- **The artifact stays a "real" file** -- a JPEG with XMP is still a JPEG. Finder previews it, Photoshop opens it.
- **Per-format standards already exist** -- XMP (ISO 16684), JUMBF (ISO 19566-5), C2PA built on JUMBF.
- **C2PA proves it's operationally viable** at scale -- Adobe, Microsoft, Intel, BBC, NYT, Leica, Sony, Nikon ship this.

### Weaknesses (decisive)
- **No single mechanism works for every artifact type.** XMP comes closest but cannot embed binary, has different host conventions per format, and is dropped in some workflows. Pebble spec would need an N×M compatibility matrix.
- **Catastrophic loss on social/cloud round-trips.** Confirmed:
  - Instagram, Facebook, Imgur, WhatsApp, X all strip EXIF/XMP from uploaded photos
  - Google Photos Takeout strips EXIF and stores it in adjacent JSON (sidecar fallback)
  - Apple Photos hides metadata in a private SQLite database
  - Discord, Slack, iMessage strip on multiple paths
- **Lost on clipboard copy/paste.** Pasted images carry NO metadata across macOS/Windows clipboard. Kills the most common screenshot workflow.
- **Not searchable by Spotlight** -- documented behavior: XMP is NOT indexed unless a custom mdimporter is installed.
- **No unified write path** -- writing custom XMP needs PDF library + JPEG library + MP4 library + ID3 library + libpng + 4 more. The Pebble spec would have to ship 8+ format-specific writers.
- **Apple's AVFileTypeMPEG4 silently drops custom udta atoms** -- confirmed in Apple Developer Forums.
- **Failure mode is invisible.** When XMP gets stripped, the user has no warning. Data is gone.
- **Extended attributes are not a workable substitute** -- macOS xattrs are dropped by NFSv4, GNU mv, BSD cp, archivers, and most cloud syncs.

## What Apple/Google/Notion Actually Do

This is the most decisive evidence:

- **Apple Photos**: Hidden private SQLite database. **Database-first, not file-first.** "Apple keeps keywords and descriptions hidden away in a private database that nobody else can see or use." (NeoFinder dev)

- **Google Photos**: Server-side database. Takeout export gives `image.jpg` + `image.jpg.json` (sidecar pair) because Google **strips EXIF before upload** to the public/CDN tier. **Sidecar JSON is Google's de facto answer to this exact problem.**

- **Day One**: JSON-first. Export is a `.zip` containing `Journal.json` + `photos/` + `videos/`. **This is exactly Approach A** -- Day One's export is essentially a Pebble bundle.

- **Notion**: Block database in PostgreSQL on Notion's servers. No local file format. Export gives Markdown + `images/` folder. **Database-first; the worst possible model for "file over app."**

**The pattern: every cloud-first product uses a database internally and falls back to a sidecar JSON + folder of binaries when forced to export. None achieved reliable in-file metadata injection at scale, even Google.** This is the single most important data point in the research.

## Recommendation Matrix

| Criterion | Approach A | Approach B |
|-----------|-----------|-----------|
| Instant access without unpack | Strong | Strong |
| File-over-app durability (50-100yr) | **Strong** | Mixed |
| Universal across artifact types | **Strong** | Weak |
| Survives copy/paste, email, AirDrop | **Strong** | Weak |
| Survives social media / cloud upload | **Strong** | Catastrophic |
| Searchable by stock OS | Needs QL/mdimporter plugin | XMP not indexed by default |
| Inspectable with stock CLI tools | **Strong** | Format-specific tools required |
| Native preview in Finder/Explorer | Needs Quick Look extension | **Strong** |
| Existing prior art | EPUB, DOCX, ODF, BagIt, Day One, etc. | XMP, C2PA, JUMBF |
| One library to implement | Yes | No (8+ format writers) |
| Tamper-evident option | Free (BagIt manifest) | Hard (only C2PA, with crypto) |
| Failure mode | Loud | **Silent** |
| Plain text + binary in one bundle | **Yes** | No |
| Sharing to non-Pebble users | Needs export command | **Strong** |

**Final score: A wins 9, B wins 2, neutral 1.**

## Final Recommendation

**Adopt Approach A (zip container) as the canonical Pebble format.** Specifically:

1. **`.pebble` = ZIP archive** with magic-byte-sniffable PK header
2. **Internal layout** mirroring EPUB/BagIt:
   ```
   mimetype                # uncompressed first entry, EPUB trick
   pebble.yaml             # UKU YAML schema
   body.md                 # optional prose with own frontmatter
   artifact/<original>     # binary file(s)
   META-INF/
     manifest-sha256.txt   # optional checksums
     pebble-version        # spec version
   ```
3. **MIME type:** `application/vnd.uku.pebble+zip`
4. **First file in zip is `mimetype` stub**, uncompressed, for `file(1)` identification (EPUB trick)
5. **Ship `pebble export --native`** for "still a real file" use cases:
   - Writes artifact to disk with `.yaml` sidecar (Google Takeout pattern)
   - OR embeds XMP into the artifact when format supports it (PDF, JPEG, PNG via XMP namespace `http://uku.org/pebble/1.0/`)
   - Treat this as one-way export, not canonical storage
6. **Quick Look plugin for macOS** to render `.pebble` as preview-of-artifact + metadata table
7. **Future: align with BagIt or OCFL** if archival-grade durability needed for vaults

## Why C2PA-Style Header Injection is the Right Secondary Mode

For artifacts that need to remain useful in non-Pebble contexts (a screenshot you'll paste into a presentation, a PDF you'll email to a lawyer), having Pebbles **also** be able to inject XMP/JUMBF is genuinely valuable. Treat as the equivalent of "export to PDF" in Word -- a one-way conversion for interop, not the canonical storage.

## Three-Tier Pebble Storage Model

This gives us a clean three-tier model that solves both use cases:

| Tier | Format | Use Case | Durability |
|------|--------|----------|-----------|
| **Tier 1: Markdown** | `pebble.md` (YAML frontmatter + Markdown body) | Pure text pebbles (notes, thoughts, links) | Maximum (file-over-app gold standard) |
| **Tier 2: Pebble Bundle** | `.pebble` (zip container) | Artifact pebbles (screenshots, PDFs, audio) | High (ZIP + UTF-8 + YAML, all ISO) |
| **Tier 3: Native Export** | Original file + `.yaml` sidecar OR embedded XMP | Sharing to non-Pebble tools | Variable (depends on host format) |

Tier 1 is what UKU spec already defines. Tier 2 extends UKU to non-text artifacts. Tier 3 is the interop escape hatch.

**This is the answer to A2 (container format question): adopt the three-tier model.**
