import hashlib
import json
import time
from enum import Enum
from typing import Dict, List, Any, Optional

class IntentType(str, Enum):
    QUERY = "query"
    MUTATION = "mutation"
    WORKFLOW = "workflow"
    RESEARCH = "research"
    EVALUATION = "evaluation"
    RECOVERY = "recovery"
    SECURITY_AUDIT = "security_audit"
    UNKNOWN = "unknown"

class NodeStatus(str, Enum):
    PENDING = "pending"
    COMPILED = "compiled"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class ExecutionNode:
    def __init__(
        self,
        node_id: str,
        tool_name: str,
        parameters: Dict[str, Any],
        dependencies: Optional[List[str]] = None,
        timeout_ms: int = 5000,
        idempotent: bool = True
    ):
        self.node_id = node_id
        self.tool_name = tool_name
        self.parameters = parameters or {}
        self.dependencies = dependencies or []
        self.timeout_ms = timeout_ms
        self.idempotent = idempotent
        self.status = NodeStatus.COMPILED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "tool_name": self.tool_name,
            "parameters": self.parameters,
            "dependencies": self.dependencies,
            "timeout_ms": self.timeout_ms,
            "idempotent": self.idempotent,
            "status": self.status.value
        }

    def compute_hash(self) -> str:
        payload = f"{self.node_id}:{self.tool_name}:{json.dumps(self.parameters, sort_keys=True)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

class ExecutionPlan:
    def __init__(
        self,
        plan_id: str,
        raw_prompt: str,
        intent_type: IntentType,
        nodes: List[ExecutionNode],
        execution_order: List[List[str]],
        compilation_latency_ms: float
    ):
        self.plan_id = plan_id
        self.raw_prompt = raw_prompt
        self.intent_type = intent_type
        self.nodes = {node.node_id: node for node in nodes}
        self.execution_order = execution_order
        self.compilation_latency_ms = compilation_latency_ms
        self.merkle_root = self._compute_merkle_root()

    def _compute_merkle_root(self) -> str:
        if not self.nodes:
            return hashlib.sha256(b"empty_plan").hexdigest()
        node_hashes = [n.compute_hash() for n in sorted(self.nodes.values(), key=lambda x: x.node_id)]
        combined = ":".join(node_hashes)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "raw_prompt": self.raw_prompt,
            "intent_type": self.intent_type.value,
            "total_nodes": len(self.nodes),
            "execution_stages": self.execution_order,
            "merkle_root": self.merkle_root,
            "compilation_latency_ms": self.compilation_latency_ms,
            "nodes": [n.to_dict() for n in self.nodes.values()]
        }
