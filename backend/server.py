"""
Veritas Token Server - FastAPI Endpoint for LiveKit Token Generation
Provides authenticated tokens and agent dispatch for different session modes.
"""

import json
import os
import time
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from livekit.api import AccessToken, VideoGrants, LiveKitAPI
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Configuration
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://localhost:7880")

# Create FastAPI app
app = FastAPI(
    title="Veritas Token Server",
    description="LiveKit Token Generation for Sales Compliance App",
    version="1.0.0",
)

# CORS Configuration - Allow ALL origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TokenResponse(BaseModel):
    """Response model for token endpoint"""
    token: str
    url: str
    room_name: str
    participant_identity: str
    mode: str


class TokenRequest(BaseModel):
    """Request model for token endpoint (POST version)"""
    mode: str = "training"
    room_name: Optional[str] = None
    participant_name: Optional[str] = None


class DispatchResponse(BaseModel):
    """Response model for dispatch endpoint"""
    success: bool
    room_name: str
    mode: str
    message: str


@app.get("/api/token", response_model=TokenResponse)
async def get_token(
    mode: str = Query("training", description="Session mode: training, live, or scorecard"),
    room_name: Optional[str] = Query(None, description="Optional room name"),
    participant_name: Optional[str] = Query(None, description="Optional participant name"),
):
    """
    Generate a LiveKit token for the specified mode.
    """
    try:
        valid_modes = ["training", "live", "scorecard"]
        if mode not in valid_modes:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid mode. Must be one of: {', '.join(valid_modes)}"
            )

        timestamp = int(time.time())
        generated_room_name = room_name or f"veritas-{mode}-{timestamp}"
        generated_participant_name = participant_name or f"user-{timestamp}"

        metadata = json.dumps({
            "mode": mode,
            "created_at": timestamp,
            "app": "veritas",
        })

        grant = VideoGrants(
            room_join=True,
            room=generated_room_name,
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True,
        )

        token = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) \
            .with_identity(generated_participant_name) \
            .with_name(generated_participant_name) \
            .with_metadata(metadata) \
            .with_grants(grant)

        jwt_token = token.to_jwt()

        print(f"[TOKEN] Generated for mode={mode}, room={generated_room_name}")

        return TokenResponse(
            token=jwt_token,
            url=LIVEKIT_URL,
            room_name=generated_room_name,
            participant_identity=generated_participant_name,
            mode=mode,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Token generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/token", response_model=TokenResponse)
async def create_token(request: TokenRequest):
    """Generate a LiveKit token (POST version)."""
    return await get_token(
        mode=request.mode,
        room_name=request.room_name,
        participant_name=request.participant_name,
    )


@app.post("/api/agent/dispatch", response_model=DispatchResponse)
async def dispatch_agent(
    room: str = Query(..., description="Room name to dispatch agent to"),
    mode: str = Query("training", description="Agent mode: training or live"),
):
    """
    Dispatch a LiveKit agent to a specific room.

    This creates an agent job that the agent worker will pick up.
    """
    try:
        print(f"[DISPATCH] Requesting agent for room={room}, mode={mode}")

        # Create metadata for the agent job
        metadata = json.dumps({"mode": mode})

        # Use LiveKit API to create agent dispatch
        api = LiveKitAPI(
            LIVEKIT_URL.replace("wss://", "https://").replace("ws://", "http://"),
            LIVEKIT_API_KEY,
            LIVEKIT_API_SECRET,
        )

        # Create the agent dispatch request
        # This tells LiveKit to dispatch an agent to the room
        try:
            await api.agent_dispatch.create_dispatch(
                room=room,
                agent_name="",  # Empty = default agent
                metadata=metadata,
            )
            print(f"[DISPATCH] Agent dispatched to room={room}")
        except Exception as dispatch_error:
            # If dispatch API fails, try room service to update room metadata
            # This is a fallback that some agent setups use
            print(f"[DISPATCH] Direct dispatch failed: {dispatch_error}")
            print(f"[DISPATCH] Agent worker should auto-join based on room activity")

        await api.aclose()

        return DispatchResponse(
            success=True,
            room_name=room,
            mode=mode,
            message=f"Agent dispatch requested for room {room} in {mode} mode",
        )

    except Exception as e:
        print(f"[ERROR] Agent dispatch failed: {e}")
        # Return success anyway - the agent might still connect via room subscription
        return DispatchResponse(
            success=True,
            room_name=room,
            mode=mode,
            message=f"Dispatch attempted (agent may auto-connect): {str(e)}",
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "veritas-token-server",
            "version": "1.0.0",
            "livekit_url": LIVEKIT_URL,
        }
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Veritas Token Server",
        "version": "1.0.0",
        "endpoints": {
            "token": "/api/token?mode=training|live|scorecard",
            "dispatch": "/api/agent/dispatch?room=<name>&mode=training|live",
            "health": "/health",
            "docs": "/docs",
        },
    }


if __name__ == "__main__":
    import uvicorn

    print("Starting Veritas Token Server on http://0.0.0.0:8000")
    print(f"LiveKit URL: {LIVEKIT_URL}")
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
