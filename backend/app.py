import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv
import soundfile as sf
from typing import Optional
from pydantic import BaseModel
from fastapi.websockets import WebSocketDisconnect
import asyncio
import json
import torch
import platform
import sys

# Import all required modules
from modules.beat_selector import get_beat_path
from modules.lyrics_generator import generate_line
from modules.tts_engine import text_to_speech, mix_beat_with_tts
from modules.musicgen import init_musicgen
from utils.audio_utils import play_looped_audio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Constants
AUDIO_OUTPUT = "tts_output.wav"
MIXED_OUTPUT = "mixed_output.wav"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Get absolute paths for static directories
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
    logger.info(f"Created static directory at: {STATIC_DIR}")

# Create beats directory inside static if it doesn't exist
BEATS_DIR = os.path.join(STATIC_DIR, "beats")
if not os.path.exists(BEATS_DIR):
    os.makedirs(BEATS_DIR)
    logger.info(f"Created beats directory at: {BEATS_DIR}")


# Pydantic models for request validation
class BeatRequest(BaseModel):
    prompt: str

class SpeechRequest(BaseModel):
    text: str

class FreestyleRequest(BaseModel):
    prompt: str

class LyricsRequest(BaseModel):
    prompt: str
    beat_path: str

# Initialize FastAPI app
app = FastAPI(
    title="Vocaliq API",
    description="AI Music Generation API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Add GPU detection function
def check_gpu_availability():
    try:
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_info = []
            for i in range(gpu_count):
                gpu_info.append({
                    'name': torch.cuda.get_device_name(i),
                    'memory': torch.cuda.get_device_properties(i).total_memory
                })
            logger.info(f"GPU(s) available: {gpu_info}")
            return True, gpu_info
        else:
            logger.info("No GPU available, using CPU")
            return False, None
    except Exception as e:
        logger.error(f"Error checking GPU availability: {str(e)}")
        return False, None

# Add system info logging
def log_system_info():
    try:
        system_info = {
            'platform': platform.platform(),
            'python_version': sys.version,
            'torch_version': torch.__version__,
            'cuda_available': torch.cuda.is_available(),
            'cuda_version': torch.version.cuda if torch.cuda.is_available() else 'N/A',
            'gpu_count': torch.cuda.device_count() if torch.cuda.is_available() else 0
        }
        logger.info(f"System Information: {system_info}")
        return system_info
    except Exception as e:
        logger.error(f"Error logging system info: {str(e)}")
        return None

# Modify the startup event
@app.on_event("startup")
async def startup_event():
    try:
        # Log system information
        system_info = log_system_info()
        logger.info(f"System Information: {system_info}")
        
        # Check GPU availability
        has_gpu, gpu_info = check_gpu_availability()
        logger.info(f"GPU Available: {has_gpu}")
        if gpu_info:
            logger.info(f"GPU Information: {gpu_info}")
        
        # Set device
        device = torch.device("cuda" if has_gpu else "cpu")
        logger.info(f"Using device: {device}")
        
        # Initialize models with device
        logger.info("Initializing models...")
        try:
            init_musicgen(device)
            logger.info("MusicGen model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MusicGen model: {str(e)}")
            logger.error(f"Full error details: {str(e.__class__.__name__)}: {str(e)}")
            raise
        
    except Exception as e:
        logger.error(f"Failed to initialize models: {str(e)}")
        logger.error(f"Full error details: {str(e.__class__.__name__)}: {str(e)}")
        raise

@app.get("/")
async def root():
    """Root endpoint to check API status"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Vocaliq API",
        "status": "active",
        "version": "1.0.0"
    }

@app.post("/generate/beat")
async def generate_beat(request: BeatRequest):
    """Generate a beat based on the provided prompt"""
    try:
        logger.info(f"Beat generation requested with prompt: {request.prompt}")
        
        # Get the beat path and ensure it exists
        try:
            beat_path = get_beat_path(request.prompt)
            # Use the correct static directory path
            full_path = os.path.join(STATIC_DIR, beat_path)
            logger.info(f"Looking for beat file at: {full_path}")
            
            if not os.path.exists(full_path):
                logger.error(f"Beat file not found at path: {full_path}")
                raise HTTPException(status_code=500, detail="Failed to generate beat file")
                
            logger.info(f"Beat generated successfully at: {full_path}")
            
            # Return both the path and the file
            return {
                "status": "success",
                "message": "Beat generated successfully",
                "beat_path": beat_path,
                "file_url": f"/static/{beat_path}"
            }
        except Exception as e:
            logger.error(f"Error in beat generation: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate beat: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error in generate_beat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/lyrics")
async def generate_lyrics(request: LyricsRequest):
    """Generate a rap line"""
    try:
        logger.info(f"Lyrics generation requested with beat: {request.beat_path} and prompt: {request.prompt}")
        # Get the full path of the beat file
        beat_file_path = os.path.join(STATIC_DIR, request.beat_path)
        if not os.path.exists(beat_file_path):
            raise HTTPException(status_code=404, detail="Beat file not found")
            
        line = generate_line(beat_file_path, request.prompt)
        return {
            "status": "success",
            "message": "Lyrics generated successfully",
            "line": line
        }
    except Exception as e:
        logger.error(f"Error generating lyrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/speech")
async def generate_speech(request: SpeechRequest):
    """Convert text to speech"""
    try:
        logger.info(f"Speech generation requested for text: {request.text}")
        text_to_speech(request.text, out_path=AUDIO_OUTPUT)
        return FileResponse(
            AUDIO_OUTPUT,
            media_type="audio/wav",
            filename="speech.wav"
        )
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/freestyle")
async def freestyle_session(
    request: FreestyleRequest,
    background_tasks: BackgroundTasks
):
    """Generate a complete freestyle session with beat and vocals"""
    try:
        logger.info(f"Freestyle session started with prompt: {request.prompt}")
        
        # Generate beat
        beat_path = get_beat_path(request.prompt)
        logger.info(f"Beat generated at: {beat_path}")
        
        # Get the full path of the beat file
        beat_file_path = os.path.join(STATIC_DIR, beat_path)
        if not os.path.exists(beat_file_path):
            raise HTTPException(status_code=404, detail="Beat file not found")
        
        # Generate lyrics with both beat file and prompt
        line = generate_line(beat_file_path, request.prompt)
        logger.info(f"Generated line: {line}")
        
        # Generate speech
        text_to_speech(line, out_path=AUDIO_OUTPUT)
        logger.info("Text to speech conversion completed")
        
        # Mix beat with vocals
        mix_beat_with_tts(beat_path, AUDIO_OUTPUT, MIXED_OUTPUT)
        logger.info("Audio mixing completed")
        
        # Start beat playback in background
        background_tasks.add_task(play_looped_audio, beat_path)
        
        return {
            "status": "success",
            "message": "Freestyle session completed",
            "line": line,
            "beat_path": beat_path,
            "mixed_audio": MIXED_OUTPUT
        }
    except Exception as e:
        logger.error(f"Error in freestyle session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Get generated audio file"""
    try:
        file_path = filename
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        return FileResponse(
            file_path,
            media_type="audio/wav",
            filename=filename
        )
    except Exception as e:
        logger.error(f"Error retrieving audio file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                # Receive message from client
                message = await websocket.receive_json()
                beat_path = message.get("beat_path")
                prompt = message.get("prompt")

                logger.info(f"Received message: {message}")
                logger.info(f"Beat path: {beat_path}")
                logger.info(f"Prompt: {prompt}")
                
                if not beat_path or not prompt:
                    raise ValueError("Missing beat_path or prompt in request")
                
                # Normalize the beat path to use forward slashes
                beat_path = beat_path.replace('\\', '/')
                
                # Get the full path of the beat file
                beat_file_path = os.path.normpath(os.path.join(STATIC_DIR, beat_path))
                logger.info(f"Looking for beat file at: {beat_file_path}")
                
                # List available files in the beats directory for debugging
                beats_dir = os.path.join(STATIC_DIR, "beats")
                if os.path.exists(beats_dir):
                    available_files = os.listdir(beats_dir)
                    logger.info(f"Available files in beats directory: {available_files}")
                
                if not os.path.exists(beat_file_path):
                    logger.error(f"Beat file not found at: {beat_file_path}")
                    await websocket.send_json({
                        "type": "error",
                        "content": f"Beat file not found at: {beat_path}"
                    })
                    continue
                
                # Process audio data with both beat file and prompt
                try:
                    line = generate_line(beat_file_path, prompt)
                    
                    # Ensure the line is not too short
                    if len(line) < 5:
                        line = f"Start {line} end"
                    
                    # Send lyrics back to client as JSON
                    await websocket.send_json({
                        "type": "lyrics",
                        "content": line
                    })
                    
                    # Generate speech for the lyrics
                    text_to_speech(line, out_path=AUDIO_OUTPUT)
                    
                    # Send audio back to client as binary data
                    with open(AUDIO_OUTPUT, 'rb') as f:
                        audio_data = f.read()
                        await websocket.send_bytes(audio_data)
                except Exception as e:
                    logger.error(f"Error processing audio: {str(e)}")
                    await websocket.send_json({
                        "type": "error",
                        "content": f"Error processing audio: {str(e)}"
                    })
                    
            except WebSocketDisconnect:
                logger.info("Client disconnected")
                break
            except Exception as e:
                logger.error(f"Error in WebSocket loop: {str(e)}")
                try:
                    await websocket.send_json({
                        "type": "error",
                        "content": str(e)
                    })
                except:
                    break
                
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        try:
            await websocket.close()
        except:
            pass

# Add a dedicated endpoint for serving beat files
@app.get("/beats/{filename}")
async def get_beat(filename: str):
    """Get generated beat file"""
    try:
        file_path = os.path.join(BEATS_DIR, filename)
        logger.info(f"Attempting to serve beat file from: {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"Beat file not found at: {file_path}")
            raise HTTPException(status_code=404, detail="Beat file not found")
            
        return FileResponse(
            file_path,
            media_type="audio/wav",
            filename=filename
        )
    except Exception as e:
        logger.error(f"Error retrieving beat file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"Starting FastAPI application on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
