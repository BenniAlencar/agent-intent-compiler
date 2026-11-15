"""Diagnostics and benchmarking tools for agent-intent-compiler."""

from .bench_matrix import BenchMatrixRunner
from .doctor import run_diagnostics

__all__ = ["BenchMatrixRunner", "run_diagnostics"]
