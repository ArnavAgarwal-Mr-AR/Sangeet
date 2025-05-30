import os
from modules.beat_selector import get_beat_path
from modules.lyrics_generator import generate_line
from modules.tts_engine import text_to_speech
from utils.audio_utils import play_looped_audio
import time

if __name__ == "__main__":
    print("🎤 Welcome to Freestyle AI Rapper!")
    user_prompt = input("Enter a beat style (or choose from predefined: lofi chill, trap 808, boom bap, jazzy freestyle, drill vibes): ").strip()

    # Get beat path (pre-generated or generated)
    beat_path = get_beat_path(user_prompt)

    # Play beat loop (non-blocking)
    print(f"\n🎵 Playing beat: {beat_path}")
    play_looped_audio(beat_path)

    # Main freestyle loop
    while True:
        try:
            line = generate_line()
            print("🤖 AI:", line)
            text_to_speech(line)
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Session ended.")
            break
