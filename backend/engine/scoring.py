
# ==============================================
# DATAGUARD AI - ADAPTIVE SCORING ENGINE
# Milestone 3.2
# ==============================================


# 1. CONFIGURABLE SCORING POLICY

DIMENSION_WEIGHTS = {
    "Completeness": 0.30,
    "Validity": 0.30,
    "Uniqueness": 0.20,
    "Consistency": 0.20
}

SEVERITY_PENALTIES = {
    "Critical": 20,
    "High": 12,
    "Medium": 6,
    "Low": 2
}

SEVERITY_RANK = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4
}


# 2. CALCULATE IMPACT MULTIPLIER

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


# 3. IDENTIFY UNIQUE AFFECTED RECORDS

def collect_dimension_impact(issues, category):

    row_severity = {}
    affected_columns = set()
    matching_issues = []
    fallback_count = 0

    for issue in issues:

        if issue.get("category") != category:
            continue

        matching_issues.append(issue)

        column = issue.get("column")

        if column and column != "All Columns":
            affected_columns.add(column)

        severity = issue.get("severity", "Low")

        severity_rank = SEVERITY_RANK.get(severity, 1)

        rows = issue.get("rows", [])

        if rows:

            for row_index in rows:

                current_rank = row_severity.get(row_index, 0)

                if severity_rank > current_rank:
                    row_severity[row_index] = severity_rank

        else:
            # Fallback when row indexes are unavailable
            fallback_count += issue.get("count", 0)

    unique_affected_records = len(row_severity) + fallback_count

    highest_severity = "Low"

    if row_severity:

        highest_rank = max(row_severity.values())

        for severity, rank in SEVERITY_RANK.items():

            if rank == highest_rank:
                highest_severity = severity

    elif matching_issues:

        highest_severity = max(
            matching_issues,
            key=lambda issue: SEVERITY_RANK.get(
                issue.get("severity", "Low"), 1
            )
        ).get("severity", "Low")

    return {
        "affected_records": unique_affected_records,
        "affected_columns": sorted(affected_columns),
        "highest_severity": highest_severity,
        "matching_issues": len(matching_issues),
        "unique_rows_available": len(row_severity)
    }


# 4. CALCULATE ADAPTIVE DIMENSION PENALTY


def calculate_dimension_impact(issues, category, total_rows):

    impact_data = collect_dimension_impact(
        issues, category
    )

    # No issues means a perfect score
    if impact_data["matching_issues"] == 0:

        impact_data.update({
            "category": category,
            "affected_percentage": 0,
            "base_penalty": 0,
            "impact_multiplier": 0,
            "final_penalty": 0,
            "score": 100
        })

        return impact_data

    affected_records = impact_data["affected_records"]

    if total_rows <= 0:
        affected_percentage = 0

    else:
        affected_percentage = min(
            100,
            (affected_records / total_rows) * 100
        )

    severity = impact_data["highest_severity"]

    base_penalty = SEVERITY_PENALTIES.get(
        severity, 0
    )

    impact_multiplier = get_impact_multiplier(
        affected_percentage
    )

    final_penalty = base_penalty * impact_multiplier

    dimension_score = max(
        0,
        100 - final_penalty
    )

    impact_data.update({
        "category": category,
        "affected_percentage": round(
            affected_percentage, 2
        ),
        "base_penalty": base_penalty,
        "impact_multiplier": impact_multiplier,
        "final_penalty": round(final_penalty, 2),
        "score": round(dimension_score, 2)
    })

    return impact_data


    impact_data = collect_dimension_impact(
        issues, category
    )

    affected_records = impact_data["affected_records"]

    if total_rows <= 0:
        affected_percentage = 0

    else:
        affected_percentage = min(
            100,
            (affected_records / total_rows) * 100
        )

    severity = impact_data["highest_severity"]

    base_penalty = SEVERITY_PENALTIES.get(
        severity, 0
    )

    impact_multiplier = get_impact_multiplier(
        affected_percentage
    )

    final_penalty = base_penalty * impact_multiplier

    dimension_score = max(
        0,
        100 - final_penalty
    )

    impact_data.update({
        "category": category,
        "affected_percentage": round(
            affected_percentage, 2
        ),
        "base_penalty": base_penalty,
        "impact_multiplier": impact_multiplier,
        "final_penalty": round(final_penalty, 2),
        "score": round(dimension_score, 2)
    })

    return impact_data


