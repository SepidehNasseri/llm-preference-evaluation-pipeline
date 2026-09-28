from __future__ import annotations

from typing import Any, Dict, Iterable, List

VALID_LABELS = {"A", "B", "tie"}
REQUIRED_FIELDS = {
    "id",
    "prompt",
    "response_a",
    "response_b",
    "human_preference",
    "scores_a",
    "scores_b",
}


def validate_records(records: Iterable[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    seen_ids = set()

    for idx, record in enumerate(records, start=1):
        missing = REQUIRED_FIELDS - set(record)
        if missing:
            errors.append(f"row {idx}: missing fields {sorted(missing)}")
            continue

        record_id = str(record["id"]).strip()
        if not record_id:
            errors.append(f"row {idx}: empty id")
        elif record_id in seen_ids:
            errors.append(f"row {idx}: duplicate id '{record_id}'")
        seen_ids.add(record_id)

        if record["human_preference"] not in VALID_LABELS:
            errors.append(
                f"row {idx}: invalid human_preference "
                f"'{record['human_preference']}'"
            )

        for field in ("prompt", "response_a", "response_b"):
            if not str(record[field]).strip():
                errors.append(f"row {idx}: empty {field}")

        if not isinstance(record["scores_a"], dict):
            errors.append(f"row {idx}: scores_a must be an object")
        if not isinstance(record["scores_b"], dict):
            errors.append(f"row {idx}: scores_b must be an object")

    return errors
