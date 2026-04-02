from loader import load_csvs
from cleaner import clean_all
data = load_csvs("./sample_data")
cleaned = clean_all(data)


from visualizer import visualize_all

visualize_all(cleaned)


#from analyzer import analyze_all

#results = analyze_all(cleaned)


#for name, df in cleaned.items():
#    print(f"\nCleaned columns in {name}:")
#    for col in df.columns:
#        print(f"  '{col}': dtype={df[col].dtype}, sample={df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else 'EMPTY'}")
