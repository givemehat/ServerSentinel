import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import time
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="ServerSentinel Dashboard", layout="wide", page_icon="📡")

st.title("📡 ServerSentinel Dashboard")
st.markdown("Real-time monitoring and analytics for distributed servers.")

def fetch_servers():
    try:
        response = requests.get(f"{API_URL}/servers/")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
    return []

def fetch_metrics(server_id, limit=50):
    try:
        response = requests.get(f"{API_URL}/metrics/{server_id}?limit={limit}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    return []

servers = fetch_servers()

if not servers:
    st.warning("No servers are currently reporting metrics. Please ensure the agent is running.")
else:
    selected_server = st.selectbox("Select Server", servers)
    
    # Auto-refresh mechanism (basic via rerun button or Streamlit experimental rerun)
    if st.button("Refresh Data"):
        pass

    metrics = fetch_metrics(selected_server)
    
    if metrics:
        df = pd.DataFrame(metrics)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Latest metrics
        latest = df.iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        
        col1.metric("CPU Usage", f"{latest['cpu_percent']}%")
        col2.metric("Memory Usage", f"{latest['memory_percent']}%")
        col3.metric("Disk Usage", f"{latest['disk_percent']}%")
        
        st.markdown("### Historical Trends")
        
        tab1, tab2, tab3 = st.tabs(["CPU", "Memory", "Network"])
        
        with tab1:
            fig_cpu = px.line(df, x='timestamp', y='cpu_percent', title='CPU Usage Over Time', color_discrete_sequence=['#ef4444'])
            fig_cpu.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig_cpu, use_container_width=True)
            
        with tab2:
            fig_mem = px.line(df, x='timestamp', y='memory_percent', title='Memory Usage Over Time', color_discrete_sequence=['#3b82f6'])
            fig_mem.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig_mem, use_container_width=True)
            
        with tab3:
            fig_net = go.Figure()
            fig_net.add_trace(go.Scatter(x=df['timestamp'], y=df['bytes_sent'], mode='lines', name='Bytes Sent', line=dict(color='#10b981')))
            fig_net.add_trace(go.Scatter(x=df['timestamp'], y=df['bytes_recv'], mode='lines', name='Bytes Received', line=dict(color='#8b5cf6')))
            fig_net.update_layout(title="Network I/O Over Time")
            st.plotly_chart(fig_net, use_container_width=True)
        
        st.markdown("### Raw Data")
        st.dataframe(df.tail(10))
    else:
        st.info("Waiting for data...")
