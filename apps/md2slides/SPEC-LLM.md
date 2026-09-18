# Deck authoring spec — for LLM writers

Rules for writing card decks that the tool at `apps/md2slides/index.html`
renders without editing. Written to be pasted into a model's context: hand the
model this file plus the topic, and it returns a deck that drops straight into
the Markdown pane.

Measured against the v2 build of 2026-09-17 (1556 lines) by reading the parser and
measuring rendered cards in headless Chrome. Every number in **Fit budgets** is a
measurement, not an estimate; re-measure if the tool's CSS changes.

Tool name in the UI: *md2slides*. v2 (2026-09-17) adds two authoring-relevant
features: a **two-column slide** under a single `#` heading (exactly two `##`
sub-headings), and a full-deck **search** (`/` in slideshow) that finds titles,
bullets, paragraphs, code fences and diagram source.

---

## 1. Output contract

- Return the deck and nothing else. No preamble, no explanation, no outer code
  fence, no "here is your deck".
- Plain text, UTF-8, LF newlines.
- The first line is either `---` (frontmatter) or the first `#` heading.
- One file = one deck.

## 2. File skeleton

```
---
title: <deck title — required for a good title card>
author: <optional>
date: <optional>
venue: <optional>
closing: auto
---

<one or two sentences of preamble: this becomes the title card's supporting text>

# <card heading>

- bullet
- bullet

# <card heading>

- bullet
```

## 3. Frontmatter

Optional, and only recognised as the very first line block. A single `---` line,
then `key: value` lines, then a closing `---` line.

| Key | Read by the tool | Notes |
|---|---|---|
| `title` | Title card heading; also the footer's left label on every content card | Falls back to `Untitled deck` |
| `author`, `date`, `venue` | Byline on the title card, joined with `·` | Omitted if absent |
| `closing` | `auto` (default) → the last `#` block becomes a centred closing card. `none` → no closing card; the last `#` block is an ordinary content card | Any other value behaves as `auto` |
| `geometry` | **Parsed but ignored in this build.** The toolbar's 16:9 / 1:1 / 4:5 control decides the export size | Do not rely on it; tell the human which profile to pick |

Key syntax is one line only: `key: value`. Values are plain text; surrounding
quotes are stripped. No nesting, no lists, no multi-line strings.

## 4. Card model

| Card | Comes from | Footer |
|---|---|---|
| Title | Frontmatter + every line before the first `#` | None |
| Content | Each line matching `^# ` | `n / total` |
| Closing | The **last** `#` block, when `closing` is not `none` | None |

Rules that follow from the parser:

- A `#` line starts a new card. Its text becomes that card's heading.
- A `#` **inside a fenced code block** does not start a card, so code samples may
  contain `#` comments freely.
- Page numbers count the title card and the content cards only. In a 6-card deck
  with a closing card, the content cards read `2 / 5` … `5 / 5`.
- Everything before the first `#` is the title card's supporting text, not a card.
  Write it as one or two short sentences.
- `##` and `###` inside a card render as card sub-headings. `####` and deeper all
  render at the `###` size.
- Indented `#` (e.g. `  # x`) does **not** start a card; only a `#` at column 1 does.
- A card whose body contains **exactly two `##` sub-headings** renders as a
  two-column grid; the `#` heading stays full-width above it. A third `##` (or a
  `##` inside a code fence) disables the split and the card renders normally.

## 5. Block syntax the tool understands

| Syntax | Renders as | Notes |
|---|---|---|
| `# Heading` | New card | Column 1 only |
| `## Heading` | Card sub-heading | `###`+ render smaller |
| `- item`, `* item`, `+ item` | Bullet list | One marker style per list |
| `1. item`, `1) item` | Numbered list | Switching style starts a new list |
| `> text` | Blockquote | One line per quote; consecutive `>` lines do not merge |
| ` ``` ` … ` ``` ` | Code block, verbatim | Optional language tag |
| ` ```mermaid ` | Diagram | Rendered in the preview and the PDF; needs network on first use, otherwise shows as code |
| `---`, `***`, `___` | Horizontal rule | A bare `---` in the body is a rule, not frontmatter |
| blank line | Paragraph break | — |
| two `##` under one `#` | Two-column grid | Need exactly two; `##` inside a code fence are ignored (fence-aware) |

