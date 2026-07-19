"""LLM judge: grades the final answer against the per-case rubric.

Runs through claude-agent-sdk (the CLI's subscription auth — no API key needed),
with no tools and the SDK's bare default system prompt. Temperature is not
settable through the CLI; binary "Pass requires ALL of / Must NOT" rubrics keep
verdicts stable instead. The judge sees only question, answer, and rubric —
never the read trace, so retrieval can't leak into the grade.
"""

from dataclasses import dataclass

from pydantic import BaseModel
from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext

from .llm import LLMError, extract_json, llm_text
from .schema import AgentTrace, CaseInputs, CaseMetadata

JUDGE_PREAMBLE = """You are grading an AI data-assistant's answer against a rubric.
Judge factual alignment with the rubric only:
- Ignore style, length, and formatting.
- Do not penalize citing doc paths or adding extra correct detail.
- Do not reward confident wrongness: a required rubric item that is missing or contradicted fails.
"pass" is true only if EVERY "Pass requires" item is satisfied and no "Must NOT" item is violated.
"Bonus" items never affect "pass".
"score" is the fraction of rubric items satisfied, 0.0-1.0.
Respond with ONLY a JSON object {"pass": <bool>, "score": <float>, "reasoning": "<short>"} - no markdown fences, no other text."""


class JudgeVerdict(BaseModel):
    passed: bool
    score: float
    reasoning: str


async def judge_answer(
    question: str, answer: str, rubric: str, model: str, timeout_s: float = 120.0
) -> JudgeVerdict:
    prompt = (
        f"{JUDGE_PREAMBLE}\n\n"
        f"<question>\n{question}\n</question>\n\n"
        f"<submitted_answer>\n{answer}\n</submitted_answer>\n\n"
        f"<rubric>\n{rubric}\n</rubric>"
    )
    data = extract_json(await llm_text(prompt, model, timeout_s))
    try:
        return JudgeVerdict(
            passed=bool(data["pass"]),
            score=float(data.get("score", 0.0)),
            reasoning=str(data.get("reasoning", "")),
        )
    except (KeyError, TypeError, ValueError) as e:
        raise LLMError(f"malformed judge verdict ({e}): {data!r}") from None


@dataclass
class AnswerRubricJudge(Evaluator[CaseInputs, AgentTrace, CaseMetadata]):
    """answer_pass/answer_quality from the judge; suspect_answer flags a passing
    answer produced without reading the required docs (grep leak or model prior)."""

    model: str
    timeout_s: float = 120.0

    async def evaluate(self, ctx: EvaluatorContext[CaseInputs, AgentTrace, CaseMetadata]) -> dict:
        trace = ctx.output
        if trace.errored:
            return {
                "answer_pass": EvaluationReason(False, reason=trace.error),
                "answer_quality": 0.0,
            }
        try:
            verdict = await judge_answer(
                ctx.inputs.question, trace.answer, ctx.metadata.rubric, self.model, self.timeout_s
            )
        except LLMError as e:
            return {
                "answer_pass": EvaluationReason(False, reason=f"judge failed: {e}"),
                "answer_quality": 0.0,
                "suspect_answer": "judge-error",
            }
        required_read = set(ctx.metadata.expected_docs.required) <= set(trace.unique_docs_read)
        return {
            "answer_pass": EvaluationReason(verdict.passed, reason=verdict.reasoning),
            "answer_quality": round(verdict.score, 3),
            "suspect_answer": "suspect" if verdict.passed and not required_read else "ok",
        }
