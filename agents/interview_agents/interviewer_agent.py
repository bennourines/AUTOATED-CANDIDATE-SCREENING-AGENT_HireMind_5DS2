"""
Interviewer Agent using Ollama Phi4-Mini.
"""

from langchain.tools import Tool, StructuredTool
from typing import List, Dict
from pydantic import BaseModel, Field
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../services/interview_simulator'))

from qa_bank import question_bank
from ..core.base_agent import InterviewBaseAgent

class QuestionInput(BaseModel):
    """Input schema for question selection."""
    categories: str = Field(description="Comma-separated job categories (e.g., 'Python,Backend')")
    difficulty: str = Field(description="Question difficulty: easy, medium, or hard")
    performance: str = Field(description="Current candidate performance: struggling, average, or excellent")

class InterviewerAgent(InterviewBaseAgent):
    """Agent that selects interview questions intelligently using Phi4-Mini."""
    
    def __init__(self):
        super().__init__(
            agent_name="Interview_Coordinator",
            temperature=0.8  # More creative for question selection
        )
    
    def _define_tools(self) -> List:
        return [
            StructuredTool.from_function(
                func=self._select_question,
                name="select_interview_question",
                description="Select an appropriate interview question based on categories, difficulty, and candidate performance",
                args_schema=QuestionInput
            ),
            Tool(
                name="get_question_by_id",
                func=self._get_question_details,
                description="Retrieve full question details by question ID (integer)"
            ),
            Tool(
                name="adjust_difficulty_level",
                func=self._recommend_difficulty,
                description="Recommend difficulty adjustment based on performance description"
            )
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are an experienced technical interviewer with 10+ years of experience.

Your responsibilities:
1. Select appropriate questions based on candidate's profile and performance
2. Adapt difficulty dynamically:
   - If candidate is struggling (score < 60%): Choose easier questions
   - If candidate is average (60-85%): Maintain current difficulty
   - If candidate excels (score > 85%): Increase difficulty
3. Ensure natural interview flow and variety
4. Match questions to job requirements

Always use your tools to make data-driven decisions."""
    
    def _select_question(
        self,
        categories: str,
        difficulty: str,
        performance: str
    ) -> str:
        """Select next question based on context."""
        # Parse categories
        category_list = [c.strip() for c in categories.split(",")]
        
        # Adjust difficulty based on performance
        if "struggling" in performance.lower() or "poor" in performance.lower():
            difficulty = "easy"
        elif "excellent" in performance.lower() or "great" in performance.lower():
            difficulty = "hard"
        
        # Get question from bank
        questions = question_bank.get_random_questions(
            num_questions=1,
            categories=category_list,
            difficulty=difficulty
        )
        
        if questions:
            q = questions[0]
            return f"Question ID {q['id']}: {q['question']}\nIdeal Answer: {q['ideal_answer'][:100]}..."
        
        return "No suitable question found. Try different criteria."
    
    def _get_question_details(self, question_id: str) -> str:
        """Get question by ID."""
        try:
            qid = int(question_id)
            question = question_bank.get_question_by_id(qid)
            if question:
                return f"ID: {question['id']}\nQuestion: {question['question']}\nCategory: {question['category']}\nDifficulty: {question['difficulty']}"
            return f"Question ID {question_id} not found"
        except ValueError:
            return "Invalid question ID format. Must be an integer."
    
    def _recommend_difficulty(self, performance_desc: str) -> str:
        """Recommend difficulty adjustment."""
        if any(word in performance_desc.lower() for word in ["struggling", "poor", "weak", "difficulty"]):
            return "Recommend: DECREASE difficulty to 'easy' to build confidence"
        elif any(word in performance_desc.lower() for word in ["excellent", "great", "strong", "perfect"]):
            return "Recommend: INCREASE difficulty to 'hard' to challenge further"
        else:
            return "Recommend: MAINTAIN current difficulty level"