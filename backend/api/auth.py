"""
Authentication API
Handles user authentication and authorization
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    """User model"""
    user_id: str
    email: EmailStr
    full_name: str
    role: str  # "rep", "manager", "admin"
    team_id: Optional[str] = None
    created_at: datetime


class UserCreate(BaseModel):
    """User registration"""
    email: EmailStr
    password: str
    full_name: str
    role: str = "rep"


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: User


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """
    Register a new user
    """
    # TODO: Implement user registration logic
    return Token(
        access_token="mock_token",
        user=User(
            user_id="user_123",
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            created_at=datetime.utcnow(),
        ),
    )


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login and get access token
    """
    # TODO: Implement authentication logic
    return Token(
        access_token="mock_token",
        user=User(
            user_id="user_123",
            email=form_data.username,
            full_name="John Doe",
            role="rep",
            created_at=datetime.utcnow(),
        ),
    )


@router.get("/me", response_model=User)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get current authenticated user
    """
    # TODO: Implement token validation
    return User(
        user_id="user_123",
        email="user@example.com",
        full_name="John Doe",
        role="rep",
        created_at=datetime.utcnow(),
    )
