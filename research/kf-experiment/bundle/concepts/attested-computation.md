---
type: concept
title: Attested computation
---

- Attested computation (v0.2) is a concept type whose content is computed, not authored.
- Fields: runtime, parameters, executor (resource, receipt), attester (resource).
- An agent fills only the parameters. A deterministic attester that uses no LLM re-runs the canonical logic and emits a receipt; the verdict gates display.
- Attestation is distinct from verification: verification reviews authorship; attestation verifies a computation. The bundle itself never executes code.
