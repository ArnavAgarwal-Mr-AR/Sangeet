import logging
from transformers import pipeline

logger = logging.getLogger(__name__)

# Load model once
try:
    logger.info("Initializing GPT-2 model for lyrics generation")
    generator = pipeline("text-generation", model="gpt2")
    logger.info("GPT-2 model loaded successfully")
except Exception as e:
    logger.error(f"Failed to initialize GPT-2 model: {str(e)}")
    raise

def generate_line():
    try:
        logger.info("Generating new rap line")
        prompt = "Spitting fire on the mic,"
        
        try:
            output = generator(prompt, max_length=20, do_sample=True, temperature=1.1)
        except Exception as e:
            logger.error(f"Failed to generate text with GPT-2: {str(e)}")
            raise
            
        if not output or not isinstance(output, list) or len(output) == 0:
            raise ValueError("Invalid output from GPT-2 model")
            
        line = output[0]["generated_text"].replace(prompt, "").strip().split("\n")[0]
        
        if not line:
            raise ValueError("Generated line is empty")
            
        logger.info(f"Generated line: {line}")
        return line
        
    except Exception as e:
        logger.error(f"Error in generate_line: {str(e)}")
        raise
