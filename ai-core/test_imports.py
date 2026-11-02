import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

try:
    from firebase_bridge import FirebaseManager
    print("[SUCCESS] Firebase imported successfully!")
except Exception as e:
    print(f"[ERROR] Firebase import failed: {e}")

try:
    import mediapipe as mp
    print(f"[SUCCESS] MediaPipe {mp.__version__} imported successfully!")
except Exception as e:
    print(f"[ERROR] MediaPipe import failed: {e}")
