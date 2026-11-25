# Problems detect karna
import re
import pandas as pd
import numpy as np


# --------------------------------------------------
# 1. HELPER FUNCTION TO CREATE ISSUE REPORTS
# --------------------------------------------------

def create_issue(
    rule,
    category,
    severity,
    column,
    count,
    rows,
    description,
    recommendation
):

    return {
        "rule": rule,
        "category": category,
        "severity": severity,
        "column": column,
        "count": int(count),
        "rows": list(rows),
        "description": description,
        "recommendation": recommendation
    }


# --------------------------------------------------
# 2. DETECT MISSING VALUES
# --------------------------------------------------

def detect_missing_values(df):

    issues = []

    for column in df.columns:

        missing_rows = df.index[df[column].isnull()].tolist()
        count = len(missing_rows)

        if count > 0:

            percentage = (count / len(df)) * 100 if len(df) else 0

            if percentage >= 30:
                severity = "Critical"
            elif percentage >= 10:
                severity = "High"
            elif percentage >= 5:
                severity = "Medium"
            else:
                severity = "Low"

            issues.append(
                create_issue(
                    "MISSING_VALUES",
                    "Completeness",
                    severity,
                    column,
                    count,
                    missing_rows,
                    f"{column} contains {count} missing values "
                    f"({percentage:.2f}%).",
                    "Review the missing records and consider "
                    "appropriate imputation or removal."
                )
            )

    return issues


# --------------------------------------------------
# 3. DETECT DUPLICATE RECORDS
# --------------------------------------------------

def detect_duplicates(df):

    issues = []

    duplicate_rows = df.index[
        df.duplicated(keep="first")
    ].tolist()

    count = len(duplicate_rows)

    if count > 0:

        percentage = (count / len(df)) * 100 if len(df) else 0

        severity = "High" if percentage >= 20 else "Medium"

        issues.append(
            create_issue(
                "DUPLICATE_RECORDS",
                "Uniqueness",
                severity,
                "All Columns",
                count,
                duplicate_rows,
                f"Found {count} duplicate records.",
                "Review duplicate records before removing them."
            )
        )

    return issues


# --------------------------------------------------
# 4. DETECT INVALID EMAIL ADDRESSES
# --------------------------------------------------

def detect_invalid_emails(df):

    issues = []

    email_columns = [
        column for column in df.columns
        if "email" in str(column).lower()
    ]

    email_pattern = re.compile(
        r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
        r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
        r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$"
    )

    for column in email_columns:

        invalid_rows = []

        for index, value in df[column].items():

            if pd.isna(value):
                continue

            if not isinstance(value, str):
                invalid_rows.append(index)
                continue

            if not email_pattern.fullmatch(value.strip()):
                invalid_rows.append(index)

        if invalid_rows:

            issues.append(
                create_issue(
                    "INVALID_EMAIL",
                    "Validity",
                    "High",
                    column,
                    len(invalid_rows),
                    invalid_rows,
                    f"Found {len(invalid_rows)} invalid email values.",
                    "Review the email format and correct invalid addresses."
                )
            )

    return issues


# --------------------------------------------------
# 5. DETECT INVALID NUMERIC VALUES
# --------------------------------------------------

def detect_invalid_numeric_values(df, column_rules):

    issues = []

    for column, rules in column_rules.items():

        if column not in df.columns:
            continue

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        non_missing = df[column].notna()

        invalid_conversion = (
            non_missing & numeric_values.isna()
        )

        if invalid_conversion.any():

            rows = df.index[invalid_conversion].tolist()

            issues.append(
                create_issue(
                    "INVALID_NUMERIC_TYPE",
                    "Validity",
                    "High",
                    column,
                    len(rows),
                    rows,
                    f"Found non-numeric values in {column}.",
                    "Convert these values into valid numeric values "
                    "after reviewing the original data."
                )
            )

        invalid_mask = pd.Series(
            False,
            index=df.index
        )

        if "min" in rules:
            invalid_mask |= (
                numeric_values < rules["min"]
            )

        if "max" in rules:
            invalid_mask |= (
                numeric_values > rules["max"]
            )

        rows = df.index[invalid_mask.fillna(False)].tolist()

        if rows:

            issues.append(
                create_issue(
                    "OUT_OF_RANGE",
                    "Validity",
                    "High",
                    column,
                    len(rows),
                    rows,
                    f"Found values outside the allowed range "
                    f"for {column}.",
                    f"Review values against the configured "
                    f"minimum and maximum: {rules}."
                )
            )

    return issues


# --------------------------------------------------
# 6. DETECT STATISTICAL OUTLIERS USING IQR
# --------------------------------------------------

def detect_outliers(df):

    issues = []

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        values = df[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)

        outlier_mask = (
            (df[column] < lower_limit) |
            (df[column] > upper_limit)
        ).fillna(False)

        rows = df.index[outlier_mask].tolist()

        if rows:

            issues.append(
                create_issue(
                    "STATISTICAL_OUTLIER",
                    "Consistency",
                    "Medium",
                    column,
                    len(rows),
                    rows,
                    f"Detected {len(rows)} statistical outliers "
                    f"in {column} using the IQR method.",
                    "Investigate unusual values. Do not remove "
                    "them without domain knowledge."
                )
            )

    return issues


# --------------------------------------------------
# 7. DETECT INCONSISTENT CATEGORICAL VALUES
# --------------------------------------------------

def detect_category_inconsistency(df):

    issues = []

    for column in df.select_dtypes(
        include=["object", "string", "category"]
    ).columns:

        values = df[column].dropna()

        if values.empty:
            continue

        normalized = values.astype(str).str.strip().str.casefold()

        groups = {}

        for index, normalized_value in normalized.items():

            original_value = str(df.at[index, column])

            groups.setdefault(normalized_value, set()).add(
                original_value
            )

        inconsistent_groups = [
            variants
            for variants in groups.values()
            if len(variants) > 1
        ]

        if inconsistent_groups:

            affected_values = set().union(*inconsistent_groups)

            rows = values.index[
                values.astype(str).isin(affected_values)
            ].tolist()

            issues.append(
                create_issue(
                    "INCONSISTENT_CATEGORIES",
                    "Consistency",
                    "Low",
                    column,
                    len(rows),
                    rows,
                    f"Found inconsistent formatting in {column}.",
                    "Review capitalization and extra spaces. "
                    "Standardize categories where appropriate."
                )
            )

    return issues


# --------------------------------------------------
# 8. MASTER QUALITY DETECTION FUNCTION
# --------------------------------------------------

def run_quality_checks(df):

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame.")

    issues = []

    if df.empty:
        print("Warning: Dataset contains no rows.")
        return issues

    # Define domain-specific validation rules.
    # These are examples and should be configurable.

    column_rules = {
        "Age": {
            "min": 0,
            "max": 120
        },

        "Salary": {
            "min": 0
        }
    }

    issues.extend(detect_missing_values(df))

    issues.extend(detect_duplicates(df))

    issues.extend(detect_invalid_emails(df))

    issues.extend(
        detect_invalid_numeric_values(df, column_rules)
    )

    issues.extend(detect_outliers(df))

    issues.extend(detect_category_inconsistency(df))

    return issues
