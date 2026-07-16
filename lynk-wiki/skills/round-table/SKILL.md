---
name: round-table
description: Convenes an expert council on decisions and plans. AUTO-fires when the user explicitly asks for scrutiny — "pressure-test this plan", "design review", "what would different experts say", "pros and cons from multiple angles", "sanity-check before we commit". OFFERS first (one consent question, never a spawn without a yes) when the user asks for a deliverable that embeds a real decision: creating or needing a plan (feature, migration, rollout, roadmap, kickoff), build-vs-buy or tech selection, architecture or schema/API changes, deprecations and irreversible operations, security- or privacy-sensitive changes, big refactors, launch readiness, scope trade-offs — including implied wordings like "how should we approach", "what's the best way to", "we're thinking of moving to". SILENT on factual questions, small fixes, and routine tasks; when unsure between offering and silence, stay silent. Full tier catalog and consent rules: references/routing.md.
compatibility: Requires subagent (Task) support and the roundtable agents + panel-contracts + adjudicate skills installed alongside it (they travel as one bundle). Panelists are read-only and need Read/Grep/Glob and read-only Bash over the working repo.
---

# Round-table — tier, consent, frame, route, compose, fan out, hand off

**What it is:** the roundtable's entry point. Classifies the request (fire / ask /
stay silent), gets consent where needed, frames the decision, picks the right
positions from the roster, assigns each a temperament, runs one parallel opinion
round, and hands the structured opinions to `/adjudicate` for synthesis,
grounding, and fold. Advisory only — the roundtable never applies the plan it
produces. Single-round by design: panelists are asked once; there is no revision
pass.

**Takeaway:** the trigger promises an OFFER, not a panel — asking is cheap,
spawning is expensive. A panelist = position (WHO judges: evidence slice + rubric,
an agent file) + temperament (HOW they argue: a stance block from panel-contracts).
A panel is only worth its cost when panelists genuinely differ on lens, evidence,
AND stance — and when the request genuinely has multiple axes in tension.

## Roster — positions are DATA (pick-when pointers here; full blocks in references/positions.md)

- **architect** — decision changes system structure, boundaries, or dependencies
- **implementer** — cost, reuse, sequencing, or "how do we actually ship" is contested
- **product-strategist** — scope, user value, or "right problem?" is in question
- **operator** — must be deployed, migrated, observed, or run on-call
- **data-steward** — schemas, data contracts, APIs, or measurement change
- **security-engineer** — trust boundaries, auth, secrets, attack surface, or dependency risk
- **quality-engineer** — regression risk, test coverage, or verifiability of the change
- **ux-advocate** — user-facing friction: UI, API ergonomics, errors, docs, naming
- **privacy-officer** — personal data is collected, flows, is retained, or is exposed

Default trio for design decisions: architect + security-engineer + implementer.

**How panelists exist (Architecture A):** positions and temperaments are DATA, not
declared agents. There are only two declared agents in the plugin: the read-only
`panelist` worker and the `adjudicator`. To run a panelist you spawn the `panelist`
agent with a chosen position block (from `references/positions.md`) and a temperament
block (from panel-contracts) injected into its brief — that coupling IS the persona.
The full position blocks (evidence slice, rubric, emphases, boundaries, model) live
in `references/positions.md`; `skeptic`/`pragmatist` are retired names, never used.

Temperaments (assigned per dispatch, defined in panel-contracts): red-team ·
champion · cost-cutter · long-termist · empiricist.

## Phases

- **0 · Tier + consent (before ANYTHING else — see references/routing.md §Tiers)**
  - **AUTO** (user explicitly asked for scrutiny) → continue to Phase 1.
  - **OFFER** (deliverable request embedding a real decision — plans, selections,
    irreversible changes, risk-heavy work, per the catalog) → ask exactly one
    consent question: *"This has real trade-offs — want me to convene the
    roundtable first to make a better ⟨plan/choice/design⟩? (runs 3–5 expert
    agents, a few minutes). Otherwise I'll just ⟨do the task⟩."* Yes → Phase 1.
    No → exit the skill, do the task normally, never re-offer on this topic.
  - **SILENT** (facts, small fixes, routine tasks; or a prior decline / prior
    panel on this topic / mid-execution) → exit without a word.
  - **Tie-breaker:** unsure between OFFER and SILENT → SILENT. `/round-table` always
    exists as the user's recovery; a wrong offer has none.
