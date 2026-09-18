# md2slides — specification

Draft v0.1 · 2026-09-13 · renamed md2slides 2026-09-14 · **v2 shipped 2026-09-17** · Licence: MIT (decided)

A single-file, browser-hosted app that turns frictionless Markdown notes into cards, shows them as a
slideshow, and exports the same source as `.md` and as page-exact PDF.

Hosted at `https://janalogy.com/apps/md2slides/` — no install, no account, no server.
Storage is the visitor's own browser. Nothing is uploaded anywhere.

**v2 shipped 2026-09-17.** This document is the design target; the shipped build is `index.html`
(1556 lines). Since the rename the build added: a header with an **Examples ▾ menu** and an
*Open .md…* button; the superset **"All features"** default starter deck plus a **Markdown tutorial**
deck; a **two-column slide** (exactly two `##` under one `#` — fence-aware); a **resizable pane
divider**; the keyboard set (`z` zen · `v` slides-only · `s` slideshow from current · `S` from first ·
`/` slideshow search · digits jump 1–999); **mobile swipe** navigation; **no-wrap** navigation at the
ends; and full-text search that also indexes code fences and diagram source. Storage is the **single
live key `janalogy.mdcards.v2`** (`{ v, md, geometry, at }`, debounced 250 ms), reading `…v1` once as
a one-time migration, plus the divider width in `janalogy.mdcards.split`. The aspirational sections
below — a multi-deck library, the IndexedDB asset store, braindump mode, the one-click raster PDF,
CodeMirror — are roadmap for a later version, not this build.

---

## 1. Why this spec exists

The prerequisite question was whether an existing open-source project already does this. It does not.
Four MIT-licensed projects cover large parts of it and fail in the same three places.

Figures below were read live from the GitHub API on 2026-09-13.

| Project | Licence | Stars | Last push | What it covers | Where it fails |
|---|---|---|---|---|---|
| `marp-team/marp-cli` (+ `marp-core`, `marp-vscode`) | MIT | 3,816 / 1,150 / 2,088 | 2026-09-08 | MD → HTML/PDF/PPTX/PNG; VS Code split-pane preview; `headingDivider` | One size per deck; Mermaid plugin off by default and absent from the CLI |
| `slidevjs/slidev` | MIT | 48,639 | 2026-08-25 | Side editor; Mermaid + PlantUML built in; export PDF/PPTX/PNG/Markdown; `aspectRatio` + `canvasWidth` | Slides split on `---`, not `#`; aspect ratio is deck-level headmatter; Vue/Vite toolchain |
| `arpitbbhayani/deckrun` | MIT | 167 | 2026-09-02 | Closest UX — local split editor, autosave, caret drives preview, Mermaid + KaTeX, PDF via headless Chromium | `src/parser.ts` splits only on `/^[ \t]*---[ \t]*$/`; landscape only; no title-card semantics |
| `hakimel/reveal.js` + `webpro/reveal-md` | MIT | 72,291 / 3,915 | 2026-09-10 | Mature slideshow runtime, Markdown-driven decks | No editor pane, no PDF pipeline, no carousel geometry |
| `Open-reSource/slidev-theme-linkedin-carousel` | MIT | 25 | — | Purpose-built LinkedIn carousel export from Markdown | It is a theme, so carousel geometry is welded to the deck; layouts are Vue components |

Rejected on licence grounds: `jgm/pandoc` (GPL-2.0-or-later), `logseq/logseq` (AGPL-3.0),
`quarto-dev/quarto-cli` (licence unclassified by GitHub). Roughly a dozen small "LinkedIn carousel"
repositories are visual editors, one-shot generators or prompt packs, not Markdown authoring tools.

### 1.1 Requirement matrix

| Spec item | Closest existing support | Verdict |
|---|---|---|
| a. Frictionless braindump capture | none | no |
| b. Simple Markdown | all of them | yes |
| c. Produces cards | Marp, deckrun — partial | no |
| d. 16:9 + square + portrait from one source | none | no |
| e. Title card; `#` title, bullets, numbered lists | none | no |
| f. Text, images, links, code, Mermaid in slideshow | Slidev yes, Marp partial | partial |
| g1. Slideshow mode | reveal.js, Marp, Slidev | yes |
| g2. Export `.md` + PDF | Slidev `.md`; Marp PDF | partial |
| h. Left editor / right preview, `#` adds and switches card | none | no |

### 1.2 The three gaps, with source evidence

