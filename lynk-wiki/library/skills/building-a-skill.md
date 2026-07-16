---
type: recipe
description: Build a validated skill directory end-to-end — from a real, corrected task through frontmatter, a budgeted body, reference overflow, and validation.
---

# Building a skill

**What it is** — the end-to-end recipe from *real expertise* to a *validated* skill directory. It assumes the placement decision is already made (this is a skill, not a subagent or hook — see [skill-vs-subagent-vs-hook](skill-vs-subagent-vs-hook.md)) and turns hands-on experience into a directory a host can load (source throughout: `docs/skills-spec-notes.md`).

**Prerequisites**
- A **real task you have performed, with the corrections you made** — the expertise to extract (the spec is explicit that general training knowledge produces vague skills; → [what-makes-a-skill-good](what-makes-a-skill-good.md)).
- A target host that supports Agent Skills (source: `docs/skills-spec-notes.md` lists ~40).
- The `skills-ref` validation tool (the spec's reference library, in the standard's repo) or an equivalent validator.
- A decided scope, "coherent like a function" — one nameable job, neither too narrow nor too broad.

**Steps** (one observable outcome each)
1. **Extract the expertise** → raw notes exist capturing the steps that worked, the corrections you made, the formats and context you provided.
2. **Scaffold the directory** → a directory whose name is the skill name, containing a `SKILL.md`.
3. **Write the frontmatter** → `name` matches the directory and passes the constraints table ([what-a-skill-is](what-a-skill-is.md)); `description` states what + when (tune it separately per [writing-the-description](writing-the-description.md)).
4. **Write the body** → under 500 lines / < 5000 tokens, moderate detail, with the sections the spec recommends: step-by-step instructions, input/output examples, common edge cases.
5. **Move overflow depth to `references/`** → deep detail lives in reference files **one level deep**, each pulled by an *explicit load trigger* in the body ("Read references/api-errors.md if the API returns non-200").
6. **Bundle scripts only where traces show re-invented logic** → `scripts/` exists only for logic the agent was observed reinventing each run.

**Verification**
- `skills-ref validate ./my-skill` exits clean.
- Budget respected: count them — `awk 'END{print NR}' my-skill/SKILL.md` under 500, token estimate under 5000.
- A **dry activation**: invoke the skill on a task that matches its description and observe the body loads and is followed.

**Failure modes** (symptom → fix)
- **Generic LLM-generated content** — symptom: vague procedures like "handle errors appropriately"; fix: re-ground each line in a real trace or artifact.
- **Over-comprehensive body** — symptom: the agent pursues instructions that don't apply to the task; fix: cut by the admission test ("would the agent get this wrong without this line?").
- **Nested reference chains** — symptom: reference files pointing to other reference files; fix: flatten to one level deep. (Flat-at-one-level is a reliability best practice, not a mechanism limit — the disclosure mechanism itself allows chained references, i.e. execution recursing; → See the Progressive Disclosure book · `read-vs-execute` / the Progressive Disclosure book · `three-stages`.)
- **Name/directory mismatch or constraint violation** — symptom: `skills-ref validate` fails; fix: rename per the constraints table (lowercase, no consecutive/edge hyphens, name = directory).

**Takeaway** — **a skill ships when a validator passes, the body is inside budget, and a dry activation shows a real task loading and following it — expertise first, format second.**

**Example** — our `.claude/skills/library/SKILL.md` (real, 96 lines) maps cleanly to these steps: name matches its directory, description carries what + when, the body is a moderate-detail pipeline (spawn librarian → act on response → cite) with a documented fallback edge case, and it stays lean with no reference overflow needed. CandleKeep's `reference/skills/SKILL.md` (538 lines) is the scale-up case — same pipeline shape grown past the 500-line budget, the exact point where step 5 (move overflow to `references/`) becomes mandatory. Honest gap: neither exemplar actually ships a `references/` or `scripts/` directory, so steps 5–6 are **spec-sourced guidance, not exemplar-dissected**. *(superseded 2026-07-14: previously "83 lines" — SKILL.md grew to 96 in the pipeline restructure; see log.md)*

**In this system** — the library skill is the artifact this recipe would produce; it is itself governed by the same shape our books use. → See [writing-the-description](writing-the-description.md) to tune step 3's trigger, and [evaluating-a-skill](evaluating-a-skill.md) to measure whether the built skill actually improves the work.
