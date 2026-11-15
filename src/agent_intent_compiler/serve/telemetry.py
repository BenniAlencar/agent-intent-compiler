"""Real-Time Telemetry Engine for agent-intent-compiler.

Captures compilation latencies (P50, P90, P99), intent type distribution,
blocked injection counts, and node throughput.
"""

from __future__ import annotations

import statistics
import time
from typing import Any


class TelemetryEngine:
    """Collects real-time compilation diagnostics and intent distribution stats."""

    def __init__(self, max_history: int = 500) -> None:
        self.max_history = max_history
        self.latencies_ms: list[float] = []
        self.intent_counts: dict[str, int] = {}
        self.blocked_count: int = 0
        self.total_nodes_compiled: int = 0
        self.start_time = time.time()

    def record_compilation(
        self,
        latency_ms: float,
        intent_type: str,
        node_count: int = 1,
        blocked: bool = False,
    ) -> None:
        """Record metrics for a single intent compilation."""
        self.latencies_ms.append(latency_ms)
        if len(self.latencies_ms) > self.max_history:
            self.latencies_ms.pop(0)

        self.intent_counts[intent_type] = self.intent_counts.get(intent_type, 0) + 1
        self.total_nodes_compiled += node_count
        if blocked:
            self.blocked_count += 1

    def _percentile(self, values: list[float], p: float) -> float:
        if not values:
            return 0.0
        sorted_v = sorted(values)
        idx = min(len(sorted_v) - 1, int(len(sorted_v) * p))
        return round(sorted_v[idx], 4)

    def get_summary(self) -> dict[str, Any]:
        """Return aggregated latency percentiles and compilation metrics."""
        uptime = max(0.001, time.time() - self.start_time)
        total = len(self.latencies_ms)
        return {
            "uptime_seconds": round(uptime, 2),
            "total_compilations": total,
            "total_nodes_compiled": self.total_nodes_compiled,
            "blocked_injections": self.blocked_count,
            "latency_p50_ms": self._percentile(self.latencies_ms, 0.50),
            "latency_p90_ms": self._percentile(self.latencies_ms, 0.90),
            "latency_p99_ms": self._percentile(self.latencies_ms, 0.99),
            "mean_latency_ms": round(statistics.mean(self.latencies_ms), 4) if self.latencies_ms else 0.0,
            "intent_distribution": dict(self.intent_counts),
        }

    def render_ascii_distribution(self) -> str:
        """Render a compact ASCII bar chart of compiled intent types."""
        if not self.intent_counts:
            return "[No compilations recorded]"
        max_val = max(self.intent_counts.values(), default=1)
        lines = ["Intent Compilation Distribution:"]
        for intent, count in sorted(self.intent_counts.items()):
            bar_len = max(1, int((count / max_val) * 20))
            lines.append(f"{intent:<16} |{'#' * bar_len:<20}| ({count})")
        return "\n".join(lines)
