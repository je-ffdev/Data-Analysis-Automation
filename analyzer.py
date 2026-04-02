import pandas as pd

def analyze(df: pd.DataFrame, filename: str) -> dict:
    """Generate summary statistics and correlations for a cleaned DataFrame."""
    print(f"\n--- Analyzing: {filename} ---")
    results = {}

    # 1. Summary statistics for numeric columns
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        print("  ↳ No numeric columns found")
        return results

    print(f"  ↳ Numeric columns: {list(numeric_df.columns)}")
    summary = numeric_df.describe().round(3)
    results["summary"] = summary
    print(summary.to_string())

    # 2. Correlation matrix (only meaningful if 2+ numeric columns)
    if numeric_df.shape[1] >= 2:
        corr = numeric_df.corr().round(3)
        results["correlation"] = corr
        print(f"\n  ↳ Correlation matrix:")
        print(corr.to_string())

    # 3. Value counts for key categorical columns
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    results["value_counts"] = {}
    for col in cat_cols:
        vc = df[col].value_counts().head(5)
        results["value_counts"][col] = vc
        print(f"\n  ↳ Top 5 values in '{col}':")
        print(vc.to_string())

    return results


def analyze_all(cleaned: dict) -> dict:
    """Run analyze on every cleaned DataFrame."""
    all_results = {}
    for filename, df in cleaned.items():
        all_results[filename] = analyze(df, filename)
    return all_results