# Veritas Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- API Keys:
  - OpenAI API Key
  - ElevenLabs API Key
  - LiveKit credentials
  - The Token Company API Key (if available)

## Environment Variables

Create a `.env` file in the root directory:

```env
# API Keys
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
LIVEKIT_URL=wss://your-livekit-instance.com
TOKEN_COMPANY_API_KEY=your_token_company_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/veritas
REDIS_URL=redis://localhost:6379

# App Configuration
ENVIRONMENT=development
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Privacy Settings
MAX_AUDIO_RETENTION_SECONDS=0
ENABLE_SLIDING_WINDOW=true
WINDOW_SIZE_SECONDS=30
```

## Backend Setup (Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload --port 8000
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## LiveKit Setup

1. Sign up at [LiveKit Cloud](https://livekit.io/)
2. Create a new project
3. Copy your API key and secret to `.env`

## Database Setup

```bash
# Create database
createdb veritas

# Run migrations
cd backend
alembic upgrade head
```

## Running the Application

### Development Mode

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Redis (if not running as service)
redis-server

# Terminal 4: LiveKit (optional local instance)
livekit-server --dev
```

### Production Mode

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment instructions.

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Troubleshooting

### LiveKit Connection Issues
- Ensure your firewall allows WebSocket connections
- Check that LIVEKIT_URL is correct
- Verify API credentials

### Audio Not Working
- Check browser permissions for microphone
- Ensure Wispr Flow is properly configured
- Test with a simple audio recording first

### Compliance Engine Errors
- Verify all compliance rules are loaded
- Check that The Token Company integration is working
- Review logs in `backend/logs/`
