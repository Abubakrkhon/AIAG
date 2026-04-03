"""
Base Agent Class
All specialized agents inherit from this
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import json


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents in the system
    """
    
    def __init__(self, llm_client, name: str = "BaseAgent"):
        self.llm_client = llm_client
        self.name = name
        self.system_prompt = ""
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """
        Execute agent's main task
        
        Args:
            input_data: input data for the agent
            
        Returns:
            Processed output
        """
        pass
    
    def _call_llm(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        Call LLM with prompt
        
        Args:
            prompt: user prompt
            system_prompt: optional system prompt override
            **kwargs: additional parameters for LLM
            
        Returns:
            LLM response text
        """
        messages = []
        
        if system_prompt or self.system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt or self.system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.llm_client.chat.completions.create(
            model=self.llm_client.model,
            messages=messages,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def _parse_json_response(self, text: str) -> Dict:
        """Parse JSON from LLM response"""
        # Try to extract JSON from text
        try:
            # Direct parse
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON in text
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Try with markdown code blocks
            code_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if code_match:
                return json.loads(code_match.group(1))
            
            raise ValueError(f"Could not parse JSON from response: {text}")
