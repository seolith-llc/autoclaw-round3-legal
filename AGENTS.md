# amtocsoft-megagent

## Deliverable language

All deliverables for this project are written in **US English**: US spelling, US date and
currency formats, ASCII-only file names. No CJK characters, including font definitions inside
.docx packages (see `scripts/strip_cjk_fonts.py`).

## Prompt history (mandatory, every turn)

Every user request and the response to it is written to `docs/prompts-history/` before the turn ends.

- Path: `docs/prompts-history/<YYYY>/<MM>/<YYYY-MM-DDTHHmmss±HHMM>_<step>_<slug>.md`
  Example: `docs/prompts-history/2026/11/2026-11-06T112254-0500_step001_git-init-and-prompts-history.md`
- One file per turn, containing front matter, `## Request` (verbatim, never paraphrased), `## Response`
  (what was actually done, files touched, verification, open items), and `## Follow-ups`.
- Attachments are embedded as appendices so the entry stays self-contained.
- Multiple turns in one session still get one file each; the step id and timestamp keep them ordered.

Create an entry with the helper rather than by hand:

```powershell
pwsh scripts/prompt-log.ps1 -Action new -Step step002 -Title "Short title" `
  -RequestFile path/to/request.txt -ResponseText "What was done"
```

## Month rollover

On the first turn of a new month, run:

```powershell
pwsh scripts/prompt-log.ps1 -Action consolidate
```

It creates the new `YYYY/MM` folder and rebuilds `INDEX.md` for every month plus the root
`docs/prompts-history/INDEX.md`. Existing entries are never moved or rewritten.

## Git

- This folder is its own repository on `main`; the parent `D:\src\amtocsoft` repo (quotzo) ignores it.
- Commit each history entry together with the work it describes.
