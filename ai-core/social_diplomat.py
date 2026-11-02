import json
import os
import time
from api_manager import APIManager
from firebase_bridge import FirebaseManager

class SocialDiplomat:
    def __init__(self):
        self.firebase = FirebaseManager()
        self.api = APIManager.get_instance()
        self.contacts_file = os.path.join(os.path.dirname(__file__), 'vip_contacts.json')
        print("[SOCIAL DIPLOMAT] Online. Monitoring friendship telemetry.")
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.contacts_file):
            with open(self.contacts_file, 'r') as f:
                self.contacts = json.load(f)
        else:
            # We start empty as requested. Mukul will add these via Discord post-launch.
            self.contacts = {}
            self.save_contacts()

    def save_contacts(self):
        with open(self.contacts_file, 'w') as f:
            json.dump(self.contacts, f, indent=4)
            
        # Sync to Firebase so Dashboard can see it
        self.firebase.db.collection("command_center").document("social_diplomat").set(self.contacts)

    def add_contact(self, name, tier, notes=""):
        """tier can be 'close' (7 days) or 'normal' (14 days)"""
        self.contacts[name] = {
            "tier": tier,
            "last_contact_timestamp": time.time(),
            "notes": notes
        }
        self.save_contacts()
        print(f"[SOCIAL DIPLOMAT] Added {name} to {tier} tier.")

    def check_neglect_levels(self):
        """Checks if any friends have crossed the neglect threshold."""
        current_time = time.time()
        neglected = []

        for name, data in self.contacts.items():
            days_since = (current_time - data["last_contact_timestamp"]) / 86400.0
            threshold = 7 if data["tier"] == "close" else 14
            
            if days_since > threshold:
                print(f"[SOCIAL DIPLOMAT] ⚠️ {name} has been neglected for {int(days_since)} days.")
                neglected.append((name, data))
                
        if neglected:
            self._draft_checkins(neglected)

    def _draft_checkins(self, neglected_list):
        """Uses Gemini to draft personalized check-in messages."""
        if not self.api.get_client():
            print("[SOCIAL DIPLOMAT] Error: API Offline. Cannot draft texts.")
            return

        for name, data in neglected_list:
            prompt = f"""
            You are drafting a casual text message on behalf of Mukul to his friend '{name}'.
            Mukul hasn't spoken to them in {int((time.time() - data['last_contact_timestamp']) / 86400)} days.
            Context/Notes about this friend: {data.get('notes', 'No special context.')}
            
            Write a very short, highly realistic, casual check-in text (e.g. "Hey man, it's been a minute!").
            Return ONLY the text message. No quotes, no intro.
            """
            try:
                client = self.api.get_client()
                response = client.chats.create(model=self.api.model_name).send_message(prompt)
                draft = response.text.strip()
                
                print(f"\n[DRAFT READY for {name}]: {draft}")
                self._send_discord_approval(name, draft)
                
            except Exception as e:
                print(f"[SOCIAL DIPLOMAT] Failed to draft message for {name}: {e}")

    def _send_discord_approval(self, name, draft):
        """Sends the draft to Discord/Dashboard waiting for user approval to trigger MacroDroid."""
        print(f"[ACTION REQUIRED] Sending ping to Discord: 'Approval needed to text {name}'")
        # Push to a Firebase queue that discord_commlink.py can read
        self.firebase.db.collection("social_queue").add({
            "target": name,
            "draft_text": draft,
            "status": "pending_approval",
            "timestamp": time.time()
        })

    def log_interaction(self, name):
        """Resets the timer for a contact after Mukul talks to them."""
        if name in self.contacts:
            self.contacts[name]["last_contact_timestamp"] = time.time()
            self.save_contacts()
            print(f"[SOCIAL DIPLOMAT] Interaction logged for {name}. Timer reset.")

if __name__ == "__main__":
    sd = SocialDiplomat()
    # Simulating the post-launch setup Mukul requested:
    # sd.add_contact("Rahul", "close", "Works in IT. We usually talk about games.")
    # sd.contacts["Rahul"]["last_contact_timestamp"] -= (86400 * 9) # Simulate 9 days ago
    # sd.check_neglect_levels()
