import sounddevice as sd
import soundfile as sf
import time
import os

def record_baseline():
    samplerate = 16000
    duration = 5  # seconds
    
    phrases = [
        "I am Mukul, the architect of this system. Protocol Omega is active.",
        "Atlas, run a full diagnostic on the command center and secure the perimeter.",
        "Testing biometric verification parameters at one hundred percent normal speed."
    ]

    print("\n[ATLAS VOICE ENROLLMENT - HIGH ACCURACY MODE]")
    print("=============================================")
    print("To make the neural network bulletproof, we will record 3 different sentences.")
    
    for idx, phrase in enumerate(phrases):
        filename = f"baseline_mukul_{idx+1}.wav"
        print(f"\n--- SAMPLE {idx+1} OF 3 ---")
        print(f"When the countdown finishes, please speak clearly:")
        print(f"\n-> '{phrase}'\n")
        
        input("Press ENTER when you are ready...")
        
        for i in range(3, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
            
        print("\n[RECORDING NOW - SPEAK!]")
        mydata = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
        sd.wait()
        
        sf.write(filename, mydata, samplerate)
        print(f"[DONE] Saved {filename}")
        
    print("\n[SUCCESS] All 3 biometric baselines are permanently enrolled.")

if __name__ == "__main__":
    record_baseline()
