import argparse
from loader import load_csvs
from cleaner import clean_all
from analyzer import analyze_all
from visualizer import visualize_all

def main():
    parser = argparse.ArgumentParser(description="Automated CSV Data Analyzer")
    parser.add_argument("folder", help="Path to folder containing CSV files")
    args = parser.parse_args()

    print("=" * 50)
    print("  JBP CSV Analyzer")
    print("=" * 50)

    # Step 1 - Load
    data = load_csvs(args.folder)
    if not data:
        print("No data to process. Exiting.")
        return

    # Step 2 - Clean
    cleaned = clean_all(data)

    # Step 3 - Analyze
    analyze_all(cleaned)

    # Step 4 - Visualize
    visualize_all(cleaned)

    print("\n✓ Pipeline complete. Plots saved to ./output_plots/")

if __name__ == "__main__":
    main()