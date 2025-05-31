from TTS.api import TTS
import soundfile as sf
from pydub import AudioSegment

# Load TTS model once
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

def text_to_speech(text: str, out_path="tts_output.wav"):
    tts.tts_to_file(text=text, file_path=out_path)
    data, samplerate = sf.read(out_path)
    print(f"🗣️ Speaking: {text}")

def mix_beat_with_tts(beat_path, tts_path, out_path):
    beat = AudioSegment.from_file(beat_path)
    tts = AudioSegment.from_file(tts_path)
    combined = beat.overlay(tts, position=1000)  # start AI voice after 1 sec
    combined.export(out_path, format="wav")