**Gap 1 — one card size per deck.** Marp Core registers `size` as a *global* directive:
`Object.defineProperty(marp.customDirectives.global, 'size', …)` in `marp-core/src/size/size.ts`.
Slidev's `aspectRatio` and `canvasWidth` are headmatter-only (`slidevjs/slidev/docs/custom/config/index.md`).
Neither can emit 16:9 and 4:5 from one source file without a second build.

**Gap 2 — heading-driven splitting is nowhere the default.** Marpit's `headingDivider` is modelled on
Pandoc's `--slide-level` and stays off until declared (`marpit.marp.app/directives`). deckrun's parser
has no heading logic at all. Every tool splits on `---`.

**Gap 3 — Mermaid is the least portable requirement.** Slidev has it built in; Marp treats it as an
off-by-default plugin missing from the CLI; deckrun supports it via a client script. Mermaid renders by
measuring the DOM, so any environment that changes the renderer changes the diagram's size — which is
why the export path in §7 matters more than the rendering library.

### 1.3 One external constraint that shapes the design

LinkedIn Help, document ads specification (`linkedin.com/help/lms/answer/a493903`, read 2026-09-13):

- "The file size can't exceed 100 MB and 300 pages."
- Supported file types: PPT, PPTX, DOC, DOCX, PDF. Lead-generation document ads support PDF only.
- "Videos and other animations in documents aren't supported and will display as static images instead."
- "Hyperlinks in the document will only be clickable if the member downloads the document."
- "PDFs with multiple layers must be flattened or merged."
- **"PDFs with multiple sized pages must be fit to the same page size."**

The last line is decisive: a single PDF must not mix page sizes. Per-card geometry is therefore an
*export* concern — one PDF per geometry profile, every page inside a PDF identical. This is a real
requirement, not a preference, and no surveyed tool models it.

---

## 2. Licence and dependencies

MIT, as decided: shortest permissive licence, attribution only, and the same licence as every candidate
this spec builds on. `LICENSE` is deliberately not created yet — it is not part of this deliverable.

Every dependency is permissively licensed. Versions and sizes below were read from the npm registry and
the jsDelivr CDN on 2026-09-13.

| Dependency | Version | Licence | Distributed size | Role | Loading |
|---|---|---|---|---|---|
| `markdown-it` | 15.0.2 | MIT | 125 KB min | Markdown → HTML, CommonMark-correct | bundled in app, required |
| `DOMPurify` | 3.4.15 | MPL-2.0 OR Apache-2.0 | 29 KB min | Sanitises raw HTML when enabled | loaded only if raw HTML is enabled |
| `mermaid` | 12.0.0 | MIT | 5.4 MiB min | Diagram rendering | sibling file, lazy — loaded on first ` ```mermaid ` fence |
| `CodeMirror` | 5.65.21 | MIT | 393 KB | Optional editor with Markdown highlighting | deferred, opt-in |
| `pdf-lib` | 1.17.1 | MIT | — | One-click raster PDF path (§7.3) | deferred, opt-in |
| `html2canvas` | 1.4.1 | MIT | — | Card → canvas for the same path | deferred, opt-in |

Mermaid at 5.4 MiB is why it is a sibling file and not inlined. Inlining it would produce a 5 MB HTML
document, and the spec's own file budget (§9) forbids that. Lazy loading means a deck with no diagrams
never downloads Mermaid at all.

The dual-licensed DOMPurify contributes under Apache-2.0, which is MIT-compatible in the direction that
matters here (its code is used unmodified and its notices are kept).

No GPL, AGPL or source-available code is linked or bundled. If Pandoc is ever offered as a fallback
exporter it must be a user-installed CLI invoked as a separate process — never bundled, never linked.

---

## 3. Deployment shape

```
janalogy.com  ──►  GitHub Pages, user-site repo `rjanardan` (custom domain binds to it)
                   │
                   └── apps/
                       ├── soc-dashboard.html        (existing)
                       ├── system-design-path.html   (existing)
                       ├── md2slides/
                       │   ├── index.html            the app          → /apps/md2slides/
                       │   ├── SPEC.md               this document
                       │   ├── SPEC-LLM.md           deck-writing rules for an LLM
                       │   └── examples/             worked decks
                       └── markdown-cards/
                           └── index.html            redirect stub   → /apps/md2slides/
