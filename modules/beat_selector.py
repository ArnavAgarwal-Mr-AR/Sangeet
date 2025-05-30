import os
from modules.musicgen import init_musicgen, generate_music

def get_beat_path(prompt: str) -> str:
    safe_prompt = prompt.lower().strip().replace(" ", "_")
    path = f"beats/{safe_prompt}_musicgen.wav"
    if not os.path.exists(path):
        generate_music(prompt, output_path=path)
    return path