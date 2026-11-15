from agent_intent_compiler.serve.telemetry import TelemetryEngine


def test_telemetry_records_and_summarizes():
    tel = TelemetryEngine(max_history=10)
    tel.record_compilation(latency_ms=0.12, intent_type="query", node_count=1, blocked=False)
    tel.record_compilation(latency_ms=0.25, intent_type="mutation", node_count=2, blocked=False)
    tel.record_compilation(latency_ms=0.09, intent_type="security_audit", node_count=1, blocked=True)

    summary = tel.get_summary()
    assert summary["total_compilations"] == 3
    assert summary["total_nodes_compiled"] == 4
    assert summary["blocked_injections"] == 1
    assert summary["latency_p50_ms"] > 0
    assert summary["intent_distribution"]["mutation"] == 1

    chart = tel.render_ascii_distribution()
    assert "Intent Compilation Distribution:" in chart
    assert "security_audit" in chart
