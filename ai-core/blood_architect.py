import os
import json
import asyncio
from google import genai
import time
from firebase_bridge import FirebaseManager
from voice_engine import ATLASVoice

# Load Gemini API Key
import dotenv
dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_2")
if not api_key:
    raise ValueError("GEMINI_API_KEY_2 not found in .env")

client = genai.Client(api_key=api_key)

class BloodArchitect:
    def __init__(self):
        self.firebase = FirebaseManager()
        self.atlas = ATLASVoice()
        self.reports_dir = os.path.join(os.path.dirname(__file__), "..", "data", "health_reports")
        self.shopping_list_path = r"C:\Users\mukul\.gemini\antigravity-ide\brain\8b0db402-51dd-4021-a618-5ee36487e358\shopping_list.md"
        
        # We now use the client instead of GenerativeModel
        self.client = client
        
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
            
    async def process_new_reports(self):
        """Scans the health_reports directory for any unprocessed PDFs."""
        print("[BLOOD ARCHITECT] Scanning for new medical reports...")
        
        for filename in os.listdir(self.reports_dir):
            if (filename.endswith(".pdf") or filename.endswith(".txt")) and not filename.startswith("_PROCESSED"):
                print(f"\n[!] New Blood Report Detected: {filename}")
                pdf_path = os.path.join(self.reports_dir, filename)
                
                await self._analyze_report(pdf_path)
                
                # Mark as processed
                new_path = os.path.join(self.reports_dir, f"_PROCESSED_{filename}")
                os.rename(pdf_path, new_path)
            
    async def _analyze_report(self, pdf_path):
        print(f" -> Uploading {os.path.basename(pdf_path)} to Gemini for medical parsing...")
        
        # Upload the file to the Gemini API
        uploaded_file = self.client.files.upload(file=pdf_path)
        
        # Wait for the file to be processed by Google's backend
        while uploaded_file.state == "PROCESSING":
            print(" -> Waiting for Google to process the file...")
            time.sleep(2)
            uploaded_file = self.client.files.get(name=uploaded_file.name)
            
        print(" -> File ready. Running Biomarker Analysis...")
        
        prompt = """
        You are a world-class blood architect and longevity doctor. 
        Read the uploaded medical report. Extract all the key biomarkers.
        Compare them against the optimal baselines for a HIGH-PERFORMANCE MALE ATHLETE (not just average human ranges).
        Identify any deficiencies.
        Suggest the top 3 corrective superfoods or supplements to add to the grocery list for any deficiencies.
        
        Respond ONLY with a valid JSON in this exact format, with no markdown code blocks:
        {
            "biomarkers": [
                {
                    "name": "Vitamin D",
                    "value": "22 ng/mL",
                    "status": "Deficient",
                    "optimal_range": "50-70 ng/mL",
                    "corrective_foods": ["Salmon", "Egg Yolks"]
                }
            ],
            "overall_summary": "Short 1-sentence debrief for the user."
        }
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=[uploaded_file, prompt]
            )
            raw_text = response.text.strip()
            
            # Clean up potential markdown formatting (```json ... ```)
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:-3]
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:-3]
                
            health_data = json.loads(raw_text)
            
            await self._handle_results(health_data)
            
        except Exception as e:
            print(f"[ERROR] Failed to parse report: {e}")
        finally:
            print(" -> Cleaning up local files...")
            try:
                self.client.files.delete(name=uploaded_file.name)
                print(" -> Deleted medical file from Google servers to protect privacy.")
            except:
                pass
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

    async def _handle_results(self, health_data):
        print("\n[BLOOD ARCHITECT] Analysis Complete!")
        
        # 1. Push to Firebase
        self.firebase.db.collection("user_data").document("blood_profile").set(health_data)
        print(" -> Firebase Updated: /user_data/blood_profile")
        
        # 2. Extract corrective foods for the Shopping List
        foods_to_buy = set()
        deficiencies_found = 0
        
        for marker in health_data.get("biomarkers", []):
            # Check if status indicates a problem
            status = marker.get("status", "").lower()
            if any(word in status for word in ["deficient", "sub-optimal", "high", "low"]):
                deficiencies_found += 1
                for food in marker.get("corrective_foods", []):
                    foods_to_buy.add(food)
                    
        # 3. Update Shopping List
        if foods_to_buy:
            # Only append if the file exists, else create it
            mode = "a" if os.path.exists(self.shopping_list_path) else "w"
            with open(self.shopping_list_path, mode) as f:
                f.write("\n\n### Medical Corrections (Blood Architect)\n")
                for food in foods_to_buy:
                    f.write(f"- [ ] {food}\n")
            print(f" -> Shopping List Updated with {len(foods_to_buy)} corrective foods.")
            
        # 4. Voice Debrief
        summary = health_data.get("overall_summary", "Blood test analysis complete.")
        voice_prompt = f"Sir, I have analyzed your latest blood report. {summary} "
        if deficiencies_found > 0:
            voice_prompt += f"I detected {deficiencies_found} sub-optimal markers. I have added corrective foods like {list(foods_to_buy)[0]} to your Instamart list."
        else:
            voice_prompt += "All biomarkers are in the optimal athletic range. Outstanding work."
            
        await self.atlas._generate_and_play(voice_prompt)

if __name__ == "__main__":
    architect = BloodArchitect()
    asyncio.run(architect.process_new_reports())
