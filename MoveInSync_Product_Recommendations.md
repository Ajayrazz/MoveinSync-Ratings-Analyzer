# MoveInSync Play Store Rating Analysis & Recommendations

## 1. Executive Summary
Our current Play Store ratings suffer due to a mix of operational issues (driver behavior, late cabs) and actionable engineering/product bugs. While we cannot write code to fix a late driver, we **can** fix the app experience that frustrates users before they even step into the cab. 

By analyzing the latest **8,600+ low-rating reviews (1-3 stars)**, we isolated the app-specific complaints. Here is the priority list for the engineering and product teams to tackle immediately to stabilize our ratings.

---

## 2. What to Fix First: Top Engineering Priorities

### Priority 1: Location Tracking & ETA Accuracy (27.0% of negative reviews)
**The Problem:** Users are consistently reporting that the app's ETA calculation drastically differs from Google Maps, and the live tracking frequently freezes. In recent versions (e.g., `v12.19.0`), users report being unable to track vehicles if the trip is under an hour away.
* **Quote:** *"ETA calculator very bad... google maps always shows 3x the time shown in moveinsync app."*
* **Engineering Action Items:**
    1. **Audit Routing Engine:** Compare the internal routing/ETA logic against the Google Maps Directions API baseline during peak traffic hours. 
    2. **Fix Tracking Constraints:** Investigate and remove the bug in `v12.19.0` preventing users from tracking vans within the 1-hour window.
    3. **Background Sync:** Optimize the websocket or polling frequency for live location so the UI doesn't appear frozen.

### Priority 2: Booking UI & Metro Ticket Bugs (24.1% of negative reviews)
**The Problem:** The app feels rigid. When things go wrong (network drop, schedule change), the app fails ungracefully. A specific, highly repeatable bug exists in the Metro ticket booking flow.
* **Quote:** *"Goes to full brightness the moment you choose metro ticket option... Offline ticket unavailable. stranded if network issues... Ap says booked but no QR"*
* **Engineering Action Items:**
    1. **Metro Flow Hotfix:** Remove the forced maximum brightness when selecting a Metro ticket (it's unnecessary and breaks on high-brightness displays).
    2. **Offline Mode:** Implement local caching for booked QR codes. Once a ticket is generated on the server, cache the QR payload in local storage so it renders even if the user drops to 0 bars of signal at the metro turnstile.

### Priority 3: Authentication & Startup Crashes (17.8% and 13.1% of negative reviews)
**The Problem:** Users cannot log in due to OTP latency. Furthermore, a critical security check is misfiring, locking legitimate users out of the app entirely.
* **Quote:** *"Quite frequently it gives error as 'move in synch application can not be installed/opened as it was not downloaded from play store'."*
* **Engineering Action Items:**
    1. **Play Store Verification Bug:** Audit the App Licensing/SafetyNet checks running on app startup. It is falsely flagging legitimate Play Store downloads as side-loaded.
    2. **OTP Fallback:** Investigate SMS gateway latency. Implement an auto-retry or a WhatsApp API fallback for OTP delivery to bypass cellular network SMS delays.

---

## 3. The "Not a One-Time Ask" Solution
Since tracking Play Store ratings is a continuous effort, I have built an automated pipeline rather than just doing a manual check. 

**The Pipeline:**
I wrote a Python automation script that uses `google-play-scraper` to pull raw review data directly from the Play Store. A secondary script runs Pandas and RegEx-based natural language processing to categorize the reviews into buckets (Location, Booking, OTP, Crashes) and outputs frequency metrics. 

Going forward, a Product Manager can run this script at the end of every sprint to instantly see if a new release (e.g., `v12.20.0`) caused a spike in a specific category like "App Crashes".

---

## 4. Methodology & Tools Used
* **Data Source:** Public Google Play Store.
* **Tooling:** Python 3, `pandas` (for data manipulation), `google-play-scraper` (for API bypassing/data extraction), and standard NLP keyword tokenization for categorization.
* **Execution:** Scraped all 24,311 available reviews. Filtered for ratings ≤ 3 stars (8,604 reviews). Applied categorization heuristics to separate operational issues (which went to an "Uncategorized/Driver" bucket) from actionable engineering bugs.
* **Assumption:** Assumed that reviews mentioning "cab" or "driver" without mentioning the app UI are outside the immediate scope of the software engineering team, focusing our attention on high-leverage code fixes.