```

The custom domain is served only by the user-site repo, so the app must live inside it. A separate
project repository would serve at `rjanardan.github.io/md2slides/` and never under `janalogy.com`.
The folder form (`…/md2slides/index.html`) is chosen over the flat form (`…/md2slides.html`) because
the spec, the deck-writing rules and the example decks sit beside the app and tests can join them.
URL: `https://janalogy.com/apps/md2slides/`. The previous path, `/apps/markdown-cards/`, keeps a
two-line redirect page, so links already shared resolve instead of 404ing.

Consequences of having no server:

- No accounts, no login, no cross-device sync, no telemetry. What the visitor writes stays in their browser.
- The app is static files. `git push` is the entire deployment.
- Cost of operation is zero and there is no backend to secure.

---

## 4. Data model

Two storage tiers, because localStorage has a hard per-origin budget shared with the other apps on
`janalogy.com` and images would blow through it.

### 4.1 Decks and settings — localStorage

**Shipped reality (2026-09-17):** the live app keeps **one** JSON document under
`janalogy.mdcards.v2` — `{ v:1, md, geometry, at }` — debounced 250 ms on every edit.
It reads `janalogy.mdcards.v1` once as a one-time migration, then writes only v2. The
pane-divider width sits separately in `janalogy.mdcards.split`. The sketch below (a
multi-deck library plus a `…settings.v1` key) is roadmap, not this build.

```
key  janalogy.mdcards.v1            one JSON document, the whole library
{
  "schema": 1,
  "updatedAt": "2026-09-13T05:40:00Z",
  "activeDeckId": "d_7f3a",
  "decks": [
    { "id": "d_7f3a", "title": "Q4 platform review",
      "markdown": "---\ntitle: …\n---\n\n# …",
      "geometry": "16:9",
      "createdAt": "…", "updatedAt": "…" }
  ]
}

key  janalogy.mdcards.settings.v1   theme, last geometry profile, rawHtml flag, editor mode
```

Rules, applied because this is a shared origin:

- Writes are debounced (~400 ms) and whole-document, never per-field key sprawl.
- The key is versioned. A `schema` bump migrates on read and writes back under the same key.
- The key name still reads `mdcards`, not `md2slides`. It is deliberately unchanged: a deploy that
  renamed it would silently hide every deck saved under the old name.
- The app never seeds sample content containing a person's name, date or venue. First run creates one
  empty deck with a placeholder title card. Nothing personal ships in the file.
- If `JSON.parse` fails, the app does **not** overwrite. It moves the unreadable string to
  `janalogy.mdcards.v1.corrupt.<timestamp>`, shows a banner offering the raw text for download, and
  starts a fresh document. Silent data loss is the one unacceptable failure.
- If `setItem` throws (quota), the app surfaces a persistent banner: storage full, export now. It does
  not retry in a loop.
- The other apps on this origin (`apps/jobs/`, the agenda) share the same ~5 MB localStorage budget.
  This app keeps its document under 1 MB by putting images elsewhere, and warns when the deck document
  passes 512 KB.

### 4.2 Images — IndexedDB

Database `mdcards`, object store `assets`, key = lowercase hex SHA-256 of the bytes. Markdown references
them as `img://<hash>`. Pasted or dropped images go to IndexedDB; URL-referenced images (`![](https://…)`)
stay URLs and touch no storage.

The portability cost is real and must be visible in the UI: an `img://` reference means nothing to
another tool. So:

- Every export names unresolved references. PDF renders them (assets are resolved at render time);
  `.md` export offers "inline images as data URLs" so the file travels whole.
- The editor marks `img://` links with a distinct style and a tooltip: local asset, not portable.

### 4.3 What durable means

localStorage is a cache, not a record. Browsers evict it under pressure, clearing site data destroys it,
and a private window discards it. The spec therefore treats **export as the save button**, and the UI
says so once per session, not on every keystroke: a quiet line near the export control —
"Your notes live in this browser. Export to keep them."

---

## 5. Markdown dialect

The dialect is deliberately small. Anything not listed is passed through as text or plainly ignored,
and nothing in it is invented that Marp cannot also read (see §10).

### 5.1 Deck frontmatter

```markdown
---
title: Deck title                           # mandatory for a titled deck
author: Author name                        # optional
date: YYYY-MM-DD                           # optional
venue: Venue or event name                 # optional
geometry: 16:9                             # optional; 16:9 | 1:1 | 4:5
closing: auto                              # optional; auto | none | free text
---
```

