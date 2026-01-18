"""
API Routers Package
Exports all API routers for the Veritas application
"""

from .training import router as training_router
from .copilot import router as copilot_router
from .analytics import router as analytics_router
from .auth import router as auth_router
from .token_compression import router as token_compression_router

__all__ = [
    "training_router",
    "copilot_router",
    "analytics_router",
    "auth_router",
    "token_compression_router",
]