- **1 · Frame** — restate the decision in one paragraph and assemble the evidence
  pack: repo root, the key paths involved, and the user's request verbatim. For a
  consented deliverable request, frame the decision EMBEDDED in it ("which
  approach should the migration take"), and after the fold, produce the
  deliverable the user originally asked for, guided by the panel's
  recommendation. **Gate 1→2:** a genuine decision with trade-offs exists — if
  not (pure task, no consent context), say so and exit.
- **2 · Route** —
  **Step A — pick positions:**
  - **0 positions** if: single-fact or single-file question, no genuine trade-off
    → answer directly; skill ends.
  - **1 position** if: the user names one perspective, or the decision has exactly
    one dominant axis → run that position alone (it carries the red-team
    temperament), return its opinion clearly labeled as one expert view; skill ends.
  - **3–5 positions** if: two or more roster axes are genuinely in tension, or the
    decision is hard to reverse, or the user explicitly asked for a panel. Pick
    only positions whose lens matches an axis actually present — never pad to
    five, never exceed five. Worked examples: `references/routing.md`.

  **Step B — assign temperaments (panel case only):**
  - **Exactly one red-team per panel, always** — assign it to the position with
    the most to lose from the proposal, choosing only among positions whose
    evidence slice permits internal citation (product-strategist never carries
    red-team).
  - **Champion** goes to the position closest to the proposing side of the request.
  - Remaining panelists get distinct temperaments from cost-cutter, long-termist,
    empiricist — no temperament repeats within a panel.
  State every pick — position + temperament + a one-line reason — BEFORE spawning.
- **3 · Fan-out (the panel's only round)** — dispatch one Task per panelist, all
  in parallel. Every dispatch spawns the **`panelist` agent** (never a
  per-position agent — positions aren't declared) with the brief template from
  panel-contracts, into which you paste: the decision verbatim, the chosen
  **position block** from `references/positions.md`, and the assigned
  **temperament block** from panel-contracts. **Set the Task model to the
  position's `model` field** (opus for architect/product-strategist, sonnet
  otherwise) — omitting it silently downgrades opus positions.
  **Gate 3→4 (all checks fail closed):**
  - every return parses as `<persona_opinion>` with `persona:` = the dispatched
    position name and a `temperament:` field; a non-conforming return or a
    persona/position mismatch gets exactly ONE re-dispatch with the defect named;
    a second failure drops that panelist, recorded for Panel notes;
  - **exactly one** returned opinion carries `temperament: red-team`. Zero or two+
    means the composition drifted: stop, state the defect, and re-dispatch the
    mis-assigned panelist(s) once — never proceed to adjudication with a
    challenger-less or double-challenger panel.
- **4 · Hand off** — invoke the `/adjudicate` skill with: the framed decision, the
  parsed opinions (temperaments ride inside them), and the roster with the
  routing reasons. Adjudicate owns synthesis, grounding, and the fold from here;
  round-table does not touch the opinions again.

## Guardrails — operating contract (never overridden)

- **No panel without AUTO or a visible user "yes"** — the consent question is a
  hard gate on OFFER-tier requests, and a decline is final for that topic.
- **One offer per topic per conversation** — declined means done; nagging kills
  the capability's welcome.
- **One level deep** — panelists never spawn subagents; their briefs say so.
- **Read-only panel** — panelists never edit files; the roundtable's output is
  advisory.
- **Cap the fan at 5** — and never fan out at all when routing says 0 or 1.
  (The no-repeat temperament rule only holds because cap = 5 — these two numbers
  move together or not at all.)
- **Exactly one red-team** — enforced structurally at Gate 3→4, not by trust.
- **Two declared agents only** — every panelist is the `panelist` worker with a
  position + temperament injected; positions/temperaments are data, never declared.
- **Positions and temperaments come from their catalogs verbatim** — position
  blocks from references/positions.md, temperament blocks from panel-contracts;
  never invent or reword them at dispatch.
- **Set the position's model on every dispatch** — opus positions downgrade
  silently otherwise.
- **Typed returns only** — every dispatch names its contract; free prose is not
  accepted.
- **Never skip the tier check** — "just run everyone" is the documented
  anti-pattern; the tier + routing phases are the skill's whole economy.

## Fallback — subagents can't spawn

Run the routed panelists inline, sequentially, capped at 3: for each, read its
position block from references/positions.md and its assigned temperament block
from panel-contracts, adopt that lens + evidence slice + temperament for one pass,
and produce its typed `<persona_opinion>` yourself. Then continue into
/adjudicate's inline fallback. Don't retry spawning. Tell the user the panel ran
degraded (inline, capped) — never silently.

## Common mistakes

- Offering on trivial or musing-shaped requests — the tie-breaker says silence;
  a nagging panel gets the whole plugin disabled.
- Spawning a panel on an OFFER-tier request without the user's yes in the
  transcript.
- Re-offering after a decline, or offering when a panel already ran on the topic.
- Fanning out on a question a direct answer serves — the cheap path is Phase 2's
  first check, not a reluctant exception.
- Padding the roster to 5 because slots exist — every pick needs an axis actually
  present in the decision.
- Assigning red-team to product-strategist (it cannot cite internals) or to two
  panelists (research: multiple challengers collapse deliberation output).
- Paraphrasing the decision differently per panelist — they must all answer the
  same question or the opinions won't compose.
- Spawning a per-position agent name (architect, operator…) — those aren't
  declared; always spawn the `panelist` worker with the position block injected.
- Forgetting to set the Task model to the position's model — opus positions
  silently run on the default.
- Re-litigating opinions in the main window after handoff — adjudicate owns them.
