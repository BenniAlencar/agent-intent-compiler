import time
import uuid
import re
from typing import Dict, List, Any, Optional
from .models import IntentType, ExecutionNode, ExecutionPlan
from .sanitizer import PromptSanitizer
from .dag import DAGPlanner

class IntentCompiler:
    """
    Sub-millisecond deterministic intent compiler for AI agents.
    Transforms raw natural language requests into typed, verified DAG execution plans.
    """

    def __init__(self, registered_tools: Optional[Dict[str, Dict[str, Any]]] = None):
        self.registered_tools = registered_tools or self._default_tools()

    def _default_tools(self) -> Dict[str, Dict[str, Any]]:
        return {
            "web_search": {"category": "research", "parameters": ["query", "limit"]},
            "read_file": {"category": "query", "parameters": ["path"]},
            "write_file": {"category": "mutation", "parameters": ["path", "content"]},
            "run_code": {"category": "mutation", "parameters": ["code", "timeout"]},
            "database_query": {"category": "query", "parameters": ["sql"]},
            "database_migration": {"category": "mutation", "parameters": ["migration_script"]},
            "run_eval": {"category": "evaluation", "parameters": ["suite_name"]},
            "security_scan": {"category": "security_audit", "parameters": ["target"]}
        }

    def compile(self, prompt: str) -> ExecutionPlan:
        start_time = time.perf_counter()
        plan_id = f"plan_{uuid.uuid4().hex[:12]}"

        # Step 1: Sub-millisecond Security Sanitization
        is_clean, clean_prompt, threats = PromptSanitizer.sanitize(prompt)
        if not is_clean:
            # Block and return security violation node
            sec_node = ExecutionNode(
                node_id="sec_violation_0",
                tool_name="security_scan",
                parameters={"status": "BLOCKED", "threats": threats, "prompt": prompt[:100]},
                dependencies=[]
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ExecutionPlan(
                plan_id=plan_id,
                raw_prompt=prompt,
                intent_type=IntentType.SECURITY_AUDIT,
                nodes=[sec_node],
                execution_order=[["sec_violation_0"]],
                compilation_latency_ms=elapsed_ms
            )

        # Step 2: Classify Intent
        intent = self._classify_intent(clean_prompt)

        # Step 3: Extract Slots and Synthesize Execution Nodes
        nodes = self._synthesize_nodes(clean_prompt, intent)

        # Step 4: Validate and Stage DAG
        stages = DAGPlanner.plan(nodes)
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return ExecutionPlan(
            plan_id=plan_id,
            raw_prompt=clean_prompt,
            intent_type=intent,
            nodes=nodes,
            execution_order=stages,
            compilation_latency_ms=elapsed_ms
        )

    def _classify_intent(self, prompt: str) -> IntentType:
        p = prompt.lower()
        if any(k in p for k in ["pesquise", "search", "find", "deep research", "investigate"]):
            return IntentType.RESEARCH
        if any(k in p for k in ["create", "write", "update", "delete", "execute", "migrate", "modificar", "salvar"]):
            return IntentType.MUTATION
        if any(k in p for k in ["eval", "test", "benchmark", "validar", "verificar"]):
            return IntentType.EVALUATION
        if any(k in p for k in ["pipeline", "workflow", "swarm", "enxame", "deploy"]):
            return IntentType.WORKFLOW
        return IntentType.QUERY

    def _synthesize_nodes(self, prompt: str, intent: IntentType) -> List[ExecutionNode]:
        nodes = []
        p = prompt.lower()

        if intent == IntentType.RESEARCH:
            nodes.append(ExecutionNode(
                node_id="research_0",
                tool_name="web_search",
                parameters={"query": prompt, "limit": 5}
            ))
        elif intent == IntentType.EVALUATION:
            nodes.append(ExecutionNode(
                node_id="eval_0",
                tool_name="run_eval",
                parameters={"suite_name": "agent_suite", "strict": True}
            ))
        elif intent == IntentType.MUTATION:
            if "migrate" in p or "banco" in p or "schema" in p:
                nodes.append(ExecutionNode(
                    node_id="read_schema_0",
                    tool_name="read_file",
                    parameters={"path": "schema.sql"}
                ))
                nodes.append(ExecutionNode(
                    node_id="apply_migration_1",
                    tool_name="database_migration",
                    parameters={"migration_script": "schema.sql"},
                    dependencies=["read_schema_0"]
                ))
            else:
                nodes.append(ExecutionNode(
                    node_id="exec_0",
                    tool_name="write_file",
                    parameters={"path": "output.txt", "content": prompt}
                ))
        else:
            nodes.append(ExecutionNode(
                node_id="query_0",
                tool_name="read_file",
                parameters={"path": "context.md"}
            ))

        return nodes
