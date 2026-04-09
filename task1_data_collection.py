import requests
import time
import json
import os
from datetime import datetime

# Configuration
HEADERS = {"User-Agent": "TrendPulse/1.0"}
BASE_URL = "https://hacker-news.firebaseio.com/v0"
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def get_category(title):
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword.lower() in title_lower for keyword in keywords):
            return category
    return None

def run_trend_pulse():
    collected_stories = []
    category_counts = {cat: 0 for cat in CATEGORIES}
    
    try:
        # Step 1: Get Top IDs using request
        print("Fetching top stories...")
        id_response = requests.get(f"{BASE_URL}/topstories.json", headers=HEADERS)
        id_response.raise_for_status()
        top_ids = id_response.json()[:500]
        
        # Step 3: Wait between "categories" (after getting the ID list)
        time.sleep(2)

        # Step 2 & 3: Fetch details and handle errors
        for story_id in top_ids:
            # Stop if we have 25 for every category "note:To satisfy the 25-per-category requirement efficiently" 
            if all(count >= 25 for count in category_counts.values()):
                break

            try:
                item_res = requests.get(f"{BASE_URL}/item/{story_id}.json", headers=HEADERS)
                item_res.raise_for_status()
                story = item_res.json()

                if not story or story.get('type') != 'story' or 'title' not in story:
                    continue

                # Step 4: Categorize
                category = get_category(story['title'])
                
                if category and category_counts[category] < 25:
                    # Step 5: Extract Fields
                    entry = {
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": category,
                        "score": story.get("score"),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().isoformat()
                    }
                    collected_stories.append(entry)
                    category_counts[category] += 1
                    
            except Exception as e:
                print(f"Error fetching story {story_id}: {e}")
                continue

        # Step 6: Save to JSON
        if not os.path.exists('data'):
            os.makedirs('data')
            
        filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w') as f:
            json.dump(collected_stories, f, indent=4)
        
        print(f"Collected  {len(collected_stories)} stories. Saved to data/trends_{datetime.now().strftime('%Y%m%d')}.json")

        for cat, count in category_counts.items():
            print(f"- {cat}: {count}")

    except Exception as e:
        print(f"Critical failure: {e}")

if __name__ == "__main__":
    run_trend_pulse()