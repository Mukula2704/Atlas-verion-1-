import asyncio
import edge_tts
import os
import tempfile
import subprocess

class ATLASVoice:
    def __init__(self):
        # The official ATLAS settings approved by Mukul (Hemsworth Fusion Fast)
        self.voice = "en-AU-WilliamNeural"
        self.pitch = "-15Hz" 
        self.rate = "+10%"
    
    async def _generate_and_play(self, text):
        temp_file = os.path.join(tempfile.gettempdir(), "atlas_speech.mp3")
        try:
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, pitch=self.pitch)
            await communicate.save(temp_file)
            # Use ffmpeg to decode MP3 to WAV on the fly and pipe to aplay to avoid SDL static issues
            cmd = f"ffmpeg -v quiet -i {temp_file} -f wav -ar 48000 -ac 2 - | aplay -D plughw:1,0 -q"
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            print(f"[ATLAS Voice Error] {e}")
        finally:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
                
    def speak(self, text):
        """Synchronous wrapper to speak text out loud."""
        print(f"\n[ATLAS SPEAKS]: \"{text}\"")
        asyncio.run(self._generate_and_play(text))

# Simple test block if run directly
if __name__ == "__main__":
    engine = ATLASVoice()
    engine.speak("ATLAS Voice Engine is now online. I am ready.")
