import cv2
import time
import os
import asyncio
from firebase_bridge import FirebaseManager
from workspace_architect import WorkspaceArchitect
import threading

class SpatialCamera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.firebase = FirebaseManager()
        self.architect = WorkspaceArchitect()
        self.scan_requested = False
        
        # Initialize OpenCV Haar Cascade for Face Detection (Fast and lightweight)
        cascade_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        self.current_state = "UNKNOWN"
        self.cap = None

    def trigger_callback(self, doc_id, data):
        action = data.get("action", "")
        if action == "SCAN":
            self.scan_requested = True

    def start(self):
        print(f"[SPATIAL CAMERA] Initializing on Logitech Webcam (Camera {self.camera_index})...")
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        
        if not self.cap.isOpened():
            print("[ERROR] Could not connect to camera. Please check USB connection.")
            return

        # Request 720p
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Listen for external commands from the Voice Engine or Dashboard
        self.firebase.listen_to_collection("camera_triggers", self.trigger_callback)

        print("[SPATIAL CAMERA] Engine Active. Press 'q' to quit, 's' to simulate manual scan.")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    time.sleep(0.1)
                    continue
                
                # Check for scan trigger (either from Firebase or Keyboard 's')
                if self.scan_requested:
                    self.scan_requested = False
                    if self.current_state == "DESK / SCANNER MODE":
                        print("[SPATIAL CAMERA] Scan triggered! Capturing desk frame...")
                        scan_dir = os.path.join(os.path.dirname(__file__), "..", "data")
                        os.makedirs(scan_dir, exist_ok=True)
                        scan_path = os.path.join(scan_dir, f"scan_{int(time.time())}.jpg")
                        cv2.imwrite(scan_path, frame)
                        
                        # Offload the processing to the Workspace Architect
                        def run_scan(path):
                            asyncio.run(self.architect.scan_handwritten_note(path))
                        
                        threading.Thread(target=run_scan, args=(scan_path,)).start()
                    else:
                        print("[SPATIAL CAMERA] Cannot scan desk while a face is in the frame. Tilt camera down.")

                # Convert to grayscale for Face Detection
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(
                    gray_frame, 
                    scaleFactor=1.1, 
                    minNeighbors=5, 
                    minSize=(50, 50)
                )
                
                new_state = "DESK / SCANNER MODE"
                if len(faces) > 0:
                    new_state = "FACE / POSTURE MODE"
                    # Draw a rectangle around the face
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # State transition logic
                if new_state != self.current_state:
                    self.current_state = new_state
                    print(f" -> [STATE CHANGE] Camera is now in: {self.current_state}")
                    # Update Firebase so Dashboard knows where the camera is looking
                    self.firebase.db.collection("command_center").document("spatial_state").set({
                        "orientation": self.current_state,
                        "timestamp": time.time()
                    })
                
                # Overlay mode on the video feed
                color = (0, 255, 0) if self.current_state == "FACE / POSTURE MODE" else (0, 0, 255)
                cv2.putText(frame, self.current_state, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                
                # Show the video feed for testing
                cv2.imshow('ATLAS Spatial Camera (Testing Mode)', frame)
                
                key = cv2.waitKey(5) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    self.scan_requested = True

        except KeyboardInterrupt:
            print("\n[SPATIAL CAMERA] Shutting down...")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    camera = SpatialCamera(camera_index=0)
    camera.start()
