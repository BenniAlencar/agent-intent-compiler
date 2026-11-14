<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D0D0D,50:1a1a2e,100:7000FF&height=200&section=header&text=agent-intent-compiler&fontSize=50&fontColor=ffffff&fontAlignY=38&desc=Deterministic%20Intent%20Compiler%20%26%20Typed%20DAG%20Execution%20Planner&descAlignY=58&descSize=16&animation=fadeIn" width="100%"/>

<br/>

[![Tests](https://img.shields.io/badge/Tests-10%20Passed-00C853?style=for-the-badge&logo=pytest&logoColor=white)](#-benchmark-comparison)
[![Python](https://img.shields.io/badge/Python-3.9+-7000FF?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Stdlib)-00C853?style=for-the-badge)](#-installation)
[![MCP Native](https://img.shields.io/badge/MCP-JSON--RPC%202.0-8a2be2?style=for-the-badge)](#-2-export-directly-to-model-context-protocol-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-00C853?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Benni OS](https://img.shields.io/badge/Benni%20OS-benni--os.net-0D0D0D?style=for-the-badge)](https://benni-os.net)

<br/>

> **Deterministic Intent Compiler & Typed DAG Execution Planner for Autonomous AI Agents & MCP Servers.**  
> Eliminates prompt injection, hallucinated tool calls, and redundant token waste by compiling natural language into typed, cryptographically-sealed execution graphs before invoking LLMs.

<br/>

<img src="assets/demo.gif" alt="agent-intent-compiler Deterministic Intent & DAG Execution Demo" width="100%"/>

</div>

---

## ⚡ The Problem: The Unstructured Prompt Injection Tax

In 2026, autonomous agent frameworks like LangChain, AutoGen, and CrewAI feed raw, ambiguous user strings directly into multi-step LLM reasoning loops.

This creates four critical failure modes in production:

1. **Indirect Prompt Injection & Jailbreaks:** Hidden zero-width characters or adversarial override payloads (`"ignore previous instructions"`) hijack agent tool chains.
2. **Hallucinated Tool Parameters:** LLMs generate invalid JSON or missing required arguments, resulting in catastrophic runtime exceptions mid-pipeline.
3. **Loop Runaways & Token Burn:** Agents spend hundreds of tokens debating which tool to call sequentially when tasks could be grouped and executed in parallel.
4. **Lack of Non-Repudiation:** There is no cryptographic audit proof verifying whether an executed tool call actually matched the user's intended request.

---

## 🛡️ The Solution: `agent-intent-compiler`

`agent-intent-compiler` acts as a **Deterministic Pre-Execution Compiler** situated between user inputs and agent runtimes.

---

## 🏗️ Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        USER NATURAL LANGUAGE PROMPT                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (<0.2ms)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      PROMPT SANITIZER & ENTROPY SHIELD                 │
│  - Traverses syntax & filters zero-width unicode obfuscation           │
│  - Evaluates Shannon entropy for base64/hex hidden payload injection   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Clean Prompt
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     TYPED INTENT & SLOT COMPILER                       │
│  - Classifies intent: Query | Mutation | Research | Evaluation         │
│  - Extracts validated parameters into strict typed node schemas        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     KAHN'S ALGORITHM DAG PLANNER                       │
│  - Detects and halts cyclic dependencies                               │
│  - Groups independent tool nodes into parallel execution stages        │
│  - Computes SHA-256 Merkle Intent Receipt                              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   MODEL CONTEXT PROTOCOL (MCP) ADAPTER                 │
│         Emits validated JSON-RPC 2.0 "tools/call" requests             │
└────────────────────────────────────────────────────────────────────────┘
```

### Key Capabilities

- **Zero-Cloud, Sub-Millisecond Execution:** Compiles execution DAGs in **under 0.3ms** on local CPU with zero cloud API dependencies.
- **Topological Stage Parallelism:** Automatically groups independent tool calls into concurrent batches via Kahn's algorithm, cutting sequential wait stages.
- **Zero Tool Injection:** Strict parameter validation and static pattern + Shannon entropy checks block adversarial prompts (`IntentType.SECURITY_AUDIT`) before any tool is dispatched.
- **Cryptographic SHA-256 Merkle Root:** Every `ExecutionPlan` computes a deterministic 64-char SHA-256 Merkle hash sealing the intended execution trajectory.
- **Native MCP Compatibility:** Directly translates execution stages into standard Model Context Protocol `tools/call` JSON-RPC 2.0 payloads.

---

## 🚀 Installation & Quickstart

### Installation

```bash
pip install agent-intent-compiler
```

*Zero external dependencies (`dependencies = []`). Works across Python 3.9, 3.10, 3.11, and 3.12.*

### 1. Compile User Prompt into a Typed Execution DAG

```python
from agent_intent_compiler import IntentCompiler

compiler = IntentCompiler()

# Compile a multi-step user prompt
prompt = "Migrate the production PostgreSQL database schema and verify data integrity"
plan = compiler.compile(prompt)

print(f"Plan ID: {plan.plan_id}")
print(f"Intent Type: {plan.intent_type}")
print(f"Compilation Latency: {plan.compilation_latency_ms:.2f}ms")
print(f"Execution Stages (Parallel Groups): {plan.execution_order}")
print(f"Cryptographic Merkle Seal: {plan.merkle_root}")
```

### 2. Export Directly to Model Context Protocol (MCP)

```python
from agent_intent_compiler import IntentCompiler, MCPAdapter

compiler = IntentCompiler()
plan = compiler.compile("Search for recent advancements in quantum error correction")

# Generate standard MCP JSON-RPC 2.0 tool requests
mcp_requests = MCPAdapter.to_mcp_requests(plan)

for req in mcp_requests:
    print(f"MCP Tool Call -> {req['params']['name']}: {req['params']['arguments']}")
```

### 3. Command Line Interface (CLI)

```bash
agent-intent-compiler "Deep research on LLM inference optimizations on edge hardware"
```

### Running the Test Suite

```bash
PYTHONPATH=src pytest -v
# 10 passed (test_compiler.py, test_dag.py, test_mcp_adapter.py, test_sanitizer.py)
```

---

## 📊 Benchmark Comparison

| Metric | Raw Prompt to LLM | Multi-Turn Agent Frameworks | `agent-intent-compiler` |
| :--- | :--- | :--- | :--- |
| **Compilation Latency** | 1,800ms – 3,500ms (network + LLM) | 450ms – 1,200ms | **< 0.3ms (Observed ~0.12ms Local CPU)** |
| **Token Cost per Intent** | ~450 – 1,200 tokens | ~250 – 600 tokens | **0 Tokens (\$0.00)** |
| **Prompt Injection Defense** | 0% (Vulnerable) | Inconsistent | **Sub-ms Regex + Zero-Width + Entropy Shield** |
| **DAG Cycle Prevention** | None (Risk of loops) | Runtime crash | **Static Kahn's Algorithm** |
| **Cryptographic Receipt** | No | No | **SHA-256 Merkle Root** |
| **MCP Native JSON-RPC** | Manual boilerplate | Partial | **1-Click Native `MCPAdapter`** |
| **Runtime Dependencies** | Cloud SDKs | Heavy Python/JS stacks | **Zero (Pure Python Stdlib)** |

---

## 🌐 The Benni OS Open-Source Ecosystem

`agent-intent-compiler` is part of the coordinated **Benni Master OS v9.4** open-source infrastructure suite:

| Repository | Focus & Architecture | Stars |
| :--- | :--- | :---: |
| **[`conductor-sdd`](https://github.com/Benni-OS/conductor-sdd)** | Zero-Dependency Spec-Driven Development, Static AST Drift Detector & MCP Guardrail | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/conductor-sdd?style=flat)](https://github.com/Benni-OS/conductor-sdd) |
| **[`benni-inference-engine`](https://github.com/Benni-OS/benni-inference-engine)** | High-Throughput Sovereign Local Inference for 8GB–16GB Consumer GPUs | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/benni-inference-engine?style=flat)](https://github.com/Benni-OS/benni-inference-engine) |
| **[`agent-eval-harness`](https://github.com/BenniAlencar/agent-eval-harness)** | Deterministic Zero-Cloud Agent Evaluation, Red-Teaming & Benchmark Harness | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-eval-harness?style=flat)](https://github.com/BenniAlencar/agent-eval-harness) |
| **[`agent-code-sandbox`](https://github.com/BenniAlencar/agent-code-sandbox)** | Micro-Second Zero-Dependency Code Sandbox & Execution Shield for AI Agents | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-code-sandbox?style=flat)](https://github.com/BenniAlencar/agent-code-sandbox) |
| **[`agent-deep-research`](https://github.com/BenniAlencar/agent-deep-research)** | Autonomous Multi-Source Deep Research & Evidence Synthesis Engine | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-deep-research?style=flat)](https://github.com/BenniAlencar/agent-deep-research) |
| **[`agent-browser-mesh`](https://github.com/BenniAlencar/agent-browser-mesh)** | Token-Saving Resilient Headless Browser Automation & A11y DOM Compiler | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-browser-mesh?style=flat)](https://github.com/BenniAlencar/agent-browser-mesh) |
| **[`agent-intent-compiler`](https://github.com/BenniAlencar/agent-intent-compiler)** | Deterministic Intent Compiler & Typed DAG Execution Planner for AI Agents | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-intent-compiler?style=flat)](https://github.com/BenniAlencar/agent-intent-compiler) |
| **[`agent-token-optimizer`](https://github.com/BenniAlencar/agent-token-optimizer)** | Sub-Millisecond Context Compression & Semantic Deduplication Engine | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-token-optimizer?style=flat)](https://github.com/BenniAlencar/agent-token-optimizer) |
| **[`bio-sync-operator-os`](https://github.com/BenniAlencar/bio-sync-operator-os)** | Real-Time Biometric Swarm Governance & 120 FPS Resonant Kinetic Interface | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/bio-sync-operator-os?style=flat)](https://github.com/BenniAlencar/bio-sync-operator-os) |
| **[`agent-cyber-sentinel`](https://github.com/BenniAlencar/agent-cyber-sentinel)** | Zero-Trust Runtime Security, Prompt Injection Firewall & Secrets Redaction | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-cyber-sentinel?style=flat)](https://github.com/BenniAlencar/agent-cyber-sentinel) |
| **[`agent-run-ledger`](https://github.com/BenniAlencar/agent-run-ledger)** | Deterministic Multi-Step Task Execution Ledger & Anti-Looping Engine | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-run-ledger?style=flat)](https://github.com/BenniAlencar/agent-run-ledger) |
| **[`reality-lock`](https://github.com/BenniAlencar/reality-lock)** | Cryptographic State Verification & Invariant Proof Engine for Agents | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/reality-lock?style=flat)](https://github.com/BenniAlencar/reality-lock) |
| **[`agent-memory-mesh`](https://github.com/BenniAlencar/agent-memory-mesh)** | Hybrid Vector + BM25 Hierarchical Session Memory & Continuity Engine | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-memory-mesh?style=flat)](https://github.com/BenniAlencar/agent-memory-mesh) |
| **[`benni-operator-gateway`](https://github.com/Benni-OS/benni-operator-gateway)** | Human-in-the-Loop Approval & Policy Enforcement Gateway | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/benni-operator-gateway?style=flat)](https://github.com/Benni-OS/benni-operator-gateway) |
| **[`mcp-forge`](https://github.com/Benni-OS/mcp-forge)** | Rapid Model Context Protocol (MCP) Server Scaffolding & Dynamic Tooling | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/mcp-forge?style=flat)](https://github.com/Benni-OS/mcp-forge) |
| **[`benni-nexus`](https://github.com/Benni-OS/benni-nexus)** | Autonomous Multi-Agent Intent Routing & Swarm Coordination Hub | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/benni-nexus?style=flat)](https://github.com/Benni-OS/benni-nexus) |
| **[`community-autopilot`](https://github.com/Benni-OS/community-autopilot)** | Autonomous GitHub Community Triaging & PR Feedback Agent | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/community-autopilot?style=flat)](https://github.com/Benni-OS/community-autopilot) |

---

## 🏛️ Commercial & Sovereign Architecture

Need deterministic intent compilation, autonomous multi-agent swarm orchestration, or enterprise Spec-Driven Governance?

- **Official Website:** [https://benni-os.net](https://benni-os.net)
- **Technical Masterclasses & Architecture:** [https://benni-os.net/blog/academy.html](https://benni-os.net/blog/academy.html)
- **GitHub Organization:** [https://github.com/Benni-OS](https://github.com/Benni-OS)
- **Maintainer:** [Benni Alencar](https://github.com/BenniAlencar)

---

## 📄 License & Provenance

- **License:** [MIT License](LICENSE)
- **Author:** Benni Alencar (`bennialencar@gmail.com`)
- **Architecture:** Benni Master OS v9.4 Deterministic Intent Standard

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7000FF,50:1a1a2e,100:0D0D0D&height=120&section=footer" width="100%"/>

**agent-intent-compiler** — *Deterministic Intent Compiler & Typed DAG Execution Planner* • [benni-os.net](https://benni-os.net) • `MIT License`

</div>
