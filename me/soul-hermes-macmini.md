# SOUL — top priorities and what defines Janardan

**Source** Hermes conversations on the Mac mini only. `~/.hermes/state.db`, 2026-08-22 11:10 → 2026-09-13 00:21 IST.
**Basis** 143 sessions, 25,278 messages, of which 1,529 are Janardan's own non-cron messages. Tool traffic (13,084 rows) is used only as corroboration of what was built, never as evidence of character.
**Constraints applied** No web search, no external sources, no reading of pre-existing Emacs org-files. Everything below is reconstructed from the chat record.
**Standing caveat** This is one dimension of a multi-source portrait. It describes three weeks of behaviour, not a life. It is not a complete account and should not be treated as one.

---

## Coverage limits, stated up front

The Hermes record begins 2026-08-22, the day Hermes was installed on this machine. There is no multi-year Hermes history on the Mac mini, and no second message store on the disk. Where the record is silent, the silence is reported rather than filled.

---

## Stated priorities

Ranked by how often and how forcefully they appear in the record.

### 1. Work, treated as the organising principle of life

Stated once, plainly, when he asked for it to be written into `aboutme.md` (2026-09-07, session `20260907_124729_956d0f`, message id 14814):

> "My goal is to become AI expert who is sought out in Bengaluru/India for consulting and a CTO role. I want to spend my break from Dell Technologies to make my next 30 years of living life worth by working in AI and next generation technology. My measure of success is the money I make. I want to double my earning through salary and mostly stock, every 3 years. My target is 3 crores additional money added to my back account by 01 Dec 2029. Me and my family give me full freedom to work hard. Work is worship. All priority given to work."

Every subsequent activity in the record is consistent with this. The three weeks contain career positioning, a research-and-build programme, authoring, and community work — with no leisure thread of comparable weight.

### 2. Repositioning from large-vendor engineering to AI-first work

The record shows an active, time-boxed transition rather than a vague ambition. Evidence:
- Resumes re-cut for AI-first framing, with the Dell Director title kept factual and the surrounding language rebuilt (2026-09-06 → 09-07, session `20260906_152931_711851`).
- Explicit reach-out to startups: TrenchSecurity.ai, second discussion with founder Mayur (2026-09-08, `20260908_155145_af3ce1`); MNP Spark GCC researched with a salary band estimated (2026-09-02, `20260902_140458_4cccb8`).
- Deliberate avoidance of the "too senior, too old" filter: he asked to stop quoting "29 years total / 20 years leading", replace it with "More than 10 years…", and to mark the PhD as part-time so it does not read as a delivery risk (2026-09-04, `20260829_091604_84da08`).

### 3. Research identity — semantics in multi-agent communication

The PhD direction is stable across the three weeks: multi-agent system communication architectures with the semantic layer as the focus. See the startup-naming session (2026-08-30, `20260830_074425_55f3b4`) and the knowledge-graph-versus-embeddings argument he brought in to be tested against his own thesis (2026-08-30, `20260830_100923_bc7135`). He does not treat the thesis domain as fixed — he asks for his assumptions to be attacked.

### 4. Authorship and craft

Two book tracks run in parallel: *Mastering TypeScript* for BPB Publications (chapter 10 code reviewed 2026-09-10, `20260910_114607_b833fe`) and a series of self-published HTML field guides. Author integrity matters enough to be requested as a feature: a footnote crediting the author and naming the models involved (2026-08-22, id 946).

### 5. Community

Organiser of the Bengaluru JavaScript Meetup since 2015 (stated 2026-08-30, id 3709). On 2026-09-05 he checked RSVPs for that day's event, found 359 confirmed with zero waitlist, then harvested 346 photos across 47 albums and rebuilt the community page around them.

### 6. Family

Present but not described. The only family statement in the Hermes record is "Me and my family give me full freedom to work hard" (id 14814). A private-name list entered the record when he stripped personal data from a public book — Kavitha, Sailu, Niraj, and a family birthday on 23 August (2026-08-30, id 4739). No spouse, child, or parent is named as such anywhere in this record. Anything about those relationships comes from other sources, not from here.

---

## Operating ethos visible in the work itself

**Originality over idiom.** He objects to stock phrasing on sight: "Avoid typical AI slop and text… I don't like to be called AI-bot researcher" (2026-08-22, id 94), and a page line "How to read the result—not merely rank it" was rejected as slop in the same session (id 272). Copy-editing rules are absolute: headings never end with a period (id 129). These were added to memory on his instruction, not volunteered.

**Evidence before assertion.** He asks for the experiment, the score, the citation. When a claim cannot be supported he removes it — an unverified "17.9 GB BF16" figure was pulled before delivery during the small-model model-card work (2026-09-07, digest `20260908_121946_ca6748`).

**Cost is a design constraint.** He holds monthly subscriptions for frontier models, keeps local models for privacy and cost, and asks to be warned in advance when a repeated action will burn tokens (2026-09-09, id 21873). When an experiment stopped being worth DeepSeek credits, he stopped it mid-stream and said why: "I don't want to spend any more Deepseek credits for this. I can stop the experiment" (2026-09-07, `20260907_154646_cdc737`).

**Open source, with cloud for compute only.** Stated as a boundary rather than a preference: "I want to build using open source software, no proprietary; Only for GPU or LLMs, I can use cloud compute" (2026-09-08, id 17984).

**Delivery over decoration.** Repeated demand for layout that does not spill, text that is legible, and geometry that holds at mobile widths. Overlapping captions, 10-character-wide columns, and misplaced time slots were each reported and each fixed.

---

## Non-negotiables

- Ask first, suggest before editing. He says variants of this repeatedly: "First give me suggestions, before you do changes"; "you can only suggest, I edit each line manually"; "Only suggest me, where to add?" A large edit delivered without consent earned the sharpest line in the record: *"you screwed up royally; i didn't ask you to make a book"* (2026-09-02, `20260902_120901_badd30`).
- Never invent. What he did not say must not appear. Dates especially — instructions carry "Do not invent dates."
- Keep personal data out of public artifacts. When a book was headed for the open internet he ordered every personal name and event made generic, and the public/private split was restated as a rule (2026-08-30, id 4739; 2026-09-02, id 7239).
- Do not distort the record to win a role. When fitting a resume to a Lenovo job description: *"DO NOT completely make it 'fit' for the role. Keep my identify and experience"* (2026-09-02, id 7046).
- Verify before claiming. Push operations, HTTP responses, byte-identical regenerations, and rendered geometry are all checked against the live thing.

---

## The tension he named himself

The clearest self-description in the record is a complaint about his own working style (2026-08-30, id 4572):

> "I am very distracted with creative thoughts and don't achieve even one of the planned item. I am so unorganized, as I like to always do some creative and exploratory work."

He then asked for a planning system — half-hourly day slots, durations, a daily template — "for someone as unorganized as me". The three-week behaviour supports the diagnosis and the mitigation simultaneously: the output volume is high and the workstream count is even higher, and several threads were started and stopped inside the same day.

---

## What this file cannot tell you

Priorities only exist here as they were spoken aloud to a tool. Nothing in the Hermes record speaks to belief, ethics outside the working context, leisure, health, or the interior life of the family relationships named and unnamed above. Treat the absences as absences.
