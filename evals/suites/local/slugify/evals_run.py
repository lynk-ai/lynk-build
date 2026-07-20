"""slugify eval — a dummy repo-root `.claude` skill, showing the framework works
for the repo's OWN skills (target=project), not just plugins. Scoring is a single
DETERMINISTIC evaluator (no LLM judge): the answer must contain the exact slug.

Run:  uv run pytest suites/local/slugify
"""

from harness import load_evaluator, suite
from harness.subject import final_answer

slug = load_evaluator(__file__, "slug")

# Force the skill on so the test targets its OUTPUT, not description-triggering.
SYSTEM_DIRECTIVE = ("Use the `slugify` skill (via the Skill tool) to answer, and "
                    "output only the slug it produces.")


async def evaluate(case, events, case_dir):
    slug_r = slug.evaluate(case, final_answer(events))
    return ("PASS" if slug_r["passed"] else "FAIL"), [slug_r]


globals().update(suite.wire(__file__))
globals().update(suite.build("slugify", evaluate, directive=lambda case: SYSTEM_DIRECTIVE))
