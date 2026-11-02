import os
from datetime import datetime
from api_manager import APIManager

class AutoArchivist:
    def __init__(self):
        self.api = APIManager.get_instance()
        self.archive_dir = os.path.join(os.path.dirname(__file__), "brain_dumps")
        os.makedirs(self.archive_dir, exist_ok=True)
        
    def process_voice_dump(self, raw_transcript: str):
        print("\n[AUTO-ARCHIVIST] Processing raw voice-to-text transcript...")
        
        prompt = f"""
        You are ATLAS. The user has just recorded a chaotic voice memo / brain dump.
        Your job is to structure this dump into a clean, highly organized document.
        
        Raw Transcript:
        "{raw_transcript}"
        
        Format the output perfectly using Markdown:
        1. Give it a concise, fitting Title.
        2. Provide a 1-sentence Executive Summary.
        3. Extract clear 'Action Items' (with inferred deadlines if mentioned).
        4. Organize the rest into logical categories or bullet points.
        Remove all filler words (uh, um, yeah so).
        """
        
        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                client = self.api.get_client()
                response = client.chats.create(model=self.api.model_name).send_message(prompt)
                structured_doc = response.text.strip()
                
                # Save to "Google Docs" (Local Markdown Archive)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"braindump_{timestamp}.md"
                filepath = os.path.join(self.archive_dir, filename)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(structured_doc)
                    
                print(f"[AUTO-ARCHIVIST] Successfully structured and archived to: {filepath}")
                return structured_doc
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print("[AUTO-ARCHIVIST] Rate limit hit! Rotating to backup API key...")
                    if self.api.rotate_key():
                        attempts += 1
                        continue
                    else:
                        return "Rate limits exhausted across all keys."
                else:
                    return f"Error: {str(e)}"
                    
        return "All keys exhausted."


if __name__ == "__main__":
    archivist = AutoArchivist()
    
    # Simulated chaotic voice-to-text transcription from the user walking around their room
    simulated_voice_dump = (
        "yeah so um I was thinking about the new app dashboard we need to make sure the glassmorphism "
        "is actually rendering right on mobile because it looked super weird yesterday. Also remind me to "
        "buy milk and eggs for the house. Oh and I have that massive physics assignment due on Thursday "
        "so I should probably start drafting the formulas by Tuesday night or I'm gonna fail. And tell "
        "my sister I'll call her back this weekend."
    )
    
    print(f"RAW VOICE TRANSCRIPT:\n{simulated_voice_dump}\n")
    
    structured_note = archivist.process_voice_dump(simulated_voice_dump)
    
    print("\n=== GOOGLE DOCS / ARCHIVE OUTPUT ===")
    print(structured_note)
    print("====================================")
