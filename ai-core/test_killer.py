import os
import signal
current_pid = os.getpid()
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
for pid in pids:
    if int(pid) == current_pid: continue
    try:
        with open(f'/proc/{pid}/cmdline', 'rb') as f:
            cmdline = f.read().decode('utf-8').replace('\x00', ' ')
        if 'python3' in cmdline and ('atlas_core.py' in cmdline):
            print(f'Would kill {pid}: {cmdline}')
    except Exception:
        pass
