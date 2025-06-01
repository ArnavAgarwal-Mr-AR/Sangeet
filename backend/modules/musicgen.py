import logging
from transformers import MusicgenForConditionalGeneration, MusicgenProcessor
import torchaudio
import torch
import os

logger = logging.getLogger(__name__)

model = None
processor = None

def init_musicgen(device=None):
    try:
        global model, processor
        logger.info("Initializing MusicGen model")
        
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        try:
            processor = MusicgenProcessor.from_pretrained(
                "facebook/musicgen-small",
                device_map=device
            )
        except Exception as e:
            logger.error(f"Failed to load MusicGen processor: {str(e)}")
            raise
            
        try:
            model = MusicgenForConditionalGeneration.from_pretrained(
                "facebook/musicgen-small",
                device_map=device
            ).to(device)
            
            # Enable model optimization if on GPU
            if device.type == "cuda":
                model = model.half()  # Use FP16 for better GPU memory usage
                torch.cuda.empty_cache()  # Clear GPU cache
                
        except Exception as e:
            logger.error(f"Failed to load MusicGen model: {str(e)}")
            raise
            
        logger.info(f"MusicGen model loaded successfully on {device}")
        
    except Exception as e:
        logger.error(f"Error in init_musicgen: {str(e)}")
        raise

def generate_music(prompt, output_path="/beats/musicgen.wav", duration=10):
    try:
        global model, processor
        
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Invalid prompt provided")
            
        if model is None or processor is None:
            raise RuntimeError("MusicGen model not initialized. Call init_musicgen() first")
            
        logger.info(f"Generating music for prompt: {prompt}")
        output_path = output_path.strip().replace(" ", "_")
        output_dir = os.path.dirname(output_path)
        
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create output directory: {str(e)}")
            raise
            
        logger.info(f"Output directory created/verified: {output_dir}")
        
        try:
            inputs = processor(text=[prompt], return_tensors="pt").to(device)
        except Exception as e:
            logger.error(f"Failed to process input prompt: {str(e)}")
            raise
            
        logger.info("Generating audio values")
        try:
            audio_values = model.generate(**inputs, max_new_tokens=duration * 50)
            audio_values = audio_values[0].detach().cpu()
        except Exception as e:
            logger.error(f"Failed to generate audio: {str(e)}")
            raise
            
        logger.info(f"Saving generated music to {output_path}")
        try:
            torchaudio.save(output_path, audio_values, 32000)
        except Exception as e:
            logger.error(f"Failed to save audio file: {str(e)}")
            raise
            
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Generated music file not found at {output_path}")
            
        logger.info("Music generation completed successfully")
        
    except Exception as e:
        logger.error(f"Error in generate_music: {str(e)}")
        raise
