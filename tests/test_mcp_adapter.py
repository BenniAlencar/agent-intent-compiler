from agent_intent_compiler.compiler import IntentCompiler
from agent_intent_compiler.mcp_adapter import MCPAdapter

def test_mcp_translation():
    compiler = IntentCompiler()
    plan = compiler.compile("Search for latest neural network benchmarks")
    requests = MCPAdapter.to_mcp_requests(plan)

    assert len(requests) == 1
    req = requests[0]
    assert req["jsonrpc"] == "2.0"
    assert req["method"] == "tools/call"
    assert req["params"]["name"] == "web_search"
    assert req["meta"]["plan_id"] == plan.plan_id
