"""
Veritas Services Package
"""

from .compliance_engine import ComplianceEngine
from .websocket_manager import websocket_manager
from .ai_doctor import AIDoctorService
from .training_service import TrainingService
from .copilot_service import CopilotService
from .analytics_service import AnalyticsService

__all__ = [
    "ComplianceEngine",
    "websocket_manager",
    "AIDoctorService",
    "TrainingService",
    "CopilotService",
    "AnalyticsService",
]
