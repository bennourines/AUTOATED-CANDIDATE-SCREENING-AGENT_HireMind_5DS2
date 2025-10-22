"""
Question Bank Manager.

Loads and manages interview questions from JSON file.
Provides filtering by category, difficulty, and random selection.
"""

import json
import random
from pathlib import Path
from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)

class QuestionBank:
    """
    Manages the interview question database.
    
    This class loads questions from JSON and provides methods to:
    - Get questions by category/difficulty
    - Get random questions for a session
    - Retrieve specific questions by ID
    """
    
    def __init__(self, qa_bank_path: str = "data/qa_bank.json"):
        """
        Initialize question bank from JSON file.
        
        Args:
            qa_bank_path: Path to JSON file with questions
        """
        self.qa_bank_path = Path(qa_bank_path)
        self.questions: List[Dict] = []
        self.metadata: Dict = {}
        
        self._load_questions()
    
    def _load_questions(self):
        """
        Load questions from JSON file.
        
        If file doesn't exist, create it using the script.
        """
        if not self.qa_bank_path.exists():
            logger.warning(f"Q&A bank not found at {self.qa_bank_path}")
            logger.info("Creating default question bank...")
            
            # Create parent directory
            self.qa_bank_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Run the create_qa_bank script
            from agents.scripts.create_qa_bank import create_qa_bank
            create_qa_bank()
        
        # Load JSON
        with open(self.qa_bank_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.questions = data.get("questions", [])
        self.metadata = data.get("metadata", {})
        
        logger.info(f"Loaded {len(self.questions)} questions from {self.qa_bank_path}")
    
    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        """
        Retrieve a specific question by ID.
        
        Args:
            question_id: Question ID to retrieve
            
        Returns:
            Question dict or None if not found
        """
        for question in self.questions:
            if question["id"] == question_id:
                return question
        
        logger.warning(f"Question ID {question_id} not found")
        return None
    
    def get_questions_by_category(
        self,
        categories: Optional[List[str]] = None,
        difficulty: Optional[str] = None
    ) -> List[Dict]:
        """
        Filter questions by category and/or difficulty.
        
        Args:
            categories: List of categories to include (e.g., ["behavioral", "technical"])
            difficulty: Difficulty level ("easy", "medium", "hard")
            
        Returns:
            List of matching questions
        """
        filtered = self.questions
        
        # Filter by category
        if categories:
            filtered = [
                q for q in filtered
                if q["category"] in categories
            ]
        
        # Filter by difficulty
        if difficulty:
            filtered = [
                q for q in filtered
                if q["difficulty"].lower() == difficulty.lower()
            ]
        
        logger.info(f"Filtered {len(filtered)} questions (categories={categories}, difficulty={difficulty})")
        return filtered
    
    def get_random_questions(
        self,
        num_questions: int = 5,
        categories: Optional[List[str]] = None,
        difficulty: Optional[str] = None,
        seed: Optional[int] = None
    ) -> List[Dict]:
        """
        Get random questions for an interview session.
        
        Args:
            num_questions: Number of questions to return
            categories: Filter by categories
            difficulty: Filter by difficulty
            seed: Random seed for reproducibility (optional)
            
        Returns:
            List of random questions
        """
        # Get filtered questions
        available = self.get_questions_by_category(categories, difficulty)
        
        if not available:
            logger.error("No questions match the criteria")
            return []
        
        # Set random seed if provided (useful for testing)
        if seed is not None:
            random.seed(seed)
        
        # Sample random questions
        num_to_select = min(num_questions, len(available))
        selected = random.sample(available, num_to_select)
        
        logger.info(f"Selected {num_to_select} random questions")
        return selected
    
    def get_all_categories(self) -> List[str]:
        """
        Get list of all available categories.
        
        Returns:
            List of category names
        """
        return self.metadata.get("categories", [])
    
    def get_total_questions(self) -> int:
        """
        Get total number of questions in the bank.
        
        Returns:
            Total question count
        """
        return len(self.questions)

# Global instance (singleton pattern)
# This is loaded once when the app starts
question_bank = QuestionBank()
