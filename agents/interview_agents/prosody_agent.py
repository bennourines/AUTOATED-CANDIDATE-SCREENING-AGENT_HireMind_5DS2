"""
Prosody Analysis Agent using Ollama Phi4-Mini.
"""

from langchain_core.tools import tool
from typing import List
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.interview_simulator.prosody_analyzer import prosody_analyzer
from core.base_agent import InterviewBaseAgent

class ProsodyAgent(InterviewBaseAgent):
    """Agent specialized in voice pattern analysis."""
    
    def __init__(self):
        super().__init__(
            agent_name="Prosody_Analyst",
            temperature=0.5
        )
    
    def _define_tools(self) -> List:
        """Define tools using @tool decorator."""
        
        @tool
        def analyze_prosody(audio_path: str) -> str:
            """
            Analyze voice patterns including pace, pitch, and pauses.
            
            Args:
                audio_path: Path to audio file
            
            Returns:
                Prosody analysis results
            """
            try:
                metrics = prosody_analyzer.analyze_audio(audio_path)
                
                result = f"""
Prosody Analysis:
- Speech Rate: {metrics.get('speech_rate', 0):.1f} words/min
- Pitch (Mean): {metrics.get('pitch_mean', 0):.1f} Hz
- Pitch (Std): {metrics.get('pitch_std', 0):.1f} Hz
- Energy (Mean): {metrics.get('energy_mean', 0):.3f}
- Pause Count: {metrics.get('pause_count', 0)}
- Pause Duration: {metrics.get('pause_duration', 0):.2f} seconds

Interpretation:
- Speaking Pace: {'Fast' if metrics.get('speech_rate', 0) > 160 else 'Normal' if metrics.get('speech_rate', 0) > 120 else 'Slow'}
- Confidence: {'High' if metrics.get('pitch_std', 0) > 30 else 'Moderate' if metrics.get('pitch_std', 0) > 15 else 'Low'}
- Hesitation: {'High' if metrics.get('pause_count', 0) > 10 else 'Moderate' if metrics.get('pause_count', 0) > 5 else 'Low'}
                """
                
                return result.strip()
                
            except Exception as e:
                return f"Prosody analysis error: {str(e)}"
        
        @tool
        def detect_stress_patterns(audio_path: str) -> str:
            """Detect stress/anxiety patterns in voice."""
            try:
                metrics = prosody_analyzer.analyze_audio(audio_path)
                
                pitch_variance = metrics.get('pitch_std', 0)
                pause_count = metrics.get('pause_count', 0)
                
                if pitch_variance > 40 and pause_count > 12:
                    return "⚠️ HIGH STRESS: Significant vocal stress detected"
                elif pitch_variance > 25 or pause_count > 8:
                    return "🟡 MODERATE STRESS: Some stress indicators present"
                else:
                    return "✅ LOW STRESS: Candidate appears calm"
                    
            except Exception as e:
                return f"Stress detection error: {str(e)}"
        
        return [analyze_prosody, detect_stress_patterns]
    
    def _get_system_prompt(self) -> str:
        return """You are a Voice Pattern Analysis specialist.

Your expertise:
- Speech rate and fluency analysis
- Pitch variation and confidence detection
- Pause pattern interpretation
- Stress and anxiety identification

Interpret prosody metrics to assess:
- Communication confidence
- Stress levels
- Speaking clarity
- Overall delivery quality"""