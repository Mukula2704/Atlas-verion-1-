import cv2
import sounddevice as sd
import numpy as np

print("--- EXTREME HARDWARE TEST ---")

# 1. Test Camera
print("\n[1] Testing Camera (Trying multiple indices)...")
for i in range(4):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            print(f" -> SUCCESS: Camera light should be ON! Found working video feed on Index {i}")
            cv2.imwrite(f"camera_test_{i}.jpg", frame)
            cap.release()
            break
        else:
            print(f" -> Index {i} opened, but returned an empty frame (Metadata node).")
        cap.release()
    else:
        print(f" -> Index {i} failed to open.")

# 2. Test Audio (ALSA Default)
print("\n[2] Testing Microphone (Recording 3 seconds)...")
try:
    # Use explicitly plughw:0,0 at 48000Hz to match the core engine exactly
    recording = sd.rec(int(3 * 48000), samplerate=48000, channels=1, dtype='int16', device=None)
    sd.wait()
    
    # Calculate volume (RMS) to see if it's dead silence or actually picking up room noise
    rms = np.sqrt(np.mean(np.square(recording, dtype=np.float64)))
    print(f" -> SUCCESS: Microphone recorded successfully! Volume Level (RMS): {rms:.2f}")
    if rms < 10:
        print(" -> WARNING: Volume is basically 0. The microphone is likely HARDWARE MUTED by Linux.")
        print("    Run this in the terminal: amixer -c 0 sset Mic 100% unmute")
except Exception as e:
    print(f" -> ERROR: Microphone crashed: {e}")

print("-----------------------------")
