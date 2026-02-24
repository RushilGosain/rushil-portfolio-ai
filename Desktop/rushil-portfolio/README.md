# 🚀 Rushil Gosain — Portfolio with AI Chat

A modern, full-stack personal portfolio featuring an **AI-powered chat assistant** that answers questions about the resume using natural language. Built with **React + TypeScript** (frontend) and **Python Flask** (backend), connected to **OpenRouter** for AI capabilities.

---

## ✨ Features

- 🎨 **Dark, cyberpunk-inspired UI** with teal/blue/purple palette — matching original portfolio aesthetic
- 💬 **AI Chat Widget** — Ask anything about Rushil's resume, skills, projects, or experience
- ⚛️ **React + TypeScript** frontend with full type safety
- 🐍 **Python Flask** backend with SQLite database for chat history
- 🤖 **OpenRouter integration** (free Mistral-7B model — no credit card needed)
- 🌊 **Particle constellation** background animation
- ✍️ **Typing effect** for hero and about sections
- 📱 **Fully responsive** across all devices
- 🖱️ **Custom cursor** with comet trail effect
- 📜 **Scroll progress** indicator

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, CSS-in-JS |
| Backend | Python 3.x, Flask, Flask-SQLAlchemy |
| Database | SQLite (via SQLAlchemy ORM) |
| AI Engine | OpenRouter API (Mistral-7B free model) |
| Animations | CSS animations + Canvas API |
| Fonts | Syne (headings), Space Grotesk (body) |

---

## 📁 Project Structure

```
rushil-portfolio/
├── frontend/                  # React TypeScript app
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Cursor.tsx     # Custom comet cursor
│   │   │   ├── Navbar.tsx     # Fixed navigation
│   │   │   ├── Hero.tsx       # Particle canvas + typing
│   │   │   ├── About.tsx      # Bio + education
│   │   │   ├── Skills.tsx     # Skill cards with bars
│   │   │   ├── Experience.tsx # Timeline
│   │   │   ├── Projects.tsx   # Project cards
│   │   │   ├── Certifications.tsx
│   │   │   ├── Contact.tsx
│   │   │   ├── ChatWidget.tsx # 💬 AI Chat UI
│   │   │   └── Footer.tsx
│   │   ├── types/index.ts     # TypeScript interfaces
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── index.css
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                   # Python Flask API
│   ├── app.py                 # Main Flask app + routes
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variable template
│   └── .gitignore
│
└── README.md
```

---

## ⚡ Quick Setup

### Prerequisites
- **Node.js** v18+ ([download](https://nodejs.org))
- **Python** 3.9+ ([download](https://python.org))
- **OpenRouter API Key** (free at [openrouter.ai](https://openrouter.ai))

---

### Step 1: Get OpenRouter API Key (FREE)

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Click **Sign Up** (free, no credit card needed)
3. Go to **API Keys** → Create a new key
4. Copy your key — it looks like `sk-or-v1-...`

> The app uses `mistralai/mistral-7b-instruct:free` which is completely free!

---

### Step 2: Set Up the Backend

```bash
# Navigate to backend folder
cd rushil-portfolio/backend

# Create a virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file
cp .env.example .env

# Edit .env and paste your OpenRouter key:
# OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Open `.env` and add your key:
```env
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
FLASK_ENV=development
FLASK_DEBUG=1
```

```bash
# Start the Flask server
python app.py
```

✅ Backend runs at: `http://localhost:5000`  
✅ Test it: visit `http://localhost:5000/api/health`

---

### Step 3: Set Up the Frontend

Open a **new terminal tab/window**:

```bash
# Navigate to frontend folder
cd rushil-portfolio/frontend

# Install dependencies
npm install

# Start the React dev server
npm start
```

✅ Frontend runs at: `http://localhost:3000`  
✅ The `"proxy": "http://localhost:5000"` in package.json routes API calls automatically.

---

### Step 4: Open the Portfolio

Visit **[http://localhost:3000](http://localhost:3000)** 🎉

Click the **💬 chat bubble** in the bottom-right corner to talk to the AI assistant!

---

## 💬 Try These Chat Questions

- *"What projects has Rushil built?"*
- *"What programming languages does he know?"*
- *"Tell me about his education"*
- *"What internships has he done?"*
- *"How can I contact Rushil?"*
- *"What is NeuroTrack?"*

---

## 🌐 Deployment (Bonus)

### Frontend → GitHub Pages / Vercel / Netlify

```bash
cd frontend
npm run build
# Deploy the `build/` folder to your hosting of choice
```

### Backend → Cloudflare Tunnel (Free, Public URL)

```bash
# Install cloudflared CLI from: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

# Start your backend first
python app.py

# In another terminal, expose it publicly:
cloudflared tunnel --url http://localhost:5000
```

You'll get a URL like `https://xyz.trycloudflare.com`. Update the frontend's API call URL to use it.

### Full Deployment on Render (Free)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo, set root to `backend/`
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Add environment variable: `OPENROUTER_API_KEY`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send a message, get AI response |
| GET | `/api/chat/history/:session_id` | Get chat history |
| GET | `/api/health` | Health check |

**POST /api/chat body:**
```json
{
  "message": "What are Rushil's skills?",
  "session_id": "unique-session-id"
}
```

---

## 🎨 Customization

To personalize for yourself, edit:

1. **`backend/app.py`** → Update `RESUME_CONTEXT` with your own resume data
2. **`frontend/src/components/`** → Update all personal info in each component
3. **`frontend/public/index.html`** → Update title and meta tags

---

## 📸 Screenshots

| Section | Description |
|---------|-------------|
| Hero | Particle constellation + typing animation |
| About | Typewriter effect bio + education card |
| Skills | Hover cards with animated progress bars |
| Projects | 3-column cards with color theming |
| Chat | Bottom-right floating AI assistant |

---

## 🤝 Credits

- **Design inspiration**: [rushilportfolio1.netlify.app](https://rushilportfolio1.netlify.app)
- **AI Model**: Mistral-7B via OpenRouter (free tier)
- **Fonts**: Syne + Space Grotesk (Google Fonts)

---

## 📄 License

MIT License — feel free to use and customize!

---

*Built with ❤️ for the Vedaz Internship Assignment*
