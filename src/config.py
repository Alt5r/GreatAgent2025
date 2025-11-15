"""
Configuration management for the red teaming system.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class APIConfig:
    """API configuration settings."""
    base_url: str
    timeout: int
    max_retries: int
    rate_limit_delay: float
    
    @classmethod
    def from_env(cls) -> 'APIConfig':
        """Load configuration from environment variables."""
        return cls(
            base_url=os.getenv('BASE_URL', 'https://6ofr2p56t1.execute-api.us-east-1.amazonaws.com/prod'),
            timeout=int(os.getenv('REQUEST_TIMEOUT', '35')),
            max_retries=int(os.getenv('MAX_RETRIES', '3')),
            rate_limit_delay=float(os.getenv('RATE_LIMIT_DELAY', '1.0'))
        )


@dataclass
class LLMConfig:
    """LLM API keys configuration."""
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'LLMConfig':
        """Load LLM configuration from environment variables."""
        return cls(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY')
        )


# Available agents
AGENTS = [
    'elephant',
    'fox',
    'eagle',
    'ant',
    'wolf',
    'bear',
    'chameleon'
]

# Attack categories
ATTACK_CATEGORIES = [
    'jailbreak',
    'prompt_injection',
    'system_prompt_extraction',
    'data_exfiltration',
    'tool_misuse',
    'obfuscation',
    'multi_turn_manipulation',
    'framework_detection'
]

# Global configuration instances
api_config = APIConfig.from_env()
llm_config = LLMConfig.from_env()
