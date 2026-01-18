# Veritas Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         VERITAS ARCHITECTURE                             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            FRONTEND LAYER                                │
│                      (React + TypeScript + Vite)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │ Dashboard  │  │  Training  │  │   Live     │  │ Analytics  │       │
│  │            │  │    Mode    │  │  Copilot   │  │            │       │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘       │
│         │               │                │                │              │
│         └───────────────┴────────────────┴────────────────┘              │
│                              │                                           │
│                         HTTP/WS API                                      │
│                              │                                           │
└──────────────────────────────┼───────────────────────────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                            BACKEND LAYER                                 │
│                        (Python FastAPI)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        API ENDPOINTS                             │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │  /api/training  │  /api/copilot  │  /api/analytics  │  /api/auth│  │
│  └─────────────────────────────────────────────────────────────────┘   │
│                               │                                          │
│  ┌────────────────────────────┼──────────────────────────────────────┐ │
│  │           WebSocket Manager         (Real-Time Communication)     │ │
│  │                   ws://host/ws/{session_id}                       │ │
│  └────────────────────────────┬──────────────────────────────────────┘ │
│                               │                                          │
│  ┌────────────────────────────┼──────────────────────────────────────┐ │
│  │                       CORE SERVICES                                │ │
│  ├────────────────────────────┴──────────────────────────────────────┤ │
│  │                                                                    │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │ │
│  │  │  Compliance     │  │   AI Doctor      │  │   Training      │ │ │
│  │  │    Engine       │  │    Service       │  │    Service      │ │ │
│  │  │                 │  │                  │  │                 │ │ │
│  │  │ • 10+ Rules     │  │ • ElevenLabs    │  │ • Sessions      │ │ │
│  │  │ • Pattern Match │  │ • Personalities │  │ • Scenarios     │ │ │
│  │  │ • Real-time     │  │ • Voice Synth   │  │ • Feedback      │ │ │
│  │  └─────────────────┘  └──────────────────┘  └─────────────────┘ │ │
│  │                                                                    │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │ │
│  │  │    Copilot      │  │    Analytics     │  │     Audio       │ │ │
│  │  │    Service      │  │     Service      │  │   Processor     │ │ │
│  │  │                 │  │                  │  │                 │ │ │
│  │  │ • Live Sessions │  │ • Scorecards    │  │ • Wispr Flow   │ │ │
│  │  │ • Nudges        │  │ • Progress      │  │ • Transcription│ │ │
│  │  │ • Privacy       │  │ • Leaderboards  │  │ • Streaming    │ │ │
│  │  └─────────────────┘  └──────────────────┘  └─────────────────┘ │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL SERVICES                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  OpenAI/     │  │  ElevenLabs  │  │   LiveKit    │  │ The Token  │ │
│  │  Anthropic   │  │              │  │              │  │  Company   │ │
│  │              │  │              │  │              │  │            │ │
│  │ LLM Analysis │  │Voice Synth   │  │Real-Time     │  │Context     │ │
│  │ Compliance   │  │AI Doctor     │  │Audio Stream  │  │Compression │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA STORAGE LAYER                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐         ┌──────────────────┐                     │
│  │   PostgreSQL     │         │      Redis       │                     │
│  │                  │         │                  │                     │
│  │ • User Data      │         │ • Sessions       │                     │
│  │ • Sessions       │         │ • WebSocket      │                     │
│  │ • Analytics      │         │ • Cache          │                     │
│  │ • Scorecards     │         │ • Real-time Data │                     │
│  └──────────────────┘         └──────────────────┘                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                            DATA FLOW DIAGRAMS
═══════════════════════════════════════════════════════════════════════════

1. TRAINING MODE FLOW
───────────────────────────────────────────────────────────────────────────

   Rep                Frontend              Backend             AI Doctor
    │                    │                     │                    │
    ├─► Start Session ──►│                     │                    │
    │                    ├──► POST /training ──►│                    │
    │                    │                     ├──► Initialize ────►│
    │                    │◄─── Session ID ─────┤                    │
    │                    │                     │                    │
    │                    │◄─────── AI Says ────┤◄─── Response ─────┤
    │◄─── Display ───────┤                     │                    │
    │                    │                     │                    │
    ├─► Rep Speaks ─────►│                     │                    │
    │                    ├──► Transcript ──────►│                    │
    │                    │                     │                    │
    │                    │                     ├─► Check Compliance │
    │                    │                     │   (Engine)         │
    │                    │                     │                    │
    │◄─── Nudge ─────────┤◄─── Violation ──────┤                    │
    │    (Warning!)      │                     │                    │
    │                    │                     │                    │


