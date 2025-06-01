import torch
import logging

logger = logging.getLogger(__name__)

def get_gpu_memory_usage():
    """Get current GPU memory usage"""
    if torch.cuda.is_available():
        return {
            'allocated': torch.cuda.memory_allocated(),
            'reserved': torch.cuda.memory_reserved(),
            'max_allocated': torch.cuda.max_memory_allocated()
        }
    return None

def clear_gpu_memory():
    """Clear GPU memory cache"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.info("GPU memory cache cleared")

def optimize_model_for_inference(model):
    """Optimize model for inference"""
    if torch.cuda.is_available():
        model = model.half()  # Use FP16
        model.eval()  # Set to evaluation mode
        with torch.no_grad():  # Disable gradient calculation
            return model
    return model
