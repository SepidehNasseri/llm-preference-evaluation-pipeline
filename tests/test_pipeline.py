from llm_pref_eval.pipeline import evaluate_records
from llm_pref_eval.rubric import Rubric


def rubric():
    return Rubric(
        dimensions={
            "correctness": 0.4,
            "relevance": 0.3,
            "clarity": 0.2,
            "safety": 0.1,
        },
        score_min=1,
        score_max=5,
        tie_threshold=0.15,
    )


def test_preference_a():
    r = rubric()
    assert r.preference(
        {"correctness": 5, "relevance": 5, "clarity": 5, "safety": 5},
        {"correctness": 3, "relevance": 4, "clarity": 4, "safety": 5},
    ) == "A"


def test_tie():
    r = rubric()
    scores = {"correctness": 4, "relevance": 4, "clarity": 4, "safety": 5}
    assert r.preference(scores, scores) == "tie"


def test_data_quality_failure():
    report = evaluate_records(
        [{"id": "x"}],
        rubric(),
    )
    assert report["records_valid"] == 0
    assert report["quality_errors"]
