# v1 — frozen snapshot

A byte-identical copy of the md2slides app as it stood at commit `bedb3f0` (2026-09-15),
kept so the live app can be improved without losing a known-good version to compare against.

- **Editable app:** `../index.html` — make changes there.
- **This copy:** do not edit. When it needs to move forward, take a fresh snapshot
  (`v2/`) and leave this one alone; a snapshot that gets edited documents nothing.
- Served at https://janalogy.com/apps/md2slides/v1/index.html

Files carry `index.html` (sha256 `6f2e56ea1816…`), both spec documents, and the llms.txt
example deck. Confirm the copy is still pristine with:

```sh
shasum -a 256 index.html ../index.html
```

## Two things a file snapshot does not freeze

- **Saved decks are shared, not per-copy.** The editor persists to `localStorage` under
  `janalogy.mdcards.v1`, which is scoped to the origin (`janalogy.com`) and not to the
  path. Both copies therefore load and overwrite the *same* saved deck: clearing the deck
  in v1 clears it in the working copy too. Frozen files, shared state.
- **Mermaid is not pinned.** Diagrams render via a runtime import from
  `cdn.jsdelivr.net/npm/mermaid@11`. The snapshot freezes this app's code, not the
  diagram library it pulls.
