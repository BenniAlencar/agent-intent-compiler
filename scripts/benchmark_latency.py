"""Sub-millisecond latency benchmark script for agent-intent-compiler."""

from agent_intent_compiler.tools.bench_matrix import BenchMatrixRunner


def main() -> None:
    runner = BenchMatrixRunner(reps=100)
    results = runner.run_matrix()
    print(runner.format_markdown_table(results))


if __name__ == "__main__":
    main()
