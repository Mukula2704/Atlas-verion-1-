import json
import time
import asyncio
from datetime import datetime
from firebase_bridge import FirebaseManager
from voice_engine import ATLASVoice

TIMETABLE_FILE = "timetable.json"

class ChronosEngine:
    def __init__(self):
        self.firebase = FirebaseManager()
        self.voice = ATLASVoice()
        self.notified_events = set()
        
    def get_timetable(self):
        with open(TIMETABLE_FILE, 'r') as f:
            return json.load(f)['events']
            
    def update_event(self, event_title_keyword, new_start, new_end=None):
        """
        Surgically updates a timetable event without hallucination.
        Intended to be called strictly via LLM function calling.
        """
        try:
            with open(TIMETABLE_FILE, 'r') as f:
                data = json.load(f)
                
            updated = False
            for event in data['events']:
                if event_title_keyword.lower() in event['title'].lower():
                    event['start_time'] = new_start
                    if new_end:
                        event['end_time'] = new_end
                    updated = True
                    break
                    
            if updated:
                with open(TIMETABLE_FILE, 'w') as f:
                    json.dump(data, f, indent=2)
                return f"Successfully updated '{event_title_keyword}' to start at {new_start}."
            return f"Error: Could not find event matching '{event_title_keyword}'."
        except Exception as e:
            return f"Error updating timetable: {e}"

    async def poll_schedule(self):
        """Continuously checks the current time against the active timetable."""
        print("[CHRONOS] Engine Online. Monitoring time-blocks...")
        
        while True:
            now = datetime.now()
            current_time_str = now.strftime("%H:%M")
            
            timetable = self.get_timetable()
            
            for event in timetable:
                if current_time_str == event['start_time'] and event['id'] not in self.notified_events:
                    await self.trigger_alert(event)
                    self.notified_events.add(event['id'])
                    
            # Clear notifications at midnight to reset for next day
            if current_time_str == "00:00":
                self.notified_events.clear()
                
            await asyncio.sleep(30) # Poll every 30 seconds

    async def trigger_alert(self, event):
        """Handles alert routing based on Priority Level."""
        title = event['title']
        desc = event['description']
        priority = event['priority']
        
        message = f"⏰ **TIME BLOCK STARTING:** {title}\n*Details:* {desc}"
        
        print(f"\n[CHRONOS] Event Triggered: {title} (Priority: {priority})")
        
        if priority == "HIGH":
            # Aggressive logic: Voice + Discord, potentially looping until acknowledged
            # For this MVP, we hit both systems simultaneously.
            print(f" -> [ROUTING] High Priority. Dispatching Voice + Discord Comm-Link.")
            
            self.firebase.db.collection("command_center").document("discord_pager").collection("pending").add({
                "message": f"🚨 {message}\n**(HIGH PRIORITY)**",
                "timestamp": time.time()
            })
            
            # Announce out loud
            voice_prompt = f"Sir. It is time for {title}. Please transition immediately."
            await asyncio.to_thread(self.voice.speak, voice_prompt)
            
            # In a full implementation, we'd spawn a while loop checking Firebase for an 'acknowledged' flag here
            
        elif priority == "MEDIUM":
            print(f" -> [ROUTING] Medium Priority. Dispatching Voice.")
            voice_prompt = f"Reminder: {title} is starting."
            await asyncio.to_thread(self.voice.speak, voice_prompt)
            
        else:
            # Low Priority: Silent Discord Ping Only
            print(f" -> [ROUTING] Low Priority. Silent Discord Ping.")
            self.firebase.db.collection("command_center").document("discord_pager").collection("pending").add({
                "message": f"ℹ️ {message}",
                "timestamp": time.time()
            })

if __name__ == "__main__":
    engine = ChronosEngine()
    # Test update function
    # print(engine.update_event("TRAINING", "17:30"))
    
    asyncio.run(engine.poll_schedule())