`title` is mandatory for a *deck*; a deck without it is allowed to exist as an untitled draft, and the
export warns. `author`, `date`, `venue` are optional and simply omitted from the rendered title card
when absent — no empty placeholders, no stray separators.

### 5.2 Cards

The first card is generated from frontmatter, never typed by hand. Then:

```markdown
# Slide title          →  starts a new card, and is the card's title
- a bullet
1. a numbered point
```

Every `#` heading starts a card. The document text before the first `#` is the title card's optional
subtitle line. `##` and deeper do not split cards; they render as sub-headings inside one.

The last `#` block is the closing card when `closing` is not `none`; with `closing: auto` the app
generates it from frontmatter plus any `links:` list, so the author does not retype what is already
written once at the top. This is the decided default.

Both bookends are furniture-free. Neither the title card nor the closing card carries a footer, and
the title card carries no eyebrow or kicker label either — its first element is the title heading. The
footer — deck title on the left, `n / m` on the right — appears on content cards only, and `m` counts the title
card plus the content cards, so the last content card reads `m / m` and no page number refers to a
bookend. With `closing: none` the last `#` block is an ordinary content card, it is numbered, and the
total includes it.

`---` on its own line is accepted as a compatibility alias for a card break, so a Marp or Slidev deck
can be opened without editing. It never appears in this app's own output, which keeps round-trips clean.

### 5.3 Content

| Content | Syntax | Slideshow | PDF |
|---|---|---|---|
| plain text | paragraphs | yes | vector text |
| bullets | `- item` | yes | vector |
| numbered | `1. item` | yes | vector |
| image by URL | `![alt](https://…)` | yes | embedded raster |
| image pasted | drop or paste → `img://<hash>` | yes | embedded raster |
| link | `[text](url)` | yes | text; clickable after download |
| code | fence or inline backticks | yes, monospace, no wrap-breaking | vector |
| Mermaid | ` ```mermaid ` fence | rendered SVG | vector where the exporter allows |

Ordered lists preserve their start number, and nested bullets indent one level per two spaces.

### 5.4 What is excluded, and why

- **Raw HTML is off by default.** When the visitor turns it on, content is sanitised through DOMPurify
  with a small allowlist. A notes app that renders pasted HTML unsanitised is an XSS delivery vehicle
  for whoever pastes the note into someone else's browser.
- **No scripting in cards, no `javascript:` URLs.** Link hrefs are scheme-checked at render time.
- **No animation.** Mermaid diagrams render static because LinkedIn flattens animations anyway (§1.3),
  and a slideshow that moves is harder to read than one that does not.
- **No LaTeX in v1.** KaTeX is another 300 KB and no requirement asks for it. Left as an open decision.

---

## 6. Geometry

Three profiles, in CSS pixels at 96 dpi, with the exact page boxes the PDF export must produce.

| Profile | Card | Inches | PDF page (72 pt/in) | Use |
|---|---|---|---|---|
| `16:9` | 1920 × 1080 px | 20.0000 × 11.2500 in | 1440.0 × 810.0 pt | slideshow |
| `1:1` | 1080 × 1080 px | 11.2500 × 11.2500 in | 810.0 × 810.0 pt | LinkedIn carousel |
| `4:5` | 1080 × 1350 px | 11.2500 × 14.0625 in | 810.0 × 1012.5 pt | LinkedIn carousel |

`16:9` is the default. Cards render at `1920 × 1080` CSS pixels in a container scaled with a CSS
`transform` to fit the pane, so the internal layout is resolution-independent and the preview is the
same layout the PDF prints.

Geometry resolves in one order, each level overriding the one before it: deck frontmatter, then a
per-card override, then the export-time profile. Concretely — the deck declares `geometry: 16:9`; a card
may carry `<!-- card: 4:5 -->` as its first line; the export dialog can force one profile across every
card. Forced export is the path that satisfies LinkedIn, because it guarantees uniform page sizes
within the file.

Typography is declared in `em` against a root size, so the same card content lays out proportionally at
all three profiles rather than reflowing differently. Two anchors set that root, and they are not the
same measure:

- **Reading text** — body, bullets, quotes, code, footers — is a fraction of card **width**:
  **2.25 % at 16:9 and 4 % at 1:1 and 4:5, all 43.2 px.** v2 (2026-09-17) raised 16:9 from
  1.8 % (34.56 px) so slides read at the same size as the carousels. A square or portrait card is
  consumed fitted to a phone's width, so width — not height — decides whether it can be read.
- The **`h1`** is a fraction of card **height** (3.2 % × 1.72 em), so it keeps its original size in
  every profile instead of growing when the reading ramp does.

Measured on a 390 px phone, at 1:1: body text 14.8 px and heading 20.4 px, against 7.5 px and 12.8 px
before the anchors were split.

---

## 7. Export

### 7.1 Markdown

Round-trip is the correctness test: parse → model → serialise must return the input, normalised only for
trailing whitespace and a final newline. Frontmatter is written back with the same keys in the same
order. Assets are either left as `img://` (default, honest) or inlined as data URLs (opt-in, portable).

