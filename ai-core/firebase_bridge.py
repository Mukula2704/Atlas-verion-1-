import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import threading

class FirebaseManager:
    def __init__(self, key_path=None):
        if key_path is None:
            key_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
            
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"Firebase key not found at {key_path}. Please download it from Firebase Console -> Project Settings -> Service Accounts.")
        
        cred = credentials.Certificate(key_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.stream_ref = self.db.collection('ai_stream')
        self.watchers = []
        
        print("[Firebase] Connected to Command Center Nervous System.")

    def log_action(self, agent_name, text, is_action=False):
        """Pushes a log to the AI Terminal on the dashboard in real-time."""
        self.stream_ref.add({
            "agent": agent_name,
            "text": text,
            "isAction": is_action,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"[{agent_name}] {text}")

    def listen_to_collection(self, collection_name, callback):
        """Sets up a continuous WebSocket listener on a Firebase collection."""
        col_ref = self.db.collection(collection_name)
        
        # We use a threading event to keep the listener alive
        callback_done = threading.Event()

        def on_snapshot(col_snapshot, changes, read_time):
            for change in changes:
                if change.type.name == 'ADDED':
                    callback(change.document.id, change.document.to_dict())

        watch = col_ref.on_snapshot(on_snapshot)
        self.watchers.append(watch)
        print(f"[Firebase] Listening to {collection_name}...")

    def update_document(self, collection, doc_id, data):
        self.db.collection(collection).document(doc_id).set(data, merge=True)
        
    def get_latest_document(self, collection_name):
        """Fetches the most recent document from a collection, ordered by timestamp."""
        try:
            docs = self.db.collection(collection_name).order_by(
                'timestamp', direction=firestore.Query.DESCENDING
            ).limit(1).stream()
            
            for doc in docs:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"[Firebase] Error fetching latest document from {collection_name}: {e}")
            return None
