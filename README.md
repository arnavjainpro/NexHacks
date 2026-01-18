# Veritas: The Real-Time Compliance Copilot

**"Train. Protect. Analyze."**

Veritas is an AI-powered sales enablement platform designed for high-stakes industries (Pharma, MedTech, Finance). Unlike existing tools that analyze sales calls after they happen, Veritas acts as an active copilot, providing real-time, text-based guidance to reps during live conversations.

## 🎯 Core Features

### 1. Dr. Doom Simulator (Training Mode)
- AI-powered voice simulation using ElevenLabs
- Realistic "trap" scenarios to test compliance knowledge
- Real-time coaching sidebar with instant feedback

### 2. Live Copilot (Live Mode)
- Silent HUD during actual sales calls
- Real-time compliance checking
- Text-based nudges to prevent violations
- Privacy-first architecture (ephemeral data)

### 3. Safety Scorecard (Analytics Mode)
- Instant post-call compliance scoring
- Highlight saved moments where violations were prevented
- Actionable feedback for improvement

## 🏗️ Architecture

```
veritas/
├── backend/
│   ├── api/              # REST API endpoints
│   ├── services/         # Core business logic
│   ├── compliance/       # Compliance rules engine
│   ├── ai/              # AI model integrations
│   └── realtime/        # LiveKit & WebSocket handlers
├── frontend/
│   ├── dashboard/       # Manager analytics dashboard
│   ├── copilot/         # Real-time HUD interface
│   └── simulator/       # Training mode UI
├── shared/
│   ├── types/           # TypeScript type definitions
│   └── utils/           # Shared utilities
└── docs/                # Documentation
```

## 🚀 Technology Stack

- **Backend**: Python (FastAPI), Node.js (Express)
- **Frontend**: React + TypeScript, TailwindCSS
- **Real-time**: LiveKit, WebSockets
- **AI/ML**: 
  - ElevenLabs (Voice synthesis)
  - Wispr Flow (Speech capture)
  - The Token Company (Context compression)
  - OpenAI/Anthropic (LLM for compliance analysis)
- **Database**: PostgreSQL + Redis
- **Privacy**: Ephemeral memory, sliding window architecture

## 🔐 Privacy & Compliance

- HIPAA-compliant data handling
- Ephemeral audio processing (immediate deletion)
- Doctor/patient data never stored
- Sliding window memory architecture

## 📊 Market Advantage

| Feature | Gong/Chorus | Veritas |
|---------|-------------|---------|
| Timing | Post-Call | Real-Time |
| Feedback | Next Day | Instant |
| Training | Passive Video | Active Voice Simulation |
| Privacy | Records Everything | Ephemeral Context |

## 🎯 Getting Started

See [SETUP.md](./SETUP.md) for installation and configuration instructions.

## 📝 License

Proprietary - All Rights Reserved
