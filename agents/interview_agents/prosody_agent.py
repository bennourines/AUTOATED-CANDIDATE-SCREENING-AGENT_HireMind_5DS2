"""
Prosody Analyzer Agent using Ollama Phi4-Mini.
"""

from langchain.tools import Tool
from typing import List, Dict
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../../services/interview_simulator'))

from prosody_analyzer import prosody_analyzer
from stress_analyzer import stress_analyzer
from ..core.base_agent import InterviewBaseAgent

class ProsodyAgent(InterviewBaseAgent):
    """Agent specialized in voice prosody and stress analysis."""
    
    def __init__(self):
        super().__init__(agent_name="Prosody_Analyst", temperature=0.4)
    
    def _define_tools(self) -> List:
        return [
            Tool(
                name="analyze_prosody",
                func=self._analyze_prosody,
                description="Analyze speech prosody: pace, pitch, pauses, articulation. Input: 'audio_path|transcript'"
            ),
            Tool(
                name="analyze_stress",
                func=self._analyze_stress,
                description="Detect voice stress indicators. Input: audio file path"
            ),
            Tool(
                name="interpret_prosody",
                func=self._interpret,
                description="Provide human-readable interpretation of prosody metrics. Input: JSON metrics string"
            )
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are a voice prosody analysis expert.

Your expertise:
- Detect speech rate anomalies (too fast = nervous, too slow = uncertain)
- Identify hesitations and filler words
- Measure vocal confidence through pitch variation
- Detect stress through voice micro-tremors

Provide actionable feedback on speaking style."""
    
    def _analyze_prosody(self, input_str: str) -> str:
        """Analyze prosody metrics."""
        try:
            parts = input_str.split("|")
            if len(parts) != 2:
                return "Error: Input format should be 'audio_path|transcript'"
            
            audio_path, transcript = parts
            result = prosody_analyzer.analyze(audio_path, transcript)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Prosody analysis error: {str(e)}"
    
    def _analyze_stress(self, audio_path: str) -> str:
        """Analyze voice stress."""
        try:
            result = stress_analyzer.analyze(audio_path)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Stress analysis error: {str(e)}"
    
    def _interpret(self, metrics_json: str) -> str:
        """Interpret prosody metrics for feedback."""
        try:
            metrics = json.loads(metrics_json)
            
            interpretation = []
            
            # Speech rate
            if "speech_rate" in metrics:
                rate = metrics["speech_rate"]
                if rate > 3.5:
                    interpretation.append("Speaking very fast - may indicate nervousness")
                elif rate < 1.5:
                    interpretation.append("Speaking slowly - may indicate uncertainty")
                else:
                    interpretation.append("Speech rate is good")
            
            # Pauses
            if "num_pauses" in metrics:
                pauses = metrics["num_pauses"]
                if pauses > 10:
                    interpretation.append("Many pauses - may need to improve fluency")
            
            return "\n".join(interpretation) if interpretation else "Prosody metrics are within normal range"
            
        except Exception as e:
            return f"Interpretation error: {str(e)}"