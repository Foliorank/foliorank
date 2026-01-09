"""
Foliorank SDK

A simulation-first framework for portfolio research and analysis.
This package provides tools for constructing, simulating, and analyzing
portfolio configurations within controlled simulation environments.

Core Components:
- ControlledAgent: AI-assisted portfolio planning with behavioral constraints
- SimulationEngine: Deterministic portfolio simulation environment
- Data schemas: Structured validation for portfolio specifications
- MCP layer: Behavioral control and action validation framework
"""

from .agent import ControlledAgent
from .simulation import SimulationEngine

__version__ = "0.1.0"
__all__ = ["ControlledAgent", "SimulationEngine"]