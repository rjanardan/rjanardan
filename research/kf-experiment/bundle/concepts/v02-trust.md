---
type: concept
title: v0.2 trust signals
---

- v0.2 adds trust signals so a consumer can decide whether to read a file before reading it: provenance, trust, freshness, attestation.
- sources: list of resources (resource, title; optionally author, usage_count, last_modified). No credibility scores are assigned; signals only, and absence of a field carries meaning.
- generated: who or what produced the file, with a timestamp (by, at).
- verified: list of verifications (by, at). Trust tiers derived from it: unverified, machine-confirmed, human-reviewed.
- Lifecycle: status is draft, stable or deprecated; a missing status means stable. stale_after is an absolute date; staleness is a deterministic date comparison.
- Compatibility: v0.2 is additive over v0.1; timestamp was renamed generated.at; the old Citations body section moved into the sources field (fallback supported).
