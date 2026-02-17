**🤖 AI-Powered System Health Monitor**

A proactive system monitoring suite that uses a Prometheus backend, Python-based AI Agents for automated Root Cause Analysis (RCA), and a Streamlit dashboard for real-time visualization.

**🌟 Key Features**

**Custom Exporter:** Scrapes CPU, Memory, Disk, Network, and Battery vitals.
**Process Identification:** Automatically identifies the "Culprit" application during CPU spikes.
**AI Diagnostics:**
    CPU Agent: Detects high usage and provides specific troubleshooting steps for known apps (Chrome, Python, etc.).
    Memory Agent: Uses trend analysis to distinguish between heavy usage and potential memory leaks.
**Live Dashboard:** High-resolution historical charts and status indicators for system health.

**🚀 Getting Started**

**1. Prerequisites**
Ensure you have Python installed and Download Prometheus.

**2. Install Dependencies**
pip install prometheus_client psutil requests streamlit pandas

Execution Steps (Run in separate terminals)
Start the Metric Collector:
python exporter.py

Start Prometheus:
(Ensure prometheus.yml is in the folder)
./prometheus --config.file=prometheus.yml

Start the AI Agent Brain:
python agents.py

Launch the Dashboard:
streamlit run dashboard.py

**🛠️ Configuration**

The prometheus.yml is configured with a 5s scrape interval to ensure the AI Agent has high-resolution data for rapid spike detection.

**📝 Project Structure**

exporter.py: The data collection engine.
agents.py: The logic layer for automated troubleshooting.
dashboard.py: The Streamlit-based visual interface.
prometheus.yml: Configuration for the time-series database.

