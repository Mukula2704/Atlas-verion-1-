from firebase_bridge import FirebaseManager

class SherlockNode:
    def __init__(self):
        self.firebase = FirebaseManager()
        print("[SHERLOCK] Context Engine Online.")

    def get_master_context(self) -> str:
        """
        Pulls the latest data from physical sensors (Firebase) and compiles it into a string.
        """
        # Fetch latest documents
        location_data = self.firebase.get_latest_document("context_location")
        biometric_data = self.firebase.get_latest_document("context_biometrics")
        gym_data = self.firebase.get_latest_document("context_gym")

        context_lines = []
        
        # Parse Location
        if location_data:
            loc = location_data.get("location_name", "Unknown Location")
            coords = location_data.get("coordinates", "")
            context_lines.append(f"Physical Location: {loc} {coords}")
        else:
            context_lines.append("Physical Location: Offline")

        # Parse Biometrics (Huawei Health)
        if biometric_data:
            sleep = biometric_data.get("sleep_hours", "Unknown")
            hr = biometric_data.get("heart_rate", "Unknown")
            hrv = biometric_data.get("hrv", "Unknown")
            context_lines.append(f"Biometrics -> Sleep: {sleep}h | HR: {hr}bpm | HRV: {hrv}ms")
        else:
            context_lines.append("Biometrics: Offline")

        # Parse Gym
        if gym_data:
            last_workout = gym_data.get("workout_type", "Unknown")
            intensity = gym_data.get("intensity", "Unknown")
            time_ago = gym_data.get("time_ago", "Unknown")
            context_lines.append(f"Gym Status -> Last Session: {last_workout} ({intensity} intensity) - {time_ago}")
        else:
            context_lines.append("Gym Status: No recent logs")

        master_context = "\n".join(context_lines)
        return f"[SYSTEM CONTEXT - DO NOT ACKNOWLEDGE TO USER DIRECTLY UNLESS RELEVANT]\n{master_context}\n[END CONTEXT]"
