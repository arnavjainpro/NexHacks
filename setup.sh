#!/bin/bash

# Veritas - Startup Script
# This script helps you get started with Veritas development

set -e

echo "🚀 Veritas - Real-Time Compliance Copilot"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the Veritas root directory"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

echo "✅ Prerequisites satisfied"
echo ""

# Setup backend
echo "🐍 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

cd ..
echo "✅ Backend setup complete"
echo ""

# Setup frontend
echo "⚛️  Setting up frontend..."
cd frontend

echo "Installing npm dependencies..."
npm install

cd ..
echo "✅ Frontend setup complete"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "🔑 IMPORTANT: Please edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - ELEVENLABS_API_KEY"
    echo "   - LIVEKIT_API_KEY"
    echo "   - LIVEKIT_API_SECRET"
    echo ""
fi

# Create logs directory
mkdir -p backend/logs

echo "✅ Setup complete!"
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Edit .env file and add your API keys"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload --port 8000"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:5173 in your browser"
echo ""
echo "📖 For more information, see:"
echo "   - README.md - Project overview"
echo "   - SETUP.md - Detailed setup instructions"
echo "   - DEVELOPMENT.md - Development guide"
echo ""
echo "🎯 Happy coding with Veritas!"
