# Interests — what the Hermes record shows him drawn to

**Source** `~/.hermes/state.db` on the Mac mini, 2026-08-22 → 2026-09-13. Hermes conversations only.
**Method** Interest is inferred from what he chose to spend time on unprompted, and from what he asked to have explained when no obligation required it. Work topics are included because in this record work and interest are not separable.
**Standing caveat** One dimension. Three weeks of chat under-represents anything he did not need a tool for.

---

## Technical subjects

### Agentic AI systems, built to enterprise shape

The dominant thread. Not the concept — the construction: routing, guardrails, evaluation, audit, cost control, observability, tool calling, context and memory management, multi-agent scaffolds. He asked for four or five candidate use cases, said he would pick the one that interested him, and then worked through requirements, architecture, building blocks, system design, wiring, implementation, testing, observability and troubleshooting as separate stages.

### Knowledge formats, representation and grounding

The thread he treats as his research home. Deep interest in Google Open Knowledge Format, specifically v0.1 and v0.2 and what the later version added in the way of trust signals. But the interest is broader: what counts as knowledge, how it is represented for humans versus agents, taxonomy and ontology vocabulary, which standards exist and which are de facto, and why interchange and selection are different problems. He built a 117 KB guide on the subject and then ran a scored experiment on it rather than stopping at the write-up.

### Neuro-symbolic AI

Listed as an active research area in his own words: typed schemas with Pydantic, symbolic reasoning and grounding with Prolog and Lisp. The pairing of neural and symbolic methods sits directly on his thesis question about the semantic layer.

### Small models and local intelligence

He is interested in small models specifically — not as a fallback but as an object of study. He benchmarked six then eight models on an 8 GB machine, asked for model cards, asked for vendor benchmarks checked against independent ones, asked what commercial deployments exist and what communities say about them, and ended with a question about fine-tuning versus knowledge-bundle grounding for "high risk and low cognitive tasks" in enterprises: cost, security, local data, latency.

### System design

Learning it deliberately as interview material and reading his own book critically while doing so. The specific fascinations in the record are partition and consumer semantics, where a stream processor belongs in the DIKW ladder, and the vocabulary of architecture — why a control path is called a control path.

### Evaluation methodology

A near-constant interest rather than a phase. Ten-task rubric suites, published benchmarks cross-checked against vendor claims, scored with-versus-without-bundle experiments, geometry assertions across nine viewports, belief statements submitted for falsification. He treats measurement as the interesting part of building.

### The toolchain that runs his life

Emacs and Org-mode receive more sustained attention than any single AI topic: capture templates, datetree structure, custom TODO states, agenda export to mobile, deft, auto-save timing, auto-revert internals, and a book written about the whole system. He is also interested in the ordering underneath it — tasks in one file, recurring items in the diary, journal entries by date, notes in their own tree.

---

## Intellectual sources and people he follows

Named in the record, mostly through the AI-ecosystem knowledge bundle he specified on 2026-09-10 and 2026-09-11:

- **Founders and researchers** asked for by name or added to the bundle: Demis Hassabis, Ilya Sutskever, Mira Murati and the OpenAI founding cohort, Andrej Karpathy, Yann LeCun, Dario Amodei, Greg Brockman, Amjad Masad, Daniel Gross, Don Valentine, Elon Musk, Durk Kingma, David Lee.
- **Investors**: NFDG, a16z, Sequoia, DST Global, SV Angel — named as entities whose portfolios he wants mapped.
- **Companies as objects of study**: Google, Meta, OpenAI, Anthropic, Alibaba, DeepSeek, Google DeepMind, SSI, Replit, Atlassian, GitHub, GitLab, Rally, and Y Combinator-funded startups founded around 2020 that became prominent after November 2022.
- **Sources he reads**: company engineering blogs, arXiv, and practitioner writing. One named non-technical read sits in the record — an artisanalgeek post on UX and sound, saved to his journal.
- **A near-miss in sourcing discipline**: he asked why Demis Hassabis leaving Google DeepMind had not been recorded in his own file. He reads his artifacts for what they are missing.

His own library, referenced as work in progress: a System Design book, an AI book, a Mermaid field guide, and a book on Emacs org-mode and diary.

---

## Work-as-interest, at the level of craft

- **Typography and layout.** He notices a heading with a trailing period, a paragraph rendered ten characters wide with the rest of the page empty, captions that spill into the next row, a first bullet numbered "01" three times. He asks for light themes, modest type scales, and diagrams that stay legible on a phone.
- **Keyboard-driven interfaces.** Single-key shortcuts with defined behaviour, distinction between lower and upper case, numeric jump with a half-second wait, zoom levels. This is an aesthetic, not a convenience.
- **Mermaid and diagram languages.** He found diagram-as-text compelling enough to commission an entire field guide on it, and he reaches for Mermaid first when visualising anything: flows, layers, timelines, comparisons.
- **Clean separation of concerns.** One file per concern, notes apart from journals, public artifacts from private, a public profile repo kept distinct from working files, contributions to one repository kept off another.
- **Diagrams as thinking tools.** A 4-layer architecture map, a left-to-right ecosystem timeline, a pipeline lifecycle, a decision tree per layer. He thinks in adjacency and flow.

---

## Community interest

The Bengaluru JavaScript Meetup, which he founded in 2015 and still runs. In the record he checks RSVPs for an event, harvests ten years of event photos, rebuilds the community page around a decade of history with attendance and venue data, and cross-links it to a wider communities page. The interest is archival as much as social — he wanted the ten-year record to exist.

---

## Reading, media and entertainment

The honest answer from this source: not present.

- **Films, series, music, games, sport, travel, food**: no mention anywhere in the Hermes record. Not dismissed — simply absent, because none of it needed a tool.
- **Books read for pleasure**: none. Books appear as something he writes.
- **Reading**: technical material, specifications, papers, company blogs, and one UX blog post.
- **Investments**: an interest in the sense that he labels emails and wants a weekly digest, with an explicit instruction to separate fact from opinion and no buy or sell advice. He asked about Dell's AI-server sales as market context for his own transition.

If a full interests picture matters, it has to come from sources that see the rest of the week — a different LLM's chat history, a photo library, a music service, a calendar. He is expected to merge exactly those.

---

## What the record says about how interest works for him

Interest and obligation are merged rather than balanced. The projects he chose to start with no requirement attached — a Ramayana ontology explorer, a model-lifecycle atlas, an OKF knowledge bundle about the AI ecosystem, a field guide to Mermaid — are all large, structured, and immediately useful to something else he is doing. The one genuine digression in the record, an overnight build he liked the look of, was still finished and QA'd the next morning.

He also named the cost of this. See the self-description in `soul-hermes-macmini.md`: creative thoughts pull him off plan, and he knows it.
