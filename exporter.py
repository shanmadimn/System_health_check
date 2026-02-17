from prometheus_client import start_http_server, Gauge
import psutil
import time

# 1. Define Gauges (Metrics)
# We keep your existing ones
CPU_USAGE = Gauge('system_cpu_usage', 'CPU usage %', ['top_process'])
MEM_USAGE = Gauge('system_memory_usage', 'Memory usage %')

# Adding Disk, Network, and Battery
DISK_USAGE = Gauge('system_disk_usage', 'Disk usage percentage')
NET_SENT = Gauge('system_network_sent_bytes', 'Network bytes sent')
NET_RECV = Gauge('system_network_recv_bytes', 'Network bytes received')
BATTERY_LEVEL = Gauge('system_battery_level', 'Battery percentage')
POWER_PLUGGED = Gauge('system_power_plugged', 'Power cable status (1=Plugged, 0=Unplugged)')

def get_top_process():
    processes = []
    ignore_list = ['System Idle Process', 'System', 'Interrupts']
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            if proc.info['name'] not in ignore_list:
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if not processes:
        return "System Background"
    top = max(processes, key=lambda x: x['cpu_percent'])
    return top['name'] if top['cpu_percent'] > 0 else "System Background"

if __name__ == "__main__":
    # Start the server on port 8080 (your working port)
    start_http_server(8080)
    print("🚀 Mega Exporter running on http://localhost:8080/metrics")
    
    while True:
        # Collect Vitals
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        top_app = get_top_process()
        disk = psutil.disk_usage('/').percent
        net = psutil.net_io_counters()
        battery = psutil.sensors_battery()

        # Update Prometheus Metrics
        CPU_USAGE.labels(top_process=top_app).set(cpu)
        MEM_USAGE.set(mem)
        DISK_USAGE.set(disk)
        NET_SENT.set(net.bytes_sent)
        NET_RECV.set(net.bytes_recv)

        # Handle Battery (some PCs might not have one)
        if battery:
            BATTERY_LEVEL.set(battery.percent)
            POWER_PLUGGED.set(1 if battery.power_plugged else 0)
            batt_status = f"{battery.percent}% ({'Plugged' if battery.power_plugged else 'On Battery'})"
        else:
            batt_status = "N/A"
        
        # Terminal Output for you to watch
        print(f"Tracking: CPU: {cpu}% ({top_app}) | Mem: {mem}% | Disk: {disk}% | Batt: {batt_status}")
        
        time.sleep(1)
