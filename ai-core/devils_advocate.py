import time
from api_manager import APIManager

class DevilsAdvocate:
    def __init__(self):
        self.api = APIManager.get_instance()
        
    def generate_interrogation(self, topic: str):
        """Generates a brutal, hyper-specific question on the topic."""
        print(f"\n[DEVIL's ADVOCATE] Initializing aggressive active-recall for: {topic}...")
        
        prompt = f"""
        You are ATLAS, acting as a "Devil's Advocate". I am studying the topic: '{topic}'.
        Do not give me a summary. Instead, hit me with a brutally difficult, hyper-specific question 
        or scenario about this topic to test my actual understanding. 
        Force me to apply the knowledge, not just recite facts. Be aggressive and demanding.
        """
        
        return self._call_atlas(prompt)

    def critique_answer(self, topic: str, question: str, user_answer: str):
        """Aggressively critiques the user's answer, pointing out flaws and weak points."""
        print(f"\n[DEVIL's ADVOCATE] Analyzing user's response...")
        
        prompt = f"""
        You are ATLAS, acting as a brutal "Devil's Advocate".
        Topic: {topic}
        Question I asked: {question}
        User's Answer: {user_answer}
        
        Critique the user's answer aggressively. Tell them exactly where their logic is weak, 
        what edge cases they completely missed, and why their understanding is flawed or incomplete. 
        Grade them out of 10. Do not be polite. Force them to think harder.
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
                    print("[DEVIL's ADVOCATE] Rate limit hit! Rotating to backup API key...")
                    if self.api.rotate_key():
                        attempts += 1
                        continue
                    else:
                        return "Rate limits exhausted across all keys."
                else:
                    return f"Error: {str(e)}"
                    
        return "All keys exhausted."


if __name__ == "__main__":
    da = DevilsAdvocate()
    
    # Simulating a study session
    study_topic = "Python Memory Management (Garbage Collection & Reference Counting)"
    
    question = da.generate_interrogation(study_topic)
    
    print("\n=== ATLAS INTERROGATION ===")
    print(question)
    print("===========================\n")
    
    # Simulating a weak user answer
    simulated_answer = "Python uses reference counting. Every time a variable is used, the count goes up. When it's not used, it goes down to zero and deletes the memory."
    print(f"USER'S ANSWER:\n\"{simulated_answer}\"")
    
    time.sleep(1) # Polite delay
    
    critique = da.critique_answer(study_topic, question, simulated_answer)
    
    print("\n=== ATLAS CRITIQUE ===")
    print(critique)
    print("======================")
