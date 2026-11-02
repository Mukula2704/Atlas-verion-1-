import os
import discord
import asyncio
from dotenv import load_dotenv
from firebase_bridge import FirebaseManager
import time
import io
import aiohttp
from voice_engine import ATLASVoice

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
ALLOWED_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

class DiscordCommLink(discord.Client):
    def __init__(self, *args, **kwargs):
        if 'intents' not in kwargs:
            intents = discord.Intents.default()
            intents.message_content = True
            kwargs['intents'] = intents
        super().__init__(*args, **kwargs)
        self.firebase = FirebaseManager()
        self.target_channel = None
        print("[DISCORD PAGER] Initializing ATLAS Notification System...")

    async def on_ready(self):
        print(f"[DISCORD PAGER] Online as {self.user}. Waiting for critical alerts...")
        # Start the background task to listen to Firebase for notifications
        self.bg_task = self.loop.create_task(self.monitor_notifications())

    async def monitor_notifications(self):
        """Polls Firebase for new critical alerts that need to be sent to Mukul"""
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                # In a real implementation, we would use Firestore listeners.
                # For this pager, we just check a 'pending_alerts' collection.
                docs = self.firebase.db.collection("command_center").document("discord_pager").collection("pending").get()
                for doc in docs:
                    alert = doc.to_dict()
                    message = alert.get("message", "System Alert")
                    
                    # Find a channel to send to if not explicitly set
                    if not self.target_channel:
                        for guild in self.guilds:
                            for channel in guild.text_channels:
                                if channel.permissions_for(guild.me).send_messages:
                                    self.target_channel = channel
                                    break
                    
                    if self.target_channel:
                        # Check Focus Mode
                        sys_state = self.firebase.db.collection("command_center").document("system_state").get().to_dict()
                        if sys_state and sys_state.get("focus_mode", False):
                            print(f"[DISCORD PAGER] Focus Mode Active. Suppressing alert: {message}")
                            # Keep it in pending, or handle differently. For now, we skip sending.
                            continue
                            
                        await self.target_channel.send(f"⚠️ **ATLAS ALERT** ⚠️\n{message}")
                        # Delete the alert so it doesn't send twice
                        self.firebase.db.collection("command_center").document("discord_pager").collection("pending").document(doc.id).delete()
            except Exception as e:
                print(f"[DISCORD PAGER] Error checking alerts: {e}")
                
            await asyncio.sleep(5) # Check every 5 seconds

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Security check (ensure it's from the allowed channel if set)
        if self.target_channel and message.channel.id != self.target_channel.id:
            return

        print(f"[DISCORD INBOX] {message.author}: {message.content}")

        # ---------------------------------------------------------
        # 1. VISION AI + OMNI-ROUTING (For Image Uploads)
        # ---------------------------------------------------------
        if message.attachments:
            attachment = message.attachments[0]
            if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'webp']):
                print(f"[DISCORD VISION] Received image: {attachment.filename}")
                
                async with message.channel.typing():
                    image_bytes = await attachment.read()
                    
                    print("[DISCORD VISION] Processing image via APIManager...")
                    try:
                        from api_manager import APIManager
                        from google.genai import types
                        api = APIManager.get_instance()
                        client = api.get_client()
                        
                        prompt = "You are ATLAS. Analyze this image. If it is food, estimate the calories and macros (protein, carbs, fats) and ask if I want to log it to The Pantry. Be concise and professional."
                        
                        part = types.Part.from_bytes(data=image_bytes, mime_type=attachment.content_type)
                        response = await asyncio.to_thread(
                            client.models.generate_content,
                            model=api.model_name,
                            contents=[prompt, part]
                        )
                        estimate = response.text.strip()
                    except Exception as e:
                        estimate = f"Vision Analysis Error: {e}"
                    
                    print("[DISCORD VISION] Context analyzed. Routing response...")
                    
                    # Omni-Routing Matrix
                    # Check if user is physically at the Mac (via Spatial Camera Firebase state)
                    doc = self.firebase.db.collection("command_center").document("spatial_state").get()
                    if doc.exists:
                        data = doc.to_dict()
                        state = data.get("orientation", "")
                        timestamp = data.get("timestamp", 0)
                        
                        # If camera saw a face within the last 5 minutes
                        if state == "FACE / POSTURE MODE" and (time.time() - timestamp) < 300:
                            print(" -> [ROUTING] User detected at Mac. Routing to Room Speaker.")
                            voice = ATLASVoice()
                            # Spontaneous output without wake-word (per user approval)
                            await asyncio.to_thread(voice.speak, estimate)
                            return
                            
                    # Default Fallback: Reply on Discord
                    print(" -> [ROUTING] User not at desk. Routing to Discord/Comm-Link.")
                    await message.channel.send(f"📸 **Vision Analysis:** {estimate}")
                return

        # ---------------------------------------------------------
        # 2. STANDARD TEXT PROCESSING (Supervisor Swarm)
        # ---------------------------------------------------------
        async with message.channel.typing():
            from supervisor import AtlasSupervisor
            brain = AtlasSupervisor()
            ai_response = await asyncio.to_thread(brain.process_command, message.content)
            
        await message.channel.send(ai_response)

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordCommLink(intents=intents)
    client.run(TOKEN)
