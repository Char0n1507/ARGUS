import streamlit as st
import pandas as pd
import time
import sqlite3
import os

st.set_page_config(
    page_title="Project Alpha | SOC Dashboard",
    page_icon="🌍",
    layout="wide",
)

# Custom CSS for "Hacker Mode"
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .metric-card {
        background-color: #262730;
        border: 1px solid #454545;
        padding: 15px;
        border-radius: 5px;
        color: white;
    }
    h1, h2, h3 {
        color: #00ff41 !important; 
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌍 Project Alpha: Global Threat Map")
st.markdown("### Specialized Operation Center (SOC) View")

# Database Connection
DB_PATH = "forensics.db"

def load_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT 100", conn)
        conn.close()
        
        if not df.empty:
            df['datetime'] = pd.to_datetime(df['human_time'])
        return df
    except Exception as e:
        st.error(f"DB Error: {e}")
        return pd.DataFrame()

# Auto-refresh
placeholder = st.empty()

while True:
    df = load_data()
    
    with placeholder.container():
        # KPI Row
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        total_threats = len(df) if not df.empty else 0
        latest_country = df['country'].iloc[0] if not df.empty else "N/A"
        avg_risk = df['score'].mean() if not df.empty else 0.0
        
        kpi1.metric("Total Anomalies (DB)", total_threats)
        kpi2.metric("Latest Origin", latest_country)
        kpi3.metric("Avg Risk Score", f"{avg_risk:.4f}")
        kpi4.metric("Active Sensors", "1 (Local)")

        # Map and Charts
        col1, col2 = st.columns([2, 1])
        
        if not df.empty:
            with col1:
                st.subheader("📍 Real-Time Threat Origins")
                # Filter for valid lat/lon
                map_data = df[(df['lat'] != 0.0) & (df['lon'] != 0.0)]
                if not map_data.empty:
                    st.map(map_data[['lat', 'lon']])
                else:
                    st.info("No Geo-localized threats yet (Waiting for public IP traffic...)")
            
            with col2:
                st.subheader("🚨 Live Feed")
                st.dataframe(df[['human_time', 'country', 'score', 'raw_summary']].head(10), hide_index=True)
                
                st.subheader("Top Attacking Countries")
                st.bar_chart(df['country'].value_counts())
        else:
            st.warning("Waiting for data... Start the Detector!")

    time.sleep(2)
