import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services import api_client

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

st.title("Admin Dashboard")

health = api_client.get_health()
if health.get("status") != "error":
    st.success("Backend is running properly.")
else:
    st.error("Cannot connect to backend.")

analytics = api_client.get_analytics()

if analytics:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Generations", analytics.get("total_generations", 0))
    col2.metric("Most Common Language", analytics.get("most_common_language", "N/A"))
    col3.metric("Most Common Age", analytics.get("most_common_age_group", "N/A"))
    
    st.metric("Average Response Time", f"{analytics.get('average_response_time_ms', 0)} ms")
else:
    st.info("No analytics data available yet.")
