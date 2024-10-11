import streamlit as st
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import plotly.express as px

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'customer_behavior_db')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'events')

# Initialize MongoDB Client
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
collection = db[MONGODB_COLLECTION]

# Set up Streamlit page configuration
st.set_page_config(page_title="Real-Time Customer Behavior Dashboard", layout="wide")

st.title("📊 Real-Time Customer Behavior Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
event_types = ["All"] + sorted(list(collection.distinct("event_type")))
selected_event = st.sidebar.multiselect("Select Event Types", event_types, default=["All"])

time_range = st.sidebar.slider(
    "Select Time Range (Last N Minutes)",
    min_value=1,
    max_value=60,
    value=10
)

# Fetch Data from MongoDB
current_time = datetime.utcnow()
past_time = current_time - timedelta(minutes=time_range)

query = {"timestamp": {"$gte": int(past_time.timestamp())}}

if "All" not in selected_event:
    query["event_type"] = {"$in": selected_event}

cursor = collection.find(query)
data = list(cursor)

# Check if there is any data and handle missing columns gracefully
if data:
    df = pd.DataFrame(data)
    
    # Debugging print to check available columns
    print("Data columns:", df.columns)  # You can remove this after debugging

    # Ensure required columns are available before proceeding
    required_columns = ['customer_id', 'event_type', 'timestamp', 'page', 'product_id', 'price']
    
    # Fill missing columns with NaN or default values if any column is missing
    for column in required_columns:
        if column not in df.columns:
            st.warning(f"Missing column: {column}. Filling with default values.")
            if column == 'timestamp':
                df[column] = int(datetime.utcnow().timestamp())  # Default to current time if missing
            else:
                df[column] = pd.NA  # Fill other missing columns with NaN

    # Convert timestamp fields
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    df['processed_at'] = pd.to_datetime(df['processed_at'], unit='s', errors='coerce')

    # Event Types Over Time Visualization
    st.subheader("Event Types Distribution")
    event_counts = df['event_type'].value_counts().reset_index()
    event_counts.columns = ['event_type', 'count']
    fig1 = px.pie(event_counts, names='event_type', values='count', title='Event Types Distribution')
    st.plotly_chart(fig1, use_container_width=True)

    # Price Distribution
    st.subheader("Price Distribution of Events")
    fig2 = px.histogram(df, x='price', nbins=50, title='Price Distribution')
    st.plotly_chart(fig2, use_container_width=True)

    # Events Over Time
    st.subheader("Events Over Time")
    df.set_index('timestamp', inplace=True)
    resampled = df.resample('1T').size().reset_index(name='counts')  # Resample per minute
    fig3 = px.line(resampled, x='timestamp', y='counts', title='Number of Events Over Time')
    st.plotly_chart(fig3, use_container_width=True)

    # Recent Events Table
    st.subheader("Recent Events")
    st.dataframe(
        df[['customer_id', 'event_type', 'timestamp', 'page', 'product_id', 'price']].sort_values(by='timestamp', ascending=False).head(100),
        height=400
    )
else:
    st.write("No data available for the selected filters.")

# Close MongoDB connection
client.close()

