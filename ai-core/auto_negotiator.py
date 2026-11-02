import time
from api_manager import APIManager

class AutoNegotiator:
    def __init__(self):
        self.api = APIManager.get_instance()
        
    def draft_corporate_negotiation(self, scenario: str, objective: str):
        """Drafts a firm but professional email to customer service or billing."""
        print(f"\n[AUTO-NEGOTIATOR] Initiating Corporate Negotiation Protocols...")
        print(f"Scenario: {scenario} | Objective: {objective}")
        
        prompt = f"""
        You are ATLAS, acting as an elite corporate negotiator and customer service expert.
        My Scenario: {scenario}
        My Objective: {objective}
        
        Draft an email on my behalf that is highly professional, politely firm, and leverages psychological principles of negotiation (e.g., loss aversion, assuming positive intent). Do not sound angry, but do not sound weak. Do not include subject line placeholders, just give me the raw Subject and Body.
        """
        return self._call_atlas(prompt)

    def draft_social_diplomacy(self, message_received: str, goal: str):
        """Drafts a polite text message to diffuse tension or decline gracefully."""
        print(f"\n[SOCIAL DIPLOMAT] Initiating Social Diplomacy Protocols...")
        print(f"Message Received: {message_received} | Goal: {goal}")
        
        prompt = f"""
        You are ATLAS, acting as a social diplomat.
        I received this text message: "{message_received}"
        My Goal: "{goal}"
        
        Draft a text message response that achieves my goal with maximum grace, empathy, and politeness. Ensure it sounds like a normal human texting, not a corporate robot. Keep it concise.
        """
        return self._call_atlas(prompt)

    def _call_atlas(self, prompt: str):
        """Helper to handle ATLAS calls with auto-rotation logic."""
        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                client = self.api.get_client()
                response = client.chats.create(model=self.api.model_name).send_message(prompt)
                return response.text.strip()
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print("[AUTO-NEGOTIATOR] Rate limit hit! Rotating to backup API key...")
                    if self.api.rotate_key():
                        attempts += 1
                        continue
                    else:
                        return "Rate limits exhausted across all keys."
                else:
                    return f"Error: {str(e)}"
                    
        return "All keys exhausted."


if __name__ == "__main__":
    negotiator = AutoNegotiator()
    
    # Test 1: Corporate Negotiation
    scenario = "My internet bill from Comcast went up by $40 this month without any warning or upgrade."
    objective = "Get them to revert the bill to the original promotional rate by threatening to switch to AT&T."
    
    email_draft = negotiator.draft_corporate_negotiation(scenario, objective)
    print("\n=== CORPORATE EMAIL DRAFT ===")
    print(email_draft)
    print("=============================\n")
    
    time.sleep(1) # Polite delay
    
    # Test 2: Social Diplomacy
    text_received = "Hey man, can you help me move my couch this Saturday morning? I know it's early but I really need help."
    social_goal = "Decline gracefully because I want to sleep in, but offer to buy him a beer later to make up for it."
    
    text_draft = negotiator.draft_social_diplomacy(text_received, social_goal)
    print("\n=== SOCIAL TEXT DRAFT ===")
    print(text_draft)
    print("=========================")
