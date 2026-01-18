"""
Token Compression API Endpoints
Provides compression capabilities for reducing API costs
"""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional
from loguru import logger

from services.token_compression import token_compression_service


router = APIRouter()


class CompressRequest(BaseModel):
    """Request model for text compression"""
    input: str = Field(..., description="Text to compress", min_length=1)
    aggressiveness: float = Field(
        0.5,
        description="Compression level (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    max_output_tokens: Optional[int] = Field(None, description="Maximum output tokens")
    min_output_tokens: Optional[int] = Field(None, description="Minimum output tokens")


class CompressResponse(BaseModel):
    """Response model for text compression"""
    success: bool
    output: str
    stats: Optional[dict] = None
    error: Optional[str] = None


@router.post("/compress", response_model=CompressResponse)
async def compress_text(request: CompressRequest):
    """
    Compress text to reduce token usage
    
    - **input**: Text to compress
    - **aggressiveness**: Compression level (0.0 = minimal, 1.0 = maximum)
    - **max_output_tokens**: Optional maximum output tokens
    - **min_output_tokens**: Optional minimum output tokens
    
    Returns compressed text and compression statistics
    """
    try:
        result = token_compression_service.compress(
            input_text=request.input,
            aggressiveness=request.aggressiveness,
            max_output_tokens=request.max_output_tokens,
            min_output_tokens=request.min_output_tokens
        )
        
        stats = token_compression_service.get_compression_stats(result)
        
        return CompressResponse(
            success=result['success'],
            output=result['output'],
            stats=stats,
            error=result.get('error')
        )
    
    except Exception as e:
        logger.error(f"Error in compress endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Compression failed: {str(e)}"
        )


@router.get("/status")
async def get_status():
    """
    Check Token Company compression service status
    
    Returns whether the service is enabled and configured
    """
    is_enabled = token_compression_service.is_enabled()
    
    return {
        "service": "Token Company Compression",
        "enabled": is_enabled,
        "status": "active" if is_enabled else "inactive",
        "message": "Service is ready" if is_enabled else "API key not configured"
    }


@router.post("/compress/demo")
async def demo_compression():
    """
    Demo endpoint showing compression at different aggressiveness levels
    
    Returns compression results for the same text at various levels
    """
    demo_text = "How many stars are there in the galaxy? This is a fascinating question that astronomers have been trying to answer for centuries."
    
    results = []
    for aggressiveness in [0.3, 0.5, 0.7]:
        result = token_compression_service.compress(
            input_text=demo_text,
            aggressiveness=aggressiveness
        )
        
        stats = token_compression_service.get_compression_stats(result)
        
        results.append({
            "aggressiveness": aggressiveness,
            "output": result['output'],
            "stats": stats,
            "success": result['success']
        })
    
    return {
        "original": demo_text,
        "results": results
    }
