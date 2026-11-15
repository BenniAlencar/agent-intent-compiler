"""Quickstart example: compile a multi-step prompt into a typed DAG ExecutionPlan."""

from agent_intent_compiler import IntentCompiler


def main() -> None:
    compiler = IntentCompiler()
    prompt = "Migrate the production PostgreSQL database schema and verify data integrity"
    plan = compiler.compile(prompt)

    print(f"Plan ID: {plan.plan_id}")
    print(f"Intent Type: {plan.intent_type.value}")
    print(f"Latency: {plan.compilation_latency_ms:.4f} ms")
    print(f"Execution Stages: {plan.execution_order}")
    print(f"Merkle Root: {plan.merkle_root}")


if __name__ == "__main__":
    main()
