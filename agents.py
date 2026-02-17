import requests
import time

def query_detailed_metric(query):
    response = requests.get("http://localhost:9090/api/v1/query", params={'query': query})
    results = response.json()['data']['result']
    if results:
        val = float(results[0]['value'][1])
        # This extracts the process name from the Prometheus labels
        name = results[0]['metric'].get('top_process', 'System')
        return val, name
    return 0, "None"

def rca_agent(cpu, app_name):
    print(f"🔍 [RCA]: High CPU of {cpu}% detected.")
    print(f"🔍 [RCA]: Found the culprit: **{app_name}**")
    return app_name

def solution_agent(culprit):
    if culprit == "chrome.exe":
        print("🛠️ [SOLUTION]: Heavy browser usage. Suggesting tab suspension.")
    elif culprit == "python.exe":
        print("🛠️ [SOLUTION]: Monitoring script or script-under-test is heavy. Checking for loops.")
    else:
        print(f"🛠️ [SOLUTION]: Restarting service for {culprit}.")

def memory_leak_agent(mem_val):
    # If memory is over 80%, we look for a 'leak' pattern
    if mem_val > 80:
        print("🚨 [MEMORY AGENT]: Warning! System RAM is nearly full.")
        print("🔍 [RCA]: Checking for apps with high 'Private Bytes'...")
        return True
    return False

# --- Main Loop ---
# --- Main Loop ---
if __name__ == "__main__":
    print("🤖 Agent Brain is active and monitoring Prometheus...")
    
    # Track previous memory to detect a 'climb' (Leak Detection)
    last_memory_val = 0

    while True:
        # 1. Fetch both CPU and Memory metrics
        cpu_val, culprit_app = query_detailed_metric('system_cpu_usage')
        mem_val, _ = query_detailed_metric('system_memory_usage')
        
        # 2. Heartbeat: Now showing both vital signs
        print(f"--- Heartbeat ---")
        print(f"Monitoring... CPU: {cpu_val}% | Top Process: {culprit_app}")
        print(f"Monitoring... MEM: {mem_val}%")

        # 3. Logic for High CPU (Spike Detection)
        if cpu_val > 5:
            print(f"🚨 [ALERT]: High CPU Usage detected!")
            rca_reason = rca_agent(cpu_val, culprit_app)
            solution_agent(rca_reason)

        # 4. Logic for Memory Leak (Pattern Detection)
        # If memory is high AND higher than the last check, it might be a leak
        if mem_val > 80 and mem_val > last_memory_val:
            print(f"⚠️ [WARNING]: Potential Memory Leak detected in {culprit_app}!")
            print(f"🔍 [RCA]: Memory increased from {last_memory_val}% to {mem_val}%")
            print(f"🛠️  [SOLUTION]: Recommend clearing cache or restarting {culprit_app}.")
        
        # Update state for next check
        last_memory_val = mem_val
        
        print(f"-----------------\n")
        time.sleep(5)
