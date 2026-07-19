---
name: lynk-build
description: >
  The primary build-and-validate entry point for the Lynk semantic layer. Builds and
  edits everything in `.lynk/` — domains, entities, features, metrics, relationships,
  and the glossary. Inspects the warehouse catalog (list schemas/tables, fetch a
  source's columns, sync sources) and runs ad-hoc Lynk SQL. Validates the layer via
  the backend semantics build, and evaluates content quality (descriptions,
  consistency, placement, SQL dialect); these flows load on demand from references/.

  Use it whenever the user wants to add, edit, model, improve, or fix anything in the
  semantic layer — "add an entity", "edit a metric", "update the glossary", "model
  this table" — even when "semantic layer" isn't said. Also use it for catalog and
  query requests ("list schemas", "sync sources", "run this SQL"), for validation
  ("validate the layer", "did the build pass"), and for quality audits ("evaluate the
  semantics", "audit my entities"). For read-only questions about Lynk or `.lynk/`,
  use `lynk-ask` instead.
---

# lynk-build-semantics

## On-demand flows (load only when needed)

Three flows live as references in this skill and are **loaded on demand** — read the
reference file only when the task calls for it, not upfront:

- **Sources** — `references/sources.md`. The warehouse catalog and Lynk SQL execution:
  list schemas/sources, fetch a source's columns, sync the catalog, reconcile entity
  schemas after source changes, run/test ad-hoc Lynk SQL. Load it when the user's request
  is catalog- or query-shaped, or when a build step below says to delegate to the sources
  flow (grounding a new model, verifying a key, checking referenced columns exist).
- **Validate** — `references/validate.md`. The backend semantics build
  (`POST /semantics/builds`): confirms the layer on a committed branch is valid and ready
  for the agent. Load it when the user asks to validate / run the build / check if the
  build passed, or when the evaluate flow's backend step needs it.
- **Evaluate** — `references/evaluate.md`. The content-quality audit: description
  quality, cross-file consistency, placement, reference integrity, dialect compatibility
  — plus the fix-offer + re-evaluation loop. Load it when the user asks to evaluate /
  audit / review / assess the layer, or from Step 8 below when the user opts into
  evaluation after an edit. It chains the validate flow internally.

When one of these flows is the *entire* task (e.g. the user just wants to list schemas or
run the build), follow that reference start-to-finish and skip the build steps below.
When it serves a build task, the build steps say exactly where to use it.

## Workflow playbooks

For the main workflows, follow the dedicated playbook alongside the steps below:

- **Init** (fresh repo, no semantics yet) — `references/init.md`
- **Add a domain** — `references/domain.md`
- **Add an entity** — `references/entity.md`
- **Extend** — no playbook of its own: it's based on the three above, depending on what the
  user wants to extend (a domain → domain.md, an entity → entity.md, business-level files →
  the init steps for that file).
- **Maintain** — editing/auditing; also based on the three above, or a simple task on its own
  (adding a metric, a feature, a glossary term…) handled directly by the steps below —
  with **validations** via `references/validate.md` and **evaluations** via
  `references/evaluate.md`.

## Rules that always apply

- **Several tickets needed → parent + subs.** For big work (init, a new entity), create a
  parent Linear ticket (story) with one sub-ticket per sub-task.
- **Missing info → placeholder, note it, move on.** If the user doesn't have something (e.g.
  no glossary file), create an empty placeholder file, mention it on the Linear ticket and to
  the user, and continue — we'll get it later (for example, when we scan their BI tool).
- **Help the users find themselves.** Make it easy to build: ask guiding questions, not
  confusing ones; suggest options they can just say yes to. Keep it simple.
- **Update the user on the plan and on each step** — as a todo list. Run independent steps in
  parallel with subagents when it helps.

## Steps

**Never run a "lean" version of this skill.** Every step below is mandatory regardless of how mechanical, repetitive, or large the edit appears. Bulk pass-through edits (e.g. "add 30 fields from this source") feel mechanical but are exactly the situations where skipped doc reads or substituted sub-skill flows produce silently wrong artifacts — the user has no way to tell until something breaks. If you believe a step can be safely skipped in a given case, **tell the user before the work** which step, why, and what's lost by skipping; wait for explicit opt-in. Never confess the shortcut after the fact.

### 1. Read the basic Lynk docs to ground yourself

**Mandatory — do not skip even for bulk pass-through edits.** The vocabulary and primitive list below is what every later step assumes you know.

- Read `${CLAUDE_PLUGIN_ROOT}/semantics_docs/concepts/README.md` to understand the Core Vocabulary and Semantic Layer structure — what Lynk primitives exist: Entity, Feature, Metric, Relationship, Glossary, Domain, Context.

For how to navigate the docs (the two anchor pages and walking from the index to leaf pages — the docs are bundled with the plugin under `semantics_docs/`, read directly with no network fetch), see `${CLAUDE_PLUGIN_ROOT}/references/lynk-docs.md`.

### 2. Understand the user's request

From the user's request, determine:
- **Concept type** — which primitive are they asking about?
- **Artifact name** — which specific one (e.g. "customer entity", "total_orders metric", "core glossary")?
- **Domain** — default to `default` unless stated otherwise
- Whether the user provided source files (CSV, text, docs) to inform the content

If the request is entirely a sources / validate / evaluate task, switch to the matching
on-demand flow (see "On-demand flows" above) instead of continuing here.

### 3. Locate the artifact in `.lynk/`

The current semantic layer:
```
! find ./.lynk -type f | sort
```

Identify which file(s) own the artifact the user mentioned by scanning the actual filenames and folder structure.

### 4. Read the relevant docs and detect the SQL engine

**Mandatory — do not skip the docs index fetch or the entity-file reads below, even for bulk pass-through edits.** A 30-field "just add these columns" request is exactly where re-reading the entity's knowledge file and task-instructions catches naming conventions, field-visibility rules, and existing groupings that the agent would otherwise miss.

**Always read the docs index** at `${CLAUDE_PLUGIN_ROOT}/semantics_docs/SUMMARY.md` to see what pages are available. This is the index of all Lynk docs. It also gives you a sense of how the docs are structured, so you can make informed decisions about which files to read for the most relevant context.

Consult the bundled Lynk docs via `Read` (under `${CLAUDE_PLUGIN_ROOT}/semantics_docs/`) — only read what you need.
Read the narrowest set of files that gives you enough context to act:

#### Entity
Users can ask to build or edit an entity, or ask about an entity's features, metrics, relationships, knowledge, task instructions, clarification policy, or output format. In all cases, the core files to read are:
- the entity's schema file (`schema.yml`)
- the entity's prose/knowledge files (`ENTITY.md` and any supporting files it links)
- the domain-level files for that entity (domain `LYNK.md`, `GLOSSARY.yml`, policies, skills)

In case the user request is referring multiple entities, read all of them, but avoid reading unrelated entities.

#### Non Entity
- If the user does not ask about an entity or its sub-primitives (metrics, features, relationships or context), and it is clear that they are asking about (might be agent behavior, a glossary term, or a domain-level context file), then read only the relevant file(s). 
If it is not clear, check with the user before moving forward.

#### Detect the SQL engine
Read `config.json` at the repo root (agent-side warehouse settings — `.lynk/lynk.yml` holds only schema/topology) for an `engine`, `dialect`, or `warehouse` field (common values: `bigquery`, `snowflake`, `postgres`, `redshift`, `databricks`). If the field is missing, empty, or the file doesn't exist, ask the user via `AskUserQuestion` — do not guess. The dialect drives Rule 7 of `${CLAUDE_PLUGIN_ROOT}/references/content-rules.md`: every SQL snippet you write must be valid in that engine.

### 5. Ground the model in the real source — fields first, then the key

**Which grounding path: prefer the sources flow (`references/sources.md` — the catalog)
whenever possible** — for both new and existing entities it's the default way to find
candidate key-source tables, keys, columns, and descriptions. For a **brand-new entity**,
`references/entity.md` adds the discovery layer on top (candidate matching, cardinality
sanity, query-history mining); go to the warehouse directly only for what the catalog
can't answer (query history, uniqueness/cardinality probes). The key-verification
procedure at the end of this step is canonical for both paths.

When the user wants to add or extend an entity, model against the source's **actual** columns, description, and keys — never guesses. The catalog already holds all of this, so the default is to go get it, not to ask the user how. Open an `AskUserQuestion` about *how* to obtain columns only when the catalog genuinely can't answer (table still not found after a sync) or the user has said they'd rather paste — not as the opening move.

#### Fetch and read the source

Load `references/sources.md` and follow it to pull the source's `description`, `keys`, column count, and column list. Do this before planning — it's the grounding pass.

- **Table name resolves** → surface the table `description` (if any) and the column types/descriptions, so the model reflects what the data *means*, not just column names.
- **Table name doesn't resolve** → don't punt to the user yet. Recommend the closest-matching catalog table name, or offer to run a `sync` (a table added since the last sync won't appear until then). Fall back to asking the user to paste columns only if it still can't be found.
- **Wide table (roughly ≥40 columns)** → don't dump every column or ask the user how to proceed. Lead with a recommended next step: model the core subset the entity's questions actually need first, or group the columns by theme and confirm the grouping. Recommend; don't offload the whole decision.
- **User-provided files** — if the user attached or pasted CSV/text/docs, use those as the column source instead of (or alongside) the catalog.

If the user says "I added fields to X" or "columns of X changed", follow the sources flow (`references/sources.md`) to sync, refetch fields, and reconcile any field features whose source columns no longer exist.

**Announce the source-fetch step for multi-field adds (≥5 fields).** Before running the sources flow, tell the user explicitly: *"Fetching current source columns from the catalog first — grounding against the live catalog so we don't model fields that no longer exist or miss ones that were just added."* The user should see the workflow happen, not have to ask afterwards whether the skill grounded itself.

#### Choose the entity key

A `keys` is mandatory and must *uniquely identify a row* — see Rule 11 in `${CLAUDE_PLUGIN_ROOT}/references/content-rules.md` for why a non-unique column is worse than none. Source it from real data, never fabricate it:

1. **Catalog reports `keys`** → use them as-is.
2. **Catalog `keys` is empty** → derive a candidate (a single id-like column, or a composite for the grain) and verify it via the sources flow's Run Lynk SQL action: `SELECT COUNT(*) AS rows, COUNT(DISTINCT <candidate>) AS distinct_rows FROM <table>` (composite → count the distinct concatenation). Unique iff `rows == distinct_rows` and non-null. **Narrate each attempt** so the user sees the reasoning, not just a verdict.
3. **At most 3 candidates.** One verifies → use it, and say it was *verified*. All 3 fail → stop and escalate via `AskUserQuestion` with the real options (a composite the user knows is unique, an upstream surrogate, or reconsidering the grain).

### 6. Plan and confirm — the plan lives in Linear

Write the plan into the **Linear ticket** (create it if one doesn't exist — always create and
update Linear as the source of truth, and show the user the ticket link). In chat, share only
a **brief summary** of the ticket and mention that everything is in the ticket. The user
iterates on the plan in Linear or here directly. Wait for approval before making any changes.

Before drafting the plan, apply every applicable rule in `${CLAUDE_PLUGIN_ROOT}/references/content-rules.md` (the rule index is at the top) to the proposed change, and call out in the plan which rules bear on it and what each requires — build enforces the same rulebook evaluate audits. A few need action *inside the plan*, not just a mental check:
- **Rule 3** — if you noticed misplaced content while reading, offer relocation here, even if it's outside the original request.
- **Rule 8** — fetch the SQL docs Rule 8 lists *before* writing any SQL; don't rely on memory.
- **Rules 10 & 11** — if you're adding an `examples:` entry / `evaluations.yml` case / SQL example, or setting an entity's `keys:`, that rule's procedure is binding (key verification runs in Step 5). State in the plan that you applied it.
- **Rule 12** — before adding a `related_source`, confirm the table is not (and won't become) its own entity and that you won't aggregate it; if either holds, model it as an entity + relationship instead. **When you create a *new* entity, reconcile in the same edit:** grep `.lynk/` for that table used as a `related_source` elsewhere (`! grep -rn "<table>" .lynk/`) and convert any hit to a relationship + entity-sourced feature. Phased modeling is exactly where a table becomes an entity *after* another entity already bolted it on as a related_source — that drift is the failure Rule 12 catches.

### 7. Execute step by step

Write or edit one file at a time. Show the user what was written before moving to the next.

After each file is saved, run the **per-file quick check** (questions 1, 2, 4, 6, 7, 8, 10 from the bottom of `${CLAUDE_PLUGIN_ROOT}/references/content-rules.md` — right place / clear / internally consistent / engine-compatible SQL / Lynk SQL syntax / domain on-topic / keys real). After all files in the edit are saved, run the **cross-file pass** (questions 3, 5, 9, 11 — appears once / references resolve / examples & evaluations valid / related-sources legit), since those checks need every edited file to be on disk first.

Fix or escalate to the user before considering the edit done. Don't silently advance past a failure: if a check fails because of a question only the user can answer (naming, contradicting definitions), surface it before continuing.

**After-action summary (mandatory before Step 8).** Once all files are saved and the cross-file pass is clean, produce a single structured recap so the user can see what happened without reconstructing it from per-file messages. Three sections, in this order, even if a section is empty (in which case say "none"):

- **Done** — what was added, changed, or removed. For bulk edits, lead with counts and grouped highlights (mirror the grouping you used during the edit — e.g., *"Added 28 features to `inventory.yml`: Product condition (5), Packaging condition (5), Bin/location flags (18)"*). Cite file paths.
- **Skipped / deferred + reason** — anything you didn't do that the user might have expected: source columns with no obvious mapping, fields whose type you couldn't confidently infer, naming choices you punted on, content that would have belonged in a file outside the edit's scope, etc. Each item gets an explicit reason.
- **Needs your input** — items you can't decide unilaterally: contradictory definitions, ambiguous naming, fields that may be PII / internal-only and need a visibility call, etc. Phrase each as a concrete question.

This recap is the user's record of the work and the bridge into Step 8. Never skip it for "small" or "obvious" edits.

### 8. Review — ask before validating or evaluating

Once all edits are saved, **ask the user** (per the operating contract): validate, evaluate, both,
neither, or something else first? Never run validation or evaluation unasked.

If they choose to evaluate, load `references/evaluate.md` and run that flow **scoped to
what you touched** plus the files that reference it or are referenced by it — never the
full graph by default. Evaluate already chains the backend validate flow
(`references/validate.md`) **and** owns the fix-offer + re-evaluation loop (capped at 3
attempts). Just present whatever evaluate returns; **do not** run a parallel fix loop
here.

**Never substitute a raw API call for the full evaluate flow.** Calling `POST
/semantics/builds` directly (or via the validate flow alone) only runs the backend
schema + warehouse-probe check — it skips the content-rules layer (description quality,
cross-file consistency, placement, Lynk SQL syntax, domain coherence) that the evaluate
flow adds on top.

## Output Format

Always respond clearly with the recommendations as bullet points, and use code blocks to show any file content.
Give references from the docs to justify your decisions. If you make assumptions, state them explicitly.

## Best Practices
- Always look for conflicts and ambiguities in the context files. Always flag them to the user and ask for clarification before proceeding.
- Never change files before getting user confirmation on the plan. Always be transparent about what you're changing and why.
- Apply `${CLAUDE_PLUGIN_ROOT}/references/content-rules.md` on every edit. Surface out-of-scope misplacements or duplications you notice (Rule 3) — don't silently accept them.
