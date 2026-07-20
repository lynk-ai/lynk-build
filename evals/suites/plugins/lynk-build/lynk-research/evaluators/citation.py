"""Answer-quality evaluator, via the shared judge.

Routing (routing.py) proves the pipeline *reached* the right place; this proves
the *answer* used it. One claim per case (`case['answer_claim']`):
  hit cases   — the answer answers from the expected book/chapter and cites it
  miss cases  — the answer states the library doesn't cover it and doesn't fabricate

Together with routing this separates PASS (reached + used) from SUSPECT
(answer right, library never reached → model prior) from FAIL.
"""

from harness.judge import judge_claims


async def evaluate(case, question, answer, workdir):
    claim = case["answer_claim"]
    j = await judge_claims(question, answer, [claim], workdir)
    if "error" in j:
        return {"name": "citation", "passed": None, "detail": j["error"],
                "cost": j.get("cost", 0), "error": j["error"]}
    _claim, happened, evidence = j["results"][0]
    return {
        "name": "citation",
        "passed": happened,
        "detail": f"{claim} → {'✓' if happened else '✗'}: {evidence}",
        "cost": j.get("cost", 0),
    }
