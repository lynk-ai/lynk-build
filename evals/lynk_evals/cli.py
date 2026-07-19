import argparse
import asyncio

from dotenv import load_dotenv

from .config import EVALS_ROOT, load_config


def main() -> None:
    load_dotenv(EVALS_ROOT / ".env")
    parser = argparse.ArgumentParser(prog="lynk-evals", description="lynk-wiki agent evaluations")
    sub = parser.add_subparsers(dest="command", required=True)

    p_eval = sub.add_parser("eval", help="run evaluations against the plugin")
    p_eval.add_argument("--tag", help="only cases with this tag")
    p_eval.add_argument("--perspective", choices=["drawers", "business"])
    p_eval.add_argument("--case", help="a single case by name")
    p_eval.add_argument("--repeat", type=int, default=1, help="run each case N times")
    p_eval.add_argument("--label", help="suffix for the run directory name")
    p_eval.add_argument("--model", help="override agent_model")
    p_eval.add_argument("--judge-model", help="override judge_model")

    p_gen = sub.add_parser("generate", help="LLM-generate candidate cases")
    p_gen.add_argument("--perspective", choices=["drawers", "business"], required=True)
    p_gen.add_argument("--n", type=int, default=10)
    p_gen.add_argument("--business", help="business scenario to use (business perspective only)")

    sub.add_parser("critic", help="LLM-grade candidate cases")

    p_rev = sub.add_parser("review", help="interactively promote candidates to datasets")
    p_rev.add_argument("--approve", help="comma-separated case names to approve non-interactively")

    args = parser.parse_args()

    if args.command == "eval":
        from .run_eval import run_eval

        cfg = load_config(agent_model=args.model, judge_model=args.judge_model)
        asyncio.run(
            run_eval(
                cfg,
                tag=args.tag,
                perspective=args.perspective,
                case=args.case,
                repeat=args.repeat,
                label=args.label,
            )
        )
    elif args.command == "generate":
        from .generate import generate

        cfg = load_config()
        asyncio.run(generate(cfg, perspective=args.perspective, n=args.n, business=args.business))
    elif args.command == "critic":
        from .critic import critique

        cfg = load_config()
        asyncio.run(critique(cfg))
    elif args.command == "review":
        from .review import review

        review(approve=args.approve)


if __name__ == "__main__":
    main()
