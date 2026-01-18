"""
WebSocket Manager - Handles real-time WebSocket connections
"""

from fastapi import WebSocket
from typing import Dict, Set
from loguru import logger
import json
import asyncio
from datetime import datetime

from services.compliance_engine import ComplianceEngine
from services.audio_processor import AudioProcessor


class WebSocketManager:
    """
    Manages WebSocket connections for real-time copilot sessions
    """
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.session_data: Dict[str, Dict] = {}
        self.compliance_engine = ComplianceEngine()
        self.audio_processor = AudioProcessor()
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.session_data[session_id] = {
            "connected_at": datetime.utcnow(),
            "transcript_buffer": [],
            "violations": [],
        }
        logger.info(f"WebSocket connected: {session_id}")
    
    async def disconnect(self, session_id: str):
        """Disconnect and cleanup a WebSocket connection"""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].close()
            except Exception as e:
                logger.error(f"Error closing websocket: {e}")
            
            del self.active_connections[session_id]
        
        # Cleanup session data (privacy-first)
        if session_id in self.session_data:
            logger.info(f"Cleaning up session data for {session_id}")
            del self.session_data[session_id]
        
        logger.info(f"WebSocket disconnected: {session_id}")
    
    async def disconnect_all(self):
        """Disconnect all active WebSocket connections"""
        session_ids = list(self.active_connections.keys())
        for session_id in session_ids:
            await self.disconnect(session_id)
    
    async def send_message(self, session_id: str, message: Dict):
        """Send a message to a specific session"""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {session_id}: {e}")
                await self.disconnect(session_id)
    
    async def broadcast(self, message: Dict):
        """Broadcast a message to all connected sessions"""
        for session_id in list(self.active_connections.keys()):
            await self.send_message(session_id, message)
    
    async def handle_audio_chunk(self, session_id: str, data: Dict):
        """
        Handle incoming audio chunk
        Process for transcription and compliance checking
        """
        try:
            audio_data = data.get("audio")
            timestamp = data.get("timestamp", datetime.utcnow().timestamp())
            
            # Process audio (transcription)
            # In production, this would use Wispr Flow or similar
            # For now, we'll expect pre-transcribed text
            
            logger.debug(f"Received audio chunk for {session_id}")
            
        except Exception as e:
            logger.error(f"Error handling audio chunk: {e}")
            await self.send_message(session_id, {
                "type": "error",
                "message": "Failed to process audio",
            })
    
    async def handle_transcript(self, session_id: str, data: Dict):
        """
        Handle incoming transcript segment
        Perform real-time compliance checking
        """
        try:
            speaker = data.get("speaker", "rep")
            text = data.get("text", "")
            timestamp = data.get("timestamp", datetime.utcnow().timestamp())
            
            logger.debug(f"Processing transcript for {session_id}: {speaker}: {text[:50]}...")
            
            # Store in buffer (sliding window)
            if session_id in self.session_data:
                self.session_data[session_id]["transcript_buffer"].append({
                    "speaker": speaker,
                    "text": text,
                    "timestamp": timestamp,
                })
                
                # Keep only last 10 segments (sliding window for privacy)
                if len(self.session_data[session_id]["transcript_buffer"]) > 10:
                    self.session_data[session_id]["transcript_buffer"].pop(0)
            
            # Check for compliance violations (rep only)
            if speaker == "rep":
                violations = await self.compliance_engine.check_text(text)
                
                if violations:
                    # Send nudges to the client
                    for violation in violations:
                        nudge = {
                            "type": "nudge",
                            "nudge_id": f"{session_id}_{timestamp}",
                            "timestamp": timestamp,
                            "severity": violation["severity"],
                            "icon": self._get_severity_icon(violation["severity"]),
                            "title": violation["rule_name"],
                            "message": violation["message"],
                            "suggested_response": violation.get("suggested_response"),
                            "regulation_reference": violation.get("regulation_reference"),
                        }
                        
                        await self.send_message(session_id, nudge)
                        
                        # Store violation
                        if session_id in self.session_data:
                            self.session_data[session_id]["violations"].append(violation)
            
        except Exception as e:
            logger.error(f"Error handling transcript: {e}")
            await self.send_message(session_id, {
                "type": "error",
                "message": "Failed to process transcript",
            })
    
    def _get_severity_icon(self, severity: str) -> str:
        """Get emoji icon for severity level"""
        icons = {
            "critical": "🛑",
            "warning": "⚠️",
            "info": "💡",
        }
        return icons.get(severity, "ℹ️")
    
    async def get_session_stats(self, session_id: str) -> Dict:
        """Get statistics for a session"""
        if session_id not in self.session_data:
            return {}
        
        data = self.session_data[session_id]
        return {
            "connected_at": data["connected_at"].isoformat(),
            "transcript_segments": len(data["transcript_buffer"]),
            "violations_detected": len(data["violations"]),
            "is_connected": session_id in self.active_connections,
        }


# Global instance
websocket_manager = WebSocketManager()
