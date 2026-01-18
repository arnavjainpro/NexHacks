"""
Training Service - Handles training session management
"""

from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime
import uuid

from services.ai_doctor import AIDoctorService


class TrainingService:
    """
    Manages training sessions with AI Doctor
    """
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.ai_doctor = AIDoctorService()
    
    async def create_session(
        self,
        user_id: str,
        difficulty: str,
        scenario_type: str,
        ai_personality: str,
    ) -> Dict:
        """Create a new training session"""
        
        session_id = str(uuid.uuid4())
        
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "difficulty": difficulty,
            "scenario_type": scenario_type,
            "ai_personality": ai_personality,
            "status": "active",
            "created_at": datetime.utcnow(),
            "conversation_history": [],
            "feedback_history": [],
        }
        
        self.sessions[session_id] = session
        logger.info(f"Created training session: {session_id}")
        
        return session
    
    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session details"""
        return self.sessions.get(session_id)
    
    async def stop_session(self, session_id: str) -> Optional[Dict]:
        """Stop a training session and generate report"""
        
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        session["status"] = "completed"
        session["ended_at"] = datetime.utcnow()
        
        # Generate final report
        report = await self._generate_session_report(session)
        
        logger.info(f"Training session stopped: {session_id}")
        
        return report
    
    async def initialize_ai_doctor(
        self,
        session_id: str,
        personality: str,
    ):
        """Initialize AI Doctor for a session"""
        
        if session_id not in self.sessions:
            logger.error(f"Session not found: {session_id}")
            return
        
        session = self.sessions[session_id]
        
        # Generate initial greeting
        greeting = await self.ai_doctor.generate_response(
            session_id=session_id,
            conversation_history=[],
            personality=personality,
            difficulty=session["difficulty"],
        )
        
        session["conversation_history"].append({
            "speaker": "ai_doctor",
            "text": greeting["text"],
            "timestamp": greeting["timestamp"],
        })
        
        logger.info(f"AI Doctor initialized for session: {session_id}")
    
    async def get_feedback_history(self, session_id: str) -> List[Dict]:
        """Get feedback history for a session"""
        
        if session_id not in self.sessions:
            return []
        
        return self.sessions[session_id].get("feedback_history", [])
    
    async def _generate_session_report(self, session: Dict) -> Dict:
        """Generate final report for training session"""
        
        # Calculate metrics
        total_violations = len([
            f for f in session.get("feedback_history", [])
            if f.get("severity") in ["warning", "critical"]
        ])
        
        total_turns = len(session.get("conversation_history", []))
        
        return {
            "session_id": session["session_id"],
            "duration_seconds": (
                (session.get("ended_at", datetime.utcnow()) - session["created_at"]).total_seconds()
            ),
            "total_turns": total_turns,
            "violations_detected": total_violations,
            "score": max(0, 100 - (total_violations * 10)),
            "feedback": session.get("feedback_history", []),
        }


class ComplianceChecker:
    """
    Compliance checking for live copilot mode
    """
    
    def __init__(self):
        from services.compliance_engine import ComplianceEngine
        self.engine = ComplianceEngine()
    
    async def check_transcript(
        self,
        session_id: str,
        speaker: str,
        text: str,
        timestamp: float,
    ) -> List[Dict]:
        """
        Check transcript for compliance issues
        Returns list of nudges to display
        """
        
        # Only check rep's speech
        if speaker != "rep":
            return []
        
        violations = await self.engine.check_text(text)
        
        # Convert violations to nudges
        nudges = []
        for violation in violations:
            nudge = {
                "nudge_id": f"{session_id}_{timestamp}",
                "timestamp": timestamp,
                "severity": violation["severity"],
                "icon": self._get_icon(violation["severity"]),
                "title": violation["rule_name"],
                "message": violation["message"],
                "suggested_response": violation.get("suggested_response"),
                "regulation_reference": violation.get("regulation_reference"),
            }
            nudges.append(nudge)
        
        return nudges
    
    def _get_icon(self, severity: str) -> str:
        """Get icon for severity"""
        icons = {
            "critical": "🛑",
            "warning": "⚠️",
            "info": "💡",
        }
        return icons.get(severity, "ℹ️")