### 7.2 PDF, path A — browser print, exact page box

The default path, and it needs no library at all. A print stylesheet sets the page box from the profile
and one card per page:

```css
@page { size: 1080px 1350px; margin: 0; }      /* lengths, never the landscape/portrait keywords */
.card { width: 1080px; height: 1350px; break-after: page; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
```

Support, from MDN browser-compat-data (read 2026-09-13): `@page { size: <length> }` is Chrome 15+,
Firefox 95+, Safari 18.2+. caniuse's `css-paged-media` data currently flags no browser version for the
feature at all — its only note concerns `marks` and `bleed`, which no engine implements. The app emits
the `size` value as two lengths (`1920px 1080px`) rather than the `landscape`/`portrait` keywords: with
the exact box already known, the keywords add nothing, and a length is the form the compat data covers
for all three engines.

Output is vector: real selectable text, KB-sized files, and a MediaBox that matches the table in §6
exactly. The cost is one dialog step — the visitor picks "Save as PDF" and confirms margins are set to
None. The app shows a three-line instruction at the moment of export, because a `.pdf` that came out at
A4 is the most likely way a visitor concludes the app is broken.

`print-color-adjust: exact` matters here: without it, Chrome drops dark fills and the cards print as
outlines. It is unprefixed from Chrome 136, Firefox 97, Safari 15.4; `-webkit-print-color-adjust` is
supported alongside it in Chrome and Safari, so both declarations ship.

`@page` margin boxes — the printer's own page furniture — are deliberately not part of v1. They are
Chrome 131+ only (Firefox and Safari: no support), and a page number that appears on Chrome and
silently vanishes on Safari is worse than no page number. This is a decision about the margin box, not
about the footer in §5.2: that footer is card content, it is inside the page box, and it prints
identically in every engine.

### 7.3 PDF, path B — one-click raster, optional

For visitors who will not use a dialog: render each card to a canvas (`html2canvas`), embed the raster
with `pdf-lib` at the exact page box from §6, download the file. Both libraries MIT, both loaded only
when this path is chosen.

Honest trade-offs, to be shown in the UI next to the button:

| | Path A (print) | Path B (raster) |
|---|---|---|
| Steps | dialog, pick Save as PDF | one click |
| Text | vector, selectable, searchable | image of text |
| File size | tens of KB per card | ~1–3 MB per card at 2× |
| Fidelity | exact — same DOM | near-exact; canvas rasterisers differ on shadows, filters, some gradients |
| Mermaid | vector | raster |

Path A is the default and the one the acceptance tests assert on. Path B exists because friction is a
requirement in §a, and it is opt-in because its output is worse.

### 7.4 Export ranges

Whole deck in the current profile (default) · one profile per file, which is what a LinkedIn carousel
needs · current card only · card ranges (`3-7`). Multi-profile export produces one file per profile,
since LinkedIn rejects a PDF with mixed page sizes.

---

## 8. Interface

```
┌────────────────────────────┬──────────────────────────────┬──────────────┐
│  Markdown input pane       │  Card preview pane           │  Card rail   │
│                            │                              │              │
│  ---                       │  ┌────────────────────────┐  │  ▢ Title     │
│  title: Deck title         │  │  Deck title            │  │  ▣ Scale     │
│  author: Author name       │  │  Author name           │  │  ▢ Cost      │
│  ---                       │  │  YYYY-MM-DD · Venue     │  │  ▢ Close     │
│                            │  └────────────────────────┘  │              │
│  # Scale                   │   ← card 2 of 7 →            │  + new card  │
│  - bullets                 │                              │              │
│  1. numbers                │  [ Edit | Slideshow ]        │  geometry    │
│  ```mermaid …```           │                              │  16:9 1:1 4:5│
├────────────────────────────┴──────────────────────────────┴──────────────┤
│  Export:  .md   PDF            Notes live in this browser — export to keep │
└──────────────────────────────────────────────────────────────────────────┘
```

