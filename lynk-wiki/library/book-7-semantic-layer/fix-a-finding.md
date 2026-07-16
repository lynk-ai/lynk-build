---
type: recipe
description: Resolve one audit finding safely — apply its class-specific fix, re-ground the metric, rebuild at the authoritative surface, get human approval, and only then take the next — the skill's human-gated fix loop written down.
---

# Fix a finding

**What it is** — the fix arc at the grain of a single punch-list item. The audit returns a *verified punch-list* and stops (source: `.claude/skills/semantic-layer-audit/SKILL.md`, "returns a verified punch-list — it never applies or commits fixes"). This recipe is the other half: how to resolve **one** finding without introducing a regression you can't attribute. It is the skill's fix-loop discipline made a recipe — the discipline is the load-bearing part, not the edit.

**Prerequisites**
- A **verified finding** from an audit — located, classed, cited to a rule, and backed by execution evidence (→ See [audit-a-layer](audit-a-layer.md)). A finding not yet proven is not ready to fix; fixing from memory or from an unproven smell is a blocked move (source: SKILL.md gate, "DON'T fix from memory").
- The **read-only warehouse** and access to the **compiled Lynk build** — you re-ground and rebuild on the same surfaces the audit used (→ See the Evals book · `verify-at-the-authoritative-surface`).
- **Human approval to proceed** — applying fixes is a separate, human-gated loop, one at a time, next only after approval (source: SKILL.md guardrails, "Audit runs end-to-end; fixes do not").

**Steps** (one observable outcome each)
1. **Take exactly one finding.** Pick a single punch-list item; leave the rest untouched. → *Outcome:* one finding selected, tree otherwise unchanged.
2. **Apply the class-specific fix.** Each value-smell class carries its own fix in `.claude/skills/semantic-layer-audit/references/bug-taxonomy.md` — averaged-ratio → rewrite as weighted `SUM/SUM`; scale-mismatch → correct the units/constant; description-vs-SQL → reconcile prose and SQL; unbacked → trace the metric to a real backing column; cross-entity cycle → break one back-edge. Apply the one that matches the finding's class (do not re-enumerate the classes here — point). → *Outcome:* the definition is edited per its class's fix.
3. **Re-ground the metric.** Run the fixed metric's SQL against the warehouse and match the externally-sourced anchor again — the fix is not done until the number is proven, not just changed (→ See [ground-a-metric](ground-a-metric.md)). → *Outcome:* the metric's `actual` now matches its external anchor.
4. **Rebuild & probe at the authoritative surface.** Re-run the Lynk build probe (Phase 1b) after the edit — "refs resolve" is not "it builds"; a green static check over a red build is false green (source: SKILL.md, "Build before commit"). → *Outcome:* the build stays green with the edit applied.
5. **Get approval, then stop before the next.** Present the single change with its re-grounding and build evidence for human review; take the next finding only after approval. → *Outcome:* one reviewed change; the loop pauses for the human.

**Verification**
- The finding's **external anchor now matches** — the number that was wrong grounds true against a value that did not come from the fixed SQL itself (source: `bug-taxonomy.md`, "Anchoring rule"; `references/gate-rules.md#anchor-external`).
- The **build stays green** — the edit compiles and every field still resolves at the authoritative surface (source: SKILL.md Phase 1b).
- The change is **attributable** — exactly one finding was touched, so any regression the rebuild reveals traces to this edit alone.
- **Nothing is committed** without the explicit word "commit," and the books are run before every commit (source: SKILL.md guardrails, "Commit only on the explicit word 'commit'").

**Failure modes** (symptom → fix/escape)
- **Batching fixes** — symptom: several findings edited before any rebuild, so a regression can't be attributed to a specific change. Fix: one finding at a time, rebuild between each (source: SKILL.md guardrails).
- **Fixing from memory** — symptom: a value edit that traces to no grounder verdict or cited source. The gate blocks it (`no-memory-fix`). Fix: ground it or cite it before editing (source: SKILL.md gate).
- **Fixing without re-grounding** — symptom: the definition changed but no one re-ran the SQL against the anchor, so "fixed" is unproven — it may compute a *different* wrong number. Fix: re-ground (step 3) before calling it done.
- **Committing without the explicit word** — symptom: the tree is committed after review but before the human said "commit," or committed batched. Fix: never commit before the explicit word, never batched, and run the books first (source: SKILL.md guardrails).

**Takeaway** — **fix one verified finding at a time — apply its class fix, re-ground the number, rebuild at the authoritative surface, get approval, and never commit without the explicit word — because a batched or remembered fix is a regression you can't trace.**

**Example** *(real — the skill's recorded run on `nba-demo-audit-sv2`)* — the audit CONFIRMED Jokić career 3P% as an averaged-ratio bug: 30.5% averaged vs the 36.5% weighted anchor, Snowflake-verified over 933 games (source: SKILL.md; `bug-taxonomy.md#averaged-ratio`). Fixing it under this recipe: rewrite the metric to `SUM(3PM)/SUM(3PA)` (its class fix), re-ground it (the value now matches the 36.5% anchor), rebuild (stays green), present the single change for approval — then, and only then, the next finding.

**In this system** — this is the "fix" arc of [the frame](the-frame.md), the direct counterpart to [audit-a-layer](audit-a-layer.md), which finds but never fixes. The highest-value specific fix — breaking a compile-time cycle — has its own recipe → See [break-a-dependency-cycle](break-a-dependency-cycle.md). The per-class fixes live in the skill's `bug-taxonomy.md` (the one home); this page owns the *safe fix discipline*, not the class list.
