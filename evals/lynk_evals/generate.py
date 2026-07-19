"""LLM-generate candidate eval cases from the docs. Output goes to candidates/,
never directly into datasets/ — the critic and a human review stand in between."""

from datetime import UTC, datetime

import yaml

from .config import CANDIDATES_DIR, PLUGIN_ROOT, Config
from .datasets import _validate_paths, load_cases
from .llm import extract_json, llm_text
from .schema import CaseInputs, CaseMetadata

DOCS_DIR = PLUGIN_ROOT / "semantics_docs"

CASE_SCHEMA_EXAMPLE = """{
  "name": "kebab-case-unique-id",
  "question": "the user's question, in the user's voice",
  "perspective": "drawers | business",
  "tags": ["topic", "topic2"],
  "business": "short-business-slug or null (business perspective only)",
  "expected_docs": {
    "required": ["semantics_docs/concepts/....md"],
    "optional": ["semantics_docs/....md"]
  },
  "optimal_hops": 3,
  "rubric": "Pass requires ALL of:\\n- ...\\nMust NOT:\\n- ...",
  "rationale": "which doc owns each claim + the assumed optimal navigation path, written out hop by hop"
}"""

GENERATOR_RULES = """Rules for every case:
- The question must NEVER name a doc file, path, or section — retrieval must be earned.
- expected_docs.required is the MINIMAL set of docs whose content is necessary to answer; optional = genuinely helpful extras. Use only paths from the doc index below.
- optimal_hops = number of doc reads on the shortest sensible navigation path, starting from an entry point (SUMMARY.md or README.md counts as hop 1) and ending when the last required doc is read. Write that path out hop-by-hop in rationale.
- rubric must be binary-gradeable: "Pass requires ALL of:" items + "Must NOT:" items, each verifiable from the expected docs' text alone. Optionally "Bonus (does not affect pass):". No vague items like "explains well".
- Every rubric claim must be supported by the expected docs — do not rely on memory of what a semantic layer usually is.

For perspective=business:
- Invent a REALISTIC business and name 2-4 warehouse tables with a few columns; the question asks how to model/route it in the Lynk semantic layer (in the user's voice, e.g. "We run X. Our warehouse has Y. How do we ...?").
For perspective=drawers:
- Ask about the semantic layer itself: its drawers (LYNK.md, GLOSSARY.yml, domains, entities, skills, policies), their scope, loading, format, or interactions."""


def _frontmatter_description(path) -> str:
    text = path.read_text()
    if not text.startswith("---"):
        return ""
    try:
        fm = yaml.safe_load(text.split("---", 2)[1])
        return fm.get("description", "") if isinstance(fm, dict) else ""
    except Exception:
        return ""


def _doc_index() -> str:
    lines = []
    for f in sorted(DOCS_DIR.rglob("*.md")):
        rel = f.relative_to(PLUGIN_ROOT)
        lines.append(f"- {rel}: {_frontmatter_description(f)}")
    return "\n".join(lines)


def _existing_names() -> set[str]:
    names = {c.name for c in load_cases()}
    for f in CANDIDATES_DIR.glob("*.yaml"):
        data = yaml.safe_load(f.read_text()) or {}
        names.update(c["name"] for c in data.get("cases", []))
    return names


async def generate(
    cfg: Config, perspective: str, n: int = 10, business: str | None = None
) -> None:
    existing = _existing_names()
    business_line = (
        f"Use this business scenario for every case: {business}\n" if business else ""
    )
    prompt = (
        "You are authoring candidate evaluation cases for a documentation-navigation "
        "benchmark. The system under test is an AI agent that answers questions about "
        "the Lynk semantic layer by navigating the docs below (progressive disclosure: "
        "SUMMARY.md is the TOC, README.md the mental model).\n\n"
        f"Produce exactly {n} cases with perspective={perspective}.\n{business_line}\n"
        f"{GENERATOR_RULES}\n\n"
        f"Already-used case names (do not reuse): {sorted(existing)}\n\n"
        f"<doc_index>\n{_doc_index()}\n</doc_index>\n\n"
        f"<readme>\n{(DOCS_DIR / 'README.md').read_text()}\n</readme>\n\n"
        f"<summary>\n{(DOCS_DIR / 'SUMMARY.md').read_text()}\n</summary>\n\n"
        f"Respond with ONLY a JSON array of case objects, each exactly this shape:\n{CASE_SCHEMA_EXAMPLE}"
    )

    raw_cases = extract_json(await llm_text(prompt, cfg.judge_model, timeout_s=600.0))
    if not isinstance(raw_cases, list):
        raise SystemExit(f"generator returned {type(raw_cases).__name__}, expected a list")

    kept, dropped = [], []
    for raw in raw_cases:
        name = raw.get("name", "?")
        try:
            if name in existing:
                raise ValueError("name already in use")
            metadata = CaseMetadata(
                perspective=perspective,
                tags=raw.get("tags", []),
                business=raw.get("business"),
                expected_docs=raw["expected_docs"],
                optimal_hops=raw["optimal_hops"],
                rubric=raw["rubric"],
                rationale=raw.get("rationale", ""),
            )
            CaseInputs(question=raw["question"])
            _validate_paths(CANDIDATES_DIR, name, metadata)
        except (KeyError, ValueError, TypeError) as e:
            dropped.append((name, str(e)))
            continue
        existing.add(name)
        kept.append(
            {
                "name": name,
                "status": "candidate",
                "inputs": {"question": raw["question"]},
                "metadata": metadata.model_dump(exclude_defaults=True, mode="json"),
            }
        )

    for name, reason in dropped:
        print(f"dropped candidate {name!r}: {reason}")
    if not kept:
        raise SystemExit("no valid candidates produced")

    stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    out = CANDIDATES_DIR / f"{stamp}-{perspective}.yaml"
    payload = {
        "generated": {
            "at": datetime.now(UTC).isoformat(),
            "model": cfg.judge_model,
            "perspective": perspective,
            "business": business,
        },
        "cases": kept,
    }
    out.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=100))
    print(f"wrote {len(kept)} candidates -> {out}")
