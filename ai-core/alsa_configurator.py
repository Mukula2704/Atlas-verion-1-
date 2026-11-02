import os

asound_conf = """
pcm.!default {
    type asym
    playback.pcm "plughw:1,0"
    capture.pcm "plughw:0,0"
}
ctl.!default {
    type hw
    card 1
}
"""

try:
    with open("/etc/asound.conf", "w") as f:
        f.write(asound_conf)
    print("\n[SUCCESS] /etc/asound.conf written successfully!")
    print("ALSA is now permanently routed:")
    print(" - Microphone -> USB Webcam (Card 0)")
    print(" - Speaker -> 3.5mm AUX Jack (Card 1)")
    print(" - Automatic software resampling enabled (plughw)")
except PermissionError:
    print("\n[ERROR] Permission denied. You must run this as root!")
except Exception as e:
    print(f"\n[ERROR] {e}")
