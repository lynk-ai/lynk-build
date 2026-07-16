# Changelog

A chronological record of how this book evolves. Most recent first.

## [2026-07-16] Cross-book links converted to name-references (books-are-independent rule; batch A) — 15 links converted, meaning preserved.

## [2026-07-13] Fixed stale line-number citation on `every-rule-is-an-eval`
Gate-cited `book-2:sourced-statements` fix. The `REGISTRY_ENFORCED` claim cited "source: `bk` line 43", but the flag's definition is now at line 51 in the current `bk` (verified: `grep -n REGISTRY_ENFORCED bk` → line 51 is the `= False` definition, line 465 its use). Corrected to a symbol-anchored citation — "source: `bk`, `REGISTRY_ENFORCED` (line 51)" — so a reader greps the symbol even if the line drifts again. The surrounding claim (flag exists, currently `False`, flips to `True` when the Phase 1 rule-registry merges) is unchanged and stays classified as sourced. Also refreshed two 2026-07-12 entries whose "Uncommitted — awaiting the gate" trailers were stale (tree committed at 352e42a).

## [2026-07-12] Revision pass — discharged graduation exception + sourced the Example
Gate-requested fixes on `verify-at-the-authoritative-surface`. (1) Overlapping-but-distinct graduation exception now discharged with reciprocal cross-pointers: `judge-calibration` and `run-a-baseline-delta` each gain a one-line Related pointer back to `verify-at-the-authoritative-surface`, naming the split (execution grounding is a *judge lever* / a *recipe prerequisite* respectively; the general principle is owned by the new page). (2) The Example is now sourced to the citable incident doc `docs/semantic-layer-build-cycle-2026-07-12.md`; the unstated "~50 metrics" figure replaced with the doc's wording "dozens of field probes failed." No other content changed. Gated and committed (352e42a).

## [2026-07-12] Added Part I principle — verify-at-the-authoritative-surface
New page `verify-at-the-authoritative-surface` (Part I #6): a verification is only as trustworthy as the surface it runs on — static/structural and proxy checks are necessary but not sufficient, and a green proxy over a red authoritative surface is *false green*. Fills the confirmed gap: execution grounding existed only as a judge lever (`judge-calibration`) and a recipe prerequisite (`run-a-baseline-delta`) with no standalone principle. Case study: the Lynk semantic-layer audit incident (a compile-surface circular dependency invisible to static resolution and raw-warehouse queries). Cross-links Book 5 `gates-and-ablation`. Index updated: new page listed at #6, Part II recipes renumbered 7–9 (display ordinals only; slugs unchanged), one-home note added distinguishing this principle from execution grounding. Gated and committed (352e42a).

## [2026-07-08] Book drafted — 8 pages
Part I principles (the-eval-matrix, every-rule-is-an-eval, judge-calibration, trajectory-and-reliability, evals-decay) and Part II recipes (calibrate-a-judge, run-a-baseline-delta, instrument-adherence). Book identity: instruments + imports — every eval imports its bar from the owning book. Facts sourced from `docs/evals-notes.md` and `docs/book-4-consumption-eval-2026-07-08.md`; git hashes 7ab2826 and a8fc53c verified against the log before printing. `instrument-adherence` computes one real number from the in-repo `.bk/reads/` logs (12 of 31 sessions constitution-first). Hand-crafted frontmatter-less index. Uncommitted — awaiting the gate.

## [2026-07-08] Book created
Empty scaffold — index and changelog only.
