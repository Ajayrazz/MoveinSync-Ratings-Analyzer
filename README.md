# MoveInSync Play Store Rating Analysis

This repository contains my submission for the **Forward Deployed Engineer** assignment.

## Contents
1. **[MoveInSync_Product_Recommendations.md](./MoveInSync_Product_Recommendations.md)**: The final product and engineering recommendation report. **(Start here)**
2. **[scrape_reviews.py](./scrape_reviews.py)**: The Python script used to automate the data extraction from the Google Play Store.
3. **[analyze_reviews.py](./analyze_reviews.py)**: The Python script that processes, cleans, and categorizes the raw reviews into actionable engineering buckets using natural language processing techniques.
4. **[moveinsync_reviews.csv](./moveinsync_reviews.csv)**: The raw dataset of 24,300+ reviews fetched by the scraper.

## How to Run the Analysis Pipeline
To satisfy the requirement that *"this is a question we'll keep asking from time to time"*, I built this as a repeatable pipeline rather than a static one-time analysis.

### Prerequisites
You need Python 3 installed.

### Setup
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the required dependencies:
   ```bash
   pip install google-play-scraper pandas streamlit plotly
   ```

### Execution
1. **Fetch the latest data:**
   ```bash
   python scrape_reviews.py
   ```
   *This will pull the latest reviews and update the `moveinsync_reviews.csv` file.*

2. **Launch the Live Interactive Dashboard (Recommended):**
   ```bash
   streamlit run dashboard.py
   ```
   *This will open a live web dashboard in your browser. It visualizes the latest rating trends, categorizes engineering complaints into interactive bar charts, and allows Product Managers to instantly filter and read specific 1-star reviews based on categories (e.g., OTP issues vs Location Tracking bugs).*

3. **(Alternative) Run the categorization analysis in terminal:**
   ```bash
   python analyze_reviews.py
   ```

## 🤖 Automation (GitHub Actions)
This repository includes a complete CI/CD pipeline (`.github/workflows/automate_scraper.yml`). 
Once pushed to GitHub, this workflow automatically spins up a server every **Monday at 9:00 AM**, runs the Python scraper to fetch new reviews, and commits the updated CSV data back to the repository. 

This ensures that the Streamlit dashboard always displays fresh, up-to-date information without requiring a developer or Product Manager to manually run any scripts!
