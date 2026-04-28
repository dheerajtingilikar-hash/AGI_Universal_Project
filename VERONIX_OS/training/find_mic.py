import sounddevice as sd

print("\n--- AVAILABLE AUDIO DEVICES ---")
print(sd.query_devices())
print("-------------------------------\n")

# This will auto-detect your system default
default_input = sd.default.device
print(f"Your system default input ID is: {default_input}")