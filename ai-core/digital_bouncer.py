import time
from firebase_bridge import FirebaseManager

class DigitalBouncer:
    def __init__(self):
        try:
            self.db = FirebaseManager()
            self.use_firebase = True
        except FileNotFoundError:
            self.use_firebase = False
            print("[DIGITAL BOUNCER] Firebase Key missing. Operating in Simulation Mode.")
            
        self.target_collection = "device_commands"
        self.doc_id = "jamming_status"
        
        self.distracting_apps = [
            "com.instagram.android",      # Instagram (Samsung)
            "com.zhiliaoapp.musically",   # TikTok
            "com.twitter.android",        # X / Twitter
            "com.snapchat.android"        # Snapchat
        ]

    def initiate_deep_work_jamming(self):
        """Pushes a jamming flag to Firebase to trigger Tasker on iQOO/Samsung."""
        print("\n[DIGITAL BOUNCER] !!! INITIATING DEEP WORK JAMMING PROTOCOL !!!")
        print("[DIGITAL BOUNCER] Dispatching Firebase command to iQOO and Samsung...")
        
        data = {
            "is_jamming_active": True,
            "blocked_apps": self.distracting_apps,
            "timestamp": time.time()
        }
        
        if self.use_firebase:
            self.db.update_document(self.target_collection, self.doc_id, data)
            print("[+] COMMAND SENT: Tasker on phones will now execute 'pm suspend'.")
        else:
            print(f"[-] [SIMULATED FIREBASE PUSH]: {data}")
                
        print("\n[DIGITAL BOUNCER] Devices are now locked down remotely. Distractions eliminated.")
        print("==============================================================\n")

    def lift_jamming(self):
        """Pushes an un-jamming flag to Firebase to restore apps on iQOO/Samsung."""
        print("\n[DIGITAL BOUNCER] >>> DEEP WORK SESSION COMPLETE <<<")
        print("[DIGITAL BOUNCER] Dispatching Firebase command to restore access...")
        
        data = {
            "is_jamming_active": False,
            "blocked_apps": self.distracting_apps,
            "timestamp": time.time()
        }
        
        if self.use_firebase:
            self.db.update_document(self.target_collection, self.doc_id, data)
            print("[+] COMMAND SENT: Tasker on phones will now execute 'pm unsuspend'.")
        else:
            print(f"[-] [SIMULATED FIREBASE PUSH]: {data}")
                
        print("\n[DIGITAL BOUNCER] Phones restored to normal operation.")
        print("=====================================================\n")


if __name__ == "__main__":
    bouncer = DigitalBouncer()
    
    # 1. User starts studying
    bouncer.initiate_deep_work_jamming()
    
    # 2. Simulate 2 hours of deep work passing
    print("(Simulating 2 hours of intense, distraction-free deep work...)")
    time.sleep(2) 
    
    # 3. User finishes studying
    bouncer.lift_jamming()
