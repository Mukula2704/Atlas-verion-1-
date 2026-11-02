import os
import PyPDF2
import csv
from api_manager import APIManager

class ShadowLearner:
    def __init__(self):
        self.api = APIManager.get_instance()
        self.client = self.api.get_client()
        
        # Ensure output directory exists
        self.output_dir = "flashcards"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def parse_pdf(self, pdf_path: str) -> str:
        """Extracts all text from a given PDF file."""
        print(f"[SHADOW LEARNER] Parsing PDF: {pdf_path}...")
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"[SHADOW LEARNER] Error reading PDF: {e}")
            return ""

    def generate_flashcards(self, text: str, deck_name: str):
        """Uses ATLAS (Gemini) to generate Anki-compatible flashcards from text."""
        if not self.client:
            print("[SHADOW LEARNER] Offline. Missing API Key.")
            return

        print(f"[SHADOW LEARNER] Analyzing {len(text)} characters of text to generate flashcards...")

        prompt = (
            "You are the Shadow Learner, a master of spaced repetition learning. "
            "Read the following text and extract the most important concepts. "
            "Format your output EXACTLY as a CSV file where each line is: Question,Answer. "
            "Do not include headers, bullet points, or markdown formatting. Just raw CSV lines. "
            f"\n\nTEXT:\n{text[:30000]}" # Limiting to 30k chars for safety
        )

        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                self.client = self.api.get_client()
                response = self.client.chats.create(model=self.api.model_name).send_message(prompt)
                
                # Clean up output
                csv_data = response.text.replace('```csv', '').replace('```', '').strip()
                
                # Save to file
                output_path = os.path.join(self.output_dir, f"{deck_name}.csv")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(csv_data)
                    
                print(f"[SHADOW LEARNER] Success! Generated flashcard deck at: {output_path}")
                return output_path
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print("[SHADOW LEARNER] Rate limit hit! Attempting to rotate to backup API key...")
                    if self.api.rotate_key():
                        attempts += 1
                        continue
                    else:
                        print("[SHADOW LEARNER] Failed: Rate limit hit and no backup keys.")
                        return None
                else:
                    print(f"[SHADOW LEARNER] Error: {e}")
                    return None
                    
        return None

if __name__ == "__main__":
    print("Testing Shadow Learner...")
    # This acts as a standalone script for now until integrated with the UI
