import pandas as pd
import matplotlib.pyplot as plt
import os

# STEP 1 — Setup
df = pd.read_csv('data/trends_analysed.csv')
if not os.path.exists('outputs'):
    os.makedirs('outputs')

def shorten_title(t):
    return t[:47] + "..." if len(str(t)) > 50 else t

# STEP 2 — Chart 1: Top 10 Stories by Score
plt.figure(figsize=(10, 6))
top_10 = df.nlargest(10, 'score').sort_values('score')
plt.barh(top_10['title'].apply(shorten_title), top_10['score'], color='teal')
plt.title('Top 10 Stories by Score')
plt.xlabel('Score')
plt.tight_layout()
plt.savefig('outputs/chart1_top_stories.png')
plt.close()

# STEP 3 — Chart 2: Stories per Category
plt.figure(figsize=(8, 6))
cat_counts = df['category'].value_counts()
colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#FFF333']
cat_counts.plot(kind='bar', color=colors[:len(cat_counts)])
plt.title('Stories per Category')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/chart2_categories.png')
plt.close()

# STEP 4 — Chart 3: Score vs Comments
plt.figure(figsize=(8, 6))
for status, group in df.groupby('is_popular'):
    plt.scatter(group['score'], group['num_comments'], 
                label='Popular' if status else 'Not Popular', alpha=0.6)
plt.title('Score vs Comments')
plt.xlabel('Score')
plt.ylabel('Comments')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/chart3_scatter.png')
plt.close()

# STEP 5 - Dashboard
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('TrendPulse Dashboard', fontsize=16)

# Dashboard Column 1: Top Stories
axes[0].barh(top_10['title'].apply(shorten_title), top_10['score'], color='teal')
axes[0].set_title('Top 10 Stories')

# Dashboard Column 2: Category Count
axes[1].bar(cat_counts.index, cat_counts.values, color='orange')
axes[1].set_title('Category Distribution')
axes[1].tick_params(axis='x', rotation=45)

# Dashboard Column 3: Correlation
for status, group in df.groupby('is_popular'):
    axes[2].scatter(group['score'], group['num_comments'], alpha=0.5)
axes[2].set_title('Score vs Comments')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('outputs/dashboard.png')
plt.show()
