"""
LLM Client wrapper for making API calls to various LLM providers
"""
import os
import json
import requests
from typing import List, Dict, Any, Optional
import time


class LLMClient:
    """Unified interface for LLM API calls"""
    
    def __init__(self, provider: str = "deepseek", model: str = None, api_key: str = None):
        """
        Initialize LLM client
        
        Args:
            provider: LLM provider (deepseek, openai, anthropic, etc.)
            model: Model name
            api_key: API key for the provider
        """
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        
        # Set default models for each provider
        self.model_map = {
            "deepseek": "deepseek-chat",
            "openai": "gpt-4-turbo-preview",
            "anthropic": "claude-3-5-sonnet-20241022",
        }
        
        self.model = model or self.model_map.get(self.provider, "deepseek-chat")
        
        # Set base URLs
        self.base_url_map = {
            "deepseek": "https://api.deepseek.com",
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com/v1",
        }
        
        self.base_url = self.base_url_map.get(self.provider, "https://api.deepseek.com")
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.7,
             max_tokens: int = 4000,
             tools: Optional[List[Dict]] = None,
             stream: bool = False) -> Dict[str, Any]:
        """
        Send chat completion request
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            tools: Optional list of function/tool definitions
            stream: Whether to stream the response
            
        Returns:
            Response dict with 'content' and optional 'tool_calls'
        """
        if self.provider in ["deepseek", "openai"]:
            return self._openai_style_chat(messages, temperature, max_tokens, tools, stream)
        elif self.provider == "anthropic":
            return self._anthropic_chat(messages, temperature, max_tokens, tools)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _openai_style_chat(self, messages: List[Dict[str, str]], 
                           temperature: float,
                           max_tokens: int,
                           tools: Optional[List[Dict]],
                           stream: bool) -> Dict[str, Any]:
        """OpenAI-compatible API call"""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract the response
            choice = result["choices"][0]
            message = choice["message"]
            
            output = {
                "content": message.get("content", ""),
                "role": message.get("role", "assistant"),
            }
            
            # Check for tool calls
            if "tool_calls" in message and message["tool_calls"]:
                output["tool_calls"] = message["tool_calls"]
            
            return output
            
        except requests.exceptions.RequestException as e:
            return {
                "content": f"API Error: {str(e)}",
                "role": "assistant",
                "error": True
            }
    
    def _anthropic_chat(self, messages: List[Dict[str, str]], 
                        temperature: float,
                        max_tokens: int,
                        tools: Optional[List[Dict]]) -> Dict[str, Any]:
        """Anthropic Claude API call"""
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        # Convert messages format
        system_message = ""
        converted_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                converted_messages.append(msg)
        
        payload = {
            "model": self.model,
            "messages": converted_messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if system_message:
            payload["system"] = system_message
        
        if tools:
            # Convert tools to Anthropic format
            payload["tools"] = self._convert_tools_to_anthropic(tools)
        
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract content
            content_blocks = result.get("content", [])
            text_content = ""
            tool_calls = []
            
            for block in content_blocks:
                if block["type"] == "text":
                    text_content += block["text"]
                elif block["type"] == "tool_use":
                    tool_calls.append({
                        "id": block["id"],
                        "type": "function",
                        "function": {
                            "name": block["name"],
                            "arguments": json.dumps(block["input"])
                        }
                    })
            
            output = {
                "content": text_content,
                "role": "assistant"
            }
            
            if tool_calls:
                output["tool_calls"] = tool_calls
            
            return output
            
        except requests.exceptions.RequestException as e:
            return {
                "content": f"API Error: {str(e)}",
                "role": "assistant",
                "error": True
            }
    
    def _convert_tools_to_anthropic(self, tools: List[Dict]) -> List[Dict]:
        """Convert OpenAI tool format to Anthropic format"""
        anthropic_tools = []
        
        for tool in tools:
            if tool["type"] == "function":
                func = tool["function"]
                anthropic_tools.append({
                    "name": func["name"],
                    "description": func["description"],
                    "input_schema": func["parameters"]
                })
        
        return anthropic_tools


# Simple mock client for testing without API keys
class MockLLMClient:
    """Mock LLM client for testing"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Return a mock response"""
        
        last_message = messages[-1]["content"]
        
        # Simple mock responses based on keywords
        if "plan" in last_message.lower():
            return {
                "content": json.dumps({
                    "tasks": [
                        {"id": 1, "description": "Create HTML structure", "file": "index.html"},
                        {"id": 2, "description": "Add CSS styling", "file": "style.css"},
                        {"id": 3, "description": "Add JavaScript functionality", "file": "script.js"}
                    ]
                }),
                "role": "assistant"
            }
        else:
            return {
                "content": "Mock response from LLM",
                "role": "assistant"
            }