### 8.1 Synchronisation, the part that carries the product

The two panes are separated by a **draggable divider** — the preview pane resizes (clamped 20–72 %,
remembered in `janalogy.mdcards.split`, hidden below 900 px). The toolbar carries an **Examples ▾**
menu (All features, Markdown tutorial, capabilities, llms.txt carousel, starter — embedded, so they
load offline) and an **Open .md…** button.

- Typing a new `#` heading creates a card immediately and switches the preview to it, before the author
  types the title. Perceived as instant: the preview shows an empty styled card with the caret in place.
- Moving the caret into an existing card switches the preview to that card within one frame.
- Moving the selection in the card rail moves the caret in the input pane to that card's `#` line and
  scrolls it into view. The link is bidirectional.
- Preview scroll position never resets on a card switch; each card keeps its own.

### 8.2 Slideshow

The Slideshow button — or `s` — enters fullscreen with one card filling the viewport at the profile's
aspect ratio; `S` starts from the first slide. `←`/`→`, `Space`, `PageUp/Down` and the ‹ / › buttons move
and **never wrap** past the first or last slide. Digit keys buffer the number shown on screen and jump
to that slide after 500 ms. `/` opens a **live search** over every title, bullet, paragraph, code fence
and diagram, with slide numbers, navigated by `↑`/`↓`/`Enter`. `z` toggles zen (both panes, chrome
hidden, full screen), `v` toggles slides-only, `f` plain fullscreen; swipe left/right on touch screens
navigates. `Esc` exits. The card shown in slideshow is the same DOM node the preview renders — not a
re-render with a different font stack. This is the property that makes preview, slideshow and PDF
agree, and it is tested (§10).

### 8.3 Braindump mode

Because §a is the point of the app. A capture mode opens a bare textarea with no preview, no rail, no
chrome; `Enter` twice ends a thought and starts a new line, `Cmd/Ctrl+Enter` appends the buffer to the
deck as new `#` blocks (one per blank-line-separated thought). The buffer survives a reload — it is
written to `sessionStorage` on every keystroke pause, so a closed tab does not cost the author their
thoughts. This is the only place in the app where notes are not immediately cards.

---

## 9. Budgets

| Budget | Target | Why |
|---|---|---|
| App payload (HTML + JS + CSS, no Mermaid) | ≤ 150 KB minified, ≤ 45 KB gzip | must feel instant on a mid-range Android phone |
| Mermaid | lazy, first diagram only | 5.4 MiB is not a page load |
| Renderer | one, unchanged | preview = slideshow = PDF is a structural property, not a hope |
| Time to interactive | < 1 s on an M1, < 2.5 s on a mid-range phone | braindump means the caret is ready before the thought finishes |
| localStorage document | warn past 512 KB | shared origin budget is ~5 MB with the other apps |
| Reading text at phone width | ≥ 4 % of card width (≥ 14 px on a 360–414 px phone) | square and portrait cards are read fitted to a phone's width, so this is the size that decides legibility |
| No build step | required | the app is edited and deployed as source; a bundler would make the deliverable unmaintainable by one person |

Vanilla ES modules, no framework. A framework's re-render model is a liability for the sync behaviour in
§8.1 and for the DOM identity that makes export exact.

---

## 10. Acceptance criteria

Every criterion is checked by a script, not by eye. The harness is headless Chromium over the DevTools
Protocol, already proven in earlier work on this machine; page-box assertions read the PDF's `/MediaBox`
with `pypdf`.

