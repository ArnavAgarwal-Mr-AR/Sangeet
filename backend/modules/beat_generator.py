import os
import numpy as np
import note_seq
from note_seq.protobuf import music_pb2
from note_seq import midi_io
from pydub import AudioSegment
import subprocess


SOUNDFONT = "/kaggle/working/soundfont.sf2"
TMP_DIR = "/kaggle/working"

DRUM_PITCHES = [36, 38, 42]  # Kick, Snare, Hi-hat

def generate_mock_drum_pattern(length=32):
    """Simulate a real pattern using fixed probability and rhythm."""
    pattern = []
    for step in range(length):
        time = step * 0.25  # 16th note grid (at 120 QPM)
        if step % 4 == 0:
            pattern.append((36, time))  # Kick
        if step % 8 == 4:
            pattern.append((38, time))  # Snare
        if step % 2 == 1:
            pattern.append((42, time))  # Hi-hat
    return pattern

def generate_beat(prompt: str, out_path: str):

    
    print(f"Generating beat for prompt: {prompt}")
    print(f"Output path: {out_path}")

    pattern = generate_mock_drum_pattern()

    sequence = music_pb2.NoteSequence()
    sequence.tempos.add(qpm=100)
    sequence.ticks_per_quarter = 220

    for pitch, time in pattern:
        note = sequence.notes.add()
        note.pitch = pitch
        note.start_time = time
        note.end_time = time + 0.1
        note.velocity = 80
        note.is_drum = True

    sequence.total_time = pattern[-1][1] + 1.0

    # Save MIDI
    midi_path = os.path.join(TMP_DIR, "drum_pattern.mid")
    midi_io.sequence_proto_to_midi_file(sequence, midi_path)

    # Convert to WAV
    wav_path = os.path.join(TMP_DIR, "drum_pattern.wav")
    subprocess.run([
        "fluidsynth", "-ni", SOUNDFONT, midi_path,
        "-F", wav_path, "-r", "44100"
    ], check=True)

    # Trim & save
    beat = AudioSegment.from_wav(wav_path)
    beat = beat[:4000]
    beat.export(out_path, format="wav")
    print(f"✅ Real beat saved at {out_path}")

