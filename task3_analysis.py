import pandas as pd
import numpy as np

# STEP 1 - Load and Explore
df = pd.read_csv('data/trends_clean.csv')

print(f"Loaded data: {df.shape}\n")
print("First 5 rows:")
print(df[['post_id', 'title', 'category', 'score', 'num_comments']].head())
print()

avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()
print(f"Average score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

# STEP 2 — Basic Analysis with NumPy
scores = df['score'].to_numpy()

print("\n--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):,.0f}")
print(f"Median score : {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score    : {np.max(scores):,}")
print(f"Min score    : {np.min(scores):,}")

# Category analysis
category_counts = df['category'].value_counts()
top_cat = category_counts.idxmax()
top_count = category_counts.max()
print(f"\nMost stories in: {top_cat} ({top_count} stories)")

# Most commented story
top_commented_idx = df['num_comments'].idxmax()
top_title = df.loc[top_commented_idx, 'title']
top_comments = df.loc[top_commented_idx, 'num_comments']
print(f"Most commented story: \"{top_title}\"  — {top_comments:,} comments")

# STEP 3 — Add New Columns
df['engagement'] = df['num_comments'] / (df['score'] + 1)
df['is_popular'] = df['score'] > avg_score

# STEP 4 — Save the Result
output_path = 'data/trends_analysed.csv'
df.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")