"""Phase-0 spike: one hardcoded question end-to-end, printing the raw navigation trace.

Usage: uv run python -m lynk_evals.spike ["custom question"]
"""

import asyncio
import sys

from .config import load_config
from .runner import run_case

DEFAULT_QUESTION = "What's the difference between a policy and a skill in Lynk?"


async def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUESTION
    cfg = load_config()
    print(f"question: {question}")
    print(f"agent_model: {cfg.agent_model} | system_prompt: {cfg.system_prompt}\n")

    trace = await run_case(question, cfg)

    print(f"resolved model: {trace.model}")
    print(f"session: {trace.session_id} | turns: {trace.num_turns} | {trace.duration_s}s | ${trace.total_cost_usd}")
    print(f"error: {trace.error}\n")

    print(f"doc reads ({len(trace.doc_reads)}):")
    for r in trace.doc_reads:
        marks = ("" if r.first_touch else " [re-read]") + (" [subagent]" if r.from_subagent else "")
        page = f" offset={r.offset} limit={r.limit}" if r.offset or r.limit else ""
        print(f"  {r.order:2d}. {r.path}{page}{marks}")

    print(f"\nsearches ({len(trace.searches)}):")
    for s in trace.searches:
        print(f"  {s.tool}({s.pattern!r}, path={s.path}, glob={s.glob})")

    print(f"\nother tool calls ({len(trace.other_tool_calls)}): {trace.other_tool_calls}")
    print(f"\nanswer ({len(trace.answer)} chars):\n{'-' * 60}\n{trace.answer[:1500]}")


if __name__ == "__main__":
    asyncio.run(main())
