from agent_intent_compiler.tools.bench_matrix import BenchMatrixRunner
from agent_intent_compiler.tools.doctor import run_diagnostics


def test_doctor_diagnostics_healthy():
    report = run_diagnostics()
    assert report["package"] == "agent-intent-compiler"
    assert report["healthy"] is True
    assert all(report["checks"].values())


def test_bench_matrix_runner():
    runner = BenchMatrixRunner(reps=5)
    data = runner.run_matrix()
    assert data["reps"] == 5
    assert len(data["matrix_results"]) == 5
    md = runner.format_markdown_table(data)
    assert "| Category | Intent Type |" in md
