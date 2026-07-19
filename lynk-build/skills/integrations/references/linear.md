# Linear — usage

Linear is the **system of record** for all work (see the operating contract → "Task tracking").
Every task is a Linear ticket; users review plans, approve, comment, and add teammates there.

**Use the project's designated Linear team/board only** — the team chosen during setup (see
`linear-setup.md`). Do not search or create on other teams/boards. Pull requests link their
issue (e.g. a PR body containing "Closes ABC-123", where `ABC` is the team's issue prefix).

If Linear isn't connected, see `linear-setup.md`.

## The board — stages

In board order, with what each means and when you move a ticket:

| Stage | Type | Meaning / when to use |
| --- | --- | --- |
| **Triage** | triage | Just reported, not yet reviewed. New reports land here until verified real. |
| **Backlog** | backlog | Accepted but not scheduled — real work, no one is on it yet. |
| **Todo** | unstarted | Ready to work: the ticket carries a plan awaiting (or just given) user approval. |
| **In Progress** | started | Plan approved; implementation is happening. Move here when you start editing. |
| **Awaiting Verification** | started | Implementation done; waiting on verification — validation/evaluation runs or the user checking the result. |
| **In Review** | started | A PR is open and under review. |
| **Done** | completed | The PR is merged; the work is live. The authoritative "done". |
| **Canceled** | canceled | Triaged and rejected (not real / won't fix). Record a one-line reason — this prevents re-litigating. |
| **Duplicate** | duplicate | Same issue as an existing ticket — link the original, close this one. |

Mapping to the task workflow in the operating contract: plan on the ticket (**Todo**) → user approves →
implement (**In Progress**) → validate/evaluate/review (**Awaiting Verification**) → PR opened
(**In Review**) → merged (**Done**).

## What you can do

Once the Linear MCP server is connected, its actions are available as tools. The common ones:

- **Find work:** list/search issues, get a single issue's details, list projects and cycles —
  always scoped to the project's Linear team.
- **Past references:** when given a task, search the board for similar or past tickets on the
  same issue — completed tickets show how it was handled before.
- **Create & update:** create a new issue, update status/assignee/labels, add a comment.
- **Link to code:** when opening a PR, reference the issue id so the two stay connected.

## Priorities

Urgent → High → Medium → Low → No priority. When picking "the most important" ticket, rank by
priority first, then prefer Todo/Backlog over already-started; skip Done/Canceled/Duplicate.

## Good habits

- **Every ticket you create — show the user its link. Always.** (The `url` field on the
  created issue.)
- Keep everything on the project's Linear team. Don't create or search elsewhere unless told otherwise.
- **Don't ask permission to create a ticket — just create it** (the ticket *is* the plan; the
  user iterates on it there). Creating and commenting are visible to the team, so keep
  titles/descriptions professional.
- Status changes are part of the work: move the ticket as you cross each stage above — never
  leave a merged ticket sitting in In Review.
- When you write issue descriptions or comments, send real newlines and markdown directly (no
  literal `\n`).
