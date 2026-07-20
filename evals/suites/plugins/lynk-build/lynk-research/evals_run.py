"""lynk-research eval — the golden-questions confusion matrix.

Skill-specific bits only; the shared runner (harness.suite) owns concurrency,
artifacts, -k filtering, and the run reports.

Run:  uv run pytest suites/plugins/lynk-build/lynk-research
      uv run pytest suites/plugins/lynk-build/lynk-research -k q06
"""

from harness import load_evaluator, suite
from harness.subject import final_answer

routing = load_evaluator(__file__, "routing")
citation = load_evaluator(__file__, "citation")

HIT = ("reach-book", "reach-chapter")

# Forces the pipeline to run for reach-* cases (a bare session answers from prior
# knowledge and never invokes the skill). no-activation cases run WITHOUT it — the
# point there is to test that the skill correctly stays out. Says nothing about HOW
# to route or WHEN to refuse — that judgment is what's under test.
SYSTEM_DIRECTIVE = (
    "Answer the user's question by consulting the research library through the "
    "`lynk-research` skill (invoke it via the Skill tool). Base your answer only "
    "on what that skill returns; follow its instructions for what to do when the "
    "library has nothing relevant."
)


def directive(case):
    return None if case["expect_routing"] == "no-activation" else SYSTEM_DIRECTIVE


def _verdict(kind, routing_r, citation_r):
    if routing_r.get("passed") is None or citation_r.get("passed") is None:
        return "ERROR"
    if kind in HIT:
        if routing_r["passed"] and citation_r["passed"]:
            return "PASS"
        if citation_r["passed"] and not routing_r["passed"]:
            return "SUSPECT"          # answer right, library never reached → model prior
        return "FAIL"
    # miss + no-activation: pass only if routing was right AND the answer behaved
    return "PASS" if (routing_r["passed"] and citation_r["passed"]) else "FAIL"


async def evaluate(case, events, case_dir):
    routing_r = routing.evaluate(case, events)
    citation_r = await citation.evaluate(case, case["question"], final_answer(events), case_dir)
    return _verdict(case["expect_routing"], routing_r, citation_r), [routing_r, citation_r]


globals().update(suite.wire(__file__))
globals().update(suite.build("lynk_research", evaluate, directive))
