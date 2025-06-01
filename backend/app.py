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

STATIC_DIR = os.getenv("STATIC_DIR", "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Create beats directory inside static if it doesn't exist
BEATS_DIR = os.path.join(STATIC_DIR, "beats")
if not os.path.exists(BEATS_DIR):
    os.makedirs(BEATS_DIR)

# Pydantic models for request validation
class BeatRequest(BaseModel):
    prompt: str

class SpeechRequest(BaseModel):
    text: str

class FreestyleRequest(BaseModel):
    prompt: str

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

# Initialize MusicGen on startup
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Initializing MusicGen on startup")
        init_musicgen()
        logger.info("MusicGen initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize MusicGen: {str(e)}")
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
async def generate_beat(request: Request):
    """Generate a beat based on the provided prompt"""
    try:
        body = await request.json()
        logger.info(f"Received request body: {body}")
        
        if not isinstance(body, dict) or "prompt" not in body:
            raise HTTPException(status_code=400, detail="Invalid request body. Expected {'prompt': 'string'}")
            
        prompt = body["prompt"]
        logger.info(f"Beat generation requested with prompt: {prompt}")
        beat_path = get_beat_path(prompt)
        return {
            "status": "success",
            "message": "Beat generated successfully",
            "beat_path": beat_path
        }
    except Exception as e:
        logger.error(f"Error generating beat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/lyrics")
async def generate_lyrics():
    """Generate a rap line"""
    try:
        logger.info("Lyrics generation requested")
        line = generate_line()
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
        
        # Generate lyrics
        line = generate_line()
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
            # Receive audio data from client
            data = await websocket.receive_bytes()
            
            # Process audio data (you'll need to implement this)
            # For now, we'll just generate new lyrics
            line = generate_line()
            
            # Send lyrics back to client
            await websocket.send_json({
                "type": "lyrics",
                "content": line
            })
            
            # Generate speech for the lyrics
            text_to_speech(line, out_path=AUDIO_OUTPUT)
            
            # Send audio back to client
            with open(AUDIO_OUTPUT, 'rb') as f:
                audio_data = f.read()
                await websocket.send_json({
                    "type": "audio",
                    "content": audio_data
                })
                
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"Starting FastAPI application on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
