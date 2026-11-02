import os
import json
from api_manager import APIManager

class InnerCircle:
    def __init__(self):
        self.api = APIManager.get_instance()
        self.client = self.api.get_client()
        print("[INNER CIRCLE] Online. Monitoring coupled biometrics.")

    def analyze_biometrics(self, user_hrv: int, gf_hrv: int, gf_sleep_hours: float, cycle_day: int = None, recent_texts: list = None):
        """
        Synthesizes biometric data AND textual subtext between the user and their partner 
        to predict friction and trigger pre-emptive actions.
        """
        # If texts are provided, we bypass the hardcoded logic and let ATLAS 
        # analyze the tone and subtext directly with the biometrics.
        return self._generate_response(user_hrv, gf_hrv, gf_sleep_hours, cycle_day, recent_texts)

    def _generate_response(self, user_hrv, gf_hrv, sleep, cycle, texts):
        if not self.client:
            return {"status": "Error", "message": "API Offline"}

        texts_str = "\n".join(texts) if texts else "No recent texts."

        prompt = f"""
        You are ATLAS, the predictive Inner Circle engine for the user's relationships.
        You monitor biological telemetry AND analyze textual subtext to predict mood and friction. 
        
        Current Biological State:
        - User HRV: {user_hrv}ms (Stress capacity)
        - Girlfriend HRV: {gf_hrv}ms (Stress capacity)
        - Girlfriend Sleep: {sleep} hours
        - Girlfriend Menstrual Cycle Day: {cycle if cycle else 'Unknown'}

        Recent Texts from Girlfriend:
        \"\"\"
        {texts_str}
        \"\"\"

        Analyze the hidden sentiment, tone, and subtext of her recent texts. Combine that with the biological 
        telemetry (e.g., if she is sleep-deprived and sending short, cold texts, friction is extremely high).
        
        Write a short JSON response with EXACTLY the following structure:
        {{
            "risk_level": "LOW, MODERATE, HIGH, or EXTREME",
            "analysis": "2 sentences describing her true mood based on the texts and biometrics.",
            "headless_node_action": "e.g., 'TRIGGER_SWIGGY_CHOCOLATE' or 'NONE'",
            "suggested_text": "A brief, empathetic text message for the user to send her."
        }}
        """

        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                self.client = self.api.get_client()
                response = self.client.chats.create(model=self.api.model_name).send_message(prompt)
                
                raw_json = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_json)
                print(f"[INNER CIRCLE] Analysis complete. Risk: {data.get('risk_level')}")
                return data
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print("[INNER CIRCLE] Rate limit hit! Attempting to rotate to backup API key...")
                    if self.api.rotate_key():
                        attempts += 1
                        continue
                    else:
                        return {"status": "Error", "message": "Rate limits exhausted across all keys."}
                else:
                    return {"status": "Error", "message": str(e)}
                    
        return {"status": "Error", "message": "All keys exhausted."}

if __name__ == "__main__":
    ic = InnerCircle()
    print("Testing Inner Circle Multimodal Synthesis...")
    
    # Simulating a subtle situation: Biometrics are okay-ish, but the texts are cold.
    fake_texts = [
        "I'm fine.",
        "Just busy.",
        "Do whatever you want."
    ]
    
    result = ic.analyze_biometrics(user_hrv=55, gf_hrv=40, gf_sleep_hours=6.5, cycle_day=14, recent_texts=fake_texts)
    print(json.dumps(result, indent=2))
