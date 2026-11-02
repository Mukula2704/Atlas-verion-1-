import os
import time
import asyncio
import sounddevice as sd
import soundfile as sf
import torch
from speechbrain.inference.speaker import SpeakerRecognition
from speechbrain.utils.fetching import LocalStrategy
from voice_engine import ATLASVoice

def record_test_audio(filename="test_sample.wav", duration=5, samplerate=16000):
    print("\n[ATLAS LIVE VERIFICATION TEST]")
    print("==============================")
    print("Say anything you want! For example: 'Atlas, verify my identity.'")
    
    for i in range(3, 0, -1):
        print(f"Recording in {i}...")
        time.sleep(1)
        
    print("\n[RECORDING NOW - SPEAK!]")
    mydata = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
    sd.wait()
    
    sf.write(filename, mydata, samplerate)
    print(f"[DONE] Test audio saved.")
    return filename

async def verify_user():
    test_file = record_test_audio()
    
    print("\n[ATLAS] Booting Neural Network (SpeechBrain ECAPA-TDNN)...")
    print("        (This may take a few seconds the very first time to load the model)")
    
    # Load the pre-trained Speaker Recognition model
    verification = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", 
        savedir="pretrained_models/spkrec-ecapa-voxceleb",
        run_opts={"device":"cpu"}, # Using CPU to ensure compatibility
        local_strategy=LocalStrategy.COPY # Fix for Windows Admin/Symlink error
    )
    
    print("\n[ATLAS] Analyzing vocal frequencies against your 3 baselines...")
    
    scores = []
    # Compare against all 3 baselines
    for i in range(1, 4):
        baseline_file = f"baseline_mukul_{i}.wav"
        if not os.path.exists(baseline_file):
            print(f"Error: Could not find {baseline_file}")
            continue
            
        score, prediction = verification.verify_files(test_file, baseline_file)
        # score is a tensor, we extract the float value
        scores.append(score.item())
        print(f" -> Match vs Baseline {i}: Score {score.item():.4f}")
        
    if not scores:
        print("No baselines found to compare against!")
        return
        
    avg_score = sum(scores) / len(scores)
    print(f"\n[RESULT] Average Match Score: {avg_score:.4f}")
    
    # Typically, a score above 0.25 indicates a strong match for this specific model
    THRESHOLD = 0.25 
    
    atlas = ATLASVoice()
    
    if avg_score >= THRESHOLD:
        print("\n>> VERIFICATION SUCCESSFUL. IDENTITY CONFIRMED: MUKUL <<")
        await atlas._generate_and_play("Voice pattern recognized. Welcome back, Mukul.")
    else:
        print("\n>> VERIFICATION FAILED. UNRECOGNIZED VOICE GUEST DETECTED <<")
        await atlas._generate_and_play("Unrecognized voice detected. Switching to Guest Mode. Limited access granted.")
        
    # Clean up test file
    try:
        os.remove(test_file)
    except:
        pass

if __name__ == "__main__":
    asyncio.run(verify_user())