# 5. CALCULATE ONE DIMENSION SCORE

def calculate_dimension_score(
    issues, category, total_rows=0
):

    impact = calculate_dimension_impact(
        issues, category, total_rows
    )

    return impact["score"]


# 6. CALCULATE ALL DIMENSION SCORES

def calculate_all_dimension_scores(
    issues, total_rows=0
):

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

    return round(
        weighted_score / total_weight,
        2
    )


# 8. GENERATE QUALITY RATING

def get_quality_rating(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 50:
        return "Average"

    else:
        return "Poor"


# 9. GENERATE ISSUE EXPLANATIONS

def explain_issues(issues, total_rows):

    explanations = []

    for issue in issues:

        count = issue.get("count", 0)

        rows = issue.get("rows", [])

        severity = issue.get("severity", "Low")

        if total_rows > 0:

            percentage = min(
                100,
                (count / total_rows) * 100
            )

        else:
            percentage = 0

        explanations.append({

            "rule": issue.get("rule"),

            "category": issue.get("category"),

            "column": issue.get("column"),

            "severity": severity,

            "affected_records": count,

            "affected_percentage": round(
                percentage, 2
            ),

            "row_indexes": rows,

            "recommendation": issue.get(
                "recommendation",
                "Review the affected records."
            ),

            "explanation": (
                f"{count} records were flagged "
                f"by {issue.get('rule')}. "
                f"The issue affects approximately "
                f"{percentage:.2f}% of the dataset."
            )
        })

    return explanations


# 10. GENERATE COLUMN-LEVEL IMPACT REPORT

def generate_column_impact(issues, total_rows):

    column_report = {}

    for issue in issues:

        column = issue.get("column", "Unknown")

        if column == "All Columns":
            continue

        if column not in column_report:

            column_report[column] = {
                "issue_count": 0,
                "affected_rows": set(),
                "rules": set()
            }

        column_report[column]["issue_count"] += 1

        column_report[column]["rules"].add(
            issue.get("rule", "Unknown")
        )

        for row_index in issue.get("rows", []):

            column_report[column]["affected_rows"].add(
                row_index
            )

    final_report = {}

    for column, data in column_report.items():

        affected = len(data["affected_rows"])

        percentage = 0

        if total_rows > 0:

            percentage = (
                affected / total_rows
            ) * 100

        final_report[column] = {

            "issue_count": data["issue_count"],

            "affected_records": affected,

            "affected_percentage": round(
                percentage, 2
            ),

            "rules": sorted(data["rules"])
        }

    return final_report


# 11. GENERATE ACTIONABLE RECOMMENDATIONS

def generate_recommendations(
    dimension_details, column_impact
):

    recommendations = []

    for dimension, details in dimension_details.items():

        if details["affected_records"] == 0:
            continue

        recommendations.append({

            "dimension": dimension,

            "severity": details["highest_severity"],

            "affected_records": details["affected_records"],

            "recommendation": (
                f"Investigate {details['affected_records']} "
                f"affected records in the {dimension} dimension."
            )
        })

    for column, details in column_impact.items():

        recommendations.append({

            "column": column,

            "affected_records": details["affected_records"],

            "recommendation": (
                f"Review column '{column}', which has "
                f"{details['issue_count']} detected findings."
            )
        })

    return recommendations


# 12. GENERATE COMPLETE SCORING REPORT

def generate_scoring_report(issues, total_rows):

    dimension_details = {}

    dimension_scores = {}

    for dimension in DIMENSION_WEIGHTS:

        details = calculate_dimension_impact(
            issues,
            dimension,
            total_rows
        )

        dimension_details[dimension] = details

        dimension_scores[dimension] = details["score"]

    overall_score = calculate_overall_score(
        dimension_scores
    )

    quality_rating = get_quality_rating(
        overall_score
    )

    issue_explanations = explain_issues(
        issues,
        total_rows
    )

    column_impact = generate_column_impact(
        issues,
        total_rows
    )

    recommendations = generate_recommendations(
        dimension_details,
        column_impact
    )

    return {

        "dimension_scores": dimension_scores,

        "dimension_details": dimension_details,

        "overall_score": overall_score,

        "quality_rating": quality_rating,

        "issue_explanations": issue_explanations,

        "column_impact": column_impact,

        "recommendations": recommendations,

        "dimension_weights": DIMENSION_WEIGHTS.copy()
    }
