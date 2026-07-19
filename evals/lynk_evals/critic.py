"""Critic gate: an independent LLM pass grading each candidate case for eval quality.

The critic reads the FULL text of the candidate's expected docs, so groundedness is
checked against real content — not the generator's memory. Scores are 1-5, 5 = best.
All scores >= 4 (and plausible optimal_hops) -> status: ready_for_review.
"""

import asyncio

import yaml

from .config import CANDIDATES_DIR, PLUGIN_ROOT, Config
from .llm import LLMError, extract_json, llm_text

CRITIC_PROMPT = """You are reviewing a candidate evaluation case for a documentation-navigation benchmark.
The system under test navigates the Lynk semantic-layer docs to answer questions.

Grade the CASE (not any answer) on four dimensions, integer 1-5 (5 = best):
- clarity: is there a single defensible correct answer? (5 = unambiguous)
- no_leakage: does the question avoid revealing the answer, doc names, or paths? (5 = no leakage)
- groundedness: is every rubric claim supported by the expected docs' text below? (5 = fully supported)
- routing_value: does answering genuinely require navigating TO these docs? (5 = strong navigation test)

Also assess:
- optimal_hops_plausible: is the stated optimal_hops consistent with a shortest sensible
  path from an entry point (SUMMARY.md/README.md = hop 1) to the required docs?
- verdict: "approve" | "revise" | "reject"
- notes: concrete problems and how to fix them (short).

<case>
{case_yaml}
</case>

<expected_docs_full_text>
{docs_text}
</expected_docs_full_text>

Respond with ONLY a JSON object:
{{"scores": {{"clarity": n, "no_leakage": n, "groundedness": n, "routing_value": n}},
 "optimal_hops_plausible": <bool>, "verdict": "approve|revise|reject", "notes": "<short>"}}"""


async def critique(cfg: Config) -> None:
    files = sorted(CANDIDATES_DIR.glob("*.yaml"))
    if not files:
        raise SystemExit("no candidate files in candidates/")

    sem = asyncio.Semaphore(cfg.max_concurrency)
    total = ready = 0

    for f in files:
        data = yaml.safe_load(f.read_text()) or {}
        targets = [c for c in data.get("cases", []) if c.get("status") == "candidate"]
        if not targets:
            continue

        async def one(case: dict) -> None:
            async with sem:
                await _critique_case(case, cfg)

        await asyncio.gather(*(one(c) for c in targets))
        f.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100))

        total += len(targets)
        ready += sum(1 for c in targets if c["status"] == "ready_for_review")
        for c in targets:
            print(f"{c['name']}: {c['status']}  {c.get('critic', {}).get('notes', '')[:100]}")

    print(f"\n{ready}/{total} candidates ready for review (make review)")


async def _critique_case(case: dict, cfg: Config) -> None:
    docs = case["metadata"]["expected_docs"]
    paths = docs.get("required", []) + docs.get("optional", [])
    docs_text = "\n\n".join(
        f"=== {p} ===\n{(PLUGIN_ROOT / p).read_text()}" for p in paths
    )
    case_view = {k: v for k, v in case.items() if k not in ("status", "critic")}
    prompt = CRITIC_PROMPT.format(
        case_yaml=yaml.safe_dump(case_view, sort_keys=False, allow_unicode=True),
        docs_text=docs_text,
    )
    try:
        result = extract_json(await llm_text(prompt, cfg.judge_model, timeout_s=300.0))
        scores = {k: int(v) for k, v in result["scores"].items()}
        hops_ok = bool(result.get("optimal_hops_plausible", False))
        verdict = result.get("verdict", "revise")
    except (LLMError, KeyError, TypeError, ValueError) as e:
        case["critic"] = {"error": str(e)}
        case["status"] = "critic_error"
        return

    case["critic"] = {
        "scores": scores,
        "optimal_hops_plausible": hops_ok,
        "verdict": verdict,
        "notes": str(result.get("notes", "")),
        "model": cfg.judge_model,
    }
    approved = min(scores.values()) >= 4 and hops_ok and verdict == "approve"
    case["status"] = "ready_for_review" if approved else "needs_revision"
