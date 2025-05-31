from transformers import MusicgenForConditionalGeneration, MusicgenProcessor
import torchaudio
import torch
import os

model = None
processor = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def init_musicgen():
    global model, processor
    processor = MusicgenProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)

def generate_music(prompt, output_path="/beats/musicgen.wav", duration=10):
    global model, processor
    output_path = output_path.strip().replace(" ", "_")
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    inputs = processor(text=[prompt], return_tensors="pt").to(device)
    audio_values = model.generate(**inputs, max_new_tokens=duration * 50)
    audio_values = audio_values[0].detach().cpu()
    torchaudio.save(output_path, audio_values, 32000)
    print(f"✅ Music generated at {output_path}")
