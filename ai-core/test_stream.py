import sounddevice as sd
print("Testing sd.rec...")
recording = sd.rec(100, samplerate=48000, channels=1, dtype='int16', device=None)
sd.wait()
print("sd.rec success!")

print("Testing sd.RawInputStream...")
def callback(indata, frames, time, status):
    pass
with sd.RawInputStream(samplerate=48000, blocksize=24000, device=None, dtype='int16', channels=1, callback=callback):
    print("sd.RawInputStream success!")
