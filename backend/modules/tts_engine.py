import logging
from TTS.api import TTS
import torch
import soundfile as sf
from pydub import AudioSegment
import os

logger = logging.getLogger(__name__)

# Load TTS model with GPU support
try:
    logger.info("Initializing TTS model")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(
        model_name="tts_models/en/ljspeech/tacotron2-DDC",
        progress_bar=False,
        gpu=torch.cuda.is_available()
    )
    logger.info(f"TTS model loaded successfully on {device}")
except Exception as e:
    logger.error(f"Failed to initialize TTS model: {str(e)}")
    raise

def text_to_speech(text: str, out_path="tts_output.wav"):
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Invalid text input provided")
            
        logger.info(f"Converting text to speech: {text}")
        
        try:
            # Use GPU if available
            tts.tts_to_file(
                text=text,
                file_path=out_path,
                gpu=torch.cuda.is_available()
            )
        except Exception as e:
            logger.error(f"Failed to generate speech: {str(e)}")
            raise
            
        if not os.path.exists(out_path):
            raise FileNotFoundError(f"TTS output file not found at {out_path}")
            
        try:
            data, samplerate = sf.read(out_path)
        except Exception as e:
            logger.error(f"Failed to read generated audio file: {str(e)}")
            raise
            
        logger.info(f"Text to speech completed, saved to {out_path}")
        
    except Exception as e:
        logger.error(f"Error in text_to_speech: {str(e)}")
        raise

def mix_beat_with_tts(beat_path, tts_path, out_path):
    try:
        if not os.path.exists(beat_path):
            raise FileNotFoundError(f"Beat file not found at {beat_path}")
        if not os.path.exists(tts_path):
            raise FileNotFoundError(f"TTS file not found at {tts_path}")
            
        logger.info(f"Mixing beat {beat_path} with TTS {tts_path}")
        
        try:
            beat = AudioSegment.from_file(beat_path)
            tts = AudioSegment.from_file(tts_path)
        except Exception as e:
            logger.error(f"Failed to load audio files: {str(e)}")
            raise
            
        try:
            combined = beat.overlay(tts, position=1000)  # start AI voice after 1 sec
            combined.export(out_path, format="wav")
        except Exception as e:
            logger.error(f"Failed to mix and export audio: {str(e)}")
            raise
            
        if not os.path.exists(out_path):
            raise FileNotFoundError(f"Mixed audio file not found at {out_path}")
            
        logger.info(f"Mixed audio saved to {out_path}")
        
    except Exception as e:
        logger.error(f"Error in mix_beat_with_tts: {str(e)}")
        raise