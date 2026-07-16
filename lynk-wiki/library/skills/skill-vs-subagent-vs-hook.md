---
type: principle
description: When to use a skill, a subagent, or a hook — decided by the portability ladder (skills port everything, hooks port only event names) and by what each mechanism is for.
---

# Skill vs. subagent vs. hook

**What it is** — the placement decision: the same capability can live in a skill, a subagent, or a hook, and where you put it decides how far it ports and how it fires. The deciding lens is the **portability ladder** (source: `docs/talk-outline.md` §E).

**Mechanics** — how far each layer ports across hosts (source: `docs/talk-outline.md` §E, reproduced):

| Layer | Shared across hosts | Differs per host | Porting work |
|---|---|---|---|
| **Skills** | Everything — SKILL.md is an open standard | Nothing that matters | Copy the folder. **Write once.** |
| **Subagents** | The content (role, prompt, tools, model) | Wrapper format (MD+YAML vs TOML) | Re-serialize. Write once, package ×3. |
| **Plugins** | The bundle | The manifest (no shared spec) | Three descriptors. Wire ×3. |
| **Hooks** | Only the event *names* | Matcher syntax, payloads, output contracts | Re-implement. **Rewrite ×3.** |

The decision that follows:

| Need | Put it in |
|---|---|
| Knowledge & procedure | a **skill** — it ports for free |
| Heavy isolated work behind a strict brief | a **subagent** (→ the Subagents book · `the-strict-brief`) |
| A guaranteed lifecycle intervention that must fire itself, fail-closed | a **hook** (→ the Best Context book · `hook-vs-router`: hooks raise the floor, routers guard the door) |

The four rules of the road (source: `docs/talk-outline.md` §E): hook only against the *intersection* of host events; keep skill frontmatter standard; your gate runs *inside* the host's gate; one source of truth, three generated manifests.

**Takeaway** — **put the logic where it ports: knowledge and procedure in skills; hooks stay thin per-host adapters you expect to write three times.**

**Example** — our own system (real): the `.claude/skills/library/SKILL.md` skill carries the whole librarian → reader → writer → gate *procedure* (ports by copying the folder); the SessionStart hook only injects the small pointer note that tells the agent the library exists (a thin, host-specific adapter — rewrite per host); the librarian, book-reader, and gate are *subagents* doing heavy isolated work behind strict briefs. Each capability sits on the ladder rung that matches how far it needs to travel.

**In this system** — this page is the routing decision *before* [building-a-skill](building-a-skill.md): confirm the capability is knowledge/procedure (skill territory) rather than isolated work (subagent) or a fire-itself guarantee (hook). A skill's enforced pipeline stages are a codification of the Progressive Disclosure book · `habit-vs-contract` — the forced flow turns a polite convention into a contract the runtime carries. → See [what-a-skill-is](what-a-skill-is.md) for the format, and the Best Context book · `hook-vs-router` for why the fire-itself/guard-the-door split decides hook-vs-router placement.
