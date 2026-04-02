import pandas as pd

def clean_dataframe(df: pd.DataFrame, filename: str) -> pd.DataFrame:
    """Clean a single DataFrame — standardize columns, handle nulls, fix types."""
    print(f"\n--- Cleaning: {filename} ---")
    original_shape = df.shape

    # 1. Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # 2. Drop fully empty rows and columns
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)

    # 3. Drop duplicate rows
    before_dedup = len(df)
    df.drop_duplicates(inplace=True)
    dupes_removed = before_dedup - len(df)
    if dupes_removed > 0:
        print(f"  ↳ Removed {dupes_removed} duplicate row(s)")

    # 4. Infer better data types (e.g. "123" stored as string → int)
    df = df.infer_objects()

    # 5. Try to convert object columns to numeric where possible
    for col in df.select_dtypes(include="object").columns:
        non_null_values = df[col].dropna()
        if len(non_null_values) == 0:
            continue
        try:
            converted = pd.to_numeric(non_null_values)
            if len(converted) == len(non_null_values):
                df[col] = pd.to_numeric(df[col], errors="coerce")
                print(f"  ↳ Converted column '{col}' to numeric")
        except (ValueError, TypeError):
            pass  # leave text columns alone

    # 6. Report missing values
    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if not null_cols.empty:
        print(f"  ↳ Columns with missing values:")
        for col, count in null_cols.items():
            pct = (count / len(df)) * 100
            print(f"      '{col}': {count} missing ({pct:.1f}%)")
    else:
        print(f"  ↳ No missing values found")

    print(f"  ↳ Shape: {original_shape} → {df.shape}")
    return df


def clean_all(dataframes: dict) -> dict:
    """Run clean_dataframe on every loaded CSV."""
    cleaned = {}
    for filename, df in dataframes.items():
        cleaned[filename] = clean_dataframe(df, filename)
    return cleaned
