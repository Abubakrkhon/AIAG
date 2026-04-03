"""
Base agent class for all AI agents in the system
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from loguru import logger


class AgentResponse(BaseModel):
    """Standard response format for all agents"""
    success: bool
    data: Any
    message: str = ""
    metadata: Dict[str, Any] = {}


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.
    
    All agents must implement:
    - process(): Main processing logic
    - get_capabilities(): Return agent capabilities
    - validate_input(): Validate input data
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = logger.bind(agent=name)
        
    @abstractmethod
    async def process(self, input_data: Any, **kwargs) -> AgentResponse:
        """
        Process input data and return results.
        
        Args:
            input_data: Input data to process
            **kwargs: Additional parameters
            
        Returns:
            AgentResponse with processed results
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Return agent capabilities and supported operations.
        
        Returns:
            Dictionary with capability information
        """
        pass
    
    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data before processing.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if valid, False otherwise
        """
        if input_data is None:
            self.logger.warning("Input data is None")
            return False
        return True
    
    def format_output(self, data: Any, format_type: str = "json") -> Any:
        """
        Format output data according to specified format.
        
        Args:
            data: Data to format
            format_type: Output format (json, markdown, text, etc.)
            
        Returns:
            Formatted data
        """
        if format_type == "json":
            return data
        elif format_type == "markdown":
            return self._format_markdown(data)
        elif format_type == "text":
            return str(data)
        else:
            return data
    
    def _format_markdown(self, data: Any) -> str:
        """Convert data to markdown format"""
        if isinstance(data, dict):
            md = ""
            for key, value in data.items():
                md += f"## {key}\n\n{value}\n\n"
            return md
        elif isinstance(data, list):
            return "\n".join([f"- {item}" for item in data])
        else:
            return str(data)
    
    async def initialize(self) -> None:
        """Initialize agent resources (override if needed)"""
        self.logger.info(f"Initializing {self.name} agent")
    
    async def cleanup(self) -> None:
        """Cleanup agent resources (override if needed)"""
        self.logger.info(f"Cleaning up {self.name} agent")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and health information"""
        return {
            "name": self.name,
            "status": "active",
            "config": self.config
        }
