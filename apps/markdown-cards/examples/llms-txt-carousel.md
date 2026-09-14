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

# The file from 2024

- Jeremy Howard proposed `/llms.txt` in September 2024 to give agents "concise, expert-level information gathered in a single, accessible location."
- A curated index for inference, not a rule set for crawling. The H1 is the only required section; H2 sections hold link lists, and an `Optional` section marks what an agent may skip.

# What the file looks like

```
# Acme Docs
> Short summary of the project

## Guides
- [Setup](https://acme.com/setup.md): 10-minute path
```

# What actually fetches it

- Ahrefs, June 2026: 137,210 domains. 28% publish an `llms.txt`; 97% got zero requests in May.
- Of the fetches that did happen, 96% were bots — audit tools ~21%, coding agents 10%, AI retrieval bots ~1%. Not one request went to a path that 404s; bots never go looking.
- Google's AI optimization guide: Search ignores the file, and shipping one neither helps nor hurts rankings.

# Where AEO fits

- Answer engine optimization is the umbrella: making a brand the answer, not just a result. llms.txt is one lever under it — and not a citation lever.
- It is plumbing for agents that already want you: Chrome's Lighthouse audits it as part of its agentic browsing checks, Mintlify generates it, and OpenAI, Anthropic and Gemini publish their own.

# Why citations miss the file

- SE Ranking checked 300,000 domains: no relationship between publishing one and being cited.
- A self-declared summary is unverifiable. Citation comes from pages a system can check, not a file it must trust.

# Write it for the agent, not the crawler

It costs an afternoon and buys clarity for the one audience that reads it. The citations were never in the file.
