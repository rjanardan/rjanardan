# Skills — conclusions drawn from the Hermes conversations

**Source** `~/.hermes/state.db` on the Mac mini, 2026-08-22 → 2026-09-13. Hermes conversations only.
**Method** Skills below are inferred from behaviour in the record — how he scoped work, corrected it, verified it, and what he refused — not from self-report. Each carries the evidence that produced the inference.
**Standing caveat** One dimension. A skill not visible in three weeks of chat may still be strong; a skill visible here may be overstated by the sample.

---

## Technical execution

### Specification before implementation

He front-loads the specification and resists being surprised by it. Agenda-page requirements were split into numbered clauses before any build; the mobile-export question was asked twice before the tool was trusted; conflicting asks were invited to the surface: "Any clarifications on requirements or conflicting asks I gave?" (2026-08-29, `20260829_000931_b1b7f5`). The clearest evidence that this is a skill rather than a habit is what happened when it was skipped: a delivered book against an unstated intent drew *"you screwed up royally; i didn't ask you to make a book… I wanted the central diagram to be the decision tree for each layer"* (2026-09-02). He has been consistent about the ordering ever since.

### Verification with a hard edge

He does not accept a claim of completion. Examples from the record: a page published to a custom domain was checked with an HTTP status from the live URL; regenerated output had to be byte-identical to the previous version, not merely similar; a photo gallery was geometry-checked at nine viewport widths from 1440 down to 320; a repo status line was rejected because a stray caret made the message look incomplete (2026-09-06, id 9172). He also verifies the negative — asking whether the sync script can see browser-made changes, and whether a mobile edit can round-trip.

### Diagnosing by instrument rather than by guess

Repeated pattern: capture the real artefact, then reason from it. A sync-panel error arrived as a screenshot and was resolved by OCR-ing it and reading the HTTP code. An errant status line was traced to a stale comment versus an actual interval. A blank graph was traced to a one-shot relayout rather than to the renderer. A stalled animation was diagnosed as an occluded automation window rather than an application bug. He supplies the instrument (a screenshot, a log dump, a terminal output) and expects the conclusion to follow from it.

### Parallel delegation

He will hand nine pieces of independent authoring to nine parallel subagents against one shared schema, as in the model-lifecycle content build, and separately commissioned nine parallel digest passes over a week of his own chat history. He understands the shape of the work: same contract, independent units, one integration step.

### Cost engineering

Token and credit economy is treated as an engineering constraint. He asks for advance warning when a repeated operation will burn tokens, chose a cheaper local path where quality allowed, stopped an experiment mid-stream when the cost stopped being justified, and asked how to pin an older, cheaper model version after a provider redirected aliases. This is a real skill and a rare one: most builders optimise quality alone.

### Multi-machine repository hygiene

Fetch before push, rebase rather than force, recover a blocked rebase rather than clobber it, and treat one repository as authoritative. He diagnosed and cleaned a 59-commit-stale duplicate clone, preserved divergent local work instead of discarding it, and rejected a push that would have published a scratch edit to a live public site.

---

## Cognitive and strategic

### Turning work into evidence

The strongest strategic skill in the record. Almost nothing is done for its own sake. The job tracker is also a portfolio artifact. The job-search agent's stated primary purpose is to claim system-architecture experience in interviews, with actual use secondary. The local-model study is framed as a formal design of experiments — hypothesis, execution, results, analysis, next questions — because it doubles as published research. The knowledge bundles are built with their downstream uses specified before the content is written: graph, wiki, article, whitepaper, JSON-LD, Q&A.

### Holding a portfolio of workstreams without losing them

Within one day he moved between Emacs configuration, a resume pass, a benchmark run, a portfolio deploy and a community page. Open threads are recalled and resumed across days — the Ramayana explorer built overnight was QA'd the next morning; a schema fix deferred in one session was raised in the next.

### Distinguishing an experiment from a commitment

He starts exploratory work deliberately and ends it deliberately. The Gemma figure-caption experiment was stopped with an explicit reason, not abandoned silently: "why is it such a big deal to get this python code write, is this highlighting the limitation of a small model like Gemma? I don't want to spend any more Deepseek credits for this. I can stop the experiment" (2026-09-07). Two wiki products — Flatnotes and Outline — were started and cancelled the same day when the cost of the detour became clear.

### Judging audiences separately

The same material is re-cut for different readers without being distorted. Public books get personal names removed; resumes keep the factual Dell title while the surrounding framing changes; the interview pitch is calibrated to a founder with a finance and strategy background rather than a technical one.

---

## Leadership and interpersonal style

### Delegating with a contract, not a vibe

Subagent briefs specify the schema, the output path, and the file to write. Integration is his job and he does it: the nine scenario JSON files were assembled and QA'd by him, with 409 sources carried through.

### Claiming only what survives inspection

He rejected a team-size figure of 120 in favour of 100 because a round number invites less scrutiny, kept the verifiable title even while softening the seniority around it, and refused to stretch a resume to a job description at the cost of accuracy. In a hiring conversation he treats overstatement as a liability, not a tactic.

### Taking the standard-setting role in a collaboration

He corrects the work, not the worker: names the exact defect, states the principle, then asks for the fix. Headings with periods, sloppy paragraphs, a miscounted bullet list, an unnamed column of text — each was reported precisely and generally, with a rule attached. His sharpest rebuke was reserved for scope violation rather than for quality.

### Relationship-building through usefulness

He asks for a contact and then asks what to do with it. A discussion with one contact yields a named referral to another; a research session on a company yields a salary band and a specific role. He asks what the other party needs — what the CISO fears, what the founder's strategy is, what a customer must be able to trust — before framing his own pitch.

### Teaching himself in public without pretending to be finished

He marks his own gaps in writing: new to GraphQL, databases missing from the stack, no SOC experience, no customer-facing experience. The record contains no instance of him claiming expertise he does not have, including in the material prepared for a company founder to read.

---

## Working style under load

Message timestamps across the three weeks cluster late: 23:00, 00:30, 01:20, 02:30, 03:11. A job-application batch was logged at 15:50–17:30 on one day and a ten-hour stretch of chat review ran the next. The scheduling tooling he built for himself has a half-hourly day grid precisely because he did not want to skip important slots. Whatever else this says, the record shows sustained effort at hours when most people stop.

---

## Skills that are asserted but not demonstrated here

- **Public speaking.** The panel and meetup talks are referenced as history, not shown.
- **Managing people day to day.** The enterprise record is asserted (teams of 2 to 100) and is consistent with how he delegates and reviews, but no direct management interaction occurs in this record.
- **Writing long-form prose solo.** The books exist; the drafting happens largely through the tool.
- **Negotiation.** Research and preparation appear; no negotiation is conducted.
