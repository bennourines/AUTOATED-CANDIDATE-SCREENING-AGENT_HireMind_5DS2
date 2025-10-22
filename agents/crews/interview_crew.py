"""
Interview Crew using Ollama Phi4-Mini.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, List, Optional
import logging
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.ollama_config import OllamaConfig
from interview_agents.interviewer_agent import InterviewerAgent
from interview_agents.stt_agent import STTAgent
from interview_agents.prosody_agent import ProsodyAgent
from interview_agents.emotion_agent import EmotionAgent
from interview_agents.evaluator_agent import EvaluatorAgent
from interview_agents.summarizer_agent import SummarizerAgent

logger = logging.getLogger(__name__)

class InterviewCrew:
    """
    CrewAI team using Ollama Phi4-Mini for local inference.
    
    Workflow:
    1. Interviewer selects question
    2. STT transcribes candidate response
    3. Prosody analyzes voice patterns
    4. Emotion analyzes facial expressions (if video)
    5. Evaluator provides comprehensive feedback
    6. Summarizer generates session summary
    """
    
    def __init__(self):
        # Check Ollama availability
        if not OllamaConfig.check_availability():
            raise RuntimeError("Ollama server not available. Run: ollama serve")
        
        self.llm = OllamaConfig.get_llm(temperature=0.7)
        
        # Initialize LangChain agents
        self.interviewer_langchain = InterviewerAgent()
        self.stt_langchain = STTAgent()
        self.prosody_langchain = ProsodyAgent()
        self.emotion_langchain = EmotionAgent()
        self.evaluator_langchain = EvaluatorAgent()
        self.summarizer_langchain = SummarizerAgent()
        
        # Create CrewAI agents
        self.interviewer = self._create_interviewer()
        self.stt_specialist = self._create_stt()
        self.prosody_analyst = self._create_prosody()
        self.emotion_analyst = self._create_emotion()
        self.evaluator = self._create_evaluator()
        self.summarizer = self._create_summarizer()
        
        logger.info("✅ Interview Crew initialized with Ollama Phi4-Mini")
    
    def _create_interviewer(self) -> Agent:
        """Create interviewer agent for CrewAI."""
        return Agent(
            role="Senior Technical Interviewer",
            goal="Select appropriate questions and adapt to candidate performance",
            backstory="""You are an experienced interviewer who excels at reading 
            candidates and adjusting question difficulty dynamically.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.interviewer_langchain.tools
        )
    
    def _create_stt(self) -> Agent:
        """Create STT agent for CrewAI."""
        return Agent(
            role="Speech Recognition Specialist",
            goal="Accurately transcribe all speech to text",
            backstory="""You specialize in speech-to-text with experience 
            handling various accents and audio qualities.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.stt_langchain.tools
        )
    
    def _create_prosody(self) -> Agent:
        """Create prosody agent for CrewAI."""
        return Agent(
            role="Voice Pattern Analyst",
            goal="Analyze speaking patterns and vocal delivery",
            backstory="""You specialize in prosody analysis and can detect 
            confidence, nervousness, and communication effectiveness through voice.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.prosody_langchain.tools
        )
    
    def _create_emotion(self) -> Agent:
        """Create emotion agent for CrewAI."""
        return Agent(
            role="Emotion Recognition Expert",
            goal="Detect and interpret facial emotions accurately",
            backstory="""You are trained in facial emotion recognition and 
            understand the psychology behind interview behaviors.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.emotion_langchain.tools
        )
    
    def _create_evaluator(self) -> Agent:
        """Create evaluator agent for CrewAI."""
        return Agent(
            role="Senior Evaluation Officer",
            goal="Provide comprehensive, fair, and constructive evaluations",
            backstory="""You are an expert evaluator who combines technical 
            assessment with soft skills evaluation. Your feedback is always actionable.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.evaluator_langchain.tools
        )
    
    def _create_summarizer(self) -> Agent:
        """Create summarizer agent for CrewAI."""
        return Agent(
            role="Interview Session Analyst",
            goal="Generate comprehensive session summaries",
            backstory="""You excel at synthesizing interview data into actionable 
            insights and recommendations.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.summarizer_langchain.tools
        )
    
    async def select_questions(
        self,
        categories: List[str],
        difficulty: str,
        num_questions: int,
        candidate_performance: str = "average"
    ) -> Dict:
        """
        Select interview questions using the crew.
        """
        logger.info(f"🤖 Crew selecting {num_questions} questions...")
        
        task = Task(
            description=f"""Select {num_questions} appropriate interview questions.
            
            Criteria:
            - Categories: {', '.join(categories)}
            - Difficulty: {difficulty}
            - Candidate performance: {candidate_performance}
            
            Use the select_interview_question tool to get questions.""",
            agent=self.interviewer,
            expected_output=f"List of {num_questions} selected questions"
        )
        
        crew = Crew(
            agents=[self.interviewer],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "status": "questions_selected",
            "result": str(result),
            "num_questions": num_questions
        }
    
    async def process_answer(
        self,
        question: Dict,
        audio_path: str,
        video_path: Optional[str] = None
    ) -> Dict:
        """
        Process answer through crew pipeline.
        """
        logger.info("🔄 Processing answer through crew...")
        
        # Task 1: Transcription
        transcription_task = Task(
            description=f"""Transcribe the audio from: {audio_path}
            Use the transcribe_audio tool.""",
            agent=self.stt_specialist,
            expected_output="Accurate transcript of the speech"
        )
        
        # Task 2: Prosody Analysis
        prosody_task = Task(
            description=f"""Analyze voice prosody from: {audio_path}
            Use analyze_prosody and analyze_stress tools.""",
            agent=self.prosody_analyst,
            expected_output="Prosody metrics and interpretation"
        )
        
        # Task 3: Evaluation
        evaluation_task = Task(
            description=f"""Evaluate the candidate's answer to:
            "{question['question']}"
            
            Use evaluate_answer and generate_feedback tools.""",
            agent=self.evaluator,
            expected_output="Comprehensive evaluation with scores"
        )
        
        tasks = [transcription_task, prosody_task, evaluation_task]
        
        # Add emotion analysis if video
        if video_path:
            emotion_task = Task(
                description=f"""Detect facial emotions from: {video_path}
                Use detect_emotions tool.""",
                agent=self.emotion_analyst,
                expected_output="Emotion timeline"
            )
            tasks.insert(2, emotion_task)
        
        crew = Crew(
            agents=[self.stt_specialist, self.prosody_analyst, self.emotion_analyst, self.evaluator] if video_path else [self.stt_specialist, self.prosody_analyst, self.evaluator],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "status": "completed",
            "evaluation": str(result)
        }
    
    async def generate_session_summary(self, session_data: Dict) -> Dict:
        """Generate comprehensive session summary."""
        
        summary_task = Task(
            description=f"""Generate a comprehensive interview session summary.
            
            Use calculate_average_score, identify_strengths, and identify_improvements tools.
            
            Session has {len(session_data.get('answers', []))} answers.""",
            agent=self.summarizer,
            expected_output="Executive summary with insights"
        )
        
        crew = Crew(
            agents=[self.summarizer],
            tasks=[summary_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {"summary": str(result)}