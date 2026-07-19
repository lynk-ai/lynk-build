---
type: principle
description: When a reader must choose between two similar items, the difference must show in BOTH the name and the one-line description — the complement of one-concept-one-home.
---

# Distinguishability

**What it is** — the rule that governs two *legitimately-different* things sitting side by side. A reader — human or agent — choosing between them must be able to tell them apart from their **name** and their **description** alone, because that is all a chooser reads before committing. Two items that share a name, or carry identical / near-identical descriptions, force a guess: the choice becomes a coin-flip, and everything built on the wrong pick is silently wrong. This is the complement of [one-concept-one-home](one-concept-one-home.md): one-home says *define each thing once*; distinguishability says *when two distinct things coexist, make the difference visible in both the name and the one-line description*. (Framing ours — the two rules address opposite failures: one-home kills the duplicate, distinguishability separates the genuine pair.)

**Mechanics** — a chooser routes on two surfaces, and the difference must live in **both**:

| Surface | Fails when | Fix |
|---|---|---|
| **Name** | Two distinct items share one name — the reader can't even address them apart. | Qualify each name with what makes it distinct (`player_total_points` vs `team_total_points`). |
| **Description** | The one-liners are identical or near-identical — the name distinguishes but the description doesn't confirm, or vice-versa. | State the discriminating fact in each (`…scored by the player…` vs `…by the team…`). |

Both, not either. Fixing only the name leaves two entries whose descriptions still read the same — a reader who trusts the description is back to guessing; fixing only the description leaves a name collision a tool may not even be able to reference. Derived: a chooser that reads name-then-description stops at the first surface that resolves the ambiguity, so an ambiguity in *either* surface can strand it.

**Takeaway** — **two things a reader must choose between are distinguishable only when the difference shows in BOTH the name and the description — fixing one and leaving the other still leaves a coin-flip.**

**Example** *(real — nba-demo semantic layer; source: `docs/build-vs-docs-findings-2026-07-12.md`, finding 1.6, this repo)* — the `player_game` and `team_game` entities each defined a metric **named `total_points`** carrying the **identical description** "Total points scored across all games." One is a player's total, the other a team's — but an agent (or a text-to-SQL model) selecting a metric by name + description had no way to tell which was which, so any query that grabbed the wrong one returned player numbers where team numbers were meant, with nothing flagging the error. The fix did both: qualify the names — `player_total_points` / `team_total_points` — *and* disambiguate the descriptions — "…scored by the player…" vs "…by the team…" (source: `.claude/skills/semantic-layer-audit/references/bug-taxonomy.md`, `domain-duplicate-metric-name`).

**In this system** — the Book Standard · `toc-discipline` (`label-matches-content`) enforces that *one* page's H1 + description honestly promise *its own* body; distinguishability adds the between-items dimension its per-page check can't see — two pages (or two metrics) that each pass in isolation can still be indistinguishable *as a pair*. Two convergent rules justify it: Book 4's admission test — "would the agent get this wrong without this instruction?" (the Agent Skills book · `what-makes-a-skill-good`) — is exactly the pass/fail here (identical descriptions guarantee the agent gets the pick wrong), and the Book Standard · `non-inferable-only` says the discriminating fact must be *stated* because the chooser cannot infer it. The semantic-layer book applies this rule directly to Lynk metric naming: the Lynk Semantic Layer book · `build-a-layer` avoids the collision at authoring time and the Lynk Semantic Layer book · `audit-a-layer` flags it (gate rule `distinguishable`, severity major) when it slips through. → See [one-concept-one-home](one-concept-one-home.md) (the complement — kill duplicates vs separate genuine pairs) and [four-failure-modes](four-failure-modes.md) (a wrong pick from an ambiguous choice is clash and confusion made silent).
