
import pytest

from engine.scoring import (
    calculate_dimension_score,
    calculate_all_dimension_scores,
    calculate_overall_score,
    get_quality_rating,
    calculate_dimension_impact,
    generate_scoring_report
)


# ==========================================
# TEST 1: CLEAN DATASET
# ==========================================

def test_clean_dataset_gets_full_score():

    issues = []

    scores = calculate_all_dimension_scores(
        issues,
        total_rows=100
    )

    for score in scores.values():
        assert score == 100


# ==========================================
# TEST 2: OVERALL SCORE
# ==========================================

def test_overall_score_calculation():

    dimension_scores = {
        "Completeness": 80,
        "Validity": 90,
        "Uniqueness": 100,
        "Consistency": 70
    }

    result = calculate_overall_score(
        dimension_scores
    )

    assert result == 85


# ==========================================
# TEST 3: QUALITY RATINGS
# ==========================================

@pytest.mark.parametrize(
    "score, expected",
    [
        (95, "Excellent"),
        (80, "Good"),
        (60, "Average"),
        (30, "Poor")
    ]
)
def test_quality_rating(score, expected):

    result = get_quality_rating(score)

    assert result == expected


# ==========================================
# TEST 4: OVERLAPPING RECORDS
# ==========================================

def test_overlapping_rows_are_counted_once():

    issues = [
        {
            "rule": "OUT_OF_RANGE",
            "category": "Validity",
            "severity": "High",
            "count": 1,
            "rows": [5],
            "column": "Age"
        },
        {
            "rule": "STATISTICAL_OUTLIER",
            "category": "Validity",
            "severity": "Medium",
            "count": 1,
            "rows": [5],
            "column": "Age"
        }
    ]

    result = calculate_dimension_impact(
        issues,
        "Validity",
        total_rows=100
    )

    assert result["affected_records"] == 1

    assert result["highest_severity"] == "High"


# ==========================================
# TEST 5: MORE AFFECTED RECORDS
# ==========================================

def test_more_affected_records_increase_penalty():

    one_record_issue = [
        {
            "rule": "MISSING_VALUES",
            "category": "Completeness",
            "severity": "High",
            "count": 1,
            "rows": [1],
            "column": "Email"
        }
    ]

    many_record_issue = [
        {
            "rule": "MISSING_VALUES",
            "category": "Completeness",
            "severity": "High",
            "count": 100,
            "rows": list(range(100)),
            "column": "Email"
        }
    ]

    small_impact = calculate_dimension_impact(
        one_record_issue,
        "Completeness",
        1000
    )

    large_impact = calculate_dimension_impact(
        many_record_issue,
        "Completeness",
        1000
    )

    assert (
        large_impact["final_penalty"]
        >
        small_impact["final_penalty"]
    )


# ==========================================
# TEST 6: EMPTY DATASET SIZE
# ==========================================

def test_zero_rows_do_not_crash():

    result = calculate_dimension_score(
        [],
        "Completeness",
        total_rows=0
    )

    assert result == 100


# ==========================================
# TEST 7: SCORES NEVER GO BELOW ZERO
# ==========================================

def test_dimension_score_never_negative():

    issues = [
        {
            "rule": "MISSING_VALUES",
            "category": "Completeness",
            "severity": "Critical",
            "count": 100,
            "rows": list(range(100)),
            "column": "Email"
        }
    ]

    score = calculate_dimension_score(
        issues,
        "Completeness",
        total_rows=100
    )

    assert score >= 0


# ==========================================
# TEST 8: COMPLETE SCORING REPORT
# ==========================================

def test_complete_scoring_report():

    report = generate_scoring_report(
        issues=[],
        total_rows=100
    )

    assert report["overall_score"] == 100

    assert report["quality_rating"] == "Excellent"

    assert len(report["dimension_scores"]) == 4

    assert report["issue_explanations"] == []

    assert report["recommendations"] == []
