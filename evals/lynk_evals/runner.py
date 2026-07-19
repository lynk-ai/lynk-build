"""Run one question through a headless Claude session with the lynk-wiki plugin.

Two profiles, chosen per case by run_eval:
- "docs": semantics_docs retrieval — Read/Grep/Glob navigation, Bash disallowed.
- "library": the book pipeline (skill -> librarian -> book-reader scouts -> bk CLI).
  Bash is required (bk is Bash-only) and gated to block destructive/network shell;
  CLAUDE_PLUGIN_ROOT is injected so scouts resolve bk instead of hunting for it.
"""

import asyncio
import tempfile
import time
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    SystemMessage,
    ToolUseBlock,
    query,
)

from .config import PLUGIN_ROOT, Config
from .schema import AgentTrace
from .trace import build_trace

# No writes, no web, ever. Bash is added back only for the library profile.
BASE_DISALLOWED = ["Write", "Edit", "NotebookEdit", "WebSearch", "WebFetch"]
BASE_ALLOWED = ["Read", "Grep", "Glob", "Task", "Skill", "TodoWrite"]


def _build_options(cfg: Config, scratch_dir: str, profile: str) -> ClaudeAgentOptions:
    allowed = list(BASE_ALLOWED)
    disallowed = list(BASE_DISALLOWED)
    env: dict[str, str] = {}
    if profile == "library":
        # The library pipeline (librarian + book-reader scouts) reaches book
        # content only through the bk CLI, which is Bash. Bash runs open here:
        # a PreToolUse Bash gate would work for the top-level agent but the SDK
        # doesn't apply it to subagent Bash under bypassPermissions, so gating
        # breaks the scouts. Writes/web stay blocked via disallowed_tools.
        allowed.append("Bash")
        # Inject CLAUDE_PLUGIN_ROOT so scouts resolve bk instead of hunting for
        # it; CLAUDE_PROJECT_DIR anchors .bk/ state. LIBRARY ONLY — injecting it
        # for docs lets the router/session hooks resolve the library and drags a
        # semantics_docs question into a bk pipeline it can't run (Bash disallowed).
        env = {"CLAUDE_PLUGIN_ROOT": str(PLUGIN_ROOT), "CLAUDE_PROJECT_DIR": scratch_dir}
    else:
        disallowed.append("Bash")

    return ClaudeAgentOptions(
        plugins=[{"type": "local", "path": str(PLUGIN_ROOT)}],
        # The SDK default is an EMPTY system prompt — evaluating a different
        # agent than the one users run. The preset restores the Claude Code prompt.
        system_prompt={"type": "preset", "preset": cfg.system_prompt},
        model=cfg.agent_model,
        permission_mode="bypassPermissions",
        allowed_tools=allowed,
        disallowed_tools=disallowed,
        max_turns=cfg.library_max_turns if profile == "library" else cfg.max_turns,
        cwd=scratch_dir,
        # Isolation: only the bundled plugin, none of the user's global config.
        # setting_sources=[] drops user/project plugins + hooks; strict_mcp_config
        # with no servers drops the user's MCP tools (Gmail/Linear/etc.), which
        # setting_sources alone does NOT — they otherwise leak into the session.
        setting_sources=[],
        mcp_servers={},
        strict_mcp_config=True,
        env=env,
    )


async def run_case(question: str, cfg: Config, profile: str = "docs") -> AgentTrace:
    """Always returns an AgentTrace; session failures land in .error with a partial trace."""
    tool_calls: list[dict] = []
    session: dict = {"answer": "", "session_id": "", "model": "", "error": None}

    timeout_s = cfg.library_timeout_s if profile == "library" else cfg.per_case_timeout_s
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="lynk-eval-") as scratch:
        options = _build_options(cfg, scratch, profile)
        try:
            async with asyncio.timeout(timeout_s):
                async for msg in query(prompt=question, options=options):
                    _consume(msg, tool_calls, session)
        except TimeoutError:
            session["error"] = f"session errored: timeout after {timeout_s:.0f}s"
        except Exception as e:  # CLI/transport failures must not crash the run
            session["error"] = f"session errored: {type(e).__name__}: {e}"

        # Parse .bk/ before the scratch dir is cleaned up (library retrieval telemetry).
        bk_dir = Path(scratch) / ".bk"
        return build_trace(
            tool_calls,
            bk_dir=bk_dir if bk_dir.is_dir() else None,
            answer=session["answer"],
            num_turns=session.get("num_turns", 0),
            duration_s=round(time.monotonic() - start, 2),
            total_cost_usd=session.get("total_cost_usd"),
            input_tokens=session.get("input_tokens"),
            output_tokens=session.get("output_tokens"),
            session_id=session["session_id"],
            model=session["model"],
            error=session["error"],
        )


def _consume(msg, tool_calls: list[dict], session: dict) -> None:
    if isinstance(msg, SystemMessage) and msg.subtype == "init":
        session["session_id"] = msg.data.get("session_id", "")
        session["model"] = msg.data.get("model", "")
        plugin_names = {p.get("name") for p in msg.data.get("plugins", []) if isinstance(p, dict)}
        if "lynk-wiki" not in plugin_names:
            session["error"] = f"session errored: lynk-wiki plugin not loaded (got {sorted(plugin_names)})"
    elif isinstance(msg, AssistantMessage):
        for block in msg.content:
            if isinstance(block, ToolUseBlock):
                tool_calls.append(
                    {
                        "tool": block.name,
                        "input": block.input,
                        "parent_tool_use_id": msg.parent_tool_use_id,
                    }
                )
    elif isinstance(msg, ResultMessage):
        session["num_turns"] = msg.num_turns
        session["total_cost_usd"] = msg.total_cost_usd
        usage = msg.usage or {}
        session["input_tokens"] = usage.get("input_tokens")
        session["output_tokens"] = usage.get("output_tokens")
        if msg.subtype == "success" and not msg.is_error:
            session["answer"] = msg.result or ""
        elif session["error"] is None:
            session["error"] = f"session errored: {msg.subtype}"
