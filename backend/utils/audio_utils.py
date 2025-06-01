import logging
from pydub import AudioSegment
from pydub.playback import play
import threading
import tempfile
import os

logger = logging.getLogger(__name__)

try:
    os.environ["TMPDIR"] = "G:/Sangeet/temp"  # Or any directory you have write access to
    tempfile.tempdir = "G:/Sangeet/temp"
    logger.info(f"Set temporary directory to: {tempfile.tempdir}")
except Exception as e:
    logger.error(f"Failed to set temporary directory: {str(e)}")
    raise

def play_looped_audio(filepath: str):
    try:
        if not filepath or not isinstance(filepath, str):
            raise ValueError("Invalid filepath provided")
            
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Audio file not found at {filepath}")
            
        logger.info(f"Starting audio loop playback for file: {filepath}")
        
        def loop():
            try:
                logger.info("Loading audio file for playback")
                beat = AudioSegment.from_file(filepath)
                logger.info("Starting continuous playback loop")
                while True:
                    try:
                        play(beat)
                    except Exception as e:
                        logger.error(f"Error during audio playback: {str(e)}")
                        break
            except Exception as e:
                logger.error(f"Error in audio loop: {str(e)}")
                
        thread = threading.Thread(target=loop, daemon=True)
        thread.start()
        logger.info("Audio playback thread started")
        
    except Exception as e:
        logger.error(f"Error in play_looped_audio: {str(e)}")
        raise
