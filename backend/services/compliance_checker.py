"""
Compliance Checker Service
Wrapper around compliance engine for real-time checking
"""

from typing import List, Dict
from loguru import logger

from services.compliance_engine import ComplianceEngine


class ComplianceChecker:
    """
    Compliance checking for live copilot mode
    Wrapper around the compliance engine
    """
    
    def __init__(self):
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
