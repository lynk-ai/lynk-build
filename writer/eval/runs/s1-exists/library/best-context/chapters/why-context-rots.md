---
name: Why context rots
description: The measured thresholds and attention-level mechanisms behind context rot — it degrades before the window is full because of how attention works, not just "too much text". Read when you need hard numbers or the mechanism for why long context degrades — to justify a budget, cite a threshold, or explain the cause beyond "too much text".
labels: [context rot, long context, degradation, why long context degrades, NoLiMa, lost in the middle, Ms-PoE, attention, RoPE, causal attention, benchmarks, distractor, give-up, thresholds, Chroma]
---

This is the evidence and mechanism under [context-rot](context-rot.md). The principle chapter states *that* quality drops; this one collects *how far before the window fills* (measured thresholds) and *why* (attention-level causes), so a reader can cite a number and name a cause rather than assert "too much text".

Degradation starts early, and a single distractor bites:

| Finding | Number | Source |
|---|---|---|
| Degradation begins far below the advertised window | At 32K tokens, 11 of 13 LLMs (all claiming ≥128K) fell below 50% of their <1K-token baseline; GPT-4o 99.3% → 69.7% | NoLiMa, ICML 2025 (arXiv 2502.05167) |
| Non-uniform decline across 18 models, even on simple tasks; a *single* distractor measurably cuts retrieval, worse at length | 18 models, 8 lengths, 11 needle positions | Chroma, *Context Rot* (2025) |
| Focused prompts (only relevant history) beat full prompts on LongMemEval; Claude showed the largest gap | — | Chroma (2025) |
| Long-horizon agentic search: models increasingly *give up* or answer prematurely as trajectory grows; pruning the accumulated context drives give-up near zero (causal) | give-up 0–38.6% across 4 open models × 3 benchmarks | ContextRot, GAIR-NLP (2026, arXiv 2606.29718) |

And it's attention, not size. Causal attention favors early tokens and RoPE positional encoding decays attention to distant ones, so mid-context tokens are hardest to retrieve regardless of window size (*Found in the Middle* / Ms-PoE, 2024, arXiv 2403.04797) — cite the causal-attention half with more confidence than the RoPE half, since ICML 2025 work argues the U-shape stems from causal masking alone. Retrieval also leans on surface string matching: NoLiMa's needles share minimal lexical overlap with the question, and that is precisely where models collapse, so long-context recall is more lexical than semantic. And goal attention decays over turns: the Goal Accessibility Ratio drops 27–48% within 50 turns (*When Attention Closes*, 2026), and closing the channel collapsed 20-fact recall from ~100% to 11.2%.

**Context rot is an attention effect with measurable onset — degradation by ~32K, a single distractor enough — not a capacity limit, which is why curation beats a bigger window.** The clearest single result is focused-vs-full (Chroma, LongMemEval): the same model answers better given only the relevant history than given the full transcript containing it — direct evidence for SELECT and condensed, cited returns. Caveats to cite honestly: Chroma is a vector-DB vendor with an incentive against long contexts, but NoLiMa and RULER corroborate; the Claude focused-vs-full gap is partly conservative abstention under ambiguity, not pure retrieval failure; and the give-up and GAR results are preprints on open models.

The practical upshot: route small pieces on demand instead of one big prompt, and keep returns condensed and cited rather than full — the mechanism says curation beats capacity. See [context-rot](context-rot.md) for the principle, [four-failure-modes](four-failure-modes.md) — the distractor and give-up evidence grounds distraction and confusion — and [compression](compression.md) for the lever the numbers justify.