**Line breaks are not preserved.** Consecutive non-blank lines are joined into a
single paragraph with spaces, so do not hand-wrap paragraphs. One paragraph per
blank-line-separated block.

## 6. Inline syntax the tool understands

| Syntax | Renders as | Notes |
|---|---|---|
| `**bold**` | Strong | — |
| `*em*`, `_em_` | Italic | Needs a space or `(` before the opening marker |
| `` `code` `` | Inline code | Protected from emphasis |
| `~~strike~~` | Strikethrough | — |
| `[text](https://url)` | Link | Only `http:`, `https:`, `mailto:`, `/`, `#` targets become links |
| `![alt](https://img)` | Image | Capped at 38% of card height |
| `![alt](https://img "title")` | Image with title | — |

## 7. Syntax that silently degrades

Emit none of these. They render as literal text or lose structure, with no error.

| Don't write | What happens |
|---|---|
| Markdown tables | Rendered as a paragraph of `|`-separated text |
| Nested / indented lists | Flattened into one list |
| `- [ ] task` | Bullet with a literal `[ ]` |
| `[text][1]` and `[1]: url` | Literal text; the link is lost |
| `[text](page.md)` | Label only — relative URLs do not become links |
| `Title` + `=====` (setext) | Plain paragraph |
| Footnotes `[^1]` | Literal text |
| Raw HTML (`<br>`, `<b>`, `<a>`) | Escaped and shown as visible tags |
| Autolinks `<https://x>` | Escaped and shown literally |
| Backslash escapes | The backslash is shown |
| Trailing two-space line break | Ignored |
| `<!-- card: 4:5 -->` per-card geometry | Not implemented; the comment is escaped and printed as visible text on the card |

## 8. Fit budgets

Type scale: reading text — body, bullets, quotes, code, footers — is **4% of the
card width** at 1:1 and 4:5, and **2.25% of the card width at 16:9**, which lands on
the same 43.2 px in every profile (v2 raised 16:9 from 34.56 px so slides read at
the same size as the carousels). Line height 1.45. The `h1` is **3.2% of the card
height** × 1.72 em (59.4 px on a 1080-tall card, 74.3 px on a 1350-tall card) and
keeps its original size in every geometry, so it stays well above the reading text.
Card padding is 7.5% of height and 7% of width.

| Geometry | Card | Text column | Body box | Line height | ≈ body lines | ≈ chars/line |
|---|---|---|---|---|---|---|
| 16:9 landscape | 1920 × 1080 | 1651 px | 729 px | 62.6 px | 11 | ~90 |
| 1:1 square | 1080 × 1080 | ~928 px | 715 px | 62.6 px | 11 | ~40 |
| 4:5 portrait | 1080 × 1350 | ~928 px | 912 px | 62.6 px | 14 | ~40 |

1:1 and 4:5 set the same reading size at the same width, so **the aspect ratio
decides how much text fits, not the prose style**: 4:5 is 25% taller and holds
about 25% more lines. v2 (2026-09-17) raised 16:9 to the same 43.2 px physical
size, so 16:9 now holds about as many lines as a 1:1 square rather than the 14
lines it held at the old 34.56 px type.

Measured capacity (headless Chrome, this build):

| Geometry | one-line bullets | ~100-character bullets | code lines |
|---|---|---|---|
| 16:9 | ~10 | ~5 | ~6 |
| 1:1 | 9 | 5 | 5 |
| 4:5 | 12 | 6 | 7 |

The 16:9 column was re-derived on 2026-09-17 from the new 62.6 px line height
(729 px body box → ~11 lines); it was previously measured at the old 34.56 px type.
The 1:1 and 4:5 columns still match the 43.2 px type they have always used.
Re-measure exact counts if you are authoring to the limit.

Working rules:

- Budget **10 rendered lines** per card at 1:1, **13** at 4:5, and **~11** at 16:9.
- Every bullet also costs about a third of a line in margins.
- Comfortable patterns at 1:1: four bullets of up to ~110 characters, or six of up
  to ~55 characters, or three bullets plus a short quote.
- **Code blocks: keep to 5 lines or fewer at 1:1, 7 at 4:5, ~6 at 16:9.** The code box
  is capped at 46% of the body box — 60% when the fence is the card's only content —
  and scrolls past that; the overflow is *not printed*. Keep code lines under
  ~60 characters to avoid horizontal scrolling.
