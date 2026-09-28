# LLM Preference Evaluation Pipeline

A lightweight, reproducible Python project for validating preference datasets, applying weighted evaluation rubrics, and measuring agreement between rubric-based rankings and human preference labels.

This repository demonstrates core workflows used in AI/LLM evaluation:
- pairwise preference data
- rubric-based scoring
- data quality validation
- evaluation metrics
- reproducible reporting
- automated tests and CI

## Why this project

Preference data is widely used to compare model outputs and build higher-quality evaluation signals. This project shows how to turn pairwise human-review data into a clean, auditable evaluation pipeline.

## Features

- Validates pairwise preference records before evaluation
- Supports configurable weighted rubrics
- Scores response A and response B across multiple dimensions
- Predicts A / B / tie from rubric-weighted scores
- Measures agreement with human preference labels
- Flags missing fields, invalid labels, duplicates, and score-range violations
- Produces a JSON evaluation report
- Includes unit tests and GitHub Actions CI

## Rubric

The example rubric uses four dimensions:

| Dimension | Weight |
|---|---:|
| Correctness | 0.40 |
| Relevance | 0.30 |
| Clarity | 0.20 |
| Safety | 0.10 |

Weights and score ranges are configurable in `config/rubric.json`.

## Project structure

```text
llm-preference-evaluation-pipeline/
├── config/
│   └── rubric.json
├── data/
│   └── sample_pairs.jsonl
├── src/
│   └── llm_pref_eval/
│       ├── __init__.py
│       ├── cli.py
│       ├── pipeline.py
│       ├── quality.py
│       └── rubric.py
├── tests/
│   └── test_pipeline.py
├── .github/workflows/
│   └── ci.yml
├── pyproject.toml
└── README.md
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
llm-pref-eval \
  --data data/sample_pairs.jsonl \
  --rubric config/rubric.json \
  --output evaluation_report.json
```

## Example output

```json
{
  "records_total": 5,
  "records_valid": 5,
  "agreement_rate": 0.8,
  "predictions": {
    "A": 2,
    "B": 2,
    "tie": 1
  }
}
```

## Data format

Each JSONL record contains:
- `id`
- `prompt`
- `response_a`
- `response_b`
- `human_preference`: `A`, `B`, or `tie`
- dimension scores for each response

Example:

```json
{
  "id": "ex-001",
  "prompt": "Explain precision vs recall.",
  "response_a": "...",
  "response_b": "...",
  "human_preference": "A",
  "scores_a": {"correctness": 5, "relevance": 5, "clarity": 4, "safety": 5},
  "scores_b": {"correctness": 4, "relevance": 4, "clarity": 4, "safety": 5}
}
```

## Notes

This is a portfolio project focused on evaluation infrastructure and data quality. It does not call external LLM APIs, so it is deterministic, inexpensive to run, and easy to audit.
