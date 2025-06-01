import os
import logging
import uuid
from modules.musicgen import init_musicgen, generate_music

logger = logging.getLogger(__name__)

def get_beat_path(prompt: str) -> str:
    try:
        logger.info(f"Getting beat path for prompt: {prompt}")
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Invalid prompt provided")
            
        # Generate a unique UUID for the file
        unique_id = str(uuid.uuid4())
        path = f"static/beats/{unique_id}_musicgen.wav"
        
        logger.info(f"Generating new beat with unique ID: {unique_id}")
        try:
            generate_music(prompt, output_path=path)
        except Exception as e:
            logger.error(f"Failed to generate music: {str(e)}")
            raise
            
        if not os.path.exists(path):
            raise FileNotFoundError(f"Beat file not found at {path} after generation")
            
        return path
        
    except Exception as e:
        logger.error(f"Error in get_beat_path: {str(e)}")
        raise