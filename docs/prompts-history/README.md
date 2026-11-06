# Prompt history

A complete, append-only record of every request to this project and every response given.

## Layout

```
docs/prompts-history/
├── INDEX.md                  # generated: one row per month
├── README.md                 # this file
├── 2026/
│   ├── 11/
│   │   ├── INDEX.md          # generated: every entry in the month
│   │   └── 2026-11-06T112254-0500_step001_git-init-and-prompts-history.md
│   └── 12/
│       └── ...
```

Year and month folders are created on demand, so the tree stays hierarchical without empty
directories hanging around.

## Entry file name

```
<YYYY-MM-DDTHHmmss±HHMM>_<step>_<slug>.md
2026-11-06T112254-0500_step001_git-init-and-prompts-history.md
```

- Local time with the UTC offset; colons dropped from the offset so the name is valid on Windows.
- Sorts lexicographically into chronological order.
- `step` is the request's own marker (`#step001`) when the user supplies one, otherwise the next
  free `stepNNN`.

## Entry format

```markdown
---
step: step001
timestamp: 2026-11-06T11:22:54-05:00
project: amtocsoft-megagent
tags: [infrastructure, git]
---

# step001 — Git init and prompt history scaffold

## Request
(verbatim, fenced)

### Attachments
(list, or embedded as an appendix)

## Response
(what was done, files touched, verification, open items)

## Follow-ups
```

Rules:

1. The request is copied verbatim. No tidying, no summary substituting for the original.
2. The response records what actually happened, including failed attempts worth remembering.
3. Entries are immutable once written. A later correction is a new entry that references the old one.

## Consolidation

Run at each month boundary, and whenever the index looks stale:

```powershell
pwsh scripts/prompt-log.ps1 -Action consolidate
```

This creates the new month folder and regenerates `INDEX.md` for every month and for the root.
It only reads entry files — nothing is moved, merged, or deleted, so history stays auditable.
