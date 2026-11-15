# Architecture — `agent-intent-compiler`

`agent-intent-compiler` is a deterministic pre-execution compiler for AI agents and Model Context Protocol (MCP) runtimes. It compiles natural language requests into cryptographically sealed, topologically staged execution DAGs in sub-millisecond local CPU time.

## Subpackage Layout

- `agent_intent_compiler.core`:
  - `models.py`: Typed `IntentType`, `NodeStatus`, `ExecutionNode`, and `ExecutionPlan` with deterministic SHA-256 Merkle root sealing.
  - `sanitizer.py`: `PromptSanitizer` performing zero-width Unicode stripping, regex injection detection, and Shannon entropy anomaly checks.
  - `dag.py`: `DAGPlanner` implementing Kahn's topological sort with parallel stage grouping and static cycle detection.
  - `compiler.py`: `IntentCompiler` orchestrating sanitization, intent classification, node synthesis, and DAG staging.
- `agent_intent_compiler.serve`:
  - `mcp_adapter.py`: `MCPAdapter` emitting MCP JSON-RPC 2.0 `tools/call` payloads with Merkle provenance metadata.
  - `telemetry.py`: `TelemetryEngine` capturing P50/P90/P99 latencies, blocked injection counts, and intent distributions.
- `agent_intent_compiler.tools`:
  - `doctor.py`: Runtime self-diagnostics verifying stdlib-only execution, DAG compilation, MCP emission, and injection defense.
  - `bench_matrix.py`: `BenchMatrixRunner` sweeping prompt categories and reporting mean/P99 latency and throughput.

## Backwards Compatibility

Top-level imports (`agent_intent_compiler.compiler`, `agent_intent_compiler.dag`, `agent_intent_compiler.models`, `agent_intent_compiler.sanitizer`, `agent_intent_compiler.mcp_adapter`, and `agent_intent_compiler.*`) remain 100% preserved via re-export shims.
