"""
Answer Evaluator Agent using Ollama Phi4-Mini.
"""

from langchain.tools import Tool, StructuredTool
from typing import List, Dict
from pydantic import BaseModel, Field
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../../services/interview_simulator'))

from evaluator import answer_evaluator
from ..core.base_agent import InterviewBaseAgent

class EvaluationInput(BaseModel):
    """Input schema for evaluation."""
    question: str = Field(description="The interview question asked")
    transcript: str = Field(description="Candidate's answer transcript")
    metrics_json: str = Field(description="JSON string of prosody/stress metrics")

class EvaluatorAgent(InterviewBaseAgent):
    """Agent that evaluates answers comprehensively."""
    
    def __init__(self):
        super().__init__(agent_name="Evaluator", temperature=0.6)
    
    def _define_tools(self) -> List:
        return [
            StructuredTool.from_function(
                func=self._evaluate,
                name="evaluate_answer",
                description="Comprehensively evaluate answer quality with all metrics",
                args_schema=EvaluationInput
            ),
            Tool(
                name="generate_feedback",
                func=self._generate_feedback,
                description="Generate personalized feedback for improvement. Input: JSON evaluation result"
            ),
            Tool(
                name="compare_to_ideal_answer",
                func=self._compare_ideal,
                description="Compare candidate answer to ideal answer. Input: 'candidate_answer|ideal_answer'"
            )
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are a senior technical interviewer and evaluator.

Your evaluation criteria:
- Content relevance (40%): Does it answer the question?
- Technical accuracy (30%): Is the information correct?
- Communication clarity (20%): Well-structured and articulate?
- Delivery (10%): Confidence, pace, engagement

Provide constructive, actionable feedback that helps candidates improve."""
    
    def _evaluate(self, question: str, transcript: str, metrics_json: str) -> str:
        """Evaluate answer with all metrics."""
        try:
            metrics = json.loads(metrics_json)
            
            result = answer_evaluator.evaluate_answer(
                question=question,
                transcript=transcript,
                **metrics
            )
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Evaluation error: {str(e)}"
    
    def _generate_feedback(self, evaluation_json: str) -> str:
        """Generate detailed feedback."""
        try:
            evaluation = json.loads(evaluation_json)
            feedback = []
            
            # Content feedback
            content_score = evaluation.get("scores", {}).get("content_score", 0)
            if content_score < 60:
                feedback.append("Work on providing more relevant and complete answers")
            elif content_score > 85:
                feedback.append("Excellent content coverage!")
            
            # Delivery feedback
            delivery_score = evaluation.get("scores", {}).get("delivery_score", 0)
            if delivery_score < 60:
                feedback.append("Focus on improving speech pace and reducing hesitations")
            
            return "\n".join(feedback) if feedback else "Good performance overall"
            
        except Exception as e:
            return f"Feedback generation error: {str(e)}"
    
    def _compare_ideal(self, input_str: str) -> str:
        """Compare to ideal answer."""
        try:
            parts = input_str.split("|")
            if len(parts) != 2:
                return "Error: Input format should be 'candidate_answer|ideal_answer'"
            
            candidate, ideal = parts
            
            # Simple similarity check (can be enhanced with embeddings)
            candidate_words = set(candidate.lower().split())
            ideal_words = set(ideal.lower().split())
            
            overlap = len(candidate_words & ideal_words)
            similarity = overlap / max(len(ideal_words), 1) * 100
            
            return f"Similarity to ideal answer: {similarity:.1f}%"
            
        except Exception as e:
            return f"Comparison error: {str(e)}"