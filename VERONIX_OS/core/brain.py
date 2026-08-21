# AGI/core/brain.py

from io.voice import speak
from io.listen import listen
from core.agent import generate
from engine.background import start_background
from core.state import BrainState

import threading

state = BrainState()
shutdown = threading.Event()

def start_brain():
    print("[AGI] Booting Veronix Core...")

    start_background(state, shutdown)

    speak("Veronix system online. Modular brain activated.")

    while not shutdown.is_set():

        user = listen()
        if not user:
            continue

        state.update_emotion(user)

        if "exit" in user.lower():
            speak("Shutting down.")
            shutdown.set()
            break

        response = generate(user, state)
        speak(response)