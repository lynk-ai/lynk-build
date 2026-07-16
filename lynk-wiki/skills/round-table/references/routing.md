# Routing — tiers, consent, the 0 / 1 / 3–5 rule, temperament assignment

## Tiers — fire, ask, or stay silent (evaluated BEFORE anything else)

Every request lands in exactly one tier:

**AUTO — fire without asking.** The user explicitly requested scrutiny:
"pressure-test this", "design review", "what would different experts say",
"pros and cons from multiple angles", "sanity-check before we commit",
"get me multiple expert takes", or an explicit `/round-table`.

**OFFER — stop and ask ONE consent question, before any spawn.** The user asked
for a deliverable or action that embeds a real decision. The ask, verbatim shape:
*"This has real trade-offs — want me to convene the roundtable first to make a
better ⟨plan/choice/design⟩? (runs 3–5 expert agents in parallel, takes a few
minutes). Otherwise I'll just ⟨do the task⟩."*
Yes → continue to Frame (panel first, deliverable after, guided by the fold).
No → do the task normally, and never re-offer on this topic.

The OFFER catalog:
- *Planning:* create/draft a plan for a feature, migration, rollout, or upgrade ·
  quarter/sprint/roadmap planning · a plan exists and is about to be committed ·
  project kickoff ("how should we approach X?") · estimation with stakes
- *Choosing:* build vs buy · vendor/SaaS adoption · tech selection (DB, framework,
  queue, language) · two competing designs · codebase-wide dependency adoption
- *Expensive to undo:* architecture changes (split/merge services, new layer) ·
  schema or public-API changes · deprecating/deleting things users touch · big
  refactors or rewrites · cutover dates and irreversible migrations — including
  when phrased as pure execution ("drop the legacy table today")
- *Risk-heavy:* auth/secrets/permissions changes · personal data or compliance ·
  pre-launch readiness · post-incident "what do we change"
- *Scope & product:* "should we even build this" · quick-fix vs real-fix ·
  cutting scope under deadline · deprecating surfaces customers use
- *Process & team:* changing CI/CD, testing strategy, release process · adopting
  a team-wide workflow or tool

Implied wordings that put a request in OFFER even without the keywords above:
"how should we approach…", "what's the best way to…", "we're thinking of moving
to…", "is it worth switching…", "before we commit…", "we're torn between…",
"considering adopting…" — when attached to something from the catalog.

**SILENT — never offer.** Factual questions, single-file fixes, renames, routine
tasks, casual musing ("X looks cool, might try it someday"), lookups that merely
contain the word "plan". Suppression rules that force SILENT regardless of
wording: the user already declined an offer on this topic · a panel already ran
on this topic in this conversation · the user is mid-execution of an
already-made decision.

**Tie-breaker — the most important rule:** unsure between OFFER and SILENT →
**SILENT**. A missed offer costs nothing (the user can always invoke `/round-table`);
a wrong offer costs trust. Ambiguity resolves toward quiet.

## Sizing — the 0 / 1 / 3–5 rule (after AUTO or a consented OFFER)

The router's job is economic: a panel costs many times a direct answer, so most
requests must route to 0. The decision procedure:

1. **Is it a decision at all?** Tasks to execute, facts to look up, bugs to fix →
   **0** (answer or do it directly).
2. **Did the user name a single perspective?** ("security review this",
   "is this operable?") → **1**, the matching position, carrying red-team.
3. **Count the axes genuinely in tension.** An axis counts only if the decision
   could plausibly go a different way because of it. 0–1 axes → **0 or 1**.
   ≥2 axes, or hard to reverse, or user asked for a panel → **3–5**, one position
   per present axis.
4. **Never pad.** A 3-panelist panel with three real axes beats a 5-panelist panel
   with two.
5. **Then assign temperaments** (panel case): exactly one red-team, on the
   position with most to lose that can cite internals (never product-strategist);
   champion on the proposing side; the rest get distinct picks from cost-cutter /
   long-termist / empiricist.

## Worked examples (kept in sync with ../evals/routing.json)

| # | Request | Route (position+temperament) | Why |
|---|---|---|---|
| 1 | "Should we split the billing module out of the monolith into its own service?" | architect+champion, security-engineer+red-team, operator+long-termist, implementer+cost-cutter | Structure (architect, closest to the proposal → champion), failure surface has most to lose → red-team on security-engineer, deploy reality (operator), sequencing (implementer). |
| 2 | "Pressure-test this launch plan for the new onboarding flow before we commit the quarter to it." | product-strategist+champion, quality-engineer+red-team, implementer+empiricist | Scope/value is the core axis; verification of the plan's claims has most to lose → red-team on quality-engineer; product-strategist can't carry red-team anyway. |
| 3 | "What does HTTP status 429 mean?" | 0 | Single fact. No trade-off. |
| 4 | "Just give me a security review of this auth-token change." | security-engineer (+red-team, solo rule) | User named one perspective. |
| 5 | "We're torn between Postgres JSONB and a dedicated events table for the activity feed — which and why?" | data-steward+red-team, architect+long-termist, implementer+cost-cutter | Data contracts own the axis with most to lose; structural coupling; migration effort. |
| 6 | "Rename this variable and fix the typo in the README." | 0 | Task to execute, not a decision. |
| 7 | "Review this PR." | 0 or 1 | Unqualified review = normal review flow; route 1 (quality-engineer+red-team) only if the user asks what could break. |
| 8 | "Should we adopt this new ORM across the codebase?" | architect+long-termist, implementer+cost-cutter, data-steward+red-team, quality-engineer+empiricist | Cross-cutting structure, big migration, data-layer contracts have most to lose, regression surface. |
| 9 | "Compare these two libraries' APIs for our use case." | 1 (implementer+red-team) | One dominant axis: fitness-for-use and integration effort. |
| 10 | "We're changing the events schema that three consumers read — how should we roll it out?" | data-steward+red-team, operator+long-termist, implementer+cost-cutter | Contract versioning owns the break risk; rollout/compat; sequencing. |
| 11 | "Should our signup flow start collecting date-of-birth for personalization?" | privacy-officer+red-team, product-strategist+champion, data-steward+empiricist | New personal-data collection has most to lose; value case; measurement/contract. |
| 12 | "We want to redesign the CLI's flag names for v2 — worth the breaking change?" | ux-advocate+champion, implementer+cost-cutter, operator+red-team | Ergonomics is the proposal; migration/compat for existing users has most to lose. |

## Near-misses to respect (these look panel-shaped but aren't)

- "What are the pros and cons of X?" where X has a well-known answer → **0**; a
  panel would generate padding, not perspectives.
- "Design review" of a change that only touches one axis (e.g. a pure copy change)
  → **1** at most.
- Any request where the user is executing, not deciding ("migrate this table") →
  **0**; offer the panel only if they ask whether to do it.
- Never dispatch the retired `skeptic`/`pragmatist` aliases — pick a position and
  assign a temperament.
