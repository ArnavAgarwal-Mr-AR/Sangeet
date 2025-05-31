from pydub import AudioSegment
from pydub.playback import play
import threading
import tempfile
import os

os.environ["TMPDIR"] = "G:/Sangeet/temp"  # Or any directory you have write access to
tempfile.tempdir = "G:/Sangeet/temp"

def play_looped_audio(filepath: str):
    def loop():
        beat = AudioSegment.from_file(filepath)
        while True:
            play(beat)
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
