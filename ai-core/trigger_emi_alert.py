from firebase_bridge import FirebaseManager
import time

def trigger_emi_alert():
    print("Simulating Financial Sniper detecting low balance/EMI...")
    firebase = FirebaseManager()
    
    alert_text = "⚠️ **CRITICAL FINANCIAL ALERT** ⚠️\nYour account balance is dangerously low at Rs. 5000, and you have an HDFC EMI of Rs. 15000 due in 3 days. \n\nShould I initiate an emergency fund transfer from your secondary account, or do you want to handle this manually?"
    
    firebase.db.collection("command_center").document("discord_pager").collection("pending").add({
        "message": alert_text,
        "timestamp": time.time()
    })
    
    print("Alert pushed to Firebase 'discord_pager/pending' collection.")
    print("The Discord Bot will pick it up and ping the user shortly.")

if __name__ == "__main__":
    trigger_emi_alert()
