"""
Analytics API
Handles post-call analytics and Safety Scorecard generation
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger

from services.analytics_service import AnalyticsService

router = APIRouter()


class SafetyScorecard(BaseModel):
    """Safety Scorecard for a completed session"""
    session_id: str
    user_id: str
    rep_name: str
    session_type: str  # "training" or "live"
    compliance_score: float = Field(ge=0, le=100)
    duration_seconds: int
    violations_prevented: int
    total_nudges: int
    created_at: datetime
    
    # Detailed metrics
    metrics: Dict = {
        "accuracy": 0.0,
        "response_quality": 0.0,
        "confidence": 0.0,
        "compliance_consistency": 0.0,
    }
    
    # Key moments
    saved_moments: List[Dict] = []
    
    # Areas for improvement
    improvement_areas: List[Dict] = []


class SessionSummary(BaseModel):
    """Summary statistics for a session"""
    total_violations_detected: int
    violations_by_category: Dict[str, int]
    average_response_time: float
    compliance_score: float
    risk_level: str  # "low", "medium", "high"


@router.get("/scorecard/{session_id}", response_model=SafetyScorecard)
async def get_safety_scorecard(session_id: str):
    """
    Get the Safety Scorecard for a completed session
    """
    analytics_service = AnalyticsService()
    scorecard = await analytics_service.generate_scorecard(session_id)
    
    if not scorecard:
        raise HTTPException(status_code=404, detail="Session not found or not completed")
    
    return SafetyScorecard(**scorecard)


@router.get("/user/{user_id}/history")
async def get_user_session_history(
    user_id: str,
    limit: int = 50,
    offset: int = 0,
    session_type: Optional[str] = None,
):
    """
    Get session history for a user
    """
    analytics_service = AnalyticsService()
    sessions = await analytics_service.get_user_history(
        user_id=user_id,
        limit=limit,
        offset=offset,
        session_type=session_type,
    )
    
    return {
        "sessions": sessions,
        "total": len(sessions),
    }


@router.get("/user/{user_id}/progress")
async def get_user_progress(user_id: str):
    """
    Get user's progress over time
    Shows improvement trends in compliance scores
    """
    analytics_service = AnalyticsService()
    progress = await analytics_service.get_user_progress(user_id)
    
    return {
        "user_id": user_id,
        "progress": progress,
    }


@router.get("/session/{session_id}/summary", response_model=SessionSummary)
async def get_session_summary(session_id: str):
    """
    Get quick summary statistics for a session
    """
    analytics_service = AnalyticsService()
    summary = await analytics_service.get_session_summary(session_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionSummary(**summary)


@router.get("/team/leaderboard")
async def get_team_leaderboard(
    team_id: Optional[str] = None,
    time_period: str = "week",  # "week", "month", "quarter"
):
    """
    Get team leaderboard showing top performers
    """
    analytics_service = AnalyticsService()
    leaderboard = await analytics_service.get_leaderboard(
        team_id=team_id,
        time_period=time_period,
    )
    
    return {
        "time_period": time_period,
        "leaderboard": leaderboard,
    }


@router.get("/compliance/violations")
async def get_violation_trends(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    team_id: Optional[str] = None,
):
    """
    Get violation trends over time
    Useful for identifying systemic training gaps
    """
    analytics_service = AnalyticsService()
    trends = await analytics_service.get_violation_trends(
        start_date=start_date,
        end_date=end_date,
        team_id=team_id,
    )
    
    return {
        "trends": trends,
        "insights": await analytics_service.generate_insights(trends),
    }


@router.post("/session/{session_id}/export")
async def export_session_report(
    session_id: str,
    format: str = "pdf",  # "pdf", "json", "csv"
):
    """
    Export session report in various formats
    """
    analytics_service = AnalyticsService()
    
    if format not in ["pdf", "json", "csv"]:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    report_url = await analytics_service.export_report(session_id, format)
    
    return {
        "session_id": session_id,
        "format": format,
        "download_url": report_url,
    }
