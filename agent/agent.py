import time
import psutil
import requests
import socket
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/metrics/")
SERVER_ID = os.getenv("SERVER_ID", socket.gethostname())
INTERVAL = int(os.getenv("INTERVAL", "5"))

def get_system_metrics():
    """Gathers system metrics using psutil."""
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Memory usage
    mem = psutil.virtual_memory()
    memory_percent = mem.percent
    
    # Disk usage
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    
    # Network usage
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv
    
    return {
        "server_id": SERVER_ID,
        "cpu_percent": cpu_percent,
        "memory_percent": memory_percent,
        "disk_percent": disk_percent,
        "bytes_sent": bytes_sent,
        "bytes_recv": bytes_recv
    }

def main():
    print(f"Starting ServerSentinel Agent for {SERVER_ID}...")
    print(f"Reporting to {API_URL} every {INTERVAL} seconds.")
    
    while True:
        try:
            metrics = get_system_metrics()
            response = requests.post(API_URL, json=metrics, timeout=5)
            if response.status_code == 201:
                print(f"Successfully sent metrics: {metrics}")
            else:
                print(f"Failed to send metrics: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to API: {e}")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
