# Veritas Development Guide

## Project Overview

Veritas is a real-time compliance copilot for pharmaceutical sales reps. The project consists of:

- **Backend**: Python FastAPI application with real-time WebSocket support
- **Frontend**: React + TypeScript with Vite
- **Key Features**: Training Mode, Live Copilot, Analytics

## Architecture

### Backend Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── api/                   # API endpoints
│   ├── training.py       # Training mode endpoints
│   ├── copilot.py        # Live copilot endpoints
│   ├── analytics.py      # Analytics endpoints
│   └── auth.py           # Authentication
└── services/             # Business logic
    ├── compliance_engine.py    # Core compliance rules
    ├── websocket_manager.py    # Real-time WebSocket handling
    ├── ai_doctor.py           # AI Doctor for training
    ├── training_service.py    # Training session management
    ├── copilot_service.py     # Live copilot logic
    └── analytics_service.py   # Analytics generation
```

### Frontend Structure
```
frontend/
├── src/
│   ├── main.tsx          # Entry point
│   ├── App.tsx           # Router configuration
│   ├── components/       # Reusable components
│   │   └── Layout.tsx    # Main layout with navigation
│   └── pages/            # Page components
│       ├── Dashboard.tsx
│       ├── TrainingMode.tsx
│       ├── LiveCopilot.tsx
│       ├── Analytics.tsx
│       └── Profile.tsx
```

## Getting Started

### 1. Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

Required API keys:
- OpenAI API Key (for LLM)
- ElevenLabs API Key (for voice synthesis)
- LiveKit credentials (for real-time audio)

### 3. Run the Application

**Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Visit http://localhost:5173

## Key Features Implementation

### 1. Training Mode (Dr. Doom Simulator)

**Backend**: `services/training_service.py`, `services/ai_doctor.py`
- Creates training sessions with configurable difficulty
- Generates AI doctor responses with different personalities
- Provides real-time coaching feedback

**Frontend**: `pages/TrainingMode.tsx`
- Session configuration UI
- Real-time conversation interface
- Coach's sidebar with feedback nudges

### 2. Live Copilot Mode

**Backend**: `services/copilot_service.py`, `services/websocket_manager.py`
- WebSocket-based real-time communication
- Privacy-first architecture (sliding window memory)
- Real-time compliance checking

**Frontend**: `pages/LiveCopilot.tsx`
- Live session HUD
- Real-time transcript display
- Compliance nudges sidebar

### 3. Compliance Engine

**Backend**: `services/compliance_engine.py`
- Rule-based violation detection
- Categories: off-label, efficacy, safety, contraindications
- Real-time text analysis

Default rules include:
- Off-label promotion detection
- Efficacy exaggeration
- Side effect downplaying
- Contraindication dismissal
- Illegal pricing discussions

### 4. Analytics & Safety Scorecard

**Backend**: `services/analytics_service.py`
- Post-session scorecard generation
- User progress tracking
- Team leaderboards
- Violation trend analysis

**Frontend**: `pages/Analytics.tsx`
- Scorecard visualization
- Progress charts
- Improvement recommendations

## WebSocket Protocol

### Connection
```
ws://localhost:8000/ws/{session_id}
```

### Message Types

**Client → Server:**
```json
{
  "type": "transcript",
  "speaker": "rep|doctor",
  "text": "...",
  "timestamp": 123.45
}
```

**Server → Client:**
```json
{
  "type": "nudge",
  "nudge_id": "...",
  "severity": "critical|warning|info",
  "icon": "🛑|⚠️|💡",
  "title": "...",
  "message": "...",
  "suggested_response": "..."
}
```

## Privacy & Compliance

### Sliding Window Architecture
- Keeps only last 10 transcript segments in memory
- Doctor/patient audio never stored
- Immediate data deletion after processing

### Configuration
```python
# config.py
MAX_AUDIO_RETENTION_SECONDS = 0  # Immediate deletion
ENABLE_SLIDING_WINDOW = True
WINDOW_SIZE_SECONDS = 30
```

## Next Steps for Production

### 1. Integrate Real Audio Processing
- [ ] Implement Wispr Flow for speech capture
- [ ] Add Deepgram or Whisper for transcription
- [ ] Connect ElevenLabs for voice synthesis

### 2. Add LiveKit Support
- [ ] Set up LiveKit server
- [ ] Implement audio streaming
- [ ] Add participant management

### 3. Database Integration
- [ ] Set up PostgreSQL
- [ ] Create database schemas
- [ ] Implement Alembic migrations
- [ ] Add Redis for session management

### 4. Authentication & Authorization
- [ ] Implement JWT authentication
- [ ] Add user roles (rep, manager, admin)
- [ ] Secure WebSocket connections

### 5. The Token Company Integration
- [ ] Integrate for context compression
- [ ] Load FDA regulations
- [ ] Optimize token usage

### 6. Testing
- [ ] Write unit tests (pytest)
- [ ] Add integration tests
- [ ] Test WebSocket connections
- [ ] Load testing for concurrent sessions

### 7. Deployment
- [ ] Containerize with Docker
- [ ] Set up CI/CD pipeline
- [ ] Configure production environment
- [ ] Add monitoring (Sentry)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/token` - Login
- `GET /api/auth/me` - Get current user

### Training
- `POST /api/training/sessions/start` - Start training session
- `GET /api/training/sessions/{id}` - Get session details
- `POST /api/training/sessions/{id}/stop` - Stop session
- `GET /api/training/scenarios` - List scenarios

### Copilot
- `POST /api/copilot/sessions/start` - Start live session
- `GET /api/copilot/sessions/{id}` - Get session details
- `POST /api/copilot/sessions/{id}/stop` - Stop session
- `POST /api/copilot/sessions/{id}/process-transcript` - Process transcript

### Analytics
- `GET /api/analytics/scorecard/{id}` - Get Safety Scorecard
- `GET /api/analytics/user/{id}/history` - User session history
- `GET /api/analytics/user/{id}/progress` - User progress
- `GET /api/analytics/team/leaderboard` - Team leaderboard

## Troubleshooting

### Backend won't start
- Check Python version (3.11+)
- Verify all dependencies installed
- Check `.env` file exists

### Frontend won't start
- Check Node.js version (18+)
- Run `npm install` again
- Clear node_modules and reinstall

### WebSocket connection fails
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify WebSocket proxy in vite.config.ts

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## License

Proprietary - All Rights Reserved
