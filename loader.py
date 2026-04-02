import pandas as pd
import glob
import os

def load_csvs(folder_path: str) -> dict[str, pd.DataFrame]:
    """Load all CSV files from a folder. Returns a dict of {filename: DataFrame}."""
    pattern = os.path.join(folder_path, "*.csv")
    files = glob.glob(pattern)

    if not files:
        print(f" No CSV files found in: {folder_path}")
        return {}
    
    dataframes = {}
    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            df = pd.read_csv(filepath)
            dataframes[filename] = df
            print(f"✓ Loaded: {filename} — {df.shape[0]} rows, {df.shape[1]} cols")
        except Exception as e:
            print(f"✗ Failed to load {filename}: {e}")
    return dataframes
