# Knowledge — what the Hermes record shows he knows, and what he is acquiring

**Source** `~/.hermes/state.db` on the Mac mini, 2026-08-22 → 2026-09-13. Hermes conversations only.
**Method** "Established" means he used the knowledge correctly without being taught it in the session. "Acquiring" means he asked to be taught, or tested a claim he was unsure of. Claims he explicitly asked to have validated are marked as such.
**Standing caveat** One dimension. This measures what surfaced in three weeks of chat, which is a fraction of what any experienced engineer knows. Absence here is not absence of knowledge.

---

## Established — used competently, unprompted

### Local inference operations

He knows the practical envelope of running models on constrained hardware. He installed Ollama and LM Studio, chose `qwen3:4b` as the local default, and asked for benchmark evidence rather than taking a recommendation on faith. He understands the levers well enough to specify them: quantisation (Q4_K_M), context length, token-generation rate, and the difference between prompt and generation throughput. He also knows the ceilings — the record notes qwen3:4b degrading to roughly 1 tok/s at 32K context against 19.5 at 8K, and disk at 92 per cent on an 8 GB machine.

### Model-selection economics

He runs a deliberate tiering rather than a single default: local models for bounded tasks and private data, subscription frontier models inside monthly limits, paid API where quality justifies it. He reasoned about task-to-model fit explicitly and asked for a first and second choice per task. When DeepSeek aliased version 4.1 over 4.0, his immediate instinct was cost control — how to pin the cheaper version.

### Emacs and Org-mode, at configuration depth

Three weeks of sustained work in `init.el` and `lisp/`. He configures deft, org-capture templates, `file+olp+datetree` capture targets, TODO keyword sequences including a custom `PROJ` state, SCHEDULED times and durations, and active versus inactive timestamps. He diagnosed a genuine upstream `file-notify` race in auto-revert and chose the polling fix over the alternative. He separates the concerns correctly: notes in `notes/`, journal entries in `journal/`, recurring items in the diary, tasks in a single `TODO.org`.

### Git and multi-machine discipline

He runs the same repositories from several machines and knows the failure modes. "GitHub is the master and latest now. But, check and ensure local version doesn't have changes which might be overwritten. Do a proper comparision" (2026-09-02, `20260902_231248_9a5817`). Fetch before push, rebase rather than force, fast-forward-only pulls, and treat a stale clone as a hazard rather than a convenience.

### Knowledge representation and formats

He can hold a distinctions-level discussion of taxonomy, ontology and format standards, and he reads specifications rather than summaries — the OKF v0.2 spec was read in full at 1,006 lines during the knowledge-formats work. He tracks the difference between interchange and selection as separate problems in knowledge systems.

### Web and front-end engineering

TypeScript, Node.js, Angular and the browser platform are treated as baseline throughout: nine content JSON files authored against a shared schema, a scenario explorer with SVG and Mermaid rendering, responsive layouts tested at nine widths, keyboard-shortcut systems, and localStorage persistence.

### Publishing mechanics

He knows how GitHub Pages publishing actually behaves: that a custom domain binds to one repository, that Pages rebuilds take tens of seconds, that an untracked file can block a rebase, that a personal access token in a page means a client-side secret.

---

## Acquiring — asked to be taught, or tested deliberately

### System design, as interview material

A focused thread from 2026-08-28 to 2026-08-29: publisher/topic/partition/consumer semantics, where Flink sits relative to Kafka, the DIKW hierarchy and where stream processing belongs in it, and why a control path is called a control path. He was reading his own book and asking why a specific heuristic used division by ten — checking the material, not just the topic.

### GraphQL

Declared himself new to it and asked to be taught through a worked HTML/CSS/JavaScript example (2026-08-22).

### Agentic AI, as an interview subject

Two days of structured preparation (2026-09-11) on why 2023–2026 changed the calculus for agentic systems: constrained decoding making structured output an ordinary RPC, long-context usability as distinct from context length, and the trust arc customers travel when handing over autonomy.

### Neuro-symbolic methods

Added to his profile as a research area at 2026-09-09 — Pydantic for typed schemas, Prolog and Lisp for symbolic reasoning and grounding. Presented as a direction he is working in, with the profile asking what else the knowledge formats should say.

### Security domain and MSSP practice

Honest gap-recognition. Preparing for an AI-SOC startup discussion, he said plainly he lacks SOC and customer-facing experience and asked how to build the missing exposure, how to read a CISO's apprehensions about AI in their environment, and how to prepare for the pace of a booting startup.

### Emacs internals he had not used

Asked how journal and diary overlap (2026-08-30), how to restrict word completion globally, how to delete a deft buffer name in one keystroke, how to link one org file from the diary.

---

## Claims he asked to have attacked

A distinct knowledge behaviour: he brings a position and asks for it to be broken, not confirmed.

- "knowledge graphs are the thing of the past, I should rather look at new methods like embeddings and encoding… validate the statements and assumptions here" (2026-08-30, `20260830_100923_bc7135`). His own thesis is the semantic layer, so this was a test of his own direction.
- NeoSmith's Maestro technical report submitted for an explicit honesty assessment (2026-09-06, `20260906_103435_5e35bd`).
- MNP Canada and MNP Spark researched from reviews and public reporting before any salary estimate was accepted (2026-09-02).

---

## Where knowledge converts into artifacts

The record shows a consistent conversion path: a topic is studied, then a structured artifact is produced, then that artifact becomes evidence for something else.

| Knowledge area | Artifact produced | Used for |
|---|---|---|
| Local model behaviour | Ten-task benchmark suite with scored rubric; comparison page and JSON | Choosing a default local model; published as a study |
| Model lifecycle | Nine-scenario explorer, 282 cards, 409 sources | Teaching the training-and-serving stack to himself |
| Knowledge formats | A 117 KB guide plus a scored grounding experiment | Research base for papers, posts and interviews |
| Agentic AI engineering | A working job-discovery agent with telemetry | "Build System Architect skills to claim in interviews" |
| OKF specification | Two knowledge bundles with per-entity provenance | Graph, wiki and article production |

He named the purpose himself: the agentic system was built "to build System Architect skills to claim in interviews and showcase experience. Actually using is secondary purpose" (2026-09-09, id 21873). That is the sharpest available statement of how he relates building to knowing.

---

## Gaps he identified in his own knowledge

- Databases were missing entirely from his technology stack listing, which he caught himself: "I think databases is missing completely in my resume" (2026-09-09, id 20278).
- Data science tooling from his M.Tech specialisation was not represented in his stack listing and he asked whether it should be.
- Security operations and direct customer-facing or MSSP experience, as above.
