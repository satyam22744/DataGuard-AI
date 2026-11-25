# Dataset ko samajhna
import pandas as pd
def load_dataset(file_path):

    try:
        df = pd.read_csv(file_path)
        print("\nDataset loaded successfully!")
        return df

    except FileNotFoundError:
        print("\nError: Dataset file not found.")
        return None

    except pd.errors.EmptyDataError:
        print("\nError: Dataset is empty.")
        return None

    except Exception as error:
        print("\nError while loading dataset:", error)
        return None


def dataset_overview(df):

    print("\n========== DATASET OVERVIEW ==========")

    print("Total Rows:", df.shape[0])
    print("Total Columns:", df.shape[1])
    print("Total Cells:", df.size)

    print("\nColumn Names:")
    print(list(df.columns))


def column_information(df):

    print("\n========== COLUMN INFORMATION ==========")

    df.info()


def missing_value_analysis(df):

    print("\n========== MISSING VALUE ANALYSIS ==========")

    missing = df.isnull().sum()

    if len(df) > 0:
        percentage = (missing / len(df)) * 100
    else:
        percentage = pd.Series(0.0, index=df.columns)

    result = pd.DataFrame({
        "Missing Values": missing,
        "Missing Percentage": percentage
    })

    print(result)


def duplicate_analysis(df):

    print("\n========== DUPLICATE ANALYSIS ==========")

    duplicates = df.duplicated().sum()

    print("Total Duplicate Records:", duplicates)


def statistical_summary(df):

    print("\n========== STATISTICAL SUMMARY ==========")

    print(df.describe(include="all").to_string())


def profile_dataset(file_path):

    df = load_dataset(file_path)

    if df is None:
        return None

    dataset_overview(df)
    column_information(df)
    missing_value_analysis(df)
    duplicate_analysis(df)
    statistical_summary(df)

    return df

