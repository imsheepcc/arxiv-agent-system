"""
Configuration file for the Multi-Agent System
"""
import os

# LLM API Configuration
LLM_CONFIG = {
    "provider": "deepseek",  # Can be changed to other providers
    "model": "deepseek-chat",
    "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
    "base_url": "https://api.deepseek.com",
    "temperature": 0.7,
    "max_tokens": 4000,
}

# Alternative LLM configurations
ALTERNATIVE_LLMS = {
    "openai": {
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "base_url": "https://api.openai.com/v1",
    },
    "anthropic": {
        "model": "claude-3-5-sonnet-20241022",
        "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    }
}

# Project Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

# Agent Configuration
AGENT_CONFIG = {
    "max_iterations": 10,
    "enable_logging": True,
    "log_level": "INFO",
}

# Orchestrator Configuration
ORCHESTRATOR_CONFIG = {
    "max_retries": 3,
    "enable_code_execution": True,
    "enable_web_search": False,  # Set to True if web search is needed
}
