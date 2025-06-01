import logging
from transformers import MusicgenForConditionalGeneration, MusicgenProcessor
import torchaudio
import torch
import os

logger = logging.getLogger(__name__)

model = None
processor = None
device = None

def init_musicgen(device_param):
    try:
        global model, processor, device
        logger.info("Initializing MusicGen model")
        
        device = device_param if device_param is not None else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
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

def generate_music(prompt, output_path, duration=10):
    try:
        global model, processor, device
        
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Invalid prompt provided")
            
        if model is None or processor is None or device is None:
            raise RuntimeError("MusicGen model not initialized. Call init_musicgen() first")
            
        logger.info(f"Generating music for prompt: {prompt}")
        logger.info(f"Output path: {output_path}")
        
        # Convert to absolute path
        abs_output_path = os.path.abspath(output_path)
        logger.info(f"Absolute output path: {abs_output_path}")
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(abs_output_path)
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Output directory exists before creation: {os.path.exists(output_dir)}")
        logger.info(f"Output directory permissions: {oct(os.stat(output_dir).st_mode)[-3:] if os.path.exists(output_dir) else 'N/A'}")
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"Output directory exists after creation: {os.path.exists(output_dir)}")
        except Exception as e:
            logger.error(f"Failed to create output directory: {str(e)}")
            logger.error(f"Current working directory: {os.getcwd()}")
            raise
            
        try:
            logger.info("Processing input prompt...")
            inputs = processor(text=[prompt], return_tensors="pt").to(device)
            logger.info("Input processing successful")
        except Exception as e:
            logger.error(f"Failed to process input prompt: {str(e)}")
            logger.error(f"Input prompt: {prompt}")
            raise
            
        logger.info("Generating audio values")
        try:
            if torch.cuda.is_available():
                logger.info(f"GPU memory before generation: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
            
            audio_values = model.generate(**inputs, max_new_tokens=duration * 50)
            audio_values = audio_values[0].detach().cpu()
            
            if torch.cuda.is_available():
                logger.info(f"GPU memory after generation: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
                
            logger.info("Audio generation successful")
        except Exception as e:
            logger.error(f"Failed to generate audio: {str(e)}")
            if torch.cuda.is_available():
                logger.error(f"GPU memory at error: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
            raise
            
        logger.info(f"Saving generated music to {abs_output_path}")
        try:
            torchaudio.save(abs_output_path, audio_values, 32000)
            logger.info(f"File exists after save: {os.path.exists(abs_output_path)}")
            logger.info(f"File size: {os.path.getsize(abs_output_path) if os.path.exists(abs_output_path) else 'N/A'}")
            logger.info(f"File permissions: {oct(os.stat(abs_output_path).st_mode)[-3:] if os.path.exists(abs_output_path) else 'N/A'}")
        except Exception as e:
            logger.error(f"Failed to save audio file: {str(e)}")
            logger.error(f"Audio values shape: {audio_values.shape}")
            raise
            
        if not os.path.exists(abs_output_path):
            raise FileNotFoundError(f"Generated music file not found at {abs_output_path}")
            
        logger.info("Music generation completed successfully")
        
    except Exception as e:
        logger.error(f"Error in generate_music: {str(e)}")
        logger.error(f"Full error details: {str(e.__class__.__name__)}: {str(e)}")
        raise
