"""
Veritas Backend - Main Application Entry Point
Real-Time Compliance Copilot
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger
import sys

from api import training_router, copilot_router, analytics_router, auth_router, token_compression_router
from services.websocket_manager import websocket_manager
from services.compliance_engine import ComplianceEngine
from config import settings

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL,
)
logger.add(
    "logs/veritas_{time}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting Veritas backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Privacy Mode: Sliding Window Enabled={settings.ENABLE_SLIDING_WINDOW}")
    
    # Initialize compliance engine
    compliance_engine = ComplianceEngine()
    await compliance_engine.initialize()
    app.state.compliance_engine = compliance_engine
    
    logger.success("✅ Veritas backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Veritas backend...")
    await websocket_manager.disconnect_all()
    logger.success("✅ Graceful shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Veritas API",
    description="Real-Time Compliance Copilot for High-Stakes Sales",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "veritas",
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
        }
    )


# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(training_router, prefix="/api/training", tags=["Training"])
app.include_router(copilot_router, prefix="/api/copilot", tags=["Copilot"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(token_compression_router, prefix="/api/token-compression", tags=["TokenCompression"])


# WebSocket endpoint for real-time communication
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time copilot communication
    Handles audio streaming and real-time compliance checking
    """
    await websocket_manager.connect(websocket, session_id)
    logger.info(f"WebSocket connected: {session_id}")
    
    try:
        while True:
            # Receive audio data or messages
            data = await websocket.receive_json()
            
            # Process based on message type
            message_type = data.get("type")
            
            if message_type == "audio_chunk":
                # Handle audio streaming
                await websocket_manager.handle_audio_chunk(session_id, data)
            
            elif message_type == "transcript":
                # Handle transcript for compliance checking
                await websocket_manager.handle_transcript(session_id, data)
            
            elif message_type == "ping":
                # Keep-alive
                await websocket.send_json({"type": "pong"})
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
        await websocket_manager.disconnect(session_id)
    
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {e}")
        await websocket_manager.disconnect(session_id)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Veritas API - Real-Time Compliance Copilot",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
    )
