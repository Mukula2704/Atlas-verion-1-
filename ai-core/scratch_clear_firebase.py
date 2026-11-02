from firebase_bridge import FirebaseManager

fb = FirebaseManager()
db = fb.db

# Clear context collections
print("Deleting mock context_location...")
for doc in db.collection("context_location").stream():
    doc.reference.delete()

print("Deleting mock context_biometrics...")
for doc in db.collection("context_biometrics").stream():
    doc.reference.delete()

print("Deleting mock context_gym...")
for doc in db.collection("context_gym").stream():
    doc.reference.delete()

print("Firebase mock data purged!")
