from __future__ import annotations

import argparse
import json

from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate pairwise LLM preference data with a weighted rubric."
    )
    parser.add_argument("--data", required=True, help="Path to JSONL preference data")
    parser.add_argument("--rubric", required=True, help="Path to rubric JSON")
    parser.add_argument("--output", default="evaluation_report.json")
    args = parser.parse_args()

    report = run_pipeline(args.data, args.rubric, args.output)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
