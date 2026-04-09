import pandas as pd
import glob
import os

# Configuration
INPUT_PATTERN = "data/trends_20260409.json"
OUTPUT_FILE = "data/trends_clean.csv"

# STEP 1 - Load Data
files = glob.glob(INPUT_PATTERN)
if not files:
    print("No data found.")
else:
    latest_file = max(files, key=os.path.getctime)
    df = pd.read_json(latest_file)
    print(f"Loaded {len(df)} stories from {latest_file}\n")

    # STEP 2 - Clean the Data
    # Duplicates
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")
    
    # Missing values
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")
    
    # Data types
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)
    
    # Low quality
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}\n")
    
    # Whitespace
    df['title'] = df['title'].str.strip()

    # STEP 3 - Save as CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_FILE}\n")
    
    print("Stories per category:")
    # Formatting the value counts to match your indented output
    counts = df['category'].value_counts()
    for category, count in counts.items():
        print(f"  {category:<15} {count}")