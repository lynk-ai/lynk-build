---
type: principle
description: The two cost shapes inside execution — detail read into context (pay the full token price of the text) vs code executed outside it (only the output is paid) — and when to prefer each; the cheapest disclosure never enters the window.
---

# Read vs execute

**What it is** — the split *inside* the third stage of [three-stages](three-stages.md). Execution has two cost shapes, not one. Detail can be **read** into context — a reference doc the model pulls in, paying the full token price of every word. Or work can be **executed** outside context — a script run through a shell, whose code never loads at all; only whatever it prints back is paid for. The cheapest disclosure is content that never enters the window.

**Mechanics** — the two shapes, contrasted:

| | **Read** | **Execute** |
|---|---|---|
| What loads | The full text of the reference. | Nothing — the code runs in a shell. |
| What's paid | Every token of the document. | Only the output the run prints back. |
| Prefer when | The model must **reason over** the material — API semantics, a policy, a schema it interprets. | The work is **deterministic** and only the result matters — a fetch, a transform, a validation. |

Reading is for material the model has to think with; executing is for mechanical work where the reasoning is already settled and only the answer needs to come back. A 400-line script costs zero tokens to run and a handful to report; the same 400 lines read as a reference cost their full length whether or not the model needed all of it (derived: token cost tracks what enters the context window, and executed code never enters it — only its stdout does).

**Takeaway** — **read what the model must reason over; execute what only needs its result — the cheapest disclosure is the content that never enters the window at all.**

**Example** — Agent Skills draw exactly this line in the directory layout: `references/` holds docs loaded on demand (read — the model reasons over them), while `scripts/` holds executable code run when needed (executed — the code itself is never loaded into context, only its output) (source: `docs/skills-spec-notes.md` — the `scripts/` vs `references/` split and "resources loaded only when required"; the read-vs-execute cost distinction is derived from that split, see Mechanics).

**In this system** — our fetch stage is this principle running. `scripts/fetch-pointers.sh` executes `bk read` on exactly the pointed chapters, deterministically — zero model tokens are spent deciding to fetch or doing the fetch (it is a hook: `scripts/fetch-pointers.sh` sets `BK_ROLE=hook` and writes the fetched text to `.bk/fetch/`, while the `bk` CLI reads that env var and logs the read with its role to the telemetry under `.bk/reads/` — sources: `scripts/fetch-pointers.sh` and `bk`). The script's own logic never enters any agent's window; it writes the chapters to a file under `.bk/fetch/`, and only the chapters the main agent then Reads from that file are paid for — read cost incurred only on what the answer actually needs. → See [three-stages](three-stages.md) for the execution stage this splits, [the-economics](the-economics.md) for why keeping content out of the window keeps cost flat, and the Agent Skills book · `what-a-skill-is` for the `scripts/`/`references/`/`assets/` format this rides on.
