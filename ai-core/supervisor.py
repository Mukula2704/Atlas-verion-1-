import os
import json
import time
import importlib
import sys
from google import genai
from dotenv import load_dotenv
from api_manager import APIManager
from sherlock import SherlockNode
from brain_db import BrainDB
from voice_engine import ATLASVoice

class AtlasSupervisor:
    def __init__(self, log_callback=None):
        self.name = "ATLAS"
        self.api = APIManager.get_instance()
        self.client = self.api.get_client()
        self.model_name = self.api.model_name
        self.log = log_callback if log_callback else print

        self.sherlock = SherlockNode()
        self.brain = BrainDB()
        self.voice = ATLASVoice()
        self.discord = None # Removed circular import
        
        self.skills_dir = os.path.join(os.path.dirname(__file__), "skills")
        if self.skills_dir not in sys.path:
            sys.path.append(self.skills_dir)

        try:
            with open(os.path.join(os.path.dirname(__file__), "ATLAS_MANIFESTO.md"), "r", encoding="utf-8") as f:
                manifesto = f.read()
        except Exception:
            manifesto = ""
            
        try:
            self.chat = self.client.chats.create(
                model=self.model_name,
                config=genai.types.GenerateContentConfig(
                    system_instruction=f"You are {self.name}. \n\n{manifesto}"
                )
            )
            self.log(f"[{self.name}] Cognitive engine initialized.")
        except Exception as e:
            self.log(f"[{self.name}] Failed to initialize client: {str(e)}")
            self.client = None

    def _extract_and_save_memories(self, user_text):
        """Extracts facts and saves them to the Semantic Lobe, triggering an Event Synthesis."""
        if not self.client: return
        
        prompt = f"""
        Extract any enduring facts, preferences, life states, or schedule changes from this user message.
        If there are none, reply with EXACTLY 'NONE'.
        Otherwise, reply with a short summary of the facts.
        
        User Message: '{user_text}'
        """
        try:
            response = self.client.chats.create(model=self.model_name).send_message(prompt)
            facts = response.text.strip()
            if "NONE" not in facts.upper() and len(facts) > 5:
                # Log to the Semantic Lobe. The BrainDB will automatically handle Neural Pulse + Overlap Prevention.
                self.brain.log_event("Semantic", {"memory": facts}, is_user_chat=True)
                self.log(f"[BRAIN DB] New Semantic Memory Committed: {facts}")
        except Exception as e:
            self.log(f"[BRAIN DB] Semantic Extraction failed: {e}")

    def process_command(self, user_text, log_callback=None):
        """The core interaction loop."""
        if not self.client:
            return "ATLAS [System]: Neural link offline."
            
        try:
            # 1. Extract new semantic memories (sync)
            self._extract_and_save_memories(user_text)
            
            # 2. Get hardware context
            hardware_context = self.sherlock.get_master_context()
            
            # 3. Get historical memory context from Semantic Lobe
            relevant_memories = self.brain.get_semantic_context(user_text)
            memory_context = ""
            if relevant_memories:
                memory_context = "[RELEVANT PAST MEMORIES]\n" + "\n".join([f"- {m}" for m in relevant_memories]) + "\n[END MEMORIES]\n"
                
            # 4. Expose Autonomous Skills
            available_skills = []
            if os.path.exists(self.skills_dir):
                for f in os.listdir(self.skills_dir):
                    if f.endswith(".py") and f != "__init__.py":
                        available_skills.append(f.replace(".py", ""))
            
            skills_context = ""
            if available_skills:
                skills_context = f"[AVAILABLE AUTONOMOUS SKILLS]\nYou have evolved the following tools: {', '.join(available_skills)}.\nTo use one, reply EXACTLY with the text: [SKILL: skill_name] followed by your response.\n[END SKILLS]\n"
                
            # 5. Synthesize prompt
            full_prompt = f"{hardware_context}\n{memory_context}\n{skills_context}\nUser says: {user_text}"
            
            # 6. Generate response
            response = self.chat.send_message(full_prompt)
            resp_text = response.text
            
            # 7. Check if ATLAS wants to use an evolved skill
            if "[SKILL:" in resp_text:
                skill_name = resp_text.split("[SKILL:")[1].split("]")[0].strip()
                self.log(f"[EVOLUTION ENGINE] Triggering autonomous skill: {skill_name}")
                try:
                    # Dynamically load the python module
                    module = importlib.import_module(skill_name)
                    # We assume every skill has an 'execute(context)' function
                    if hasattr(module, 'execute'):
                        skill_result = module.execute(user_text)
                        # Feed the result back into the prompt
                        resp_text = self.chat.send_message(f"Skill {skill_name} executed. Result: {skill_result}. Continue.").text
                    else:
                        resp_text = self.chat.send_message(f"Skill {skill_name} is malformed. Proceed without it.").text
                except Exception as e:
                    self.log(f"[EVOLUTION ENGINE] Skill execution failed: {e}")
            
            # 8. Check if ATLAS wants to move a physical limb (Motor Command)
            if "[MOTOR_COMMAND:" in resp_text:
                motor_string = resp_text.split("[MOTOR_COMMAND:")[1].split("]")[0].strip()
                try:
                    parts = motor_string.split(":", 1)
                    action = parts[0].strip()
                    details = parts[1].strip() if len(parts) > 1 else ""
                    
                    self.log(f"[MOTOR CORTEX] Impulse Generated -> {action}: {details}")
                    
                    # Push to the Spinal Cord (Firebase)
                    self.sherlock.firebase.db.collection("motor_cortex").add({
                        "action": action,
                        "details": details,
                        "timestamp": time.time(),
                        "status": "pending"
                    })
                    
                    # Discord Verification Loop for Payments
                    if "stage_payment" in action.lower():
                        msg = f"🛒 **ATLAS Procurement Verification**\nI have staged the following order: {details}.\n\nReply 'approve' to execute the final button press."
                        self.sherlock.firebase.db.collection("command_center").document("discord_pager").collection("pending").add({
                            "message": msg,
                            "timestamp": time.time()
                        })
                except Exception as e:
                    self.log(f"[MOTOR CORTEX] Failed to route impulse: {e}")
                    
            return resp_text
                
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                return "Sir, our cognitive neural-link quota has been exhausted for the day. Please check billing."
            return f"System Error: {error_str}"
