"""
Speech-to-Text Agent using Ollama Phi4-Mini.
"""

from langchain.tools import Tool
from typing import List
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../services/interview_simulator'))

from stt_handler import stt_handler
from ..core.base_agent import InterviewBaseAgent

class STTAgent(InterviewBaseAgent):
    """Agent specialized in audio transcription."""
    
    def __init__(self):
        super().__init__(
            agent_name="STT_Specialist",
            temperature=0.3  # Lower temp for accuracy
        )
    
    def _define_tools(self) -> List:
        return [
            Tool(
                name="transcribe_audio",
                func=self._transcribe,
                description="Transcribe audio file to text using Vosk. Input: audio file path"
            ),
            Tool(
                name="extract_audio_from_video",
                func=self._extract_audio,
                description="Extract audio track from video file. Input: video file path"
            ),
            Tool(
                name="validate_audio_quality",
                func=self._validate_audio,
                description="Check if audio quality is sufficient for transcription. Input: audio file path"
            )
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are a Speech-to-Text specialist agent.

Your responsibilities:
- Extract audio from video if needed
- Transcribe speech accurately using Vosk
- Handle multiple languages if detected
- Flag low-quality audio
- Clean and format transcripts

Always validate audio quality before transcription."""
    
    def _transcribe(self, audio_path: str) -> str:
        """Transcribe audio file."""
        try:
            transcript = stt_handler.transcribe_audio(audio_path)
            return transcript if transcript else "No speech detected"
        except Exception as e:
            return f"Transcription error: {str(e)}"
    
    def _extract_audio(self, video_path: str) -> str:
        """Extract audio from video."""
        try:
            audio_path = stt_handler.extract_audio_from_video(video_path)
            return f"Audio extracted to: {audio_path}"
        except Exception as e:
            return f"Extraction error: {str(e)}"
    
    def _validate_audio(self, audio_path: str) -> str:
        """Validate audio quality."""
        # Basic validation - can be enhanced
        try:
            import os
            if not os.path.exists(audio_path):
                return "Audio file not found"
            
            file_size = os.path.getsize(audio_path)
            if file_size < 1000:
                return "Audio quality: TOO SHORT - file may be corrupted"
            elif file_size > 100_000_000:
                return "Audio quality: FILE TOO LARGE - may take long to process"
            else:
                return "Audio quality: ACCEPTABLE - ready for transcription"
        except Exception as e:
            return f"Validation error: {str(e)}"