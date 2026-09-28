from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict
import json


@dataclass(frozen=True)
class Rubric:
    dimensions: Dict[str, float]
    score_min: float
    score_max: float
    tie_threshold: float

    @classmethod
    def from_json(cls, path: str | Path) -> "Rubric":
        payload = json.loads(Path(path).read_text())
        dimensions = payload["dimensions"]

        total_weight = sum(dimensions.values())
        if abs(total_weight - 1.0) > 1e-9:
            raise ValueError(f"Rubric weights must sum to 1.0; got {total_weight:.4f}")

        if payload["score_min"] >= payload["score_max"]:
            raise ValueError("score_min must be less than score_max")

        return cls(
            dimensions=dimensions,
            score_min=float(payload["score_min"]),
            score_max=float(payload["score_max"]),
            tie_threshold=float(payload.get("tie_threshold", 0.0)),
        )

    def weighted_score(self, scores: Dict[str, float]) -> float:
        missing = set(self.dimensions) - set(scores)
        if missing:
            raise ValueError(f"Missing rubric dimensions: {sorted(missing)}")

        total = 0.0
        for name, weight in self.dimensions.items():
            value = float(scores[name])
            if not self.score_min <= value <= self.score_max:
                raise ValueError(
                    f"{name}={value} outside allowed range "
                    f"[{self.score_min}, {self.score_max}]"
                )
            total += value * weight
        return round(total, 4)

    def preference(self, scores_a: Dict[str, float], scores_b: Dict[str, float]) -> str:
        score_a = self.weighted_score(scores_a)
        score_b = self.weighted_score(scores_b)
        delta = score_a - score_b

        if abs(delta) <= self.tie_threshold:
            return "tie"
        return "A" if delta > 0 else "B"
