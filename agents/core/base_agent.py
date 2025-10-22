"""
Base agent class using Ollama Phi4-Mini (Simplified for LangChain 1.0+).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain.tools import BaseTool
import logging
import json

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
        self.verbose = verbose
        self.tools = self._define_tools()
        self.chat_history = []
        
    @abstractmethod
    def _define_tools(self) -> List[BaseTool]:
        """Define agent-specific tools."""
        pass
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Define agent's role and instructions."""
        pass
    
    def _build_prompt(self, task: str) -> str:
        """Build prompt with system instructions and tools."""
        tools_desc = "\n".join([
            f"- {tool.name}: {tool.description}" 
            for tool in self.tools
        ])
        
        history = "\n".join([
            f"User: {h['user']}\nAgent: {h['agent']}" 
            for h in self.chat_history[-3:]  # Last 3 exchanges
        ]) if self.chat_history else "No previous conversation."
        
        prompt = f"""You are {self.agent_name}.

{self._get_system_prompt()}

AVAILABLE TOOLS:
{tools_desc}

CONVERSATION HISTORY:
{history}

CURRENT TASK:
{task}

INSTRUCTIONS:
1. Think about which tool(s) you need to use
2. Use the tools by calling them mentally
3. Provide a clear, actionable response
4. Be concise and specific

YOUR RESPONSE:"""
        
        return prompt
    
    def _execute_tool(self, tool_name: str, tool_input: Any) -> str:
        """Execute a tool by name."""
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    if self.verbose:
                        logger.info(f"[{self.agent_name}] Executing tool: {tool_name}")
                    result = tool.func(tool_input)
                    return str(result)
                except Exception as e:
                    logger.error(f"Tool {tool_name} failed: {e}")
                    return f"Error executing {tool_name}: {str(e)}"
        return f"Tool {tool_name} not found"
    
    async def execute(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute agent task."""
        try:
            if self.verbose:
                logger.info(f"[{self.agent_name}] Executing: {task[:100]}...")
            
            # Build prompt
            prompt = self._build_prompt(task)
            
            # Call LLM
            response = await self.llm.ainvoke(prompt)
            
            # Store in history
            self.chat_history.append({
                "user": task,
                "agent": response
            })
            
            return {
                "success": True,
                "agent": self.agent_name,
                "result": response,
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
            if self.verbose:
                logger.info(f"[{self.agent_name}] Executing sync: {task[:100]}...")
            
            # Build prompt
            prompt = self._build_prompt(task)
            
            # Call LLM synchronously
            response = self.llm.invoke(prompt)
            
            # Store in history
            self.chat_history.append({
                "user": task,
                "agent": response
            })
            
            return {
                "success": True,
                "agent": self.agent_name,
                "result": response,
                "metadata": context
            }
        except Exception as e:
            logger.error(f"[{self.agent_name}] Error: {e}")
            return {
                "success": False,
                "agent": self.agent_name,
                "error": str(e)
            }
    
    def call_tool(self, tool_name: str, tool_input: Any) -> str:
        """
        Manually call a tool (for when agent needs to use tools).
        This can be used by CrewAI or manually.
        """
        return self._execute_tool(tool_name, tool_input)
    
    def reset_history(self):
        """Reset conversation history."""
        self.chat_history = []