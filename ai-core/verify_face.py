import cv2
import face_recognition
import pickle
import os
import time

def verify_face(baseline_path="face_baseline.pkl", timeout_seconds=15):
    """
    Opens the webcam and scans for a face matching the baseline.
    Returns True if Mukul is identified within the timeout, False otherwise.
    """
    if not os.path.exists(baseline_path):
        print(f"[ERROR] Baseline file {baseline_path} not found. Run enroll_face.py first.")
        return False
        
    print("[ATLAS] Loading Facial Encodings...")
    with open(baseline_path, 'rb') as f:
        known_face_encodings = pickle.load(f)
        
    if not known_face_encodings:
        print("[ERROR] No encodings found in baseline.")
        return False

    print("\n[ATLAS WAKE-LOCK] Camera active. Scanning for Mukul...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot access the webcam.")
        return False

    start_time = time.time()
    identified = False
    
    while (time.time() - start_time) < timeout_seconds:
        ret, frame = cap.read()
        if not ret:
            continue
            
        # Optional: resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Display the scanner window
        cv2.imshow('ATLAS BIOMETRIC WAKE-LOCK SCANNER', frame)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for face_encoding in face_encodings:
            # Compare with our baseline (tolerance 0.4 is strict, 0.6 is default)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            
            # If we get enough True matches against our 10-15 baseline photos
            if True in matches:
                identified = True
                print("\n[SUCCESS] VISUAL IDENTITY CONFIRMED: MUKUL.")
                break
                
        if identified:
            break
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    if not identified:
        print("\n[FAIL] Wake-Lock timeout. Unrecognized or no face detected.")
        
    return identified

if __name__ == "__main__":
    result = verify_face()
    print(f"Final Verification Result: {result}")
