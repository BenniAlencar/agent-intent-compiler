from typing import Dict, Any, List
from .models import ExecutionPlan, ExecutionNode

class MCPAdapter:
    """
    Translates an ExecutionPlan into official Model Context Protocol (MCP)
    JSON-RPC 2.0 tool call requests.
    """

    @staticmethod
    def to_mcp_requests(plan: ExecutionPlan) -> List[Dict[str, Any]]:
        requests = []
        for stage_idx, stage in enumerate(plan.execution_order):
            for node_id in stage:
                node = plan.nodes[node_id]
                requests.append({
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": node.tool_name,
                        "arguments": node.parameters
                    },
                    "id": f"mcp_{node.node_id}",
                    "meta": {
                        "plan_id": plan.plan_id,
                        "stage": stage_idx,
                        "merkle_root": plan.merkle_root
                    }
                })
        return requests
