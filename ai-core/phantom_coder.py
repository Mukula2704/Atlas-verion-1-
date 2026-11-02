import time
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from api_manager import APIManager
from firebase_bridge import FirebaseManager

class PhantomEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.api = APIManager.get_instance()
        try:
            self.db = FirebaseManager()
            self.use_firebase = True
        except FileNotFoundError:
            self.use_firebase = False
        
        self.debounce_timers = {}
        self.debounce_seconds = 2.0  # Wait 2 seconds after the last save to process
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        filepath = event.src_path
        # Only check code files, ignore sqlite, env, etc.
        if not filepath.endswith(('.py', '.js', '.html')):
            return
            
        # Ignore our own script to prevent infinite loops if we self-modify
        if "phantom_coder.py" in filepath or "venv" in filepath or "__pycache__" in filepath:
            return

        # Debounce logic: if user is mashing Ctrl+S, we only trigger once they stop
        if filepath in self.debounce_timers:
            self.debounce_timers[filepath].cancel()
            
        timer = threading.Timer(self.debounce_seconds, self.analyze_file, args=[filepath])
        self.debounce_timers[filepath] = timer
        timer.start()

    def analyze_file(self, filepath):
        print(f"\n[PHANTOM CODER] Detected save on: {os.path.basename(filepath)}. Scanning for bugs...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code_content = f.read()
        except Exception as e:
            print(f"[PHANTOM CODER] Could not read file: {e}")
            return
            
        if not code_content.strip():
            return
            
        # We cap the length to avoid sending massive bundles
        if len(code_content) > 10000:
            code_content = code_content[:10000] + "\n...[TRUNCATED]"

        prompt = f"""
        You are ATLAS, an elite AI Pair Programmer (The Phantom Coder).
        I just saved this file: {os.path.basename(filepath)}.
        
        Review the code. 
        1. If it looks perfectly fine, respond exactly with "PASS". 
        2. If there is a bug, security flaw, or severe optimization issue, you must fix it.
           Output your response in the following strict format:
           EXPLANATION: (Short explanation of the bug and fix)
           CODE:
           ```python
           [Insert full corrected code here]
           ```
           
        DO NOT provide the CODE section if there are no bugs.
        Code:
        ```python
        {code_content}
        ```
        """
        
        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                client = self.api.get_client()
                response = client.chats.create(model=self.api.model_name).send_message(prompt)
                result = response.text.strip()
                
                if result.upper() == "PASS" or "PASS" in result[:10]:
                    print(f"[PHANTOM CODER] {os.path.basename(filepath)} looks clean. No bugs detected.")
                else:
                    print(f"\n🚨 [PHANTOM CODER WARNING] 🚨")
                    
                    explanation = result.split("CODE:")[0].replace("EXPLANATION:", "").strip() if "CODE:" in result else result
                    print(explanation)
                    
                    # Non-Destructive Evolution: Extract the fixed code and save it as a patch
                    if "```python" in result:
                        fixed_code = result.split("```python")[1].split("```")[0].strip()
                        patch_dir = os.path.join(os.path.dirname(filepath), "patches")
                        os.makedirs(patch_dir, exist_ok=True)
                        
                        patch_path = os.path.join(patch_dir, f"fixed_{os.path.basename(filepath)}")
                        with open(patch_path, "w", encoding="utf-8") as pf:
                            pf.write(fixed_code)
                            
                        print(f"[EVOLUTION PROTOCOL] Auto-Correction generated. Patch safely saved to: {patch_path}")
                        print(" -> Your original legacy module remains untouched. Review the patch before deploying.")
                        
                    if self.use_firebase:
                        self.db.log_action("PHANTOM_CODER", f"Bug detected and patched in {os.path.basename(filepath)}.", is_action=True)
                break # Success, exit loop
            except Exception as e:
                print(f"[PHANTOM CODER] Rate limit hit! Rotating to backup API key...")
                self.api.rotate_key()
                attempts += 1
        
        if attempts == max_retries:
            print("[PHANTOM CODER] AI Analysis failed: All API keys exhausted.")

class PhantomCoder:
    def __init__(self, watch_dir):
        self.watch_dir = watch_dir
        self.observer = Observer()
        self.event_handler = PhantomEventHandler()
        
    def start_monitoring(self):
        print(f"\n[PHANTOM CODER] Initializing... Monitoring directory: {self.watch_dir}")
        print("[PHANTOM CODER] Waiting for you to save a file...\n")
        
        self.observer.schedule(self.event_handler, self.watch_dir, recursive=True)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("\n[PHANTOM CODER] Monitoring stopped.")
        
        self.observer.join()

if __name__ == "__main__":
    # Monitor the parent directory (comand-center) so we catch both /ai-core and /public
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    phantom = PhantomCoder(target_dir)
    phantom.start_monitoring()
