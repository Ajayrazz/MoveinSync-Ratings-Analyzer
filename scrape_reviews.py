import pandas as pd
from google_play_scraper import Sort, reviews_all

def scrape_moveinsync_reviews():
    app_package = 'com.moveinsync.ets'
    print(f"Scraping reviews for {app_package}...")
    
    try:
        # Fetching all reviews can take time, but let's grab them. 
        # For initial analysis, pulling all gives us a good dataset.
        result = reviews_all(
            app_package,
            sleep_milliseconds=0, # defaults to 0
            lang='en', # defaults to 'en'
            country='in', # defaults to 'us', let's use 'in' for India as it's an Indian company
            sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
        )
        
        df = pd.DataFrame(result)
        
        if df.empty:
            print("No reviews found or incorrect package name.")
            return

        # Keep relevant columns
        columns_to_keep = ['reviewId', 'userName', 'content', 'score', 'thumbsUpCount', 'reviewCreatedVersion', 'at', 'replyContent']
        df = df[columns_to_keep]
        
        # Save to CSV
        output_file = 'moveinsync_reviews.csv'
        df.to_csv(output_file, index=False)
        
        print(f"Successfully scraped {len(df)} reviews and saved to {output_file}")
        
        # Print a quick summary
        print("\n--- Quick Summary ---")
        print(f"Total Reviews: {len(df)}")
        print(f"Average Score: {df['score'].mean():.2f}")
        print("\nScore Distribution:")
        print(df['score'].value_counts().sort_index())
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_moveinsync_reviews()
