import pandas as pd
from collections import Counter
import re

def analyze_reviews():
    print("Loading reviews...")
    df = pd.read_csv('moveinsync_reviews.csv')
    
    # Filter for low ratings (1, 2, and 3 stars)
    low_reviews = df[df['score'] <= 3].copy()
    
    print(f"Total low ratings (1-3 stars): {len(low_reviews)}")
    
    # Define keywords for product/engineering categories vs operational categories
    categories = {
        'Authentication (OTP/Login)': ['otp', 'login', 'log in', 'password', 'sign in', 'authenticate', 'number'],
        'App Performance (Crash/Lag)': ['crash', 'hang', 'slow', 'freeze', 'loading', 'lag', 'stuck', 'not opening', 'glitch', 'bug', 'worst app'],
        'Location/Map Tracking': ['location', 'gps', 'map', 'tracking', 'track', 'route', 'wrong path', 'navigation'],
        'Booking/UI Experience': ['book', 'schedule', 'shift', 'roster', 'cancel', 'reschedule', 'ui', 'interface', 'update'],
        'Operational (Driver/Cab)': ['driver', 'cab', 'vehicle', 'late', 'rude', 'dirty', "didn't come", 'no show', 'ac']
    }

    def categorize(text):
        text = str(text).lower()
        cats = []
        for cat, keywords in categories.items():
            if any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in keywords) or \
               any(kw in text for kw in ['didn\'t come', 'not opening', 'worst app', 'wrong path']):
                cats.append(cat)
        return ', '.join(cats) if cats else 'Uncategorized/Vague'

    low_reviews['category'] = low_reviews['content'].apply(categorize)
    
    # Count frequencies
    cat_counts = Counter()
    for cats in low_reviews['category']:
        for c in cats.split(', '):
            if c:
                cat_counts[c] += 1
                
    print("\n--- Primary Complaint Categories (1-3 Star Reviews) ---")
    for cat, count in cat_counts.most_common():
        print(f"{cat}: {count} reviews ({count/len(low_reviews)*100:.1f}%)")
        
    print("\n--- Recent 1-Star Quotes for Top Engineering Issues ---")
    # Let's show recent examples of App Performance and Location tracking to frame the problem
    eng_reviews = low_reviews[low_reviews['category'].str.contains('App Performance|Location')]
    recent_eng = eng_reviews.sort_values('at', ascending=False).head(10)
    
    for idx, row in recent_eng.iterrows():
        print(f"[{row['at'][:10]}] v{row['reviewCreatedVersion']}: {row['content']}")

if __name__ == "__main__":
    analyze_reviews()
