from collections import deque, defaultdict
from typing import List, Dict, Set
from .models import ExecutionNode

class DAGPlanner:
    """
    Constructs a Directed Acyclic Graph from ExecutionNodes and performs
    topological sorting into parallelizable execution stages using Kahn's algorithm.
    """

    @staticmethod
    def plan(nodes: List[ExecutionNode]) -> List[List[str]]:
        if not nodes:
            return []

        adj = defaultdict(list)
        in_degree = {node.node_id: 0 for node in nodes}
        all_ids = set(in_degree.keys())

        for node in nodes:
            for dep in node.dependencies:
                if dep in all_ids:
                    adj[dep].append(node.node_id)
                    in_degree[node.node_id] += 1
                else:
                    # Missing external dependency -> invalid DAG
                    raise ValueError(f"Node '{node.node_id}' depends on non-existent node '{dep}'")

        # Kahn's algorithm with stage grouping for maximum parallelism
        queue = deque([node_id for node_id, deg in in_degree.items() if deg == 0])
        stages: List[List[str]] = []
        visited_count = 0

        while queue:
            current_stage = []
            for _ in range(len(queue)):
                curr = queue.popleft()
                current_stage.append(curr)
                visited_count += 1

                for neighbor in adj[curr]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
            stages.append(sorted(current_stage))

        if visited_count != len(nodes):
            raise ValueError("Cycle detected in ExecutionNode dependencies! Execution DAG must be acyclic.")

        return stages
