---
type: concept
title: Bundle structure
---

- A bundle is a folder of Markdown files. index.md at the root is the entry point: overview plus links into the concepts.
- One concept per file, grouped in subfolders by topic. log.md (optional) is a changelog.
- Official sample bundles in the okf directory of the knowledge-catalog repository: acme_retail, ga4, stackoverflow, crypto_bitcoin.
- Reference tooling in the same repository: an enrichment agent (BigQuery to Markdown with citations), a static HTML visualizer, and a consumption MCP server. Google Knowledge Catalog can ingest OKF bundles.
