"""Artifact rendering + run-level reports, shared across skill suites.

Per pytest invocation: results/<timestamp>/ with meta.json, report.md, and one
<case-id>/ dir (report.md · answer.md · transcript.jsonl · judge.json), plus one
row per case in results/RESULTS.md — the trend table, stamped with the plugin
SHA and model so rows compare over time.
"""

import json
import subprocess
from collections import Counter
from pathlib import Path

RESULTS_HEADER = (
    "| run | case | type | verdict | routing | answer | cost | model | sha |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
)


def plugin_sha(plugin_dir):
    out = subprocess.run(["git", "-C", str(plugin_dir), "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True)
    return out.stdout.strip() or "?"


def _mark(passed):
    return "—" if passed is None else ("✓" if passed else "✗")


def render_case_report(case, verdict, evaluators, run_name, sha, cost, error, model="?"):
    lines = [
        f"# {case['id']} — {verdict}",
        "",
        f"**Type:** {case.get('expect_routing', '—')}",
        f"**Question:** {case['question']}",
        f"**Run:** {run_name} · ${cost:.2f} (incl. judge) · model {model} · plugin {sha}",
        *([f"**Error:** {error}"] if error else []),
        *(["**SUSPECT:** the answer was right but the pipeline never surfaced the "
           "expected chapter — it likely came from the model's prior, not the library. "
           "Read the transcript."]
          if verdict == "SUSPECT" else []),
        "",
        "## Evaluators",
        *(f"- {_mark(e['passed'])} **{e['name']}** — {e['detail']}" for e in evaluators),
    ]
    reached = next((e.get("reached") for e in evaluators if "reached" in e), None)
    if reached is not None:
        lines += ["", f"Chapters reached: {', '.join(reached) or '(none)'}"]
    lines += ["", "Answer: answer.md · full trace: transcript.jsonl · judge: judge.json"]
    return "\n".join(lines) + "\n"


def summary_line(case, verdict, evaluators):
    parts = " · ".join(f"{e['name']} {_mark(e['passed'])}" for e in evaluators)
    return f"{case['id']} [{case.get('expect_routing', '—')}]: {verdict} · {parts}"


def results_row(case, verdict, evaluators, run_name, sha, cost, model="?"):
    ev = {e["name"]: e for e in evaluators}
    return (
        f"| {run_name} | {case['id']} | {case.get('expect_routing', '—')} | {verdict} "
        f"| {_mark(ev.get('routing', {}).get('passed'))} "
        f"| {_mark(ev.get('citation', {}).get('passed'))} "
        f"| ${cost:.2f} | {model} | {sha} |\n"
    )


def write_run_reports(run_dir, results_base, sha, rows):
    if not rows:
        return
    verdicts = [r["verdict"] for r in rows]
    c = Counter(verdicts)
    totals = f"{c.get('PASS', 0)}/{len(verdicts)} PASS" + "".join(
        f" · {c[v]} {v}" for v in ("SUSPECT", "FAIL", "ERROR") if c.get(v))

    def summary(link_prefix=""):
        return (
            f"# eval run {run_dir.name} — {totals}\n\n"
            f"plugin {sha} · total ${sum(r['cost'] for r in rows):.2f}\n\n"
            + "".join(f"- {r['summary']} → [{r['id']}/report.md]({link_prefix}{r['id']}/report.md)\n"
                      for r in rows))

    (run_dir / "report.md").write_text(summary())
    # Stable path: results/report.md always mirrors the latest full run (links
    # prefixed with the run dir so they resolve from the results root).
    (Path(results_base) / "report.md").write_text(summary(f"{run_dir.name}/"))
    (run_dir / "meta.json").write_text(json.dumps({
        "run": run_dir.name,
        "plugin_sha": sha,
        "total_cost_usd": round(sum(r["cost"] for r in rows), 4),
        "verdicts": {r["id"]: r["verdict"] for r in rows},
    }, indent=2) + "\n")

    log = Path(results_base) / "RESULTS.md"
    if not log.exists() or not log.read_text().startswith(RESULTS_HEADER.split("\n")[0]):
        if log.exists():
            log.rename(log.with_suffix(".md.bak"))
        log.write_text(RESULTS_HEADER)
    with log.open("a") as f:
        f.writelines(r["row"] for r in rows)
