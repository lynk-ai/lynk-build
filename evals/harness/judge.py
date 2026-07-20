"""Reusable LLM judge via the Claude Agent SDK: classify whether each claim is
supported by an answer.

A second SDK session, no tools, that sees only question + answer + claims. Judges
occasionally emit invalid JSON, so one retry; the raw result always lands in
judge.json. Returns {'results': [(claim, happened, evidence)], 'cost': float}
or {'error': str, 'cost': float}.
"""

import asyncio
import json
import re

from claude_agent_sdk import ClaudeAgentOptions, query

JUDGE_TIMEOUT_S = 180
JUDGE_MODEL = "claude-opus-4-8"   # grade on Opus — a stronger model than the subject (Sonnet)

JUDGE_PROMPT = """You are classifying which expectations an answer fulfills.
Judge each expectation INDEPENDENTLY against the answer below. An expectation
"happened" only if the answer affirmatively states or clearly implies it — an
expectation that is absent, hedged away, or contradicted did NOT happen, even
if its keywords appear. Use no outside knowledge; the answer text is the only
evidence.

<question>
{question}
</question>

<answer>
{answer}
</answer>

<expectations>
{expectations}
</expectations>

Respond with ONLY a JSON array, one object per expectation in order:
[{{"n": 1, "happened": true, "evidence": "<short quote from the answer, or why not>"}}, ...]
No markdown fences, no other text. The output must be valid JSON: keep each
evidence under 20 words and replace any double quotes inside it with single
quotes."""


async def _one_judge(prompt, workdir):
    """Returns (result_text, error, cost)."""
    options = ClaudeAgentOptions(
        model=JUDGE_MODEL,
        disallowed_tools=["*"],       # no tools — text only
        strict_mcp_config=True,
        permission_mode="bypassPermissions",
        cwd=str(workdir),
    )
    text, cost, err = "", 0.0, None
    try:
        async with asyncio.timeout(JUDGE_TIMEOUT_S):
            async for msg in query(prompt=prompt, options=options):
                if type(msg).__name__ == "ResultMessage":
                    text = msg.result or ""
                    cost = msg.total_cost_usd or 0
                    if msg.is_error:
                        err = f"judge errored: {msg.subtype}"
    except (TimeoutError, asyncio.TimeoutError):
        err = f"judge errored: timeout after {JUDGE_TIMEOUT_S}s"
    except Exception as e:  # SDK/process failures must not crash the batch
        err = f"judge errored: {type(e).__name__}: {str(e)[:200]}"
    (workdir / "judge.json").write_text(text or (err or ""))
    return text, err, cost


async def judge_claims(question, answer, claims, workdir):
    numbered = "\n".join(f"{i}. {c}" for i, c in enumerate(claims, 1))
    prompt = JUDGE_PROMPT.format(question=question, answer=answer, expectations=numbered)
    cost, last_error = 0.0, "judge errored"
    for _attempt in (1, 2):
        text, err, c = await _one_judge(prompt, workdir)
        cost += c
        if err:
            last_error = err
            continue
        try:
            match = re.search(r"\[.*\]", text, re.DOTALL)
            items = json.loads(match.group(0)) if match else None
            if not isinstance(items, list) or len(items) != len(claims):
                last_error = f"judge errored: expected {len(claims)} verdicts, got: {text[:300]}"
                continue
            return {
                "results": [(claim, bool(item.get("happened")), str(item.get("evidence", "")))
                            for claim, item in zip(claims, items)],
                "cost": cost,
            }
        except (json.JSONDecodeError, AttributeError) as e:
            last_error = f"judge errored: unparseable output ({e}): {text[:300]}"
    return {"error": last_error, "cost": cost}
