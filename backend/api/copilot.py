"""
Live Copilot API
Handles real-time compliance monitoring during live sales calls
"""

from fastapi import APIRouter, HTTPException, WebSocket
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from loguru import logger

from services.copilot_service import CopilotService
from services.compliance_checker import ComplianceChecker

router = APIRouter()


class StartCopilotRequest(BaseModel):
    """Request to start a live copilot session"""
    user_id: str
    rep_name: str
    doctor_specialty: Optional[str] = None
    product_focus: str
    call_type: str = Field(default="in_person")  # "in_person", "virtual", "phone"


class CopilotSessionResponse(BaseModel):
    """Copilot session information"""
    session_id: str
    user_id: str
    rep_name: str
    product_focus: str
    status: str
    started_at: datetime
    websocket_url: str


class ComplianceNudge(BaseModel):
    """Real-time compliance nudge"""
    nudge_id: str
    timestamp: float
    severity: str  # "info", "warning", "critical"
    icon: str  # "💡", "⚠️", "🛑"
    title: str
    message: str
    suggested_response: Optional[str] = None
    regulation_reference: Optional[str] = None


class TranscriptSegment(BaseModel):
    """Transcript segment for processing"""
    speaker: str  # "rep" or "doctor"
    text: str
    timestamp: float
    confidence: float = 1.0


@router.post("/sessions/start", response_model=CopilotSessionResponse)
async def start_copilot_session(request: StartCopilotRequest):
    """
    Start a new live copilot session
    Returns WebSocket URL for real-time communication
    """
    try:
        copilot_service = CopilotService()
        session = await copilot_service.create_session(
            user_id=request.user_id,
            rep_name=request.rep_name,
            doctor_specialty=request.doctor_specialty,
            product_focus=request.product_focus,
            call_type=request.call_type,
        )
        
        logger.info(f"Copilot session started: {session['session_id']}")
        
        return CopilotSessionResponse(**session)
    
    except Exception as e:
        logger.error(f"Failed to start copilot session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}")
async def get_copilot_session(session_id: str):
    """
    Get copilot session details
    """
    copilot_service = CopilotService()
    session = await copilot_service.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session


@router.post("/sessions/{session_id}/stop")
async def stop_copilot_session(session_id: str):
    """
    Stop a copilot session and trigger analytics generation
    """
    copilot_service = CopilotService()
    result = await copilot_service.stop_session(session_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "message": "Session stopped",
        "session_id": session_id,
        "analytics_id": result.get("analytics_id"),
    }


@router.post("/sessions/{session_id}/process-transcript")
async def process_transcript(
    session_id: str,
    segment: TranscriptSegment
):
    """
    Process a transcript segment for real-time compliance checking
    Returns any compliance nudges that should be displayed
    """
    try:
        compliance_checker = ComplianceChecker()
        
        # Check for compliance issues
        nudges = await compliance_checker.check_transcript(
            session_id=session_id,
            speaker=segment.speaker,
            text=segment.text,
            timestamp=segment.timestamp,
        )
        
        if nudges:
            logger.warning(f"Compliance issues detected in session {session_id}")
        
        return {
            "nudges": [ComplianceNudge(**n) for n in nudges],
            "processed": True,
        }
    
    except Exception as e:
        logger.error(f"Error processing transcript: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}/nudges")
async def get_session_nudges(session_id: str) -> List[ComplianceNudge]:
    """
    Get all nudges generated during a session
    """
    copilot_service = CopilotService()
    nudges = await copilot_service.get_nudges(session_id)
    
    return [ComplianceNudge(**n) for n in nudges]


@router.post("/sessions/{session_id}/context")
async def update_session_context(
    session_id: str,
    context: Dict
):
    """
    Update session context (e.g., product being discussed, doctor concerns)
    This helps the compliance engine provide more accurate guidance
    """
    copilot_service = CopilotService()
    await copilot_service.update_context(session_id, context)
    
    return {"message": "Context updated", "session_id": session_id}


@router.get("/products")
async def get_available_products() -> List[Dict]:
    """
    Get available products and their compliance rules
    """
    return [
        {
            "id": "glucomax",
            "name": "GlucoMax",
            "indication": "Type 2 Diabetes Management",
            "off_label_concerns": ["weight loss", "PCOS", "prediabetes"],
            "key_warnings": [
                "Not approved for Type 1 diabetes",
                "Contraindicated in severe renal impairment",
                "Risk of hypoglycemia when combined with insulin",
            ],
        },
        {
            "id": "cardioguard",
            "name": "CardioGuard",
            "indication": "Hypertension",
            "off_label_concerns": ["heart failure", "atrial fibrillation"],
            "key_warnings": [
                "Not for use in pregnancy",
                "Monitor potassium levels",
                "May cause dizziness",
            ],
        },
    ]
