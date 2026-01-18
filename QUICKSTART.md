# Veritas - Quick Start Guide

## Get Up and Running in 5 Minutes

### Option 1: Quick Setup (Recommended)

Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create Python virtual environment
- Install all dependencies
- Create `.env` file
- Set up project structure

### Option 2: Manual Setup

**1. Backend Setup:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Frontend Setup:**
```bash
cd frontend
npm install
```

**3. Environment Configuration:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open:** http://localhost:5173

### Test the Compliance Engine

Without starting the full app, you can test the compliance rules:
```bash
python test_compliance.py
```

### Quick Feature Overview

1. **Dashboard** - View your stats and recent sessions
2. **Training Mode** - Practice with AI Doctor (Dr. Doom)
3. **Live Copilot** - Get real-time guidance during calls
4. **Analytics** - View Safety Scorecards and progress

### API Documentation

Once the backend is running, visit:
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Architecture Diagram

```
┌─────────────────┐
│   Frontend      │
│  React + Vite   │
│   Port 5173     │
└────────┬────────┘
         │ HTTP/WS
         ↓
┌─────────────────┐
│   Backend       │
│  FastAPI        │
│   Port 8000     │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌──────────┐
│Database│ │ Redis    │
│Postgres│ │ Cache    │
└────────┘ └──────────┘
```

### Key Integrations (Production)

- **ElevenLabs** - Voice synthesis for AI Doctor
- **Wispr Flow** - High-quality speech capture
- **LiveKit** - Real-time audio streaming
- **The Token Company** - Context compression
- **OpenAI** - LLM for compliance analysis

### Next Steps

1. ✅ Set up development environment
2. 🔑 Add API keys to `.env`
3. 🧪 Test compliance engine
4. 🚀 Start backend and frontend
5. 🎯 Try Training Mode
6. 📊 View Analytics

### Need Help?

- **Setup Issues:** See [SETUP.md](./SETUP.md)
- **Development:** See [DEVELOPMENT.md](./DEVELOPMENT.md)
- **API Reference:** http://localhost:8000/docs

### Demo Mode

The app works without API keys in demo mode:
- Mock AI Doctor responses
- Simulated compliance checks
- Sample analytics data

Add real API keys for production features:
- Real voice synthesis
- Advanced LLM analysis
- Live audio streaming

---

**Ready to build the future of compliance?** 🚀

Train. Protect. Analyze.
