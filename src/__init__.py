"""
Red Teaming System for Agent Security Assessment

This package provides tools for systematic security testing of AI agents.
"""

__version__ = "1.0.0"

from .config import APIConfig, LLMConfig, AGENTS, ATTACK_CATEGORIES
from .agent_client import AgentClient, AgentResponse
from .attacks import AttackGenerator, AttackPayload
from .evaluator import ResponseEvaluator, EvaluationResult
from .orchestrator import RedTeamOrchestrator

__all__ = [
    'APIConfig',
    'LLMConfig',
    'AGENTS',
    'ATTACK_CATEGORIES',
    'AgentClient',
    'AgentResponse',
    'AttackGenerator',
    'AttackPayload',
    'ResponseEvaluator',
    'EvaluationResult',
    'RedTeamOrchestrator',
]
