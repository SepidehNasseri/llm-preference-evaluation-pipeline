from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Dict, List
import json

from .quality import validate_records
from .rubric import Rubric


def load_jsonl(path: str | Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    with Path(path).open() as f:
        for line_number, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc.msg}"
                ) from exc
    return records


def evaluate_records(records: List[Dict[str, Any]], rubric: Rubric) -> Dict[str, Any]:
    quality_errors = validate_records(records)
    if quality_errors:
        return {
            "records_total": len(records),
            "records_valid": 0,
            "quality_errors": quality_errors,
            "agreement_rate": None,
            "predictions": {},
            "results": [],
        }

    results = []
    agreements = 0
    predictions = Counter()

    for record in records:
        score_a = rubric.weighted_score(record["scores_a"])
        score_b = rubric.weighted_score(record["scores_b"])
        predicted = rubric.preference(record["scores_a"], record["scores_b"])
        human = record["human_preference"]
        agreed = predicted == human

        agreements += int(agreed)
        predictions[predicted] += 1

        results.append(
            {
                "id": record["id"],
                "score_a": score_a,
                "score_b": score_b,
                "margin": round(score_a - score_b, 4),
                "human_preference": human,
                "predicted_preference": predicted,
                "agreement": agreed,
            }
        )

    n = len(records)
    return {
        "records_total": n,
        "records_valid": n,
        "quality_errors": [],
        "agreement_rate": round(agreements / n, 4) if n else None,
        "predictions": dict(predictions),
        "results": results,
    }


def run_pipeline(
    data_path: str | Path,
    rubric_path: str | Path,
    output_path: str | Path,
) -> Dict[str, Any]:
    rubric = Rubric.from_json(rubric_path)
    records = load_jsonl(data_path)
    report = evaluate_records(records, rubric)
    Path(output_path).write_text(json.dumps(report, indent=2))
    return report
