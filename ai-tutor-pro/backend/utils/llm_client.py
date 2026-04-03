"""
LLM Client - Unified interface for multiple LLM providers
Supports OpenAI, Anthropic, and local models
"""
from typing import Any, Dict, List, Optional
import json
from loguru import logger

from ..config.settings import settings


class LLMClient:
    """
    Unified client for interacting with various LLM providers.
    
    Supported providers:
    - OpenAI (GPT-4, GPT-3.5-turbo)
    - Anthropic (Claude 3)
    - Local models (via Ollama, vLLM, etc.)
    """
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or self._detect_provider()
        self.model_name = self._get_model_name()
        self.logger = logger.bind(llm_provider=self.provider)
        
        # Initialize clients lazily
        self._openai_client = None
        self._anthropic_client = None
        
    def _detect_provider(self) -> str:
        """Detect available LLM provider based on API keys"""
        if settings.OPENAI_API_KEY:
            return "openai"
        elif settings.ANTHROPIC_API_KEY:
            return "anthropic"
        elif settings.LOCAL_LLM_ENABLED:
            return "local"
        else:
            raise ValueError("No LLM provider configured. Set API keys in environment.")
    
    def _get_model_name(self) -> str:
        """Get model name based on provider"""
        if self.provider == "openai":
            return settings.OPENAI_MODEL
        elif self.provider == "anthropic":
            return settings.ANTHROPIC_MODEL
        elif self.provider == "local":
            return settings.LOCAL_LLM_MODEL
        else:
            return "unknown"
    
    @property
    def openai_client(self):
        """Lazy initialization of OpenAI client"""
        if self._openai_client is None:
            try:
                from openai import AsyncOpenAI
                self._openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            except ImportError:
                raise ImportError("Please install openai package: pip install openai")
        return self._openai_client
    
    @property
    def anthropic_client(self):
        """Lazy initialization of Anthropic client"""
        if self._anthropic_client is None:
            try:
                from anthropic import AsyncAnthropic
                self._anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            except ImportError:
                raise ImportError("Please install anthropic package: pip install anthropic")
        return self._anthropic_client
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using the configured LLM provider.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system instruction
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text response
        """
        try:
            if self.provider == "openai":
                return await self._generate_openai(
                    prompt, system_prompt, max_tokens, temperature, **kwargs
                )
            elif self.provider == "anthropic":
                return await self._generate_anthropic(
                    prompt, system_prompt, max_tokens, temperature, **kwargs
                )
            elif self.provider == "local":
                return await self._generate_local(
                    prompt, system_prompt, max_tokens, temperature, **kwargs
                )
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
                
        except Exception as e:
            self.logger.error(f"Generation error: {str(e)}")
            raise
    
    async def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> str:
        """Generate using OpenAI API"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = await self.openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    async def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> str:
        """Generate using Anthropic API"""
        response = await self.anthropic_client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            system=system_prompt or "You are a helpful assistant.",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            **kwargs
        )
        
        return response.content[0].text
    
    async def _generate_local(
        self,
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> str:
        """Generate using local model (Ollama-compatible API)"""
        import httpx
        
        url = f"{settings.LOCAL_LLM_URL}/api/generate"
        
        payload = {
            "model": settings.LOCAL_LLM_MODEL,
            "prompt": prompt,
            "system": system_prompt or "",
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            },
            "stream": False
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            result = response.json()
            
        return result.get("response", "")
    
    def parse_json(self, text: str, default: Any = None) -> Any:
        """
        Parse JSON from LLM response.
        
        Args:
            text: Response text that may contain JSON
            default: Default value if parsing fails
            
        Returns:
            Parsed JSON object or default value
        """
        if not text:
            return default
        
        # Try to extract JSON from text
        try:
            # Direct parse
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in text
        import re
        
        # Look for JSON object
        json_pattern = r'\{[^{}]*\}|\[[^\[\]]*\]'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        for match in reversed(matches):
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        
        # Try to clean and parse
        cleaned = text.strip()
        # Remove markdown code blocks
        cleaned = re.sub(r'```json\s*|\s*```', '', cleaned)
        cleaned = re.sub(r'```\s*|\s*```', '', cleaned)
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass
        
        return default
    
    async def generate_with_retry(
        self,
        prompt: str,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """Generate with automatic retry on failure"""
        from tenacity import retry, stop_after_attempt, wait_exponential
        
        @retry(stop=stop_after_attempt(max_retries), wait=wait_exponential(multiplier=1, min=4, max=10))
        async def _generate():
            return await self.generate(prompt, **kwargs)
        
        return await _generate()
    
    def get_available_models(self) -> List[str]:
        """Get list of available models for current provider"""
        if self.provider == "openai":
            return [
                "gpt-4-turbo-preview",
                "gpt-4",
                "gpt-3.5-turbo",
                "gpt-4-vision-preview"
            ]
        elif self.provider == "anthropic":
            return [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
        elif self.provider == "local":
            return [settings.LOCAL_LLM_MODEL]
        else:
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get client status information"""
        return {
            "provider": self.provider,
            "model": self.model_name,
            "available": bool(
                settings.OPENAI_API_KEY or 
                settings.ANTHROPIC_API_KEY or 
                settings.LOCAL_LLM_ENABLED
            )
        }
