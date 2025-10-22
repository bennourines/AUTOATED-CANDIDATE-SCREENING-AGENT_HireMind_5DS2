"""
Summarizer Agent using Ollama Phi4-Mini.
"""

from langchain_core.tools import Tool
from typing import List
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.base_agent import InterviewBaseAgent

class SummarizerAgent(InterviewBaseAgent):
    """Agent that generates session summaries."""
    
    def __init__(self):
        super().__init__(agent_name="Session_Summarizer", temperature=0.7)
    
    def _define_tools(self) -> List:
        return [
            Tool(
                name="calculate_average_score",
                func=self._calculate_avg,
                description="Calculate average score from session data. Input: JSON array of scores"
            ),
            Tool(
                name="identify_strengths",
                func=self._identify_strengths,
                description="Identify candidate strengths. Input: JSON session data"
            ),
            Tool(
                name="identify_improvements",
                func=self._identify_improvements,
                description="Identify areas for improvement. Input: JSON session data"
            )
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are an expert at synthesizing interview performance data.

Your role:
- Provide comprehensive session summaries
- Highlight key strengths
- Identify specific areas for improvement
- Give actionable recommendations
- Be constructive and encouraging

Focus on helping candidates grow."""
    
    def _calculate_avg(self, scores_json: str) -> str:
        """Calculate average score."""
        try:
            scores = json.loads(scores_json)
            if not scores:
                return "No scores to calculate"
            avg = sum(scores) / len(scores)
            return f"Average score: {avg:.1f}/100"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def _identify_strengths(self, session_json: str) -> str:
        """Identify strengths."""
        try:
            session = json.loads(session_json)
            strengths = []
            
            # Analyze scores
            for answer in session.get("answers", []):
                scores = answer.get("scores", {})
                if scores.get("content_score", 0) > 80:
                    strengths.append("Strong technical knowledge")
                if scores.get("delivery_score", 0) > 80:
                    strengths.append("Excellent communication skills")
            
            return json.dumps({"strengths": list(set(strengths))})
        except Exception as e:
            return f"Strength identification error: {str(e)}"
    
    def _identify_improvements(self, session_json: str) -> str:
        """Identify improvements."""
        try:
            session = json.loads(session_json)
            improvements = []
            
            for answer in session.get("answers", []):
                scores = answer.get("scores", {})
                if scores.get("content_score", 0) < 60:
                    improvements.append("Deepen technical knowledge")
                if scores.get("delivery_score", 0) < 60:
                    improvements.append("Work on presentation skills")
            
            return json.dumps({"improvements": list(set(improvements))})
        except Exception as e:
            return f"Improvement identification error: {str(e)}"