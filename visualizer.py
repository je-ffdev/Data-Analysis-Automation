import matplotlib
matplotlib.use("Agg")  # must be before importing pyplot
import matplotlib.pyplot as plt
import pandas as pd
import os

OUTPUT_DIR = "./output_plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_distribution(df: pd.DataFrame, filename: str):
    """Histogram of all numeric columns."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return

    for col in numeric_cols[:3]:  # limit to first 3 numeric cols
        plt.figure(figsize=(10, 5))
        df[col].dropna().plot.hist(bins=50, color="steelblue", edgecolor="white")
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, f"{filename}_{col}_distribution.png")
        plt.savefig(path)
        plt.close()
        print(f"  ↳ Saved: {path}")


def plot_top_categories(df: pd.DataFrame, filename: str):
    """Bar chart — top value counts for first categorical column."""
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    if not cat_cols:
        return

    col = cat_cols[0]  # use first categorical column
    top = df[col].value_counts().head(10)

    plt.figure(figsize=(12, 6))
    top.sort_values().plot.barh(color="steelblue", edgecolor="white")
    plt.title(f"Top values in '{col}'")
    plt.xlabel("Count")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, f"{filename}_{col}_top_values.png")
    plt.savefig(path)
    plt.close()
    print(f"  ↳ Saved: {path}")


def plot_correlation(df: pd.DataFrame, filename: str):
    """Heatmap-style correlation table as a chart."""
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        return

    corr = numeric_df.corr().round(2)
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(corr.columns, fontsize=8)
    plt.colorbar(im, ax=ax)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, f"{filename}_correlation.png")
    plt.savefig(path)
    plt.close()
    print(f"  ↳ Saved: {path}")


def visualize_all(cleaned: dict):
    for filename, df in cleaned.items():
        print(f"\n--- Visualizing: {filename} ---")
        plot_distribution(df, filename)
        plot_top_categories(df, filename)
        plot_correlation(df, filename)