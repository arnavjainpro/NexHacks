"""
Token Company Compression Service
Provides text compression to reduce token usage and API costs
"""

import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from loguru import logger

load_dotenv()


class TokenCompressionService:
    def __init__(self):
        self.base_url = os.getenv('TOKEN_COMPANY_BASE_URL', 'https://api.thetokencompany.com/v1')
        self.api_key = os.getenv('TOKEN_COMPANY_API_KEY')
        
        if not self.api_key:
            logger.warning('TOKEN_COMPANY_API_KEY is not set in environment variables')
            self.enabled = False
        else:
            self.enabled = True
            logger.success('Token Company compression service initialized')
    
    def compress(
        self,
        input_text: str,
        aggressiveness: float = 0.5,
        max_output_tokens: Optional[int] = None,
        min_output_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Compress text to reduce token usage
        
        Args:
            input_text: Text to compress
            aggressiveness: 0.0-1.0, default 0.5
                          0.0 = minimal compression (safer)
                          1.0 = maximum compression (more aggressive)
            max_output_tokens: Maximum output tokens
            min_output_tokens: Minimum output tokens
            
        Returns:
            Dictionary with compression results
        """
        if not self.enabled:
            return {
                "success": False,
                "error": "Token Company API key not configured",
                "output": input_text
            }
        
        try:
            logger.info(f"Compressing text with aggressiveness={aggressiveness}")
            
            response = requests.post(
                f"{self.base_url}/compress",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": "bear-1",
                    "compression_settings": {
                        "aggressiveness": aggressiveness,
                        "max_output_tokens": max_output_tokens,
                        "min_output_tokens": min_output_tokens
                    },
                    "input": input_text
                },
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            logger.success(
                f"Compression successful: {data.get('original_input_tokens', 0)} → "
                f"{data.get('output_tokens', 0)} tokens"
            )
            
            return {
                "success": True,
                "data": data,
                "output": data.get("output", input_text)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Token compression error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "output": input_text
            }
    
    def get_compression_stats(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get compression statistics from result"""
        if not result.get('success'):
            return None
        
        data = result.get('data', {})
        original_tokens = data.get('original_input_tokens', 0)
        output_tokens = data.get('output_tokens', 0)
        saved_tokens = original_tokens - output_tokens
        compression_ratio = (saved_tokens / original_tokens * 100) if original_tokens > 0 else 0
        
        return {
            'original_tokens': original_tokens,
            'compressed_tokens': output_tokens,
            'saved_tokens': saved_tokens,
            'compression_ratio': f"{compression_ratio:.2f}%",
            'compression_time': data.get('compression_time', 0)
        }
    
    def is_enabled(self) -> bool:
        """Check if the service is enabled and configured"""
        return self.enabled


# Singleton instance
token_compression_service = TokenCompressionService()
