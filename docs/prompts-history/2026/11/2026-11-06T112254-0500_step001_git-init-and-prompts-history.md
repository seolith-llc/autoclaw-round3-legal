---
step: step001
timestamp: 2026-11-06T11:22:54-05:00
title: Git init and prompt history scaffold
project: amtocsoft-megagent
tags: [infrastructure, git, prompt-history]
---

# step001 - Git init and prompt history scaffold

## Request

```text
Initialize Git if not already done so. Save every request and response in a date time stamped markdown file inside prompts-history directory inside docs directory and keep them organized in an hierarchical year month folder structure after consolidation every new month. #step001
```

### Attachments

- `pasted_text_20261106T162121329Z_60e70488.txt` (2366 bytes) - a list of 19 agent-engineering
  build ideas. Captured verbatim below; no work was started on it in this step.

<details>
<summary>Attachment contents (verbatim)</summary>

```text
* Build a computer-use agent that parses the DOM, diffs screenshots and maps clicks to coordinates so it can drive legacy software with zero APIs

* Ship generative UI where your LLM returns live React components instead of markdown blobs and watch your product feel 10 years newer

* Wire a System-One router that resolves 95% of requests in milliseconds for fractions of a cent, escalating only the hard 5% to reasoning models

* Kill your while True loop and rebuild it as a Temporal state machine that resumes from the exact node after a crash or a 3-day approval

* Write a raw MCP server in pure JSON-RPC so any external agent can call your product with scoped credentials, no SDK required

* Add grammar-constrained decoding so your agent emits 100% valid JSON on the first try, every try, forever

* Build a trajectory grader in CI that blocks the merge the second a tool-call sequence deviates from the golden path

* Ship an inter-agent sanitization proxy that executes prompt injections before they cross a single agent boundary

* Wire a PII unmasking proxy that swaps sensitive data for UUIDs before inference and restores it after with full audit logs

* Add a cost kill-switch that halts any loop projected to exceed $0.50 and degrades frontier -> mid-tier -> local -> cache

* Implement KV-cache prefix sharing at the gateway and cut Time-To-First-Token by 80% on repeated system prompts

* Set up speculative decoding: local 3B drafts, frontier 70B verifies, acceptance rate logged on every single request

* Shadow-route 5% of production traffic to your new model, diff trajectories and cost silently, auto-post the report to Slack

* Automate the DPO flywheel: thumbs-down -> preference pairs -> nightly LoRA -> eval-verified promotion, zero human touch

* Build a voice loop with VAD and sub-1s interruption handling, streaming tokens and tool calls simultaneously

* Ship an API-to-browser fallback that spawns a headless browser the moment a REST endpoint 404s, finishing the job anyway

* Add a WebGPU shim so a 2B model runs in the browser when the cloud dies and your users never see a spinner

* Fuzz your own agent swarm with malformed tool outputs and context overflow until it self-heals without a single pager alert

* Publish one benchmark: your system vs the naive baseline, on cost, latency and task success, fully reproducible
```

</details>

## Response

Git was already present, but not for this project: `D:\src\amtocsoft` is a repository for the
`quotzo` work on branch `main` (diverged from `quotzo/main`, 80 vs 33 commits). The
`amtocsoft-megagent` folder sat untracked inside it and was ignored through `.zwork/.gitignore`.

Decision: this folder gets its own repository, matching the existing precedent recorded in the
parent `.gitignore` for `amtocsoft-ceo-guide` ("standalone sub-project has its own git repo").
Mixing a new agent project into the quotzo history would have been wrong, and a nested repo inside
a tracked tree risks being committed as a stray gitlink.

Work done:

1. `git init -b main` in `D:\src\amtocsoft\amtocsoft-megagent`. Identity `seolithdev01` is already
   configured, so no local override was needed.
2. `.gitignore` - excludes `.zwork/` (agent tool state; attachments are preserved inside log
   entries instead), dependencies, build output, logs, local env files, OS noise.
3. `AGENTS.md` - the standing rule: every request and response is logged, with the exact path
   pattern, the entry shape, and the month-rollover command, so later turns keep the record going
   instead of relying on memory.
4. `docs/prompts-history/README.md` - layout, file naming, entry format, immutability rule, and the
   consolidation procedure.
5. `scripts/prompt-log.ps1` - PowerShell 7 helper with two actions:
   - `new` writes a timestamped entry (`yyyy-MM-ddTHHmmss+HHMM`), slugging the title and refusing
     to overwrite an existing file.
   - `consolidate` creates the current `YYYY/MM` folder and regenerates `INDEX.md` for every month
     plus the root `docs/prompts-history/INDEX.md`; it only reads entries, never moves or deletes.
6. This entry as `2026/11/2026-11-06T112254-0500_step001_git-init-and-prompts-history.md`.
7. Added `amtocsoft-megagent/` to the parent repository's `.gitignore` so the nested repository is
   never picked up as a gitlink by a `git add -A` in the quotzo tree.

Verification: `git status` in the new repository shows exactly the four scaffold files plus the
history tree; `pwsh scripts/prompt-log.ps1 -Action consolidate` reports one entry and one month
folder and writes both index files.

Open item: the attached list of 19 agent-engineering ideas is recorded, not started. It reads like
a backlog for this project rather than a request for step001, and nothing in the message asked for
implementation.

## Follow-ups

- Turn the 19 ideas into a prioritised plan when asked (`#step002` onward, one idea per step).
- First commit of the new repository: scaffold and this entry together.