- Sub-headings cost about two lines each.
- Images take up to 38% of the card height; budget about eight lines of text for one.
- Overflow is silent. Nothing warns you; the text is simply cut off in the PDF.

## 9. Writing rules

- One idea per card. If a card needs two headings, it is two cards.
- Card headings: a claim or a label, up to six words, sentence case, no trailing
  period. They are the largest text on the card.
- Title card: the title is the hook, not a description. The preamble is one or two
  sentences (up to ~240 characters) that make a claim and set up the deck.
- Bullets: aim for one line each, up to ~110 characters. No sub-bullets. Do not
  end every bullet with a period unless the bullets are full sentences.
- Stats: always name the source and the date inside the same bullet — "Ahrefs,
  June 2026: 137,210 domains." A number without a source is not usable.
- Quotes: at most one `>` per card, and keep it under one line.
- Two-column cards (two `##` + bullets) pair best at ~3 short bullets per column.
- Name things precisely — the `/` slideshow search indexes titles, bullets,
  paragraphs **and** the text inside code fences and diagrams, so a distinctive
  word makes a card findable.
- Closing card: one line, up to ~90 characters. No bullets. It is centred and
  carries no footer.
- No filler openings, no marketing adjectives, no rhetorical questions as
  headings, no "in today's fast-paced world", no summary-of-the-summary.
- Prefer concrete nouns and figures over abstractions: "84 of 62,100 requests"
  beats "very few requests".
- Do not repeat the deck title as the first card's heading.
- 6–10 cards is a typical length for a carousel; the tool itself sets no limit.

## 10. Self-check before returning a deck

1. First line is `---` (frontmatter present) or the first `#` heading.
2. Frontmatter keys are only `title`, `author`, `date`, `venue`, `closing`.
3. Card count = 1 title card + one per `#` line. The last `#` is the closing card.
4. No table, no nested list, no task list, no footnote, no reference link, no raw
   HTML, no autolink.
5. Every `*` or `_` emphasis marker is preceded by a space or `(`.
6. Every statistic has a source and a date in the same bullet.
7. No card exceeds ~10 rendered lines at 1:1 (13 at 4:5 and 16:9); no code block
   exceeds 5 lines at 1:1.
8. The deck ends with the closing card's single line — not with a call to action.
9. Output contains no commentary and no outer code fence.

## 11. Worked example

`examples/llms-txt-carousel.md` is a measured 8-card square deck: it fits at 1:1
and 4:5 with no overflow in any card, and exports as an 8-page, 810 × 810 pt PDF.

```
---
title: llms.txt is not the new robots.txt
geometry: 1:1
closing: auto
---

One file asks machines to leave. The other hands them a map. Twenty-eight percent of sites have shipped the second one — and 97% of those files went unread last May.

# The file from 1994

- `robots.txt` is a permission file. Martijn Koster wrote it in 1994; RFC 9309 finally standardised it in 2022.
- It tells crawlers what to skip: `Disallow: /drafts`, `Crawl-delay: 10`, where the sitemap lives.
- RFC 9309, §1: "These rules are not a form of access authorization." A request, not a lock.
- Its whole job is subtraction. It was never a way to be seen, and nobody pretended otherwise.
```

Other worked decks ship in `examples/`: `capabilities.md` (images, three diagram
types, a two-column slide) and `markdown-tutorial.md` (a beginner Markdown course).
The default starter deck on a fresh load is the superset "every feature in one deck".

## 12. Limits of this build

- `geometry:` in frontmatter does nothing; the toolbar chooses the export profile.
- Per-card geometry overrides (`<!-- card: 4:5 -->`) do not exist.
- `closing:` accepts `auto` or `none` only; free text after `closing:` is ignored.
- No table support, no nested lists, no footnotes, no citation notes.
- Overflow is silent in both the preview and the PDF.
- Two-column slides need exactly two `##` and none inside a code fence; a third
  `##` disables the split.
- The `/` search opens only in slideshow mode and reads the current editor text
  only — not a filesystem search, and it does not see decks on disk.
- Mermaid needs network access on first render; offline the fence stays visible as
  code with a note.
- The title card carries no kicker, eyebrow or label. The title heading is the first
  element on card 1, so anything you want above it has to be part of the title itself.
