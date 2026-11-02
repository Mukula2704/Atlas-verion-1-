import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
from voice_engine import ATLASVoice
from firebase_bridge import FirebaseManager
from firebase_admin import firestore

# Load env variables
dotenv.load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080")

# The default playlist URI to wake up to. (User can change this)
# E.g., Spotify's "Wake Up Happy" playlist
DEFAULT_PLAYLIST = "spotify:playlist:37i9dQZF1DX0AERO4QhAKb"

class BiorhythmDJ:
    def __init__(self):
        self.atlas = ATLASVoice()
        self.firebase = FirebaseManager()
        self.sp = None
        self.device_id = None
        self._authenticate()

    def _authenticate(self):
        """Authenticates with Spotify API. Will open a browser window on the very first run."""
        if not CLIENT_ID or not CLIENT_SECRET:
            print("\n[!] SPOTIFY CREDENTIALS MISSING [!]")
            print("To use the Bio-Rhythm DJ, you must:")
            print("1. Go to https://developer.spotify.com/dashboard/")
            print("2. Create an App (Name it 'ATLAS Alarm').")
            print("3. Set the Redirect URI in settings to: http://127.0.0.1:8080")
            print("4. Add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to your .env file.")
            print("5. Run this script again.")
            exit(1)

        print("[BIORHYTHM DJ] Authenticating with Spotify...")
        # Scope required to read what's playing and modify playback (play/pause/volume)
        scope = "user-modify-playback-state user-read-playback-state"
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=scope
        ))
        
        # Verify connection by getting the user's active devices
        devices = self.sp.devices()
        if devices and 'devices' in devices and len(devices['devices']) > 0:
            self.device_id = devices['devices'][0]['id']
            print(f"[BIORHYTHM DJ] Connected! Active Device found: {devices['devices'][0]['name']}")
        else:
            print("[WARNING] No active Spotify devices found! Please open Spotify on your PC or Phone and start playing a song, then try again.")
            exit(1)

    def smart_alarm_trigger(self, playlist_uri=DEFAULT_PLAYLIST):
        """Checks GPS context before sounding the alarm."""
        print("\n[BIORHYTHM DJ] Alarm scheduled. Verifying GPS Context...")
        
        location_doc = self.firebase.get_latest_document("context_location")
        
        if not location_doc or location_doc.get("location_name") == "Home":
            print("[GPS VERIFIED] User is at Home. Triggering Unkillable Room Alarm.")
            self.start_alarm(playlist_uri)
        else:
            loc = location_doc.get("location_name", "Unknown")
            print(f"[GPS VERIFIED] User is Away ({loc}). Muting room speakers.")
            print(" -> Sending remote Webhook to iQOO phone for standard alarm.")
            
            # Send remote alarm trigger to Firebase so MacroDroid can pick it up
            self.firebase.db.collection("command_center").document("discord_pager").collection("pending").add({
                "message": f"⏰ **GPS Smart Alarm:** You are away from Home ({loc}). Triggering phone alarm now.",
                "action_trigger": "REMOTE_PHONE_ALARM",
                "timestamp": firestore.SERVER_TIMESTAMP
            })

    def start_alarm(self, playlist_uri=DEFAULT_PLAYLIST):
        """Starts the unkillable alarm with volume ramping."""
        print(f"\n[ALARM TRIGGERED] Starting Bio-Rhythm Wakeup Sequence...")
        
        # 1. Ensure volume starts low (e.g., 10%)
        try:
            self.sp.volume(10, device_id=self.device_id)
        except Exception as e:
            print("[ERROR] Could not set volume (some devices like iPhones block remote volume control via API).")

        # 2. Start the playlist
        self.sp.start_playback(device_id=self.device_id, context_uri=playlist_uri)
        print(" -> Music started.")
        
        # 3. Enter the "Unkillable" Loop
        self._enforce_unkillable_loop()

    def _enforce_unkillable_loop(self):
        """
        Ramps volume and resists user attempts to pause the music.
        The ONLY way to kill this is if the flag file is generated.
        """
        flag_file = os.path.join(os.path.dirname(__file__), "..", "data", "alarm_killed.txt")
        # Ensure flag doesn't exist from a previous run
        if os.path.exists(flag_file):
            os.remove(flag_file)
            
        print("\n[!] ALARM IS LOCKED. [!]")
        print(" -> Try pausing Spotify... ATLAS will force it back on.")
        print(f" -> To kill the alarm, say 'Atlas, I am awake' or create the file:\n    {flag_file}")
        
        target_volume = 10
        
        while True:
            # Check if the user successfully requested to kill the alarm via Voice
            if os.path.exists(flag_file):
                print("\n[BIORHYTHM DJ] Kill-switch voice command detected.")
                # Temporarily pause music so ATLAS can speak
                try: self.sp.pause_playback(device_id=self.device_id)
                except: pass
                
                self.atlas.speak("Voice command recognized. Please step in front of the camera for facial verification.")
                
                # Trigger Facial Recognition Scanner
                from verify_face import verify_face
                baseline_path = os.path.join(os.path.dirname(__file__), "face_baseline.pkl")
                is_mukul = verify_face(baseline_path, timeout_seconds=15)
                
                if is_mukul:
                    self.atlas.speak("Facial identity confirmed. Good morning, Mukul. The Bio-Rhythm alarm has been permanently disabled.")
                    os.remove(flag_file)
                    break
                else:
                    self.atlas.speak("Verification failed. Wake-lock remains active. Resuming alarm at maximum volume.")
                    os.remove(flag_file)
                    target_volume = 100
                    try:
                        self.sp.volume(target_volume, device_id=self.device_id)
                        self.sp.start_playback(device_id=self.device_id)
                    except: pass
            
            # --- The normal unkillable loop ---
            try:
                playback = self.sp.current_playback()
                if playback:
                    # 1. Ramp Volume (increase by 5% every 10 seconds up to 100%)
                    if target_volume < 100 and not getattr(self, 'volume_locked', False):
                        target_volume += 5
                        try:
                            self.sp.volume(target_volume, device_id=self.device_id)
                            print(f" -> Ramping Volume: {target_volume}%")
                        except spotipy.SpotifyException as e:
                            if e.http_status == 403:
                                print("[!] Device blocks remote volume control (likely an iPhone/Android). Skipping volume ramps.")
                                self.volume_locked = True
                        except Exception:
                            pass
                            
                    # 2. Check if user tried to pause it!
                    if not playback.get('is_playing', False):
                        print("[!] Unkillable Protocol: User tried to pause. Forcing playback ON and maxing volume!")
                        target_volume = 100
                        try:
                            self.sp.volume(target_volume, device_id=self.device_id)
                            self.sp.start_playback(device_id=self.device_id)
                        except:
                            pass
            except Exception as e:
                # Catch temporary API connection drops and just loop
                pass
                
            time.sleep(10)

if __name__ == "__main__":
    dj = BiorhythmDJ()
    dj.smart_alarm_trigger()
