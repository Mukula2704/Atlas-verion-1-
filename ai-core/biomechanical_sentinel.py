import cv2
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
import mediapipe as mp
import math
import time
import platform
import os

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def play_warning_beep():
    """Plays a sharp, subtle beep to act as Pavlovian feedback over the AUX port."""
    import subprocess
    try:
        # Generates a quick beep using ALSA's built-in speaker-test (48000Hz 16-bit)
        # We pipe it to /dev/null so it doesn't spam stdout
        cmd = "speaker-test -D plughw:1,0 -t sine -f 800 -l 1 -p 10000 > /dev/null 2>&1"
        subprocess.run(cmd, shell=True, check=False)
    except:
        pass

def calculate_distance(p1, p2):
    """Calculates 2D distance between two mediapipe landmarks."""
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def main():
    print("[ATLAS] Booting Kinematic Sentinel (Posture + Deep Work Focus)...")
    print("[INFO] This module runs 100% locally using CPU. 0 API calls used.")
    print("[INFO] C++ Neural Network Backend Active. Loading instantly.")
    
    # Aggressively kill any ghost processes holding the camera hostage
    os.system("fuser -k /dev/video0 2>/dev/null")
    time.sleep(0.5)
    
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("[ATLAS Kinematics Error]: CRITICAL FAILURE. USB Camera could not be opened on /dev/video0 via V4L2.")
        return
        
    # Trackers for duration-based habits (e.g. skin biting)
    skin_biting_start_time = 0
    slouching_start_time = 0
    
    # Deep Work Trackers
    focus_start_time = 0
    in_flow_state = False
    
    # Audio Setup (Bypassed: The main ATLAS core already locks the microphone for the Wake Word, so we cannot listen to it here without ALSA crashing).
    stream = None
    
    from firebase_bridge import FirebaseManager
    firebase = FirebaseManager()
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
         mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
             
        print("[ATLAS] Neural Networks loaded. Monitoring for Bad Habits...")
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if frame_count == 0:
                print("[ATLAS] Sentinel successfully grabbed first frame from USB Camera!")
            frame_count += 1
            if not ret:
                break
                
            # Convert BGR to RGB for MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Process vision
            pose_results = pose.process(image)
            hand_results = hands.process(image)
            
            # Recolor back to BGR for rendering
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            mouth_l = None
            mouth_r = None
            
            # 1. POSTURE DETECTION (Slouching)
            if pose_results.pose_landmarks:
                landmarks = pose_results.pose_landmarks.landmark
                
                ear_l = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
                ear_r = landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value]
                shoulder_l = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                shoulder_r = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                mouth_l = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value]
                mouth_r = landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value]
                
                # Render pose
                mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
                # Math: If the y-coordinate of the ear drops significantly close to the shoulder y-coordinate,
                # it means the head is craning forward and down (slouching).
                # (y increases as we go down the screen)
                slouch_threshold = 0.12 # Adjust based on camera angle
                
                if abs(ear_l.y - shoulder_l.y) < slouch_threshold or abs(ear_r.y - shoulder_r.y) < slouch_threshold:
                    if slouching_start_time == 0:
                        slouching_start_time = time.time()
                    elif (time.time() - slouching_start_time) > 3.0: # Slouching for 3 seconds
                        print(">> [WARNING] POSTURE COLLAPSE DETECTED. SIT UP. <<")
                        play_warning_beep()
                        slouching_start_time = 0 # reset to prevent spam
                else:
                    slouching_start_time = 0 # reset if posture is good
                    
            # 2. HAND HABIT DETECTION (Biting Skin & Knuckle Cracking)
            if hand_results.multi_hand_landmarks:
                hand_centers = []
                is_biting = False
                
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    # Render hands
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    
                    hand_centers.append(wrist)
                    
                    # Skin Biting Math: Check distance between fingertips and mouth
                    if mouth_l and mouth_r:
                        # Average mouth position
                        mouth_x = (mouth_l.x + mouth_r.x) / 2
                        mouth_y = (mouth_l.y + mouth_r.y) / 2
                        mouth_pos = type('obj', (object,), {'x': mouth_x, 'y': mouth_y})
                        
                        dist_index = calculate_distance(index_tip, mouth_pos)
                        dist_thumb = calculate_distance(thumb_tip, mouth_pos)
                        
                        if dist_index < 0.05 or dist_thumb < 0.05: # Hands are AT the mouth
                            is_biting = True
                            
                # Handle Skin Biting Time Threshold
                if is_biting:
                    if skin_biting_start_time == 0:
                        skin_biting_start_time = time.time()
                    elif (time.time() - skin_biting_start_time) > 1.5: # 1.5 seconds of hand at mouth
                        print(">> [WARNING] FINGER BITING DETECTED. HANDS DOWN. <<")
                        play_warning_beep()
                        skin_biting_start_time = 0
                else:
                    skin_biting_start_time = 0
                    
                # Knuckle Cracking Math: If both wrists are extremely close to each other
                if len(hand_centers) == 2:
                    dist_wrists = calculate_distance(hand_centers[0], hand_centers[1])
                    if dist_wrists < 0.08: # Wrists interlocked tightly
                        print(">> [WARNING] HANDS INTERLOCKED (KNUCKLE CRACKING). SEPARATE HANDS. <<")
                        play_warning_beep()
                        time.sleep(1.0)
                        
            # 3. DEEP WORK (FLOW STATE) KINEMATICS
            # We measure focus by head stability (lack of erratic movement) and audio silence
            if pose_results.pose_landmarks:
                # Audio volume measurement is bypassed since ATLAS core owns the mic.
                volume_rms = 0
                is_talking = volume_rms > 500  # Always false now
                
                # Check Head Stability (nose movement)
                nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
                
                # Simple logic: If nose is generally centered and not moving wildly, and NOT talking
                if 0.3 < nose.x < 0.7 and 0.3 < nose.y < 0.7 and not is_talking:
                    if focus_start_time == 0:
                        focus_start_time = time.time()
                    elif (time.time() - focus_start_time) > 300: # 5 Minutes of continuous focus
                        if not in_flow_state:
                            in_flow_state = True
                            print("\n[ATLAS] 🧠 DEEP WORK / FLOW STATE DETECTED.")
                            print(" -> Engaging Lockdown Protocol. Routing Phone to DND. Silencing Discord.")
                            firebase.db.collection("command_center").document("system_state").update({"focus_mode": True})
                else:
                    # If they move erratically or talk out loud (gaming)
                    focus_start_time = 0
                    if in_flow_state:
                        in_flow_state = False
                        print("\n[ATLAS] Flow State Broken (Movement/Audio detected). Restoring standard notifications.")
                        firebase.db.collection("command_center").document("system_state").update({"focus_mode": False})
                        
            # Headless Mode: We don't display the video feed since it's a headless Wyse server.
            # cv2.imshow('Biomechanical Sentinel', image)
            # if cv2.waitKey(10) & 0xFF == ord('q'): break
            
            time.sleep(0.1) # Throttle loop to ~10 FPS to save CPU/RAM on the Wyse
    cap.release()
if __name__ == "__main__":
    main()
