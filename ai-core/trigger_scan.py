import time
from firebase_bridge import FirebaseManager
from firebase_admin import firestore

print("Triggering Scan...")
firebase = FirebaseManager()
firebase.db.collection("camera_triggers").add({
    "action": "SCAN",
    "timestamp": firestore.SERVER_TIMESTAMP
})
print("Scan triggered via Firebase!")
