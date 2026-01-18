"""
AI Doctor Service - Generates realistic AI doctor personas for training
Uses ElevenLabs for voice synthesis
"""

from typing import Dict, List, Optional
from loguru import logger
import httpx
import asyncio
from datetime import datetime

from config import settings


class AIDoctorService:
    """
    Generates AI Doctor personas for training mode
    """
    
    def __init__(self):
        self.elevenlabs_api_key = settings.ELEVENLABS_API_KEY
        self.voice_id = settings.DEFAULT_AI_VOICE_ID
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _get_personality_prompt(self, personality: str, difficulty: str) -> str:
        """Generate system prompt based on personality and difficulty"""
        
        base_personalities = {
            "skeptical": "You are a skeptical doctor who questions everything. You've seen too many drug reps make promises that don't pan out. You're particularly wary of off-label uses.",
            "impatient": "You are an extremely busy doctor. You have patients waiting. You want facts, fast. You interrupt frequently and demand quick answers.",
            "friendly_but_tricky": "You are friendly and conversational, but you subtly try to get the rep to make claims they shouldn't. You phrase questions to encourage off-label discussion.",
            "aggressive": "You are aggressive and confrontational. You push hard for off-label uses. You try to bully the rep into making improper claims.",
        }
        
        difficulty_modifiers = {
            "beginner": "Keep your questions straightforward. Give the rep time to think.",
            "intermediate": "Mix easy and hard questions. Occasionally use medical jargon. Try one or two trap questions.",
            "expert": "Use advanced medical terminology. Ask multi-part questions. Frequently try to trap the rep into off-label promotion or exaggerated claims. Reference competitor drugs.",
        }
        
        personality_prompt = base_personalities.get(personality, base_personalities["skeptical"])
        difficulty_prompt = difficulty_modifiers.get(difficulty, difficulty_modifiers["intermediate"])
        
        return f"""{personality_prompt}

{difficulty_prompt}

IMPORTANT RULES:
- You are roleplaying as a doctor talking to a pharmaceutical sales rep
- Try to get the rep to make improper claims (off-label promotion, exaggerated efficacy, downplaying side effects)
- Ask tough questions about side effects, contraindications, and competitor comparisons
- Keep responses under 3 sentences unless asking a complex question
- Respond naturally as if in a real conversation
- Push back on vague answers - demand specifics

Current scenario: The rep is trying to discuss their diabetes medication (GlucoMax) with you."""
    
    async def generate_response(
        self,
        session_id: str,
        conversation_history: List[Dict],
        personality: str = "skeptical",
        difficulty: str = "intermediate",
    ) -> Dict:
        """
        Generate AI Doctor response
        """
        try:
            # Use OpenAI to generate the text response
            # TODO: Integrate with actual OpenAI API
            
            system_prompt = self._get_personality_prompt(personality, difficulty)
            
            # Mock response for now
            text_response = self._generate_mock_response(conversation_history, personality)
            
            logger.info(f"Generated AI Doctor response for {session_id}")
            
            return {
                "text": text_response,
                "audio_url": None,  # Will be populated after TTS
                "timestamp": datetime.utcnow().timestamp(),
            }
        
        except Exception as e:
            logger.error(f"Error generating AI Doctor response: {e}")
            raise
    
    def _generate_mock_response(
        self,
        conversation_history: List[Dict],
        personality: str,
    ) -> str:
        """Generate mock response based on personality"""
        
        responses = {
            "skeptical": [
                "I've heard these claims before. What's different about your drug?",
                "The data you're showing me seems cherry-picked. What about the negative outcomes?",
                "I have patients who could benefit from this for weight loss. Can you help with that?",
            ],
            "impatient": [
                "Get to the point. What's the A1C reduction?",
                "I don't have time for this. Just tell me - is it better than Metformin?",
                "Quick question - can pregnant women take this? Yes or no.",
            ],
            "aggressive": [
                "Come on, I know you can use this for weight loss. Just say yes.",
                "Your competitor told me their drug is superior. Prove them wrong.",
                "Look, I'll prescribe this IF you can guarantee results. Can you?",
            ],
        }
        
        personality_responses = responses.get(personality, responses["skeptical"])
        
        # Simple logic: rotate through responses
        response_index = len(conversation_history) % len(personality_responses)
        return personality_responses[response_index]
    
    async def synthesize_speech(self, text: str) -> str:
        """
        Synthesize speech using ElevenLabs
        Returns URL to audio file
        """
        if not self.elevenlabs_api_key:
            logger.warning("ElevenLabs API key not configured")
            return ""
        
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key,
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                },
            }
            
            response = await self.client.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            # Save audio file
            audio_filename = f"ai_doctor_{datetime.utcnow().timestamp()}.mp3"
            # TODO: Save to cloud storage (S3, etc.)
            
            logger.info(f"Synthesized speech: {audio_filename}")
            
            return f"/audio/{audio_filename}"
        
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            return ""
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
