from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001"])

# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ─── Database Models ────────────────────────────────────────────
class ChatSession(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), db.ForeignKey('chat_session.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# ─── Resume Context ─────────────────────────────────────────────
RESUME_CONTEXT = """
You are Rushil Gosain's AI portfolio assistant. Answer questions based ONLY on the following resume data. Be helpful, concise, and friendly.

=== RUSHIL GOSAIN - RESUME ===

PERSONAL INFO:
- Name: Rushil Gosain
- Email: rushilgosain10@gmail.com
- Phone: +91 8860816875
- LinkedIn: linkedin.com/in/rushil-gosain-434b57285
- GitHub: github.com/RushilGosain

EDUCATION:
- B.Tech, Computer Science — Dr. Akhilesh Das Gupta Institute Of Professional Studies (GGSIPU), 2022–2026
- CBSE Class 12 (Science), 2022
- CBSE Class 10 — Scored 86.5%, 2020

SKILLS:
- C++ (90%) — Strong OOP, problem-solving, optimized code
- HTML (85%) — Semantic, accessible web pages
- CSS (80%) — Responsive, visually appealing UI
- JavaScript (70%) — Dynamic interactions, DOM manipulation
- Data Structures & Algorithms (60%)
- AI Tools (75%) — ChatGPT, automation, intelligent workflows
- React (65%) — Component-based modern apps
- Python (70%) — Backend, AI integration

TRAININGS / EXPERIENCE:
1. Software Engineering Virtual Experience Trainee — Commonwealth Bank (Forage), May 2025
   - Built responsive web page with HTML & CSS
   - Applied cybersecurity principles
   - Drafted secure web hosting proposal

2. Full Stack Web Development Intern — Global Next Consulting India Pvt. Ltd., Aug–Sep 2025
   - Developed and styled responsive web apps
   - Client interaction, data privacy standards
   - Submitted final project

PROJECTS:
1. NeuroTrack – AI-Powered Mental Health Tracking Platform
   - AI-based platform for mental health trend monitoring
   - Sentiment analysis, text summarization
   - Stack: HTML/CSS/JS, Flask (Python), OpenAI API, MySQL
   - GitHub: github.com/RushilGosain/NEUROTRACK

2. My Portfolio
   - Personal portfolio with particle constellations, comet cursor, aurora waves
   - Stack: HTML5, CSS3, HTML5 Canvas
   - GitHub: github.com/RushilGosain/My-Portfolio

3. Blittz-Quiz
   - Interactive quiz app with Next.js 13, TypeScript, Tailwind CSS
   - Sign-in, categories, responsive UI
   - Stack: Next.js, TypeScript, NextAuth.js, API Integration
   - GitHub: github.com/RushilGosain/blittz-quiz

CERTIFICATIONS:
- Front End Development — Great Learning, July 2024–Sept 2025
- AI & Machine Learning Training — Acmegrade, July 2024–Aug 2024

ABOUT:
Rushil is a B.Tech CS student passionate about coding, web development, and building digital experiences. He enjoys building interactive applications and efficient solutions. Off screen, football keeps him disciplined and focused. His approach: write clean code, solve problems effectively, and build impactful solutions.

=== END OF RESUME ===

Keep answers friendly, informative, and brief (2-4 sentences). If asked something not in the resume, politely say you only have info from the resume.
"""

# ─── Chat API ────────────────────────────────────────────────────
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()
    session_id = data.get('session_id', 'default')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    # Get or create session
    session = ChatSession.query.get(session_id)
    if not session:
        session = ChatSession(id=session_id)
        db.session.add(session)
        db.session.commit()

    # Save user message
    user_msg = ChatMessage(session_id=session_id, role='user', content=message)
    db.session.add(user_msg)
    db.session.commit()

    # Build conversation history (last 10 messages)
    history = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at).limit(10).all()
    messages = [{'role': m.role, 'content': m.content} for m in history]

    # Call OpenRouter API
    openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
    
    if not openrouter_key:
        response_text = "API key not configured. Please set OPENROUTER_API_KEY in .env file."
    else:
        try:
            api_messages = [{'role': 'system', 'content': RESUME_CONTEXT}] + messages
            
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {openrouter_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'http://localhost:3000',
                    'X-Title': 'Rushil Portfolio',
                },
                json={
                    'model': 'mistralai/mistral-7b-instruct:free',
                    'messages': api_messages,
                    'max_tokens': 400,
                    'temperature': 0.7,
                },
                timeout=30
            )
            
            result = response.json()
            if 'choices' in result and result['choices']:
                response_text = result['choices'][0]['message']['content']
            else:
                response_text = f"Sorry, I couldn't get a response. Error: {result.get('error', {}).get('message', 'Unknown')}"
        except Exception as e:
            response_text = f"Connection error: {str(e)}"

    # Save assistant message
    assistant_msg = ChatMessage(session_id=session_id, role='assistant', content=response_text)
    db.session.add(assistant_msg)
    db.session.commit()

    return jsonify({'response': response_text, 'session_id': session_id})

# ─── History API ─────────────────────────────────────────────────
@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_history(session_id):
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at).all()
    return jsonify([{'role': m.role, 'content': m.content, 'timestamp': m.created_at.isoformat()} for m in messages])

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Rushil Portfolio API running'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
