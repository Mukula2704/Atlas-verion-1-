import time
import json
from api_manager import APIManager
from firebase_bridge import FirebaseManager

class SpamCallAssistant:
    def __init__(self):
        self.api = APIManager.get_instance()
        try:
            self.db = FirebaseManager()
            self.use_firebase = True
        except FileNotFoundError:
            self.use_firebase = False

    def handle_incoming_call(self, caller_id: str, initial_transcript: str):
        print(f"\n[CALL ASSISTANT] Incoming call intercepted from: {caller_id}")
        print(f"[CALL ASSISTANT] Caller's opening line: '{initial_transcript}'")
        print("[CALL ASSISTANT] ATLAS is analyzing caller intent...")

        prompt = f"""
        You are an AI personal assistant answering a phone call for your boss, Mukul. 
        You have intercepted an unknown caller. 
        
        Caller's Opening Line: "{initial_transcript}"
        
        Analyze the intent and respond with a JSON object. 
        If it's a scam/spam (credit card, car warranty, vague "business opportunity"), generate a response to shut them down or waste their time, and set action to HANG_UP.
        If it's a delivery driver, politely ask them to hold for a moment while you connect them to Mukul, and set action to PAGE_MUKUL.
        If it's legitimate (doctor, friend on new number), ask them to leave a message, and set action to HANG_UP or PAGE_MUKUL depending on urgency.
        
        Format exact JSON:
        {{
            "classification": "SPAM" | "DELIVERY" | "LEGITIMATE",
            "ai_verbal_response": "The exact script you will speak out loud to the caller via TTS",
            "action": "HANG_UP" | "STAY_ON_LINE" | "PAGE_MUKUL"
        }}
        """

        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                client = self.api.get_client()
                response = client.chats.create(model=self.api.model_name).send_message(prompt)
                
                # Strip out any markdown code blocks the LLM might return
                raw_json = response.text.replace('```json', '').replace('```', '').strip()
                result = json.loads(raw_json)
                
                classification = result.get('classification', 'UNKNOWN')
                verbal_response = result.get('ai_verbal_response', '')
                action = result.get('action', 'HANG_UP')
                
                print(f"\n=== CALL ANALYSIS ===")
                print(f"Classification: {classification}")
                print(f"ATLAS Speaks: \"{verbal_response}\"")
                print(f"System Action: {action}")
                print(f"=====================\n")
                
                if action == "PAGE_MUKUL":
                    print(f"\n[MAC SPEAKER] ATLAS Announcing to Mukul...")
                    from voice_engine import ATLASVoice
                    voice = ATLASVoice()
                    voice.speak(verbal_response)
                    
                if self.use_firebase:
                    self.db.log_action("CALL_ASSISTANT", f"Intercepted {classification} call from {caller_id}. Action: {action}", is_action=True)
                
                return result
                
            except json.JSONDecodeError:
                print("[CALL ASSISTANT] Error: ATLAS returned invalid JSON. Retrying...")
                attempts += 1
            except Exception as e:
                print(f"[CALL ASSISTANT] Execution Error: {e}")
                self.api.rotate_key()
                attempts += 1
                
        print("[CALL ASSISTANT] Failed to process call. Defaulting to hang up.")
        return {"classification": "ERROR", "ai_verbal_response": "Sorry, I am just an AI. Goodbye.", "action": "HANG_UP"}

if __name__ == "__main__":
    assistant = SpamCallAssistant()
    
    # Scenario 1: Classic Telemarketer/Scam
    scam_transcript = "Hello sir, I am calling from the refund department. We noticed a charge of $499 on your Amazon account and need you to verify your banking details to cancel it."
    assistant.handle_incoming_call("+1-800-555-0199", scam_transcript)
    
    time.sleep(2)
    
    # Scenario 2: Swiggy / Delivery Driver
    delivery_transcript = "Hi sir, I am your Swiggy delivery partner. I am standing outside the main gate, where should I leave the package?"
    assistant.handle_incoming_call("+91-9876543210", delivery_transcript)
