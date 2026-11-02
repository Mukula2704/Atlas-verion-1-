import cv2
import face_recognition
import pickle
import os
import time

def enroll_face(num_photos=10, save_path="face_baseline.pkl"):
    print("\n[ATLAS FACIAL ENROLLMENT]")
    print("=========================")
    print("This will turn on your webcam and capture 10 images of your face.")
    print("Please slowly move your head side-to-side and up-and-down.")
    print("Press Enter to start...")
    input()
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot access the webcam.")
        return

    known_face_encodings = []
    photos_captured = 0
    
    print("\n[ATLAS] Camera active. Look at the lens.")
    
    while photos_captured < num_photos:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break
            
        # Display the frame to the user
        cv2.imshow('ATLAS Enrollment - Press Q to abort', frame)
        
        # Convert BGR (OpenCV) to RGB (face_recognition)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_frame)
        
        # If exactly one face is found, extract encodings
        if len(face_locations) == 1:
            encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            if encodings:
                known_face_encodings.append(encodings[0])
                photos_captured += 1
                print(f" -> Captured Photo {photos_captured}/{num_photos}")
                time.sleep(0.5) # Slight delay so they can move their head
        elif len(face_locations) > 1:
            print(" -> WARNING: Multiple faces detected. Please stand alone.")
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    if len(known_face_encodings) > 0:
        # Save to pickle file
        with open(save_path, 'wb') as f:
            pickle.dump(known_face_encodings, f)
        print(f"\n[SUCCESS] Extracted {len(known_face_encodings)} face encodings.")
        print(f"Saved baseline to {save_path}. ATLAS now knows your face.")
    else:
        print("\n[ERROR] No valid faces were captured. Enrollment failed.")

if __name__ == "__main__":
    enroll_face()
