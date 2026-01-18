"""
Copilot Service - Manages live copilot sessions
"""

from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime
import uuid

from config import settings


class CopilotService:
    """
    Manages live copilot sessions during real sales calls
    """
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    async def create_session(
        self,
        user_id: str,
        rep_name: str,
        doctor_specialty: Optional[str],
        product_focus: str,
        call_type: str,
    ) -> Dict:
        """Create a new copilot session"""
        
        session_id = str(uuid.uuid4())
        
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "rep_name": rep_name,
            "doctor_specialty": doctor_specialty,
            "product_focus": product_focus,
            "call_type": call_type,
            "status": "active",
            "started_at": datetime.utcnow(),
            "websocket_url": f"ws://localhost:8000/ws/{session_id}",
            "transcript": [],
            "nudges": [],
            "context": {},
        }
        
        self.sessions[session_id] = session
        logger.info(f"Created copilot session: {session_id}")
        
        return session
    
    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session details"""
        return self.sessions.get(session_id)
    
    async def stop_session(self, session_id: str) -> Optional[Dict]:
        """Stop a copilot session"""
        
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        session["status"] = "completed"
        session["ended_at"] = datetime.utcnow()
        
        # Trigger analytics generation
        analytics_id = await self._trigger_analytics(session)
        
        # Clean up session data (privacy)
        await self._cleanup_session_data(session_id)
        
        logger.info(f"Copilot session stopped: {session_id}")
        
        return {
            "analytics_id": analytics_id,
            "session_id": session_id,
        }
    
    async def get_nudges(self, session_id: str) -> List[Dict]:
        """Get all nudges for a session"""
        
        if session_id not in self.sessions:
            return []
        
        return self.sessions[session_id].get("nudges", [])
    
    async def update_context(self, session_id: str, context: Dict):
        """Update session context"""
        
        if session_id in self.sessions:
            self.sessions[session_id]["context"].update(context)
            logger.debug(f"Updated context for session {session_id}")
    
    async def _trigger_analytics(self, session: Dict) -> str:
        """Trigger analytics generation for completed session"""
        
        from services.analytics_service import AnalyticsService
        
        analytics_service = AnalyticsService()
        analytics_id = await analytics_service.create_analytics(session)
        
        return analytics_id
    
    async def _cleanup_session_data(self, session_id: str):
        """Clean up sensitive session data (privacy-first)"""
        
        if session_id in self.sessions:
            # Clear transcript and audio data
            self.sessions[session_id]["transcript"] = []
            logger.info(f"Cleaned up session data for {session_id} (privacy)")


class AudioProcessor:
    """
    Processes audio for transcription
    """
    
    def __init__(self):
        self.sample_rate = settings.AUDIO_SAMPLE_RATE
    
    async def process_audio_chunk(self, audio_data: bytes) -> str:
        """
        Process audio chunk and return transcription
        In production, this would use Wispr Flow or Deepgram
        """
        
        # TODO: Implement actual audio processing
        # For now, return empty string
        return ""
    
    async def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribe audio file
        """
        
        # TODO: Implement transcription using Whisper or Deepgram
        return ""
