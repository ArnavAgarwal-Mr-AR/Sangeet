# Musicano
Our submission to 100xbuildathon2

# AI-Powered Music Collaboration Platform 🎤🤖🎵

## 🔗 Problem Statement

We are building a platform for **beginner songwriters, rappers, lyricists, and singers** to practice and publish music without the need for a producer. The system enables users to select or generate a beat, freestyle or sing over it, and interact in real-time with an AI model that joins the session. The AI understands beat timing and voice input, and alternates performing with the user — speaking or singing when the user pauses, and stopping when the user resumes.

For rapping, the AI uses a fine-tuned Qwen model to generate context-aware rap bars. For singing, the AI leverages **Gemini 2.5 Pro** to understand the beats and generate lyrics that fit the selected beat.

---

## ✅ Core Features

1. **Beat Selection/Generation**  
   - AI beat generation from user prompt  
   - Display BPM (beats per minute) and key  
   - Upload user vocals or select/upload a beat  

2. **Live Music Session**  
   - User and AI alternate performing (rapping or singing) in real-time  
   - Voice activity detection (AI pauses when user performs; AI responds when user pauses)  
   - AI generates lyrics or bars based on style (rap or singing) and beat context  

3. **Recording and Publishing**  
   - Mix user and AI vocals with background beat  
   - Optionally autotune user vocals  
   - Export final audio and share  

4. **Admin Dashboard**  
   - Manage users, beats, AI sessions, and logs  
   - View analytics and usage statistics  

---

## 📊 Technical Stack

| Layer             | Technology/Service                                  |
|-------------------|---------------------------------------------------|
| **Frontend**      | Next.js (React) + WebRTC + Supabase JS SDK        |
| **Backend**       | FastAPI (AI & processing APIs) + Supabase Python client |
| **Database**      | Supabase (PostgreSQL + Realtime)                   |
| **Authentication**| Supabase Auth                                      |
| **Storage**       | Supabase Storage (for beats and audio files)       |
| **Real-Time Control** | WebSockets or Supabase Realtime (signaling)      |
| **Media Streaming**  | WebRTC (live voice/audio streaming)                |

---

### Backend AI Models

- **Rapping**: Fine-tuned Qwen model for generating rap lyrics  
- **Singing**: Gemini 2.5 Pro for beat understanding and singing lyrics generation  
- **Beat Generation**: Facebook MusicGen  
- **Text-to-Speech**: Tacotron2 (tts_models/en/ljspeech)  

---

## 🔄 Data & Session Flow

1. User logs in and selects or generates a beat  
2. User chooses performance style: rap or singing  
3. Beat plays client-side  
4. Microphone captures user input  
   - Voice Activity Detection (VAD) detects when user is performing or pausing  
   - WebSocket signals sent to backend ("user performing" / "paused")  
5. AI listens and responds accordingly (rap or sing)  
6. Vocals and beat recorded with optional autotune/effects  
7. Final mix created and saved  

