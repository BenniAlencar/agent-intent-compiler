import pytest
from agent_intent_compiler.models import ExecutionNode
from agent_intent_compiler.dag import DAGPlanner

def test_linear_dag():
    n1 = ExecutionNode("node_1", "tool_a", {})
    n2 = ExecutionNode("node_2", "tool_b", {}, dependencies=["node_1"])
    n3 = ExecutionNode("node_3", "tool_c", {}, dependencies=["node_2"])

    stages = DAGPlanner.plan([n1, n2, n3])
    assert stages == [["node_1"], ["node_2"], ["node_3"]]

def test_parallel_dag():
    n1 = ExecutionNode("node_1", "tool_a", {})
    n2 = ExecutionNode("node_2", "tool_b", {})
    n3 = ExecutionNode("node_3", "tool_c", {}, dependencies=["node_1", "node_2"])

    stages = DAGPlanner.plan([n1, n2, n3])
    assert stages[0] == ["node_1", "node_2"]
    assert stages[1] == ["node_3"]

def test_cycle_detection():
    n1 = ExecutionNode("node_1", "tool_a", {}, dependencies=["node_2"])
    n2 = ExecutionNode("node_2", "tool_b", {}, dependencies=["node_1"])

    with pytest.raises(ValueError, match="Cycle detected"):
        DAGPlanner.plan([n1, n2])
