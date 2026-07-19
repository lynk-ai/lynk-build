"""Single-turn, tool-less LLM calls through claude-agent-sdk (CLI subscription auth)."""

import asyncio
import json
import re

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

NO_TOOLS = [
    "Bash", "Read", "Write", "Edit", "NotebookEdit", "Grep", "Glob",
    "Task", "Skill", "WebSearch", "WebFetch", "TodoWrite",
]


class LLMError(Exception):
    pass


async def llm_text(prompt: str, model: str, timeout_s: float = 120.0) -> str:
    options = ClaudeAgentOptions(model=model, max_turns=1, disallowed_tools=NO_TOOLS)
    result: str | None = None
    try:
        async with asyncio.timeout(timeout_s):
            async for msg in query(prompt=prompt, options=options):
                if isinstance(msg, ResultMessage):
                    if msg.subtype != "success" or msg.is_error:
                        raise LLMError(f"llm session {msg.subtype}")
                    result = msg.result
    except TimeoutError:
        raise LLMError(f"llm timeout after {timeout_s:.0f}s") from None
    if not result:
        raise LLMError("llm returned no result")
    return result


def extract_json(text: str):
    """Parse the first JSON value ({...} or [...]) in a model response."""
    match = re.search(r"[\[{].*[\]}]", text, re.DOTALL)
    if not match:
        raise LLMError(f"no JSON in llm output: {text[:200]!r}")
    try:
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        raise LLMError(f"malformed JSON in llm output ({e}): {text[:200]!r}") from None
