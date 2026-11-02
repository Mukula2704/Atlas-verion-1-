import json
import os
import time
from firebase_bridge import FirebaseManager

class PantryModule:
    def __init__(self):
        self.firebase = FirebaseManager()
        self.inventory_file = os.path.join(os.path.dirname(__file__), 'pantry_inventory.json')
        print("[PANTRY MODULE] Initializing... Tracking Family (+2) Base Logistics.")
        self.load_inventory()

    def load_inventory(self):
        if os.path.exists(self.inventory_file):
            with open(self.inventory_file, 'r') as f:
                self.inventory = json.load(f)
        else:
            # Baseline assumptions for Family of 3
            self.inventory = {
                "packaged_essentials": {
                    "milk_liters": 2.5,
                    "curd_kg": 1.0,
                    "bread_loaves": 1
                },
                "veggies_kg": 5.0,
                "wholesale_items": {
                    "chicken_kg": 3.0, # Tracked but not auto-ordered
                    "eggs": 60       # Tracked but not auto-ordered
                }
            }
            self.save_inventory()

    def save_inventory(self):
        with open(self.inventory_file, 'w') as f:
            json.dump(self.inventory, f, indent=4)
        
        # Sync to Firebase for the Dashboard UI
        self.firebase.db.collection("command_center").document("pantry_status").set(self.inventory)

    def log_meal(self, food_type, quantity):
        """Deducts consumed food from inventory based on Vision AI or Manual input."""
        print(f"[PANTRY] Deducting {quantity} of {food_type} from inventory.")
        # Logic to deduct based on food_type mapping
        # Example: if food_type == 'milk': self.inventory['packaged_essentials']['milk_liters'] -= quantity
        self.save_inventory()
        self.check_thresholds()

    def check_thresholds(self):
        """Checks if packaged daily essentials have dropped below threshold for a family of 3."""
        needs_order = False
        cart_items = []

        # We only auto-order the cheap/daily packaged stuff via Quick Commerce
        if self.inventory["packaged_essentials"]["milk_liters"] <= 0.5:
            cart_items.append("2L Milk (Cheapest Option)")
            needs_order = True
            
        if self.inventory["packaged_essentials"]["curd_kg"] <= 0.2:
            cart_items.append("1KG Curd (Cheapest Option)")
            needs_order = True

        if needs_order:
            print(f"[PANTRY] ALERT: Essentials running low. Requesting auto-procurement for: {cart_items}")
            self.trigger_procurement(cart_items)

    def trigger_procurement(self, items):
        """Sends a signal to the Autonomous Procurement Engine (MacroDroid) to build a Blinkit cart."""
        self.firebase.db.collection("procurement_queue").add({
            "items": items,
            "status": "pending_approval",
            "timestamp": time.time(),
            "notes": "Select cheapest available option. Brand agnostic."
        })
        print("[PANTRY] Procurement signal sent. Awaiting Mukul's Discord/Voice approval.")

    def detect_junk_food(self, vision_context, source="camera"):
        """
        Anti-Craving Protocol.
        Checks if the Vision AI or Swiggy SMS interceptor has flagged junk food (chips, soda, etc.).
        """
        junk_keywords = ['chips', 'soda', 'coke', 'fries', 'burger', 'pizza', 'ice cream', 'doritos']
        if any(junk in vision_context.lower() for junk in junk_keywords):
            print(f"[PANTRY] ⚠️ JUNK FOOD DETECTED via {source}: {vision_context}")
            self.intervene_junk_food()
            return True
        return False

    def intervene_junk_food(self):
        """
        The 'I Hate Hard Work' override logic. If ATLAS catches Mukul ordering/eating junk,
        it triggers the Devils Advocate or Room Speaker to challenge him.
        """
        # Log the failure
        self.firebase.db.collection("command_center").document("junk_strikes").set({
            "last_strike": time.time(),
            "warning": "Cravings triggered. Protocol breached."
        }, merge=True)
        
        # Trigger Voice Engine to shame/remind Mukul of the 120-130g protein goal.
        print(" -> [INTERVENTION] Triggering Room Speaker: 'Mukul, put the chips down. You are compromising the ₹12 Cr protocol.'")

if __name__ == "__main__":
    pantry = PantryModule()
    # Test Junk Detection
    pantry.detect_junk_food("I just bought some Lays chips", source="discord_vision")
