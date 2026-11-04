import sys
import json
from .compiler import IntentCompiler
from .mcp_adapter import MCPAdapter

def main():
    if len(sys.argv) < 2:
        print("Usage: agent-intent-compiler \"<user prompt>\"")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    compiler = IntentCompiler()
    plan = compiler.compile(prompt)
    mcp_calls = MCPAdapter.to_mcp_requests(plan)

    output = {
        "plan": plan.to_dict(),
        "mcp_tool_calls": mcp_calls
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
