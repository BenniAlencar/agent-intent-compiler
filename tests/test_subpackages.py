from agent_intent_compiler import (
    DAGPlanner,
    ExecutionNode,
    ExecutionPlan,
    IntentCompiler,
    IntentType,
    MCPAdapter,
    NodeStatus,
    PromptSanitizer,
)
from agent_intent_compiler.core import (
    DAGPlanner as CoreDAGPlanner,
    IntentCompiler as CoreIntentCompiler,
    PromptSanitizer as CorePromptSanitizer,
)
from agent_intent_compiler.serve import MCPAdapter as ServeMCPAdapter


def test_backwards_compatible_subpackage_imports():
    assert IntentCompiler is CoreIntentCompiler
    assert DAGPlanner is CoreDAGPlanner
    assert PromptSanitizer is CorePromptSanitizer
    assert MCPAdapter is ServeMCPAdapter
    assert ExecutionNode is not None
    assert ExecutionPlan is not None
    assert IntentType.QUERY.value == "query"
    assert NodeStatus.COMPILED.value == "compiled"