| # | Criterion | Assertion |
|---|---|---|
| A1 | `#` starts a card | 7 `#` headings → 7 cards, titles equal to the heading text |
| A2 | Title card from frontmatter | rendered title card equals frontmatter; absent fields leave no separator or placeholder |
| A3 | `---` compatibility | a Marp-style deck parses to the same card count as its `#` equivalent |
| A4 | Markdown round-trip | parse → serialise → parse is byte-stable after normalisation |
| A5 | Card content renders | text, image, link, code and Mermaid each appear in preview and slideshow |
| A6 | Mermaid in slideshow | the diagram is an `<svg>` in the slideshow DOM |
| A7 | Mermaid survives export as vector | the Mermaid card's PDF page contains no image XObject |
| A8 | Exact page box | a 6-card deck at `4:5` prints a 6-page PDF, every page `/MediaBox [0 0 810 1013.04]`. The literal `1012.5` is unreachable: Chrome quantises the page box to hundredths of an inch, so 1350 px (14.0625 in) prints as 14.07 in. Assert the measured box, and keep every `@page` length in whole hundredths of an inch |
| A9 | Uniform page size | a mixed-geometry deck exported per profile yields PDFs with one page size each |
| A10 | Page count | PDF page count equals card count |
| A11 | Sync on typing | inserting `#` at the end of a card adds a card and switches the preview within one frame |
| A12 | Sync on caret | moving the caret between cards switches the preview; the rail selection follows |
| A13 | Persistence | reload restores decks, active deck, geometry and caret card |
| A14 | Corrupt storage | a corrupted document is preserved aside, never overwritten, and the app still starts |
| A15 | Quota failure | a full localStorage surfaces the export-now banner and does not loop |
| A16 | No unsanitised HTML | raw HTML stays inert with the flag off; with the flag on, `<script>` and `javascript:` hrefs are removed |
| A17 | Link scheme | `javascript:` and `data:` hrefs are not clickable in preview or slideshow |
| A18 | Portability | a fixture deck using only frontmatter, `---`, bullets and code fences renders equivalently under Marp |
| A19 | Bookends carry no footer | title card and closing card contain no footer node; every content card does; the last content card's footer reads `n / n` |
| A20 | Bookends carry no furniture | the title card contains no kicker, eyebrow or label node; its first child is the `h1` |
| A21 | Reading type fits a phone | at 1:1 and 4:5 the reading size is ≥ 4 % of card width, so a card fitted to a 390 px viewport renders body text at ≥ 14 px; the `h1` keeps its height-relative share (8 % for a title, 5.5 % for a card heading) in all three profiles |
| A22 | Fence-only body uses more of the card | a card whose body is a single code fence is capped at 60 % of the body box, not 46 % |
| A23 | Phone preview fits by width | below 900 px the stage fits the card to the pane width and the pane scrolls, so a 1:1 card renders 370 px wide on a 390 px viewport instead of shrinking to fit the pane height |
| A24 | Two-column slide | a card with two `##` renders 2 columns (`.cols`); one `##`, or `##` inside a code fence, renders as a normal card |
| A25 | Full-deck slide search | `/` in slideshow lists matching titles, bullets, paragraphs, code fences and Mermaid source with their slide numbers; `/` in edit mode does nothing |
| A26 | Resizable panes | dragging the divider changes `--split` (clamped 20–72 %) and persists to `janalogy.mdcards.split`; the divider is hidden below 900 px |
| A27 | No-wrap navigation | `←`/`→`, `Space`, PageUp/Down, the ‹ / › buttons and swipe stop at the first and last slide instead of circling |
| A28 | Default deck | a fresh load with no saved state opens the superset "All features" starter (10 cards, zero overflow) |

A16–A17 are the security gate; A18 is the exit gate. A19 records the closing-card decision: both
bookends — title and closing — carry no footer, so no page number refers to a card that is not a page
of content. A8's literal was corrected against measurement on 2026-09-13. If a user can leave this tool for Marp without
rewriting their deck, the format is honest rather than a trap.

---

## 11. Build order

Each step ends at a state that can be pushed to `janalogy.com` and used that day.

| Step | Deliverable | Ends when |
|---|---|---|
| P0 | Parser, card model, `.md` round-trip, headless test harness | A1–A4 pass |
| P1 | Split pane, caret/H1 sync, card rail, geometry switch, localStorage | A11–A15 pass |
| P2 | Slideshow mode, fullscreen, keyboard, presenter aid | A5, A6 pass |
| P3 | Print stylesheet, PDF path A, per-profile export | A7–A10, A18 pass |
| P4 | Braindump capture mode, sessionStorage buffer, first-run experience | usable as a notes app, not just a deck tool |
| P5 | Vendored Mermaid, lazy load, sanitisation, asset store | A16, A17 pass |
| P6 | One-click raster PDF (path B), download-the-deck as `.md` bundle | friction removed for non-technical visitors |

P0 and P1 are the whole product. Everything after them is the same model seen from different angles, so
the tempting order — build the slideshow first because it is the visible part — is the wrong one: a
slideshow over a parser that splits on the wrong character is a rewrite.

---

## 12. Open decisions

Not answered by the brief; each needs the owner's call before or during P1.

