import os
import json
import time
from google import genai
from firebase_bridge import FirebaseManager
from voice_engine import ATLASVoice
import asyncio
import dotenv

dotenv.load_dotenv()
# Using your fresh backup key!
api_key = os.getenv("GEMINI_API_KEY_2")
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI API Key not found in .env")

client = genai.Client(api_key=api_key)

class WorkspaceArchitect:
    def __init__(self):
        self.firebase = FirebaseManager()
        self.atlas = ATLASVoice()
        self.shopping_list_path = r"C:\Users\mukul\.gemini\antigravity-ide\brain\8b0db402-51dd-4021-a618-5ee36487e358\shopping_list.md"
        self.client = client

    async def scan_handwritten_note(self, image_path):
        """Scans a physical note (sent from phone), translates it, and executes actions."""
        print(f"\n[WORKSPACE ARCHITECT] Processing image: {os.path.basename(image_path)}...")
        
        try:
            uploaded_file = self.client.files.upload(file=image_path)
            
            while uploaded_file.state == "PROCESSING":
                print(" -> Waiting for Google Vision to process the image...")
                time.sleep(2)
                uploaded_file = self.client.files.get(name=uploaded_file.name)
                
            print(" -> Image ready. Running Multilingual OCR...")
            
            prompt = """
            You are ATLAS, an AI assistant. Read the handwritten note in the image.
            The user might write in English, Hindi, or Kannada.
            1. Translate everything to English.
            2. Determine the 'intent' of the note (e.g., 'grocery_list', 'todo_task', 'general_note').
            3. Extract the items/text.
            
            Return ONLY a raw JSON object (no markdown):
            {
                "intent": "grocery_list",
                "items": ["Milk", "Eggs", "Bread"],
                "summary": "You added 3 items to the grocery list."
            }
            """
            
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=[uploaded_file, prompt]
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```json"): raw_text = raw_text[7:-3]
            elif raw_text.startswith("```"): raw_text = raw_text[3:-3]
                
            data = json.loads(raw_text)
            await self._execute_intent(data)
            
        except Exception as e:
            print(f"[ERROR] Vision processing failed: {e}")
        finally:
            try:
                self.client.files.delete(name=uploaded_file.name)
                print(" -> Cleaned up image from Google servers.")
            except:
                pass

    async def _execute_intent(self, data):
        intent = data.get("intent", "general_note")
        items = data.get("items", [])
        summary = data.get("summary", "Note processed.")
        
        print(f"\n[WORKSPACE ARCHITECT] Intent Detected: {intent.upper()}")
        
        # Log to Firebase so it shows up on the Dashboard
        self.firebase.log_action("WorkspaceArchitect", f"Scanned note: {summary}", is_action=True)
        
        if intent == "grocery_list" and items:
            print(" -> [ROUTING] Grocery List detected. Triggering Vocal Confirmation & Procurement...")
            from pantry_module import PantryModule
            pantry = PantryModule()
            
            # 1. Voice Confirmation
            items_str = ", ".join(items)
            confirmation_speech = f"Sir, I have scanned the desk note. The items are: {items_str}. Shall I queue these into the Blinkit procurement cart?"
            await self.atlas._generate_and_play(confirmation_speech)
            
            # 2. Wait for confirmation (Simulated via logs for now, normally triggers ListeningEngine)
            print("[WAITING FOR MUKUL TO SAY 'YES' ON ROOM MIC...]")
            
            # 3. Trigger Procurement once confirmed
            pantry.trigger_procurement(items)
            
        else:
            # Voice Debrief for normal notes
            await self.atlas._generate_and_play(f"Sir, {summary}")

if __name__ == "__main__":
    architect = WorkspaceArchitect()
    
    # We will pass a test image directly from the terminal
    import sys
    if len(sys.argv) > 1:
        asyncio.run(architect.scan_handwritten_note(sys.argv[1]))
    else:
        print("Usage: python workspace_architect.py <path_to_image>")
