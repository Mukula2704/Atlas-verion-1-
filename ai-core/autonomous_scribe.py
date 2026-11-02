import os
from datetime import datetime
from api_manager import APIManager
from firebase_bridge import FirebaseManager
from firebase_admin import firestore
import time

class AutonomousScribe:
    def __init__(self):
        self.api = APIManager.get_instance()
        self.firebase = FirebaseManager()
        self.notes_dir = os.path.join(os.path.dirname(__file__), "lecture_notes")
        os.makedirs(self.notes_dir, exist_ok=True)
        
    def process_lecture_audio(self, audio_path: str, course_name: str = "General"):
        print(f"\n[AUTONOMOUS SCRIBE] Uploading audio to Gemini: {audio_path}")
        
        prompt = f"""
        You are ATLAS, acting as an elite academic Autonomous Scribe.
        I have provided an audio recording of a live university lecture / meeting.
        
        Your objective:
        1. Give the lecture a clear, structured Title based on the topic.
        2. Write a highly structured set of Markdown notes (Use headings, bullet points, and bold text for key terms).
        3. Identify any core formulas, definitions, or dates and isolate them in a "Key Takeaways" section.
        4. Generate a 3-question active-recall quiz at the very bottom to test the user's understanding of this specific lecture.
        
        Do not output any pleasantries, just the Markdown document.
        """
        
        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                client = self.api.get_client()
                
                # Upload the audio file to Gemini
                uploaded_file = client.files.upload(file=audio_path)
                print(f"[AUTONOMOUS SCRIBE] Audio uploaded as {uploaded_file.name}. Generating notes...")
                
                # Wait for the file to be processed
                while uploaded_file.state.name == "PROCESSING":
                    print(".", end="", flush=True)
                    time.sleep(2)
                    uploaded_file = client.files.get(name=uploaded_file.name)
                print()
                
                # Generate content using the audio file
                response = client.models.generate_content(
                    model=self.api.model_name,
                    contents=[uploaded_file, prompt]
                )
                structured_notes = response.text.strip()
                
                # Cleanup the file from Gemini
                client.files.delete(name=uploaded_file.name)
                print(f"[AUTONOMOUS SCRIBE] Audio file cleaned up from Gemini server.")
                
                # Save the notes locally
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{course_name.replace(' ', '_')}_Lecture_{timestamp}.md"
                filepath = os.path.join(self.notes_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(structured_notes)
                    
                print(f"[AUTONOMOUS SCRIBE] Success! Notes and Quiz generated: {filepath}")
                
                # Push the alert to Discord via Firebase Pager
                self.firebase.db.collection("command_center").document("discord_pager").collection("pending").add({
                    "message": f"🎓 **Lecture Processed:** {course_name}\n\nI have finished transcribing the audio and generating your active-recall notes. Check the dashboard or the local `lecture_notes` directory for the full markdown file.\n\n**Preview:**\n{structured_notes[:500]}...",
                    "timestamp": firestore.SERVER_TIMESTAMP
                })
                print("[AUTONOMOUS SCRIBE] Sent notification to Discord Pager.")
                
                return filepath
                
            except Exception as e:
                print(f"[AUTONOMOUS SCRIBE] Error or Rate limit hit: {e}. Rotating to backup API key...")
                self.api.rotate_key()
                attempts += 1
                
        print("[AUTONOMOUS SCRIBE] Failed: All API keys exhausted.")
        return None

if __name__ == "__main__":
    # Test script if run directly
    print("[AUTONOMOUS SCRIBE] Module loaded. Ready to process audio.")
