"""MCP pipeline export example with real-time TelemetryEngine tracking."""

import json

from agent_intent_compiler import IntentCompiler, MCPAdapter
from agent_intent_compiler.serve.telemetry import TelemetryEngine


def main() -> None:
    compiler = IntentCompiler()
    telemetry = TelemetryEngine()

    prompts = [
        "Search for recent advancements in quantum error correction",
        "Migrate the database schema for users",
        "Benchmark the agent routing pipeline",
    ]
    for prompt in prompts:
        plan = compiler.compile(prompt)
        telemetry.record_compilation(
            latency_ms=plan.compilation_latency_ms,
            intent_type=plan.intent_type.value,
            node_count=len(plan.nodes),
            blocked=plan.intent_type.value == "security_audit",
        )
        mcp_calls = MCPAdapter.to_mcp_requests(plan)
        print(f"[{plan.intent_type.value}] -> {len(mcp_calls)} MCP call(s)")

    print("\nTelemetry Summary:")
    print(json.dumps(telemetry.get_summary(), indent=2))


if __name__ == "__main__":
    main()
