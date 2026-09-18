---
type: concept
title: OKF overview
sources:
  - resource: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
    title: Google Cloud blog, Introducing the Open Knowledge Format, 13 Jun 2026
  - resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: OKF SPEC v0.2
---

- OKF = Open Knowledge Format: an open, vendor-neutral specification for portable knowledge bundles usable by humans and AI agents.
- Announced by Google Cloud on 13 June 2026 (authors Sam McVeety and Amir Hormati).
- Formalizes the LLM-wiki pattern popularized by Andrej Karpathy in mid-2025.
- Shape: a directory of Markdown files, one concept per file, YAML frontmatter, links between files forming a graph.
- Principles: minimally opinionated (only type is required), producers and consumers independent, format not platform.
- Versions: v0.1 June 2026; v0.2 on 25 July 2026 adds trust signals. v0.2 is additive and backward compatible.
