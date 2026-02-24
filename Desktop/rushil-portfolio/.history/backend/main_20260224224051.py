from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os
import json
from datetime import datetime
from database import Database

app = FastAPI(title="Rushil Portfolio AI Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()

# --- Rushil's Resume Context ---
RUSHIL_CONTEXT = """
You are an AI assistant representing Rushil Gosain's portfolio. Answer questions about Rushil accurately and helpfully.

=== RUSHIL GOSAIN - PROFILE ===

Name: Rushil Gosain
Email: rushilgosain10@gmail.com
Phone: (+91) 8860816875
LinkedIn: https://www.linkedin.com/in/rushil-gosain-434b57285/
GitHub: https://github.com/RushilGosain

=== EDUCATION ===
- B.Tech, Computer Science — Dr. Akhilesh Das Gupta Institute Of Professional Studies (GGSIPU), 2022–2026
- CBSE Class 12 (Science) — 2022
- CBSE Class 10 — 86.5%, 2020

=== SKILLS ===
- C++ (90%): Strong OOP, data structures, competitive programming
- HTML5 (85%): Semantic, accessible, structured web pages
- CSS3 (80%): Responsive design, animations, Flexbox/Grid
- React + TypeScript (70%): Component architecture, hooks, modern patterns
- DSA (60%): Arrays, trees, graphs, algorithms
- AI Tools (75%): ChatGPT, OpenAI API, workflow automation

=== EXPERIENCE / TRAININGS ===
1. Full Stack Web Development Intern — Global Next Consulting India Pvt. Ltd. (Aug 2025 – Sep 2025)
   - Developed responsive web applications using frontend and backend technologies
   - Client interaction, data privacy standards
   - Submitted final project demonstrating technical skills

2. Software Engineering Virtual Experience Trainee — Commonwealth Bank (Forage), May 2025
   - Built responsive web page with HTML/CSS following branding guidelines
   - Applied cybersecurity principles for client security recommendations
   - Drafted secure web hosting proposal

=== PROJECTS ===
1. NeuroTrack – AI-Powered Mental Health Tracking Platform
   - AI-based platform monitoring mental health trends for students and professionals
   - Personalized insights via sentiment analysis and text summarization
   - Stack: HTML, CSS, JavaScript, Flask (Python), OpenAI API, MySQL
   - GitHub: https://github.com/RushilGosain/NEUROTRACK.git

2. Expert-Booking Platform
   - Built a full-stack booking platform enabling users to browse experts, book appointments, and manage their booking history.
   - Implemented secure user authentication using JWT tokens and bcrypt password hashing, with protected routes and
middleware-based token verification.
   - Stack: HTML, CSS, JavaScript, Flask (Python), OpenAI API, MySQL
   - GitHub: https://github.com/RushilGosain/NEUROTRACK.git
   
2. My Portfolio
   - Personal tech portfolio with interactive animations (particle constellations, comet cursor, aurora waves)
   - Stack: HTML5, CSS3, HTML5 Canvas, GSAP
   - GitHub: https://github.com/RushilGosain/My-Portfolio

3. Blittz Quiz – Interactive Quiz Application
   - Sign in, choose categories, attempt quizzes with clean responsive UI
   - Stack: Next.js 13, TypeScript, NextAuth.js, API Integration
   - GitHub: https://github.com/RushilGosain/blittz-quiz

=== CERTIFICATIONS ===
- Front End Development — Great Learning (July 2024 – Sept 2025)
- AI & Machine Learning Training — Acmegrade (July 2024 – Aug 2024)

=== AVAILABILITY ===
- Rushil is available for internships and job opportunities immediately
- Graduating in 2026 (B.Tech CS)
- Open to both remote and on-site positions in Delhi/NCR and beyond

=== PERSONALITY ===
- Passionate about coding, web development, and building digital experiences
- Football enthusiast — stays disciplined and focused through sports
- Approach: clean code, effective problem solving, efficient and engaging solutions

Respond concisely but informatively. Be friendly and professional. If asked about something not in the above context, say you don't have that specific information but direct them to contact Rushil directly.
"""

# --- Models ---
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    timestamp: str

# --- OpenRouter API call ---
async def call_openrouter(messages: list) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        return "⚠️ OpenRouter API key not configured. Please set OPENROUTER_API_KEY in the .env file."
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://rushilgosain.dev",
                "X-Title": "Rushil Portfolio",
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",  # Free model on OpenRouter
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7,
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"OpenRouter error: {response.text}")
        
        data = response.json()
        return data["choices"][0]["message"]["content"]

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Rushil Portfolio API is running ✅", "version": "1.0.0"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # Build message history for AI
    messages = [{"role": "system", "content": RUSHIL_CONTEXT}]
    
    # Add conversation history (last 6 messages for context)
    for msg in (req.history or [])[-6:]:
        messages.append({"role": msg.role, "content": msg.content})
    
    # Add current message
    messages.append({"role": "user", "content": req.message})
    
    # Get AI response
    ai_response = await call_openrouter(messages)
    
    # Save to database
    timestamp = datetime.utcnow().isoformat()
    db.save_message(req.message, ai_response, timestamp)
    
    return ChatResponse(response=ai_response, timestamp=timestamp)

@app.get("/chat/history")
def get_history(limit: int = 50):
    """Get recent chat history from database"""
    return {"history": db.get_recent(limit)}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
