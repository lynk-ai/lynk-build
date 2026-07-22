"""book-writer eval — the repo's own `.claude/` book-writing pipeline
(diagnose → research → author → verify → promote). Target is the repo's `.claude/`,
inherited from suites/local/conftest.py (mode="project") — same as slugify.

Scored for now by ONE deterministic evaluator: does the pipeline's terminal state
match the case's `expect_outcome`. Structure + quality graders (writer/eval/check.py
and a best-context judge) get layered in once the suite runs end-to-end in a sandbox.

Run:  uv run pytest suites/local/book-writer
      uv run pytest suites/local/book-writer -k bw05-needs-info
"""

from harness import load_evaluator, suite
from harness.subject import final_answer, transcript_text

outcome = load_evaluator(__file__, "outcome")
promote_location = load_evaluator(__file__, "promote_location")

# Force the pipeline on so the test targets its BEHAVIOUR, not description-triggering.
DIRECTIVE = (
    "Use the `book-writer` skill (via the Skill tool) to handle this request. "
    "Build its brief from the user's message: the ask verbatim · what was searched "
    "and missed (or 'direct request') · the specific gap · the target book/chapter "
    "if stated. Let the skill's own DIAGNOSE stage decide exists/partial/absent. "
    "When it finishes, output its final RETURN verbatim — including the terminal "
    "state (found-existing / enriched / created / removed / nothing-written / needs-info)."
)


async def evaluate(case, events, case_dir):
    o = outcome.evaluate(case, final_answer(events))
    loc = promote_location.evaluate(transcript_text(events))
    # promote_location is a guard: n/a (None) never fails a case; only a wrong
    # store (False) does, on top of the terminal-state check.
    ok = bool(o["passed"]) and loc["passed"] is not False
    return ("PASS" if ok else "FAIL"), [o, loc]


globals().update(suite.wire(__file__))
globals().update(suite.build("book_writer", evaluate, directive=lambda case: DIRECTIVE))
