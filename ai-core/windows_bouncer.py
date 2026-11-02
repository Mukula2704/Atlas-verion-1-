import os
import time
import firebase_admin
from firebase_admin import credentials, firestore
import ctypes
import sys

# Path to Windows Hosts file
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
# Redirect IP for blocking
REDIRECT_IP = "127.0.0.1"

# The sites we want to block during Deep Work
BLACKLIST = [
    "www.youtube.com",
    "youtube.com",
    "www.reddit.com",
    "reddit.com",
    "www.instagram.com",
    "instagram.com",
    "www.twitter.com",
    "twitter.com",
    "x.com"
]

def is_admin():
    """Checks if the script is running with Windows Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def enable_focus_mode():
    """Modifies the hosts file to block distracting websites."""
    print("[BOUNCER] Engaging Focus Mode: Blackholing distracting websites...")
    try:
        with open(HOSTS_PATH, 'r+') as file:
            content = file.read()
            # Prevent writing duplicates if already blocked
            if "youtube.com" not in content:
                file.write("\n# === ATLAS DIGITAL BOUNCER (FOCUS MODE) ===\n")
                for site in BLACKLIST:
                    file.write(f"{REDIRECT_IP} {site}\n")
        print(" -> Lockdown successful.")
    except PermissionError:
        print("[ERROR] Permission denied. You must run this script as Administrator.")

def disable_focus_mode():
    """Restores the hosts file to its normal state."""
    print("[BOUNCER] Flow State broken. Restoring internet access...")
    try:
        with open(HOSTS_PATH, 'r') as file:
            lines = file.readlines()
            
        with open(HOSTS_PATH, 'w') as file:
            for line in lines:
                if not any(site in line for site in BLACKLIST) and "ATLAS DIGITAL BOUNCER" not in line:
                    file.write(line)
        print(" -> Access restored.")
    except PermissionError:
        print("[ERROR] Permission denied. You must run this script as Administrator.")

def main():
    print("========================================")
    print("   ATLAS WINDOWS BOUNCER (DEEP WORK)    ")
    print("========================================")
    
    if not is_admin():
        print("[CRITICAL ERROR] This script requires Administrator privileges to modify the hosts file.")
        print("Please right-click and 'Run as Administrator'.")
        # Request Admin privileges and restart (Windows specific trick)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    print("[INFO] Admin privileges confirmed.")
    
    # Initialize Firebase
    try:
        cred = credentials.Certificate(r"C:\Users\mukul\OneDrive\Desktop\comand-center\ai-core\firebase_key.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("[INFO] Connected to ATLAS Firebase backend.")
    except Exception as e:
        print(f"[ERROR] Failed to connect to Firebase: {e}")
        return

    # Track state locally so we don't spam the hosts file writes
    current_focus_state = False

    print("[BOUNCER] Polling for Flow State updates...")
    try:
        while True:
            # Poll Firebase (A listener would be better for production, but polling is fine for this demo script)
            doc = db.collection("command_center").document("system_state").get()
            if doc.exists:
                focus_mode = doc.to_dict().get("focus_mode", False)
                
                if focus_mode and not current_focus_state:
                    enable_focus_mode()
                    current_focus_state = True
                elif not focus_mode and current_focus_state:
                    disable_focus_mode()
                    current_focus_state = False
            
            time.sleep(5) # Poll every 5 seconds
            
    except KeyboardInterrupt:
        print("\n[BOUNCER] Shutting down. Ensuring network is restored...")
        if current_focus_state:
            disable_focus_mode()

if __name__ == "__main__":
    main()
