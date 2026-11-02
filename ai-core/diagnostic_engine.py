import sounddevice as sd
import cv2
import os

print("\n--- ATLAS HARDWARE DIAGNOSTICS ---")

# 1. Test Audio Devices
print("\n[1] AUDIO DEVICES:")
print(sd.query_devices())
try:
    default_input = sd.default.device[0]
    default_output = sd.default.device[1]
    print(f"\nDefault Input Device ID: {default_input}")
    print(f"Default Output Device ID: {default_output}")
except Exception as e:
    print(f"Error getting default devices: {e}")

# 2. Test MediaPipe
print("\n[2] MEDIAPIPE TEST:")
try:
    import mediapipe as mp
    print(f"MediaPipe imported. Version: {getattr(mp, '__version__', 'unknown')}")
    if hasattr(mp, 'solutions'):
        print("MediaPipe Solutions loaded successfully!")
    else:
        print("CRITICAL: MediaPipe is installed but 'solutions' is missing. This usually means a broken pip wheel on DietPi.")
except Exception as e:
    print(f"MediaPipe Import Error: {e}")

# 3. Test Camera
print("\n[3] CAMERA TEST:")
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("Camera 0 is accessible and opened successfully.")
    cap.release()
else:
    print("Camera 0 is NOT accessible. It might be on an index like 1 or 2.")
    cap1 = cv2.VideoCapture(1)
    if cap1.isOpened():
        print("Camera 1 is accessible!")
        cap1.release()

print("\n----------------------------------")