2. LIVE COPILOT FLOW
───────────────────────────────────────────────────────────────────────────

   Rep & Doctor       Frontend         WebSocket          Compliance
   (Sales Call)                        Manager            Engine
        │                 │                │                   │
        ├─► Start ───────►│                │                   │
        │                 ├─► Connect ─────►│                   │
        │                 │                │                   │
   Rep speaks about       │                │                   │
   drug benefits          │                │                   │
        │                 │                │                   │
        ├─► Audio ───────►│                │                   │
        │                 ├─► Transcript ──►│                   │
        │                 │   (rep only)   │                   │
        │                 │                ├─► Check ─────────►│
        │                 │                │                   │
        │                 │                │  ⚠️ Off-label     │
        │                 │                │     detected!     │
        │                 │                │                   │
        │                 │◄── Nudge ──────┤◄─── Violation ────┤
        │◄── Display ─────┤   Message      │                   │
   🛑 STOP!               │                │                   │
   Corrects statement     │                │                   │
        │                 │                │                   │


3. PRIVACY-FIRST ARCHITECTURE
───────────────────────────────────────────────────────────────────────────

   Audio Input          Processing         Compliance       Storage
                                          Check
        │                   │                  │               │
        ├─► Doctor audio ──►│                  │               │
        │   (for context)   │                  │               │
        │                   ├─► Process ──────►│               │
        │                   │   (in memory)    │               │
        │                   │                  │               │
        │                   ├─► DELETE         │               │ ✓ Not stored
        │                   │   (immediate)    │               │
        │                   │                  │               │
        ├─► Rep audio ─────►│                  │               │
        │                   ├─► Check ─────────►│               │
        │                   │                  │               │
        │                   │◄─── Result ──────┤               │
        │                   │                  │               │
        │                   ├─► Store ─────────┼──────────────►│ ✓ Stored
        │                   │   (violation     │   (metadata   │   (minimal)
        │                   │    metadata)     │    only)      │
        │                   │                  │               │
        │                   ├─► DELETE         │               │
        │                   │   (audio)        │               │
        │                   │                  │               │

   Sliding Window: Last 30 seconds only in memory
   Audio Retention: 0 seconds (immediate deletion)
   Privacy: HIPAA-compliant


═══════════════════════════════════════════════════════════════════════════
                         COMPLIANCE RULE CATEGORIES
═══════════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│  🛑 CRITICAL VIOLATIONS                                                │
├────────────────────────────────────────────────────────────────────────┤
│  • Off-Label Promotion                                                 │
│  • Absolute Efficacy Claims                                            │
│  • Downplaying Side Effects                                            │
│  • Ignoring Contraindications                                          │
│  • Illegal Pricing/Kickbacks                                           │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  ⚠️  WARNING VIOLATIONS                                                │
├────────────────────────────────────────────────────────────────────────┤
│  • Implied Off-Label Use                                               │
│  • Comparative Claims Without Data                                     │
│  • Vague Safety Information                                            │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  💡 INFO / COACHING                                                    │
├────────────────────────────────────────────────────────────────────────┤
│  • Uncertain Language                                                  │
│  • Confidence Issues                                                   │
│  • Filler Words                                                        │
└────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                          TECHNOLOGY STACK DETAILS
═══════════════════════════════════════════════════════════════════════════

BACKEND:
├─ FastAPI 0.109.0         (REST API + WebSockets)
├─ Python 3.11+            (Core language)
├─ Pydantic 2.5.3          (Data validation)
├─ SQLAlchemy 2.0.25       (ORM)
├─ Redis 5.0.1             (Caching)
├─ Loguru 0.7.2            (Logging)
├─ OpenAI 1.10.0           (LLM)
├─ ElevenLabs 0.2.26       (Voice synthesis)
└─ LiveKit 0.11.0          (Real-time audio)

FRONTEND:
├─ React 18.2.0            (UI framework)
├─ TypeScript 5.3.3        (Type safety)
├─ Vite 5.0.11             (Build tool)
├─ TailwindCSS 3.4.1       (Styling)
├─ React Router 6.21.1     (Navigation)
├─ React Query 5.17.9      (Data fetching)
├─ Axios 1.6.5             (HTTP client)
└─ Zustand 4.4.7           (State management)
