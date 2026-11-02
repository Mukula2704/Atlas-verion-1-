import socket
import concurrent.futures

def scan_port(ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.2)
            if s.connect_ex((ip, 22)) == 0:
                return ip
    except:
        pass
    return None

ips_to_scan = [f"192.168.1.{i}" for i in range(1, 255)]
active_ips = []

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(scan_port, ips_to_scan)
    for result in results:
        if result:
            active_ips.append(result)

print("Found SSH servers at:", active_ips)
