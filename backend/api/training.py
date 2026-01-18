"""
Training Mode API
Handles Dr. Doom Simulator and training sessions
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from loguru import logger

from services.training_service import TrainingService
from services.ai_doctor import AIDoctorService

router = APIRouter()


class StartTrainingRequest(BaseModel):
    """Request to start a training session"""
    user_id: str
    difficulty: str = Field(default="intermediate", pattern="^(beginner|intermediate|expert)$")
    scenario_type: str = Field(default="off_label_pressure")
    ai_doctor_personality: str = Field(default="skeptical")


class TrainingSessionResponse(BaseModel):
    """Training session information"""
    session_id: str
    user_id: str
    difficulty: str
    scenario_type: str
    status: str
    created_at: datetime
    audio_url: Optional[str] = None


class TrainingFeedback(BaseModel):
    """Real-time feedback during training"""
    feedback_id: str
    timestamp: float
    message: str
    severity: str  # "info", "warning", "critical"
    suggestion: Optional[str] = None


@router.post("/sessions/start", response_model=TrainingSessionResponse)
async def start_training_session(
    request: StartTrainingRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a new training session with AI Doctor
    """
    try:
        training_service = TrainingService()
        session = await training_service.create_session(
            user_id=request.user_id,
            difficulty=request.difficulty,
            scenario_type=request.scenario_type,
            ai_personality=request.ai_doctor_personality,
        )
        
        # Initialize AI Doctor in background
        background_tasks.add_task(
            training_service.initialize_ai_doctor,
            session["session_id"],
            request.ai_doctor_personality,
        )
        
        logger.info(f"Training session started: {session['session_id']}")
        
        return TrainingSessionResponse(**session)
    
    except Exception as e:
        logger.error(f"Failed to start training session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}", response_model=TrainingSessionResponse)
async def get_training_session(session_id: str):
    """
    Get training session details
    """
    training_service = TrainingService()
    session = await training_service.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return TrainingSessionResponse(**session)


@router.post("/sessions/{session_id}/stop")
async def stop_training_session(session_id: str):
    """
    Stop a training session and generate final report
    """
    training_service = TrainingService()
    result = await training_service.stop_session(session_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session stopped", "session_id": session_id, "report": result}


@router.post("/sessions/{session_id}/ai-speak")
async def trigger_ai_doctor_response(
    session_id: str,
    background_tasks: BackgroundTasks
):
    """
    Trigger AI Doctor to speak (for scenario progression)
    """
    ai_doctor = AIDoctorService()
    
    # Generate response in background
    background_tasks.add_task(
        ai_doctor.generate_response,
        session_id,
    )
    
    return {"message": "AI Doctor is generating response"}


@router.get("/scenarios")
async def get_training_scenarios() -> Dict:
    """
    Get available training scenarios
    """
    return {
        "scenarios": [
            {
                "id": "off_label_pressure",
                "name": "Off-Label Pressure",
                "description": "Doctor aggressively pushes for off-label use",
                "difficulty_range": ["beginner", "intermediate", "expert"],
            },
            {
                "id": "contraindications_quiz",
                "name": "Contraindications Quiz",
                "description": "Doctor asks about contraindications and side effects",
                "difficulty_range": ["beginner", "intermediate"],
            },
            {
                "id": "competitive_pressure",
                "name": "Competitive Pressure",
                "description": "Doctor compares your drug to competitors",
                "difficulty_range": ["intermediate", "expert"],
            },
            {
                "id": "time_pressure",
                "name": "Time Pressure",
                "description": "Doctor is impatient and rushing",
                "difficulty_range": ["beginner", "intermediate", "expert"],
            },
        ]
    }


@router.get("/feedback/history/{session_id}")
async def get_feedback_history(session_id: str) -> List[TrainingFeedback]:
    """
    Get all feedback generated during a training session
    """
    training_service = TrainingService()
    feedback = await training_service.get_feedback_history(session_id)
    
    return [TrainingFeedback(**f) for f in feedback]
