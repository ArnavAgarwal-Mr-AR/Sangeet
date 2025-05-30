import gradio as gr
from modules.beat_selector import get_beat_path
from modules.lyrics_generator import generate_line
from modules.tts_engine import text_to_speech
from modules.musicgen import init_musicgen  # ✅ ADD THIS
from utils.audio_utils import play_looped_audio
import os
import time
import soundfile as sf

AUDIO_OUTPUT = "tts_output.wav"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# ✅ INIT MUSICGEN ON APP START
init_musicgen()

def freestyle_session(prompt):
    beat_path = get_beat_path(prompt)
    play_looped_audio(beat_path)
    
    # AI generates and speaks a line
    line = generate_line()
    text_to_speech(line, out_path=AUDIO_OUTPUT)
    
    # Load audio for Gradio playback
    data, sr = sf.read(AUDIO_OUTPUT)
    return line, (sr, data)

ui = gr.Interface(
    fn=freestyle_session,
    inputs=gr.Textbox(label="Enter Beat Style", placeholder="e.g. lofi chill, trap 808, or your custom vibe"),
    outputs=[
        gr.Textbox(label="AI Rap Line"),
        gr.Audio(label="AI Vocal")
    ],
    title="🎤 Freestyle AI Rapper",
    description="Enter a vibe and let the AI drop a freestyle line over a matching beat!"
)

if __name__ == "__main__":
    ui.launch(share=True)