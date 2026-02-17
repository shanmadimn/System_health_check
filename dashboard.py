import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# Page Config
st.set_page_config(page_title="System AI Monitor", layout="wide")
st.title("🤖 AI Agent Command Center")

# Sidebar for Status
st.sidebar.header("System Status")
st.sidebar.success("Prometheus: Connected")
st.sidebar.info("Agent: Monitoring")

# 1. Placeholders for top-row metrics (Gauges/KPIs)
col1, col2, col3, col4 = st.columns(4)
with col1:
    cpu_metric = st.empty()
with col2:
    mem_metric = st.empty()
with col3:
    disk_metric = st.empty()
with col4:
    batt_metric = st.empty()

# 2. Placeholders for charts
st.markdown("### Resource Trends")
chart_placeholder = st.empty()

# Data storage for the history
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'CPU', 'Memory', 'Disk', 'Battery'])

def query_prometheus(query):
    try:
        url = "http://localhost:9090/api/v1/query"
        res = requests.get(url, params={'query': query}).json()
        return float(res['data']['result'][0]['value'][1])
    except:
        return 0.0

def get_all_metrics():
    cpu = query_prometheus('system_cpu_usage')
    mem = query_prometheus('system_memory_usage')
    disk = query_prometheus('system_disk_usage')
    batt = query_prometheus('system_battery_level')
    plugged = query_prometheus('system_power_plugged')
    return cpu, mem, disk, batt, plugged

# Main Loop
while True:
    cpu, mem, disk, batt, plugged = get_all_metrics()
    
    # Update Top Row Metrics
    cpu_metric.metric("CPU", f"{cpu}%")
    mem_metric.metric("Memory", f"{mem}%")
    disk_metric.metric("Disk Space", f"{disk}%")
    
    # Custom battery display
    batt_label = "Charging ⚡" if plugged == 1 else "Discharging 🔋"
    batt_metric.metric("Battery", f"{batt}%", delta=batt_label)
    
    # Update History Graph
    new_data = pd.DataFrame({
        'Time': [datetime.now()], 
        'CPU': [cpu], 
        'Memory': [mem],
        'Disk': [disk],
        'Battery': [batt]
    })
    
    st.session_state.history = pd.concat([st.session_state.history, new_data]).tail(30)
    
    # Display the combined chart
    chart_placeholder.line_chart(st.session_state.history.set_index('Time'))
    
    time.sleep(2)
