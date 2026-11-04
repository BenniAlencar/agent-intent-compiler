"""
agent-intent-compiler: Deterministic Intent Compiler & Typed DAG Execution Planner
for Autonomous AI Agents and Model Context Protocol (MCP) Servers.
"""

from .models import IntentType, ExecutionNode, ExecutionPlan, NodeStatus
from .compiler import IntentCompiler
from .sanitizer import PromptSanitizer
from .dag import DAGPlanner
from .mcp_adapter import MCPAdapter

__version__ = "1.0.0"
__author__ = "Benni Alencar"
__all__ = [
    "IntentType",
    "ExecutionNode",
    "ExecutionPlan",
    "NodeStatus",
    "IntentCompiler",
    "PromptSanitizer",
    "DAGPlanner",
    "MCPAdapter"
]