1. **Folder or flat file.** Settled in the rename: `apps/md2slides/index.html` plus its spec and
   examples. The flat `apps/md2slides.html` remains possible (it would match `soc-dashboard.html` and
   `system-design-path.html`), at the cost of losing the sibling documents.
2. **Name.** Decided 2026-09-14: **md2slides**. The folder was renamed from `markdown-cards`, and
   `/apps/markdown-cards/` keeps a redirect stub so the old link still resolves. Earlier candidates
   (`deckmd`, `mddeck`, `notecards-md`, `cardmine`, `slidecake`) were all unclaimed on npm and on this
   GitHub account, and were not taken.
3. **Mermaid delivery.** Shipped in v2: pinned CDN (`cdn.jsdelivr.net/npm/mermaid@11`, loaded by
   runtime `import()` lazily on the first diagram). A vendored sibling file (offline, no third party)
   and inlining (rejected, ~5.4 MiB HTML) remain open if offline support is ever wanted.
4. **Editor.** Plain textarea with a highlight overlay (P1, zero dependencies) and/or vendored
   CodeMirror 5 (393 KB, Markdown highlighting, folding). The brief's examples are all handled by a
   textarea; CodeMirror is comfort, not capability.
5. **Images.** IndexedDB with `img://` references (recommended, keeps the document small) versus data
   URLs inline (self-contained `.md`, bloats the shared localStorage budget).
6. **Path B raster PDF.** Ship as an option, or wait until someone actually refuses the dialog.
7. **`##` split.** Partially shipped (v2): two `##` under one `#` render as a two-column grid
   (`twoCols()`, fence-aware); three or more `##` stay a normal card. Multi-level `#` splitting is
   still not offered.
8. **LaTeX.** Not in v1. KaTeX adds ~300 KB for content no requirement asks for.

---

## 13. References

Read live on 2026-09-13. Each entry states the one claim it supports.

| Source | Supports |
|---|---|
| `linkedin.com/help/lms/answer/a493903` | 100 MB / 300 pages; PDF-only for lead gen; animations flatten to static; hyperlinks clickable only after download; multi-layer PDFs flattened; **multiple page sizes must be unified** |
| `github.com/mdn/browser-compat-data` — `css/at-rules/page.json` | `@page size`: Chrome 15, Firefox 95, Safari 18.2. No `landscape`/`portrait` sub-key exists in the data, hence §7.2 emitting lengths |
| `github.com/mdn/browser-compat-data` — `css/properties/print-color-adjust.json` | `print-color-adjust`: Chrome 136, Firefox 97, Safari 15.4 unprefixed; `-webkit-` prefixed in Chrome and Safari |
| `github.com/Fyrd/caniuse` — `features-json/css-paged-media.json` | no browser version currently flagged for the feature; the only note concerns `marks`/`bleed` |
| `github.com/marp-team/marp-core/blob/main/src/size/size.ts` | `size` is registered as a **global** directive — gap 1 |
| `github.com/slidevjs/slidev/blob/main/docs/custom/config/index.md` | `aspectRatio`/`canvasWidth` are headmatter-only — gap 1 |
| `marpit.marp.app/directives` | `headingDivider` follows Pandoc's `--slide-level` and is off by default — gap 2 |
| `github.com/arpitbbhayani/deckrun/blob/main/src/parser.ts` | splits only on `/^[ \t]*---[ \t]*$/` — gap 2 |
| `github.com/electron/electron/blob/main/docs/api/web-contents.md` | `printToPDF` returns a `Buffer`; the `landscape` option is ignored when `@page` is present |
| `github.com/tauri-apps/tauri` — README | TAO + WRY, per-OS system webviews, Apache-2.0; the official plugin set has no print or PDF plugin |
| npm registry + jsDelivr CDN | dependency versions, licences and distributed sizes in §2 |

The Tauri and Electron rows are recorded because they were evaluated and rejected, not because they are
planned. A hosted page already sits in a browser: the browser is the shell, `Ctrl/Cmd-P` is the PDF
engine, and a desktop wrapper would add an install step to an app whose first requirement is that a
thought can be captured without ceremony.

---

## 14. Non-goals

- Multi-user collaboration, comments, or shared decks.
- Accounts, sync, or any server-side storage.
- PPTX export. Marp's PPTX path is a raster-and-wrap trick; a PDF is more honest.
- A general-purpose Markdown editor. The dialect in §5 is the whole contract.
- Templating beyond the title and closing cards. A theme gallery is a different product.
