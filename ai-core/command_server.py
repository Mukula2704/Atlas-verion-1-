from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import os
import torch
from speechbrain.inference.speaker import SpeakerRecognition
from speechbrain.utils.fetching import LocalStrategy
from api_manager import APIManager
import json

app = Flask(__name__)
CORS(app)

print("\n[SECURITY] Loading ECAPA-TDNN Voice Verification Model into RAM...")
verification_model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb", 
    savedir=os.path.join(os.path.dirname(__file__), "pretrained_models", "spkrec-ecapa-voxceleb"),
    run_opts={"device":"cpu"},
    local_strategy=LocalStrategy.COPY
)
print("[SECURITY] Neural Network Loaded.")

class SecurityManager:
    def __init__(self):
        self.last_verified_time = 0
        self.auth_timeout_seconds = 300 # 5 minutes cache
        
    def verify_audio(self, test_file):
        # 1. Check cache to prevent latency
        if (time.time() - self.last_verified_time) < self.auth_timeout_seconds:
            print("[SECURITY] Active Session Cache hit. Voice verified instantly.")
            return True
            
        print("[SECURITY] Authenticating new session voice print...")
        scores = []
        for i in range(1, 4):
            baseline = os.path.join(os.path.dirname(__file__), f"baseline_mukul_{i}.wav")
            if os.path.exists(baseline) and test_file:
                score, prediction = verification_model.verify_files(test_file, baseline)
                scores.append(score.item())
                
        if not scores:
            return False
            
        avg_score = sum(scores) / len(scores)
        print(f"[SECURITY] Voice Match Score: {avg_score:.4f}")
        
        if avg_score >= 0.25:
            print(">> IDENTITY CONFIRMED: MUKUL <<")
            self.last_verified_time = time.time() # Update cache
            return True
        else:
            print(">> GUEST DETECTED. ACCESS RESTRICTED <<")
            return False

security = SecurityManager()
api = APIManager.get_instance()

class SpatialHiveMind:
    def __init__(self):
        self.lock = threading.Lock()
        self.active_window = False
        self.trigger_queue = []
        self.priority_map = {
            "mac_room_mic": 1,
            "iqoo_phone": 2,
            "samsung_phone": 3
        }

    def handle_trigger(self, device_id, audio_file=None):
        with self.lock:
            self.trigger_queue.append({"device": device_id, "audio": audio_file, "timestamp": time.time()})
            if not self.active_window:
                self.active_window = True
                threading.Thread(target=self._resolve_conflict).start()
                
    def _resolve_conflict(self):
        time.sleep(1.0) # Collect multiple devices
        
        with self.lock:
            winner = min(self.trigger_queue, key=lambda x: self.priority_map.get(x["device"], 99))
            self.trigger_queue = []
            self.active_window = False
            
        print(f"\n[HIVE MIND] Spatial Resolution: {winner['device']} takes priority.")
        if winner['audio']:
            self.process_audio(winner['audio'])
            
    def process_audio(self, filepath):
        is_mukul = security.verify_audio(filepath)
        
        # In a real scenario, this is where we send audio to Gemini.
        # If is_mukul == False, we append the Guest Jail prompt.
        prompt = ""
        if not is_mukul:
            prompt = """
            You are speaking to a GUEST, not Mukul.
            You are in GUEST MODE. 
            Do NOT reveal any database information, financials, or private messages.
            ONLY answer basic questions (weather, general facts).
            If they ask for anything else, politely say 'I am sorry, but you do not have security clearance for that.'
            """
        else:
            prompt = "You are speaking to Mukul. Full admin access granted."
            
        print(f"[LLM ENGINE] Prompt Injected:\n{prompt}")
        
        # Cleanup
        try: os.remove(filepath)
        except: pass

hive_mind = SpatialHiveMind()

@app.route('/hotword-trigger', methods=['POST'])
def hotword_trigger():
    device_id = request.form.get('device_id', 'unknown')
    audio_file = request.files.get('audio')
    
    filepath = None
    if audio_file:
        filepath = os.path.join(os.path.dirname(__file__), f"temp_{device_id}_{int(time.time())}.wav")
        audio_file.save(filepath)
        
    hive_mind.handle_trigger(device_id, filepath)
    return jsonify({"status": "queued_for_resolution"})

@app.route('/incoming-sms', methods=['POST'])
def incoming_sms():
    """
    Webhook for MacroDroid. When the 'Missed Call' SMS gets a reply, 
    MacroDroid POSTs it here to be sent to Discord.
    """
    sender = request.form.get('sender', 'Unknown')
    message_body = request.form.get('message', '')
    
    print(f"\n[CALL SCANNER] Intercepted SMS from {sender}: {message_body}")
    
    # Send to Discord Pager
    from discord_commlink import DiscordCommLink
    import asyncio
    
    alert = f"🚨 **Missed Call Scraper:**\n**From:** {sender}\n**Message:** {message_body}"
    try:
        asyncio.run(DiscordCommLink().send_message(alert))
        print(" -> Alert sent to Discord Pager successfully.")
    except Exception as e:
        print(f" -> Failed to push to Discord: {e}")
        
    return jsonify({"status": "sms_processed"})

if __name__ == '__main__':
    print("[COMMAND SERVER] Online on Port 5001")
    app.run(port=5001, debug=False)
