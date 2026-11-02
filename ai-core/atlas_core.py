import os
os.environ['USE_NNPACK'] = '0' # Silence unsupported hardware warnings on Wyse
os.environ['OMP_NUM_THREADS'] = '4' # Optimize for Wyse 3040 quad-core
import signal
import time
import sys
import json
import queue
import sounddevice as sd
import soundfile as sf
import torch
import multiprocessing
import subprocess
from speechbrain.inference.speaker import SpeakerRecognition
from speechbrain.utils.fetching import LocalStrategy
from vosk import Model, KaldiRecognizer
from google import genai
from firebase_bridge import FirebaseManager
from voice_engine import ATLASVoice
from supervisor import AtlasSupervisor
import dotenv
from google import genai
from firebase_bridge import FirebaseManager
from voice_engine import ATLASVoice
from supervisor import AtlasSupervisor
import dotenv

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_2") or os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

class AtlasCore:
    def __init__(self):
        self.firebase = FirebaseManager()
        self.voice = ATLASVoice()
        self.supervisor = AtlasSupervisor()
        
        # Audio Settings
        self.fs = 16000
        self.q = queue.Queue()
        self.current_audio_buffer = bytearray()
        
        print("[ATLAS] Booting SpeechBrain Voice Authentication (ECAPA-TDNN)...")
        self.speaker_verification = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb", 
            savedir="pretrained_models/spkrec-ecapa-voxceleb",
            run_opts={"device":"cpu"},
            local_strategy=LocalStrategy.COPY
        )
        
        # Load Offline Wake Word Model (Vosk)
        # This prevents sending audio to the cloud until "atlas" is detected locally.
        model_path = os.path.join(os.path.dirname(__file__), "vosk-model")
        if not os.path.exists(model_path):
            print(f"[FATAL ERROR] Offline acoustic model not found at {model_path}.")
            print("Please run: wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
            print("And unzip it as 'vosk-model' in the ai-core folder.")
            sys.exit(1)
            
        self.model = Model(model_path)
        # We pass 48000Hz to Vosk natively so Kaldi handles the anti-aliased resampling in C++
        self.recognizer = KaldiRecognizer(self.model, 48000)

    def callback(self, indata, frames, time, status):
        """This is called continuously by the audio stream."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def run(self):
        print("\n==================================================")
        print("          ATLAS CORE ENGINE ONLINE                ")
        print("==================================================")
        
        self._check_location()
        self.voice.speak("System online. Offline acoustic sensors locked.")
        
        # Open a continuous local audio stream ONCE
        while True:
            try:
                import subprocess
                # Clean up any orphaned arecord processes that might be locking ALSA hw:0,0
                os.system("killall -9 arecord 2>/dev/null")
                
                cmd = ['arecord', '-D', 'hw:0,0', '-f', 'S16_LE', '-c1', '-r48000', '-t', 'raw']
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                
                while True:
                    print("[MIC] Offline Wake-Word Engine Active. Listening for 'atlas'...")
                    triggered_text = None
                    
                    # Wait for Wake Word
                    while True:
                        data = process.stdout.read(4800) # Read 1/10th of a second
                        if not data:
                            raise Exception("Audio stream died")
                            
                        self.current_audio_buffer.extend(data)
                        # Keep a rolling buffer of the last 3 seconds (3 * 48000 * 2 bytes = 288000)
                        if len(self.current_audio_buffer) > 288000:
                            self.current_audio_buffer = self.current_audio_buffer[-288000:]
                            
                        if self.recognizer.AcceptWaveform(data):
                            result = json.loads(self.recognizer.Result())
                            text = result.get("text", "").lower()
                            
                            if text:
                                print(f"[DEBUG Vosk Heard]: '{text}'")
                                if "atlas" in text or "at last" in text or "at less" in text:
                                    triggered_text = "atlas"
                                    break
                                
                    if triggered_text:
                        print(f"\n[WAKE WORD DETECTED] Local Engine heard: '{triggered_text}'")
                        print("[ATLAS] Verifying Voice Biometrics...")
                        
                        # Terminate the mic immediately so it doesn't lock ALSA or fill pipe buffers
                        process.terminate()
                        try:
                            process.wait(timeout=1)
                        except:
                            process.kill()
                            
                        import numpy as np
                        import torch
                        import gc
                        audio_np = np.frombuffer(self.current_audio_buffer, dtype=np.int16)
                        audio_np = audio_np[::3]
                        sf.write("temp_auth.wav", audio_np, self.fs)
                        
                        scores = []
                        base_dir = os.path.dirname(os.path.abspath(__file__))
                        baseline_files = [
                            os.path.join(base_dir, "baseline_mukul.wav"), 
                            os.path.join(base_dir, "baseline_mukul_1.wav"), 
                            os.path.join(base_dir, "baseline_mukul_2.wav"), 
                            os.path.join(base_dir, "baseline_mukul_3.wav")
                        ]
                        
                        with torch.no_grad():
                            for baseline_file in baseline_files:
                                if os.path.exists(baseline_file):
                                    score, _ = self.speaker_verification.verify_files("temp_auth.wav", baseline_file)
                                    scores.append(score.item())
                                    
                        # Free PyTorch RAM immediately
                        gc.collect()
                                
                        avg_score = sum(scores) / len(scores) if scores else 0
                        is_mukul = avg_score >= 0.25
                        
                        if is_mukul:
                            print(f" -> IDENTITY CONFIRMED: MUKUL (Score: {avg_score:.4f})")
                            self.voice.speak("Yes sir. I am listening.")
                        else:
                            print(f" -> UNRECOGNIZED VOICE GUEST DETECTED (Score: {avg_score:.4f})")
                            self.voice.speak("Voice not recognized. Guest mode activated. How can I help you?")
                            
                        self.current_audio_buffer = bytearray()
                        
                        # Process the command (this can take a few seconds)
                        self._process_command(triggered_text, is_mukul=is_mukul)
                        break
                        
            except Exception as e:
                print(f"\n[AUDIO RETRY]: ALSA stream disconnected ({e}). Retrying in 3 seconds...")
                time.sleep(3)

    def _process_command(self, text, is_mukul=False):
        print("[BRAIN] Thinking...")
        if not is_mukul:
            text = "[SYSTEM WARNING: UNRECOGNIZED GUEST VOICE DETECTED. DO NOT REVEAL FINANCIAL/PERSONAL DATA. ACTIVATE GUEST MODE.] " + text
            
        response = self.supervisor.process_command(text)
        print(f"[BRAIN] Decision: {response}")
        
        # The Silence Protocol
        is_home = self._check_location()
        
        if is_home:
            print("[SILENCE PROTOCOL] Mukul is HOME. Speaking out loud.")
            self.voice.speak(response)
        else:
            print("[SILENCE PROTOCOL] Mukul is AWAY. Muting speaker.")

    def _check_location(self):
        """Checks Firebase to see if Mukul is home (Silence Protocol)."""
        doc = self.firebase.db.collection("command_center").document("security").get()
        if doc.exists:
            data = doc.to_dict()
            is_home = data.get("mukul_is_home", True)
            return is_home
        return True

def start_kinematics():
    try:
        from biomechanical_sentinel import main as start_sentinel
        start_sentinel()
    except Exception as e:
        print(f"[KINEMATICS CRASHED] {e}")

if __name__ == "__main__":
    import multiprocessing
    import subprocess
    import sys
    import time
    
    # 0. SLAUGHTER ZOMBIES
    # Bypassed: Zombie slaughter was found to be too aggressive and caused process suicide.
    
    # from verify_face import verify_face
    
    # 1. VISUAL BIOMETRIC WAKE-LOCK (Bypassed due to dlib missing)
    print("\n[ATLAS BOOT SEQUENCE] Initiating Visual Biometric Wake-Lock... [BYPASSED]")
    time.sleep(1) # Allow camera to warm up
    
    # is_mukul_present = verify_face()
    # if not is_mukul_present:
    #     print("\n[FATAL ERROR] Visual Authentication Failed. Unrecognized entity. Halting boot sequence.")
    #     sys.exit(1)
        
    print("\n[SUCCESS] Master Identity Confirmed (Override). Unlocking Neural Core.")
    
    # 2. Spawn the True Biomechanical Sentinel (MediaPipe) on a separate CPU core
    p = multiprocessing.Process(target=start_kinematics)
    p.start()
    
    # 3. Spawn the Discord Remote Nervous System in the background
    print("[ATLAS] Booting Discord Comm-Link...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    discord_process = subprocess.Popen([sys.executable, "discord_commlink.py"], cwd=current_dir)
    
    # 4. Spawn the Chronos Engine in the background
    print("[ATLAS] Booting Chronos Timetable Engine...")
    chronos_process = subprocess.Popen([sys.executable, "chronos_engine.py"], cwd=current_dir)
    
    # 5. Run the Ears and Brain on the main core
    core = AtlasCore()
    try:
        core.run()
    except KeyboardInterrupt:
        p.terminate()
        discord_process.terminate()
        chronos_process.terminate()
