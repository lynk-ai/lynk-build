"""Subject session via the Claude Agent SDK (async, in-process).

Runs one question through the installed lynk-build plugin and captures the
message stream. The plugin is loaded with `plugins=[local]` (so the
lynk-research → librarian → scholar skills and the enrich hook all activate) in a
throwaway cwd so no ambient project context leaks in; hook events are surfaced so
the enrich hook's injected chapter content shows up in the transcript. Failures
come back as (messages, error) — never raised — so an errored session scores
ERROR, not a wrong answer.

`messages` is a list of serialized SDK messages (plain dicts): the transcript we
persist and the string the routing evaluator scans for chapter paths.
"""

import asyncio
import contextlib
import dataclasses
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

from claude_agent_sdk import (
    CLIJSONDecodeError,
    CLINotFoundError,
    ClaudeAgentOptions,
    ProcessError,
    SdkPluginConfig,
    query,
)

SUBJECT_TIMEOUT_S = 900
# Skill (the pipeline) · Bash (librarian runs generate_book_toc) · Read (scholars read chapters).
ALLOWED_TOOLS = ["Skill", "Bash", "Read", "Glob", "Grep"]
# Subject runs on the latest Sonnet (what the plugin actually ships to); the judge
# runs on Opus (harness/judge.py) — a stronger grader than the gradee.
SUBJECT_MODEL = "claude-sonnet-5"


@dataclass(frozen=True)
class Target:
    """What the subject session loads. A suite's target fixture supplies one.

    mode="plugin"  → load the plugin at `path` via plugins=[local] in a throwaway
                     cwd (no ambient context).
    mode="project" → run IN `path` with setting_sources=['project'], loading its
                     .claude/ (skills, hooks, CLAUDE.md). The user's global
                     ~/.claude stays excluded.
    """
    mode: str
    path: Path


def _serialize(msg):
    """SDK message → plain dict (dataclasses.asdict recurses into content blocks,
    so tool inputs/results and hook data survive for the transcript scan)."""
    try:
        d = dataclasses.asdict(msg)
    except Exception:
        d = {"repr": str(msg)}
    d["_type"] = type(msg).__name__
    return d


async def run_subject(question, transcript_path, *, target,
                      timeout_s=SUBJECT_TIMEOUT_S, append_system_prompt=None, model=SUBJECT_MODEL):
    """Ask the question against `target` (a Target) and return (messages, error).

    append_system_prompt is a per-suite directive — passed in by the suite, never
    baked into the shared harness."""
    path = Path(target.path)
    env = dict(os.environ)
    system_prompt = ({"type": "preset", "preset": "claude_code", "append": append_system_prompt}
                     if append_system_prompt else None)
    common = dict(
        model=model,
        allowed_tools=ALLOWED_TOOLS,
        skills="all",                     # make the loaded skills invocable
        system_prompt=system_prompt,
        strict_mcp_config=True,           # keep user MCP servers out
        permission_mode="bypassPermissions",  # headless: never block on a prompt
        include_hook_events=True,         # surface hook-injected content (e.g. enrich)
        env=env,
    )

    if target.mode == "plugin":
        # The skills call the catalog/TOC scripts by bare name at load time — put the
        # plugin's bin/ on PATH so they resolve regardless of plugin PATH injection.
        env["PATH"] = f"{path / 'bin'}{os.pathsep}{env.get('PATH', '')}"
        cwd_ctx = tempfile.TemporaryDirectory()
    elif target.mode == "project":
        cwd_ctx = contextlib.nullcontext(str(path))
    else:
        raise ValueError(f"unknown target mode {target.mode!r}")

    messages, error = [], None
    with cwd_ctx as cwd:
        if target.mode == "plugin":
            options = ClaudeAgentOptions(
                plugins=[SdkPluginConfig(type="local", path=str(path))], cwd=cwd, **common)
        else:
            options = ClaudeAgentOptions(setting_sources=["project"], cwd=cwd, **common)
        try:
            async with asyncio.timeout(timeout_s):
                async for msg in query(prompt=question, options=options):
                    messages.append(_serialize(msg))
        except (TimeoutError, asyncio.TimeoutError):
            error = f"session errored: timeout after {timeout_s}s"
        except (CLINotFoundError, ProcessError, CLIJSONDecodeError) as e:
            error = f"session errored: {type(e).__name__}: {str(e)[:300]}"

    transcript_path.write_text(transcript_text(messages))
    if not error:
        res = result_meta(messages)
        if not res or res.get("is_error"):
            error = f"session errored: {res.get('subtype', 'no result message') if res else 'no result message'}"
    return messages, error


def result_meta(messages):
    """The terminal ResultMessage dict, or {} if none."""
    return next((m for m in reversed(messages) if m.get("_type") == "ResultMessage"), {})


def final_answer(messages):
    return result_meta(messages).get("result") or ""


def total_cost(messages):
    return result_meta(messages).get("total_cost_usd") or 0


def model_of(messages):
    return next((m["model"] for m in messages
                 if m.get("_type") == "AssistantMessage" and m.get("model")), "?")


def transcript_text(messages):
    """The whole transcript as one scannable string — the routing evaluator regexes
    it for chapter paths (they ride in tool results, the librarian's refs, and the
    enrich hook's injected content, wherever they surface)."""
    return "\n".join(json.dumps(m, ensure_ascii=False, default=str) for m in messages)
