# NexHacks - Project Overview

**Veritas: Sales Compliance Intelligence Platform**

A desktop application for pharmaceutical sales compliance training and real-time call monitoring.

---

## Quick Start

```bash
# Terminal 1: Backend Token Server
cd backend && python server.py

# Terminal 2: LiveKit Agent
cd backend && python agent.py dev

# Terminal 3: Frontend
cd frontend && npm run dev
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              ELECTRON SHELL                              │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                      REACT FRONTEND (Vite)                      │   │
│   │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │   │
│   │  │  Dashboard   │ │ TrainingMode │ │      LiveCopilot         │ │   │
│   │  │  (Overview)  │ │ (Dr. Doom AI)│ │  (Real-time Monitoring)  │ │   │
│   │  └──────────────┘ └──────────────┘ └──────────────────────────┘ │   │
│   └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                        ┌───────────┴───────────┐
                        ▼                       ▼
              ┌──────────────────┐    ┌──────────────────┐
              │   Token Server   │    │   LiveKit Agent  │
              │   (FastAPI)      │    │   (Python)       │
              │   Port 8000      │    │   Gemini + DG    │
              └──────────────────┘    └──────────────────┘
```

---

## File Structure

```
NexHacks/
├── backend/                    # Python Backend
│   ├── agent.py               # LiveKit Voice Agent (Dr. Doom + Observer)
│   ├── server.py              # FastAPI Token Server
│   ├── config.py              # Environment configuration
│   ├── main.py                # Legacy FastAPI app (unused?)
│   ├── requirements.txt       # Python dependencies
│   ├── api/                   # API Routes
│   │   ├── analytics.py       # Session analytics endpoints
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── copilot.py         # Live copilot endpoints
│   │   └── training.py        # Training session endpoints
│   └── services/              # Business Logic
│       ├── ai_doctor.py       # Dr. Doom personality/prompts
│       ├── compliance_engine.py  # Keyword detection rules
│       ├── compliance_checker.py # Compliance validation
│       ├── analytics_service.py  # Session analytics
│       ├── copilot_service.py    # Live assistance logic
│       ├── training_service.py   # Training orchestration
│       ├── websocket_manager.py  # WebSocket connections
│       └── audio_processor.py    # Audio stream processing
│
├── frontend/                  # React Frontend (Vite)
│   ├── src/
│   │   ├── App.tsx           # Main router
│   │   ├── main.tsx          # Entry point
│   │   ├── index.css         # Global styles
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx     # Home dashboard
│   │   │   ├── TrainingMode.tsx  # Dr. Doom training
│   │   │   ├── LiveCopilot.tsx   # Real-time monitoring
│   │   │   ├── Analytics.tsx     # Performance stats
│   │   │   ├── Profile.tsx       # User settings
│   │   │   └── Widget.tsx        # Floating overlay
│   │   ├── components/
│   │   │   ├── Layout.tsx        # App shell/navigation
│   │   │   └── FloatingWidget.tsx # Overlay HUD
│   │   └── types/
│   │       └── index.ts          # TypeScript types
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── electron/                  # Desktop Shell
│   ├── main.js               # Window management
│   ├── preload.js            # IPC bridge
│   └── package.json
│
└── docs/                      # Documentation
    ├── QUICKSTART.md
    ├── ARCHITECTURE.md
    ├── DEVELOPMENT.md
    └── ELECTRON_SETUP.md
```

---

## Key Components

### Backend: `agent.py`

Two modes controlled by `mode` in job metadata:

| Mode | Behavior |
|------|----------|
| `training` | Interactive Dr. Doom voice agent using Gemini LLM + Deepgram STT/TTS |
| `live` | Silent observer that detects compliance keywords and sends DataPackets |

**Stack:** Gemini 2.0 Flash + Deepgram Nova 2 + Silero VAD + MultilingualModel turn detection

### Backend: `server.py`

FastAPI token server at `http://localhost:8000`:

| Endpoint | Purpose |
|----------|---------|
| `GET /api/token?mode=training` | Generate LiveKit JWT for training sessions |
| `GET /api/token?mode=live` | Generate LiveKit JWT for live monitoring |
| `GET /health` | Health check |

### Frontend: Pages

| Page | Description |
|------|-------------|
| `Dashboard.tsx` | Home screen with stats and quick actions |
| `TrainingMode.tsx` | Configure and start Dr. Doom training sessions |
| `LiveCopilot.tsx` | Real-time compliance monitoring during calls |
| `Analytics.tsx` | Session history and performance metrics |
| `Widget.tsx` | Floating overlay widget for live mode |

### Electron: Desktop App

- **Window Management:** Standard 1200x800 dashboard, toggleable to 350x600 overlay
- **IPC Bridge:** `preload.js` exposes `window.electronAPI`
- **Always-on-top:** Overlay mode floats above Zoom calls

---

## Environment Variables

### Backend (`backend/.env`)
```
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
LIVEKIT_URL=wss://your-project.livekit.cloud
GOOGLE_API_KEY=...
DEEPGRAM_API_KEY=...
```

### Frontend (`frontend/.env`)
```
VITE_API_URL=http://localhost:8000
VITE_LIVEKIT_URL=wss://your-project.livekit.cloud
```

---

## Compliance Keywords Detected

The agent monitors for these terms in `live` mode:

- `guarantee`, `cure`, `promise`, `100%`
- `always works`, `no side effects`, `risk-free`
- `off-label`, `unapproved`, `miracle`
- `best on the market`, `better than`

When detected, a DataPacket is published to the `compliance_alerts` topic.

---

## Dependencies

### Python (backend/requirements.txt)
- `livekit-agents[turn-detector]` - Voice agent framework
- `livekit-plugins-google` - Gemini LLM
- `livekit-plugins-deepgram` - STT/TTS
- `livekit-plugins-silero` - VAD
- `fastapi`, `uvicorn` - API server
- `python-dotenv` - Environment management

### Frontend (frontend/package.json)
- `react`, `react-dom` - UI framework
- `react-router-dom` - Routing
- `@livekit/components-react` - LiveKit UI components
- `livekit-client` - LiveKit SDK
- `lucide-react` - Icons
- `tailwindcss` - Styling

---

## Running in Production

1. Build frontend: `cd frontend && npm run build`
2. Package with Electron: `cd electron && npm run build`
3. Deploy agent to LiveKit Cloud or self-hosted server
4. Deploy token server to any Python hosting (Render, Railway, etc.)
