import logging
from google import genai
import os
from dotenv import load_dotenv
import librosa

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini
try:
    logger.info("Initializing Gemini model for lyrics generation")
    client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
    logger.info("Gemini model loaded successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {str(e)}")
    raise

def analyze_beat(beat_file_path):
    y, sr = librosa.load(beat_file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return round(tempo)

def generate_line(beat_file_path, prompt):
    try:
        logger.info("Generating new rap line")
        prompt = f"This is the User requested beats style: {prompt} \n\n Generate a creative and engaging lyrics according to the uploaded beat file and user requested beats style"
        
        try:    
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            line = response.text.strip()
        except Exception as e:
            logger.error(f"Failed to generate text with Gemini: {str(e)}")
            raise
            
        if not line:
            raise ValueError("Generated line is empty")
            
        logger.info(f"Generated line: {line}")
        return line
        
    except Exception as e:
        logger.error(f"Error in generate_line: {str(e)}")
        raise
