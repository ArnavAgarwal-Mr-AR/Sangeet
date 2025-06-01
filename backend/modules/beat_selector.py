import os
import logging
import uuid
from modules.musicgen import init_musicgen, generate_music

logger = logging.getLogger(__name__)

# Get the absolute path to the static directory
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"))
BEATS_DIR = os.path.join(STATIC_DIR, "beats")

logger.info(f"Static directory: {STATIC_DIR}")
logger.info(f"Beats directory: {BEATS_DIR}")

# Ensure the beats directory exists
os.makedirs(BEATS_DIR, exist_ok=True)
logger.info(f"Beats directory exists: {os.path.exists(BEATS_DIR)}")
logger.info(f"Beats directory permissions: {oct(os.stat(BEATS_DIR).st_mode)[-3:] if os.path.exists(BEATS_DIR) else 'N/A'}")

def get_beat_path(prompt: str) -> str:
    try:
        logger.info(f"Getting beat path for prompt: {prompt}")
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Invalid prompt provided")
            
        # Generate a unique UUID for the file
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}_musicgen.wav"
        
        # Use absolute path for generation
        full_path = os.path.join(BEATS_DIR, filename)
        logger.info(f"Full output path: {full_path}")
        
        # Ensure the beats directory exists
        try:
            os.makedirs(BEATS_DIR, exist_ok=True)
            logger.info(f"Beats directory exists: {os.path.exists(BEATS_DIR)}")
            logger.info(f"Beats directory permissions: {oct(os.stat(BEATS_DIR).st_mode)[-3:] if os.path.exists(BEATS_DIR) else 'N/A'}")
        except Exception as e:
            logger.error(f"Failed to create beats directory: {str(e)}")
            raise
        
        try:
            # Generate music using absolute path
            generate_music(prompt, output_path=full_path)
            logger.info(f"File exists after generation: {os.path.exists(full_path)}")
            if os.path.exists(full_path):
                logger.info(f"File size: {os.path.getsize(full_path)}")
                logger.info(f"File permissions: {oct(os.stat(full_path).st_mode)[-3:]}")
            else:
                logger.error("File was not created after generation")
        except Exception as e:
            logger.error(f"Failed to generate music: {str(e)}")
            logger.error(f"Full error details: {str(e.__class__.__name__)}: {str(e)}")
            raise
            
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Beat file not found at {full_path} after generation")
            
        # Return the path relative to the static directory (without 'static/' prefix)
        relative_path = os.path.join("beats", filename).replace("\\", "/")
        logger.info(f"Returning relative path: {relative_path}")
        return relative_path
        
    except Exception as e:
        logger.error(f"Error in get_beat_path: {str(e)}")
        logger.error(f"Full error details: {str(e.__class__.__name__)}: {str(e)}")
        raise