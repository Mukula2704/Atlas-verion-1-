import os
from api_manager import APIManager
from google import genai

class SwarmManager:
    def __init__(self, log_callback=None):
        self.api = APIManager.get_instance()
        self.client = self.api.get_client()
        self.model_name = self.api.model_name
        self.log = log_callback if log_callback else print
        
    def _create_agent(self, role, prompt):
        return self.client.chats.create(
            model=self.model_name,
            config=genai.types.GenerateContentConfig(
                system_instruction=f"You are {role}. {prompt}"
            )
        )

    def generate_v1(self, task_description: str) -> str:
        """
        Phase 2: The Swarm collaborates to produce Version 1 (V1).
        """
        if not self.client:
            return "Swarm Offline."
            
        self.log("[SWARM] ATLAS has tasked the Swarm. The Team is assembling...")
        
        # 1. The Strategist
        strat_prompt = "You are the Strategist. Break the user's task into a highly optimized, high-level blueprint."
        strategist = self._create_agent("The Strategist", strat_prompt)
        self.log("[SWARM] The Strategist is creating the blueprint...")
        blueprint = strategist.send_message(task_description).text
        self.log(f"[STRATEGIST] Blueprint ready.")
        
        # 2. The Researcher
        res_prompt = "You are the Researcher. Analyze the Strategist's blueprint and provide any necessary data, edge-cases, or technical considerations needed before execution."
        researcher = self._create_agent("The Researcher", res_prompt)
        self.log("[SWARM] The Researcher is gathering context...")
        research = researcher.send_message(f"Task: {task_description}\n\nBlueprint:\n{blueprint}").text
        self.log(f"[RESEARCHER] Context gathered.")
        
        # 3. The Engineer
        eng_prompt = "You are the Engineer. Execute the task precisely using the Blueprint and Research provided. Output ONLY the final draft/code. No filler."
        engineer = self._create_agent("The Engineer", eng_prompt)
        self.log("[SWARM] The Engineer is building Draft V1...")
        draft_v1 = engineer.send_message(f"Task: {task_description}\n\nBlueprint:\n{blueprint}\n\nResearch:\n{research}").text
        self.log(f"[ENGINEER] Draft V1 is complete. Submitting to ATLAS for review.")
        
        return draft_v1
        
    def refine_v2(self, task_description: str, draft_v1: str, critique: str) -> str:
        """
        Phase 4: The Engineer fixes the draft based on ATLAS's ruthless critique.
        """
        if not self.client:
            return "Swarm Offline."
            
        eng_prompt = "You are the Engineer. You submitted a draft to your Boss (ATLAS), and he ripped it apart. Fix EVERY single issue he raised perfectly."
        engineer = self._create_agent("The Engineer", eng_prompt)
        self.log("[SWARM] The Engineer is frantically rewriting the draft to appease ATLAS...")
        draft_v2 = engineer.send_message(f"Original Task: {task_description}\n\nMy Draft V1:\n{draft_v1}\n\nATLAS's Critique:\n{critique}").text
        self.log(f"[ENGINEER] Draft V2 is complete. Resubmitting to ATLAS.")
        
        return draft_v2
