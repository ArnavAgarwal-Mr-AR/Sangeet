from pydub import AudioSegment
from pydub.playback import play
import threading
<<<<<<< HEAD
=======
import tempfile
import os

os.environ["TMPDIR"] = "G:/Sangeet/temp"  # Or any directory you have write access to
tempfile.tempdir = "G:/Sangeet/temp"
>>>>>>> 957fad36ec8189a52f9eb4e6227089298cab2127

def play_looped_audio(filepath: str):
    def loop():
        beat = AudioSegment.from_file(filepath)
        while True:
            play(beat)
    thread = threading.Thread(target=loop, daemon=True)
<<<<<<< HEAD
    thread.start()
=======
    thread.start()
>>>>>>> 957fad36ec8189a52f9eb4e6227089298cab2127
