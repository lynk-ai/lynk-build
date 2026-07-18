---
type: recipe
description: Turn a process rule into a measured compliance rate by extracting the behavior from telemetry, computing it per session, and carefully separating real violations from telemetry gaps.
---

# Instrument adherence

**What it is** — the recipe for an adherence eval: measuring whether a *process* rule was actually followed, from telemetry rather than opinion. Artifact evals ask "is the thing good"; adherence asks "was the process followed" (the distinction is homed in [every-rule-is-an-eval](every-rule-is-an-eval.md)).

**Prerequisites**
- A named process rule stated as a checkable predicate (e.g. "writers read the constitution first"; "readers route via the index").
- Telemetry that records the behavior — `.bk/reads/<session>.jsonl` (per-session hashed read logs) exists in this repo today.
- A window of sessions to measure over.

**Steps** (one observable outcome each)
1. **State the rule as a predicate** over one session → a yes/no test exists (e.g. "the session's first logged read is a Book 2 page").
2. **Extract the telemetry** for the window → the raw session records are in hand.
3. **Compute the predicate per session** → a pass/fail per session exists.
4. **Separate violations from telemetry gaps** → sessions with *no data* are set apart from sessions that *had data and failed* (these are not the same).
5. **Report rate plus exemplars** → a compliance rate and a few named example sessions exist.

**Verification**
- The report names the sessions and shows the predicate's output per session (not just an aggregate).
- Spot-check: open one flagged session's log and confirm the predicate's verdict by reading it.

**Failure modes** (symptom → fix/escape)
- **Telemetry gap read as violation** — symptom: compliance collapses right after a tooling change; fix: distinguish "no data logged" from "logged and violated."
- **Goodharting** — symptom: agents perform the logged action without the substance (reads are logged but the content is never used); fix: pair the adherence eval with an artifact eval.
- **Privacy / consent scope** — escape: keep telemetry in-repo, scoped to the library's own sessions.

**Takeaway** — **measure process compliance from telemetry, but split "no data" from "violated" first — an adherence number that silently counts gaps as failures measures your tooling, not your agents.**

**Example** *(real, first computed here 2026-07-08)* — predicate: "the session's first logged read is a Book 2 page." Over the **31** sessions in `.bk/reads/`, **17** touched Book 2 at all and **12** opened with it. But the denominator is the trap this recipe warns about: not all 31 were *writer* sessions — a reader session legitimately never opens the constitution, so it is a gap, not a violation. The honest report is "12 of 31 sessions were constitution-first; the writer-only rate awaits a session-type label" — not "61% non-compliance" (numbers computed from the in-repo `.bk/reads/*.jsonl` logs).

**In this system** — `.bk/reads/` is already collecting the feed; this recipe is what turns it into the adherence row of the coverage matrix ([every-rule-is-an-eval](every-rule-is-an-eval.md)). → See the Best Context book · `hook-vs-router` — the read log is a hook (cheap, every step); this eval is what reads what the hook collected.
