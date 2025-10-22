"""
Base agent class using Ollama Phi4-Mini.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
import logging

from .ollama_config import OllamaConfig

logger = logging.getLogger(__name__)

class InterviewBaseAgent(ABC):
    """Base class for all interview agents using Ollama."""
    
    def __init__(
        self,
        agent_name: str,
        temperature: float = 0.7,
        verbose: bool = True
    ):
        self.agent_name = agent_name
        self.llm = OllamaConfig.get_llm(temperature=temperature)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=False  # Phi4-mini works better with string format
        )
        self.verbose = verbose
        self.tools = self._define_tools()
        self.agent_executor = self._create_agent()
        
    @abstractmethod
    def _define_tools(self) -> List[BaseTool]:
        """Define agent-specific tools."""
        pass
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Define agent's role and instructions."""
        pass
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor using ReAct pattern."""
        
        # ReAct prompt template (works well with Phi4-Mini)
        template = """You are {role}.

{system_prompt}

TOOLS:
------
You have access to the following tools:

{tools}

To use a tool, use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a final answer, respond with:

```
Thought: I now know the final answer
Final Answer: [your answer here]
```

Begin!

Previous conversation:
{chat_history}

Question: {input}
{agent_scratchpad}"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "chat_history", "agent_scratchpad"],
            partial_variables={
                "role": self.agent_name,
                "system_prompt": self._get_system_prompt(),
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )
        
        agent = create_react_agent(self.llm, self.tools, prompt)
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=5  # Limit iterations for Phi4-Mini
        )
    
    async def execute(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute agent task."""
        try:
            logger.info(f"[{self.agent_name}] Executing: {task[:100]}...")
            
            # For async execution
            result = await self.agent_executor.ainvoke({
                "input": task
            })
            
            return {
                "success": True,
                "agent": self.agent_name,
                "result": result.get("output", ""),
                "metadata": context
            }
        except Exception as e:
            logger.error(f"[{self.agent_name}] Error: {e}")
            return {
                "success": False,
                "agent": self.agent_name,
                "error": str(e)
            }
    
    def execute_sync(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Synchronous execution (useful for testing)."""
        try:
            logger.info(f"[{self.agent_name}] Executing sync: {task[:100]}...")
            
            result = self.agent_executor.invoke({
                "input": task
            })
            
            return {
                "success": True,
                "agent": self.agent_name,
                "result": result.get("output", ""),
                "metadata": context
            }
        except Exception as e:
            logger.error(f"[{self.agent_name}] Error: {e}")
            return {
                "success": False,
                "agent": self.agent_name,
                "error": str(e)
            }