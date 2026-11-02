import os
from google import genai
from dotenv import load_dotenv

class APIManager:
    _instance = None
    
    def __init__(self):
        load_dotenv()
        self.keys = []
        # Search for any GEMINI_API_KEY in the environment
        if os.getenv("GEMINI_API_KEY"):
            self.keys.append(os.getenv("GEMINI_API_KEY"))
        if os.getenv("GEMINI_API_KEY_2"):
            self.keys.append(os.getenv("GEMINI_API_KEY_2"))
        if os.getenv("GEMINI_API_KEY_3"):
            self.keys.append(os.getenv("GEMINI_API_KEY_3"))
            
        self.current_key_index = 0
        self.model_name = "gemini-3.6-flash"
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = APIManager()
        return cls._instance
        
    def get_client(self):
        if not self.keys:
            return None
        # Return a fresh client using the current active key
        return genai.Client(api_key=self.keys[self.current_key_index])
        
    def rotate_key(self):
        """Switches to the next backup API key if the current one hits a limit."""
        if len(self.keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.keys)
            print(f"[API MANAGER] Rotated to Backup API Key (Index: {self.current_key_index})")
            return True
        else:
            print("[API MANAGER] No backup API keys available to rotate to!")
            return False

    def get_heartbeat_client(self):
        """Returns a dedicated client exclusively for the Autonomic Heartbeat evolution loop."""
        hb_key = os.getenv("GEMINI_API_KEY_HEARTBEAT")
        if hb_key:
            return genai.Client(api_key=hb_key)
        else:
            print("[API MANAGER] WARNING: GEMINI_API_KEY_HEARTBEAT missing. Falling back to primary pool.")
            return self.get_client()
