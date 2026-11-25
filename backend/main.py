
from pathlib import Path

from engine.profiler import profile_dataset
from engine.quality_checker import run_quality_checks
from engine.scoring import generate_scoring_report


# ==========================================
# FUNCTION 1: PRINT QUALITY DETECTION REPORT
# ==========================================

def print_quality_report(issues):

    print("\n")
    print("=" * 60)
    print("       DATAGUARD AI - QUALITY DETECTION REPORT")
    print("=" * 60)

    if not issues:
        print("\nNo quality issues detected.")
        return

    print("\nTotal Issues Detected:", len(issues))

    severity_levels = ["Critical", "High", "Medium", "Low"]

    print("\nSEVERITY SUMMARY")

    for severity in severity_levels:

        count = sum(
            1 for issue in issues
            if issue["severity"] == severity
        )

        print(f"{severity}: {count}")

    print("\nDETAILED ISSUE REPORT")

    for number, issue in enumerate(issues, start=1):

        print("\n" + "-" * 60)

        print(f"Issue #{number}")
        print("Rule:", issue["rule"])
        print("Category:", issue["category"])
        print("Severity:", issue["severity"])
        print("Column:", issue["column"])
        print("Affected Records:", issue["count"])
        print("Row Indexes:", issue["rows"])
        print("Description:", issue["description"])
        print("Recommendation:", issue["recommendation"])

    print("\n" + "=" * 60)
    print("QUALITY DETECTION COMPLETED")
    print("=" * 60)


# ==========================================
# FUNCTION 2: PRINT ADVANCED SCORING REPORT
# ==========================================

def print_scoring_report(scoring_report):

    dimension_scores = scoring_report["dimension_scores"]

    overall_score = scoring_report["overall_score"]

    quality_rating = scoring_report["quality_rating"]

    dimension_weights = scoring_report["dimension_weights"]

    print("\n")
    print("=" * 60)
    print("       DATAGUARD AI - ADVANCED QUALITY SCORE")
    print("=" * 60)

    print("\nDIMENSION SCORES")

    for dimension, score in dimension_scores.items():

        weight = dimension_weights[dimension] * 100

        print(
            f"{dimension}: {score}/100 "
            f"(Weight: {weight:.0f}%)"
        )

    print("\nOverall Quality Score:", overall_score, "/100")

    print("Quality Rating:", quality_rating)

    print("\nISSUE IMPACT EXPLANATIONS")

    explanations = scoring_report["issue_explanations"]

    if not explanations:

        print("No quality issues detected.")

    else:

        for number, explanation in enumerate(explanations, start=1):

            print("\nIssue:", number)
            print("Rule:", explanation["rule"])
            print("Category:", explanation["category"])
            print("Column:", explanation["column"])
            print("Severity:", explanation["severity"])

            print(
                "Affected Records:",
                explanation["affected_records"]
            )

            print(
                "Affected Percentage:",
                explanation["affected_percentage"],
                "%"
            )

            print("Penalty:", explanation["penalty"])

            print("Explanation:", explanation["explanation"])

    print("\n" + "=" * 60)
    print("ADVANCED QUALITY SCORING COMPLETED")
    print("=" * 60)


# ==========================================
# FUNCTION 3: MAIN APPLICATION
# ==========================================

def main():

    print("\n")
    print("=" * 60)
    print("                  DATAGUARD AI")
    print("       DATA QUALITY INTELLIGENCE PLATFORM")
    print("=" * 60)

    # Find the backend directory
    base_dir = Path(__file__).resolve().parent

    # Locate the sample dataset
    file_path = base_dir / "data" / "sample.csv"

    # STEP 1: DATASET PROFILING

    print("\nSTEP 1: DATASET PROFILING")

    df = profile_dataset(file_path)

    if df is None:

        print("\nApplication stopped: Dataset could not be loaded.")

        return

    # STEP 2: QUALITY ISSUE DETECTION

    print("\nSTEP 2: DATA QUALITY DETECTION")

    issues = run_quality_checks(df)

    print_quality_report(issues)

    # STEP 3: ADVANCED QUALITY SCORING

    print("\nSTEP 3: ADVANCED QUALITY SCORING")

    scoring_report = generate_scoring_report(
        issues,
        len(df)
    )

    print_scoring_report(scoring_report)

    # STEP 4: APPLICATION SUMMARY

    print("\n")
    print("=" * 60)
    print("              DATAGUARD AI SUMMARY")
    print("=" * 60)

    print("Dataset:", file_path.name)

    print("Total Records:", len(df))

    print("Total Columns:", len(df.columns))

    print("Total Quality Issues:", len(issues))

    print(
        "Overall Quality Score:",
        scoring_report["overall_score"],
        "/100"
    )

    print(
        "Final Quality Rating:",
        scoring_report["quality_rating"]
    )

    print("\nDATAGUARD AI EXECUTION COMPLETED SUCCESSFULLY")

    print("=" * 60)


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()
