# ==========================================
# DATAGUARD AI - ADVANCED SCORING ENGINE
# ==========================================

# 1. CONFIGURABLE DIMENSION WEIGHTS

DIMENSION_WEIGHTS = {
    "Completeness": 0.30,
    "Validity": 0.30,
    "Uniqueness": 0.20,
    "Consistency": 0.20
}


# 2. SEVERITY-BASED PENALTIES

SEVERITY_PENALTIES = {
    "Critical": 20,
    "High": 12,
    "Medium": 6,
    "Low": 2
}


# 3. IMPACT MULTIPLIERS

def get_impact_multiplier(affected_percentage):

    if affected_percentage <= 1:
        return 0.5

    elif affected_percentage <= 5:
        return 0.75

    elif affected_percentage <= 15:
        return 1.0

    elif affected_percentage <= 30:
        return 1.25

    else:
        return 1.5


# 4. CALCULATE ISSUE IMPACT

def calculate_issue_impact(issue, total_rows):

    affected_records = issue.get("count", 0)

    if total_rows <= 0:
        affected_percentage = 0

    else:
        affected_percentage = (
            affected_records / total_rows
        ) * 100

    severity = issue.get("severity", "Low")

    base_penalty = SEVERITY_PENALTIES.get(severity, 0)

    impact_multiplier = get_impact_multiplier(
        affected_percentage
    )

    penalty = base_penalty * impact_multiplier

    return {
        "affected_records": affected_records,
        "affected_percentage": round(affected_percentage, 2),
        "severity": severity,
        "base_penalty": base_penalty,
        "impact_multiplier": impact_multiplier,
        "final_penalty": round(penalty, 2)
    }


# 5. CALCULATE SCORE FOR ONE DIMENSION

def calculate_dimension_score(issues, category, total_rows=0):

    total_penalty = 0

    for issue in issues:

        if issue.get("category") == category:

            impact = calculate_issue_impact(
                issue, total_rows
            )

            total_penalty += impact["final_penalty"]

    score = max(0, 100 - total_penalty)

    return round(score, 2)


# 6. CALCULATE ALL DIMENSION SCORES

def calculate_all_dimension_scores(issues, total_rows=0):

    scores = {}

    for dimension in DIMENSION_WEIGHTS:

        scores[dimension] = calculate_dimension_score(
            issues,
            dimension,
            total_rows
        )

    return scores


# 7. CALCULATE WEIGHTED OVERALL SCORE

def calculate_overall_score(dimension_scores):

    if not dimension_scores:
        return 0

    weighted_score = 0
    total_weight = 0

    for dimension, weight in DIMENSION_WEIGHTS.items():

        if dimension in dimension_scores:

            weighted_score += (
                dimension_scores[dimension] * weight
            )

            total_weight += weight

    if total_weight == 0:
        return 0

    overall_score = weighted_score / total_weight

    return round(overall_score, 2)


# 8. CONVERT SCORE INTO QUALITY RATING

def get_quality_rating(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 50:
        return "Average"

    else:
        return "Poor"


# 9. EXPLAIN EACH DETECTED ISSUE

def explain_issues(issues, total_rows):

    explanations = []

    for issue in issues:

        impact = calculate_issue_impact(
            issue, total_rows
        )

        explanations.append({
            "rule": issue.get("rule"),
            "category": issue.get("category"),
            "column": issue.get("column"),
            "severity": impact["severity"],
            "affected_records": impact["affected_records"],
            "affected_percentage": impact["affected_percentage"],
            "penalty": impact["final_penalty"],
            "explanation": (
                f"{impact['affected_records']} records affected "
                f"({impact['affected_percentage']}%). "
                f"{impact['severity']} severity resulted in "
                f"a {impact['final_penalty']} point penalty."
            )
        })

    return explanations


# 10. GENERATE COMPLETE SCORING REPORT

def generate_scoring_report(issues, total_rows):

    dimension_scores = calculate_all_dimension_scores(
        issues, total_rows
    )

    overall_score = calculate_overall_score(
        dimension_scores
    )

    quality_rating = get_quality_rating(
        overall_score
    )

    issue_explanations = explain_issues(
        issues, total_rows
    )

    return {
        "dimension_scores": dimension_scores,
        "overall_score": overall_score,
        "quality_rating": quality_rating,
        "issue_explanations": issue_explanations,
        "dimension_weights": DIMENSION_WEIGHTS.copy()
    }