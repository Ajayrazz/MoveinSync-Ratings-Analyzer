import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

st.set_page_config(page_title="MoveInSync Ratings Dashboard", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('moveinsync_reviews.csv')
        df['at'] = pd.to_datetime(df['at'])
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

st.title("🚖 MoveInSync Play Store Reviews Dashboard")
st.markdown("An automated tool for the Product & Engineering teams to track app health.")

if df.empty:
    st.error("No data found. Please run `python scrape_reviews.py` first.")
    st.stop()

# Overview Metrics
total_reviews = len(df)
avg_rating = df['score'].mean()
recent_avg = df.head(1000)['score'].mean() # Average of last 1000 reviews

col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews Analyzed", f"{total_reviews:,}")
col2.metric("Overall Average Rating", f"{avg_rating:.2f} ⭐")
col3.metric("Recent Average (Last 1k)", f"{recent_avg:.2f} ⭐", f"{recent_avg - avg_rating:.2f}")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Rating Overview & Trends")
    # Pie Chart
    score_counts = df['score'].value_counts().reset_index()
    score_counts.columns = ['Rating', 'Count']
    fig_pie = px.pie(score_counts, values='Count', names='Rating', title="Overall Rating Breakdown", color_discrete_sequence=px.colors.sequential.RdBu, hole=0.3)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Line Chart (Rolling Trend)
    df['Month-Year'] = df['at'].dt.to_period('M').astype(str)
    trend_df = df.groupby('Month-Year')['score'].mean().reset_index()
    trend_df = trend_df.tail(12) # Show last 12 months
    fig_line = px.line(trend_df, x='Month-Year', y='score', title="Average Rating Trend (Last 12 Months)", markers=True)
    fig_line.update_yaxes(range=[1, 5])
    st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    # Engineering Pain Points (NLP Categorization)
    st.subheader("Engineering Pain Points (1-3 Star Reviews)")

    # Filter for low ratings
    low_reviews = df[df['score'] <= 3].copy()

    categories = {
        'Authentication (OTP/Login)': ['otp', 'login', 'log in', 'password', 'sign in', 'authenticate', 'number'],
        'App Performance (Crash/Lag)': ['crash', 'hang', 'slow', 'freeze', 'loading', 'lag', 'stuck', 'not opening', 'glitch', 'bug'],
        'Location/Map Tracking': ['location', 'gps', 'map', 'tracking', 'track', 'route', 'wrong path', 'navigation'],
        'Booking/UI Experience': ['book', 'schedule', 'shift', 'roster', 'cancel', 'reschedule', 'ui', 'interface', 'update'],
        'Operational (Driver/Cab)': ['driver', 'cab', 'vehicle', 'late', 'rude', 'dirty', "didn't come", 'no show', 'ac']
    }

    def categorize(text):
        text = str(text).lower()
        cats = []
        for cat, keywords in categories.items():
            if any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in keywords):
                cats.append(cat)
        return ', '.join(cats) if cats else 'Uncategorized/Vague'

    low_reviews['category'] = low_reviews['content'].apply(categorize)

    cat_counts = Counter()
    for cats in low_reviews['category']:
        for c in cats.split(', '):
            if c and c != 'Uncategorized/Vague' and c != 'Operational (Driver/Cab)':
                cat_counts[c] += 1

    cat_df = pd.DataFrame(cat_counts.items(), columns=['Issue Category', 'Review Count']).sort_values('Review Count', ascending=True)

    fig_bar = px.bar(cat_df, x='Review Count', y='Issue Category', orientation='h', title="Top Actionable Engineering Complaints", color='Review Count', color_continuous_scale='Reds')
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# Recent Critical Reviews
st.subheader("Recent Critical Reviews (1-Star)")
issue_filter = st.selectbox("Filter by Engineering Category:", ['All'] + list(cat_counts.keys()))

filtered_low = low_reviews[low_reviews['score'] == 1]
if issue_filter != 'All':
    filtered_low = filtered_low[filtered_low['category'].str.contains(issue_filter, regex=False)]

st.dataframe(
    filtered_low[['at', 'reviewCreatedVersion', 'score', 'content']].head(50).rename(columns={'at': 'Date', 'reviewCreatedVersion': 'App Version', 'score': 'Rating', 'content': 'Review'}),
    use_container_width=True,
    hide_index=True
)
