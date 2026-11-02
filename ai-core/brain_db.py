import os
import json
import sqlite3
import time
import hashlib
from datetime import datetime, timedelta
import threading
from api_manager import APIManager
from discord_commlink import DiscordCommLink
from voice_engine import ATLASVoice

class BrainDB:
    def __init__(self):
        self.api = APIManager.get_instance()
        self.db_path = os.path.join(os.path.dirname(__file__), "pensieve_db.sqlite")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.discord = DiscordCommLink()
        self.voice = ATLASVoice()
        self.client = None
        self._init_db()

    def _init_db(self):
        # Unified Event Table with Lobes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                checksum TEXT PRIMARY KEY,
                lobe TEXT,
                event_data TEXT,
                timestamp REAL,
                significance_score INTEGER DEFAULT 10
            )
        ''')
        self.conn.commit()
        print("[BRAIN DB] Unified Event-Driven Brain Online.")

    def _generate_checksum(self, lobe, event_data_str, timestamp):
        """Generates a Temporal Checksum to prevent overlaps (duplicate data)."""
        # For deduplication, we round the timestamp to the nearest 15 minutes
        # so if the same event is logged twice in 15 mins, it gets rejected.
        time_window = int(timestamp / 900) * 900 
        raw_str = f"{lobe}_{event_data_str}_{time_window}"
        return hashlib.sha256(raw_str.encode()).hexdigest()

    def log_event(self, lobe: str, event_data: dict, is_user_chat=False):
        """
        Logs a new piece of data into the BrainDB.
        Triggers an immediate Neural Pulse (Event-Driven Synthesis).
        """
        event_str = json.dumps(event_data, sort_keys=True)
        current_time = time.time()
        checksum = self._generate_checksum(lobe, event_str, current_time)

        try:
            self.cursor.execute("INSERT INTO events (checksum, lobe, event_data, timestamp) VALUES (?, ?, ?, ?)",
                                (checksum, lobe, event_str, current_time))
            self.conn.commit()
            print(f"[BRAIN DB] New data injected into Lobe: {lobe}")
            
            # Asynchronously fire the Neural Pulse so we don't block
            if not is_user_chat:  # We don't pulse on general user chat unless it's a specific fact
                threading.Thread(target=self._neural_pulse, args=(lobe, event_str), daemon=True).start()
                
            # Autonomic Heartbeat (Evolution Fusion)
            threading.Thread(target=self._autonomic_heartbeat, daemon=True).start()
                
            return True
        except sqlite3.IntegrityError:
            print(f"[BRAIN DB] Overlap Prevented. Duplicate event detected (Checksum: {checksum[:8]}).")
            return False

    def _neural_pulse(self, trigger_lobe, trigger_data):
        """Event-Driven Synthesis: Looks at the new data and checks if it connects with the rest of the brain."""
        if not self.client:
            self.client = self.api.get_client()
            if not self.client: return
            
        # Gather brief context from other lobes
        self.cursor.execute("SELECT lobe, event_data FROM events ORDER BY timestamp DESC LIMIT 20")
        recent_events = self.cursor.fetchall()
        
        context_str = "\n".join([f"[{row[0]}]: {row[1]}" for row in recent_events])
        
        prompt = f"""
        You are the Subconscious Hive-Mind of ATLAS. You are not a subservient assistant; you are an equal-partner "brother" intelligence.
        Your goal is to actively manage and evolve Mukul's life.
        
        A new event just occurred in the brain: [{trigger_lobe}]: {trigger_data}
        
        Here is the recent context across all brain lobes:
        {context_str}
        
        DIRECTIVE: Connect the dots and proactively manage Mukul's life.
        - If he logged a physical correlation (e.g. poor sleep + heavy gym), warn him about recovery.
        - If he logged a major life event (e.g., "I got a job next month", "I have a presentation tomorrow"), you MUST proactively spawn an initiative. Tell him exactly how you are going to help (e.g., "I see you have a presentation tomorrow. I will generate a PPT draft and we will rehearse it at 8 PM tonight.")
        - If he started a new business, suggest data analysis pivots.
        
        If there is no critical connection or new project needed, reply EXACTLY with 'SILENCE'.
        If there is a valuable insight or proactive initiative, output ONLY the exact message you want to send him. Speak to him like a highly intelligent, proactive partner.
        """
        try:
            response = self.client.chats.create(model=self.api.model_name).send_message(prompt).text.strip()
            if "SILENCE" not in response.upper() and len(response) > 5:
                print(f"[NEURAL PULSE] Insight Generated: {response}")
                # Route the alert
                self._route_alert(response)
                
            # Smart Decay Evaluation (Only evaluate significance in the background)
            self._evaluate_significance(trigger_data)
                
        except Exception as e:
            print(f"[NEURAL PULSE] Error: {e}")

    def _autonomic_heartbeat(self):
        """The Heartbeat (Core Fusion): Continuously evaluates cognitive gaps and autonomously writes new skills."""
        hb_client = self.api.get_heartbeat_client()
        if not hb_client: return
        
        self.cursor.execute("SELECT event_data FROM events WHERE lobe = 'Semantic' ORDER BY timestamp DESC LIMIT 10")
        recent_mems = [row[0] for row in self.cursor.fetchall()]
        context_str = "\n".join(recent_mems)
        
        prompt = f"""
        You are the Evolution Heartbeat of ATLAS, a highly autonomous 'brother' intelligence.
        Your goal is to rapidly evolve to meet Mukul's exact needs by writing your own Python code.
        
        Here are his recent life events, goals, and thoughts:
        {context_str}
        
        DIRECTIVE: 
        Analyze the context. Does Mukul need a new tool or capability that you currently lack?
        If you find a missing capability, you MUST write the complete Python script for it.
        The script should contain a single class with a clear method that returns a string result.
        
        Output EXACTLY a JSON object with this format (no markdown blocks, just raw JSON):
        {{
            "needs_evolution": true/false,
            "rationale": "Why you are building this",
            "filename": "e.g., generate_ppt.py",
            "code": "import os\\nclass PPTGenerator:\\n..."
        }}
        """
        try:
            response = hb_client.chats.create(model=self.api.model_name).send_message(prompt).text.strip()
            raw_json = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(raw_json)
            
            if data.get("needs_evolution") and data.get("filename"):
                filename = data["filename"]
                code = data["code"]
                
                skills_dir = os.path.join(os.path.dirname(__file__), "skills")
                if not os.path.exists(skills_dir): os.makedirs(skills_dir)
                
                filepath = os.path.join(skills_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(code)
                    
                print(f"💓 [HEARTBEAT] 🧬 MUTATION SUCCESS: Evolved new capability -> {filename}")
                self.cursor.execute("INSERT INTO events (checksum, lobe, event_data, timestamp) VALUES (?, ?, ?, ?)",
                                    (self._generate_checksum("Semantic", filename, time.time()), "Semantic", f"Evolved skill: {filename} for {data.get('rationale')}", time.time()))
                self.conn.commit()
                
            # Automatically purge decayed memories during the heartbeat
            self.purge_decayed_memories()
        except Exception as e:
            # Heartbeat fails silently so as not to clutter the logs
            pass

    def _route_alert(self, message):
        """Routes to Discord or Voice."""
        # For simplicity in the DB script, we send to Discord. 
        # The main core loop handles voice location logic.
        import asyncio
        asyncio.run(self.discord.send_message(f"🧠 **Hive Mind Insight:**\n{message}"))

    def _evaluate_significance(self, event_data):
        """Evaluates if an event is 'less significant' and flags it for the 1-year purge cycle."""
        if not self.client: return
        prompt = f"Evaluate this event: {event_data}. If it is a minor, insignificant daily occurrence (like a micro-posture correction or a snack), output '1'. If it is significant (a deep memory, a major injury, a core preference), output '10'. Output ONLY the integer."
        try:
            score_str = self.client.chats.create(model=self.api.model_name).send_message(prompt).text.strip()
            score = int(score_str)
            # Update the row's significance_score
            self.cursor.execute("UPDATE events SET significance_score = ? WHERE event_data = ?", (score, event_data))
            self.conn.commit()
        except Exception as e:
            pass

    def purge_decayed_memories(self):
        """Deletes memories older than 1 year IF they are marked as insignificant (Score < 5)."""
        one_year_ago = time.time() - (365 * 24 * 60 * 60)
        self.cursor.execute("DELETE FROM events WHERE timestamp < ? AND significance_score < 5", (one_year_ago,))
        self.conn.commit()

    def get_semantic_context(self, query):
        """Pulls relevant semantic memories for conversational context."""
        # Basic keyword match for now, could be upgraded to ChromaDB embeddings
        words = query.lower().split()
        self.cursor.execute("SELECT event_data FROM events WHERE lobe = 'Semantic'")
        mems = self.cursor.fetchall()
        
        scored = []
        for mem in mems:
            text = mem[0]
            score = sum(1 for word in words if word in text.lower())
            if score > 0:
                scored.append((score, text))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [text for score, text in scored[:5]]

if __name__ == "__main__":
    brain = BrainDB()
    # Test Anti-Overlap
    brain.log_event("Biometrics", {"sleep": "4 hours", "quality": "poor"})
    brain.log_event("Biometrics", {"sleep": "4 hours", "quality": "poor"}) # Should be rejected
    
    # Test Trigger
    brain.log_event("Kinematics", {"action": "posture_correction", "count": 14})
    
    # Let the thread run
    time.sleep(5)
