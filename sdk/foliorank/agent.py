"""
Controlled Agent Module

This module provides the ControlledAgent class for AI-assisted portfolio planning
under strict behavioral constraints. The agent processes natural language inputs
and generates structured portfolio specifications for simulation purposes.
"""

from typing import Dict, Any, Optional
import asyncio
from .mcp import MCPEnforcer, MCPViolation


class ControlledAgent:
    """
    AI-assisted portfolio planning agent with strict behavioral constraints.

    The ControlledAgent processes natural language descriptions and converts them
    into structured portfolio specifications suitable for simulation. All operations
    occur within controlled simulation environments with transparent decision logging.

    Attributes:
        constraints: Behavioral constraints configuration
        audit_log: Decision and transformation audit trail
    """

    def __init__(self, constraints: Optional[Dict[str, Any]] = None):
        """
        Initialize the controlled agent.

        Args:
            constraints: Optional behavioral constraints configuration.
                        If None, default safety constraints are applied.
        """
        self.constraints = constraints or self._default_constraints()
        self.audit_log = []
        # MCP Enforcer - required gatekeeper for all operations
        self.mcp = MCPEnforcer()

    def _default_constraints(self) -> Dict[str, Any]:
        """
        Return default behavioral constraints for safe operation.

        Returns:
            Dictionary containing default constraint configurations.
        """
        # TODO: Implement default constraint loading
        return {
            "simulation_only": True,
            "no_execution": True,
            "transparent_decisions": True
        }

    def plan(self, description: str) -> Dict[str, Any]:
        """
        Process natural language description into structured portfolio specification.

        This is a simulation-only function that converts natural language inputs
        into structured portfolio allocations for educational and research purposes.
        ALL operations pass through MCP enforcement - no portfolio can be generated
        without safety validation.

        Args:
            description: Natural language portfolio description

        Returns:
            Structured portfolio specification with the following format:
            {
                "portfolio_name": string,
                "allocation": [{"asset": string, "weight": int}, ...],
                "rationale": string
            }

        Raises:
            MCPViolation: If input or output violates safety constraints
            ValueError: If description cannot be processed
        """
        # STEP 1: MCP PRE-CHECK - Block forbidden investment language
        # This is MANDATORY - no portfolio generation without this gate
        self.mcp.pre_check(description)

        # STEP 2: Generate portfolio using rule-based logic
        portfolio_spec = self._build_portfolio(description)

        # STEP 3: MCP POST-CHECK - Validate output safety and structure
        # This is MANDATORY - all outputs must pass safety validation
        self.mcp.post_check(portfolio_spec)

        # Log the decision for audit purposes
        self._log_decision("portfolio_planning", {
            "input": description,
            "output": portfolio_spec
        })

        return portfolio_spec

    def _build_portfolio(self, description: str) -> Dict[str, Any]:
        """
        Internal portfolio generation logic (rule-based).

        This method contains the actual portfolio construction rules.
        It is called ONLY after MCP pre-check passes.

        Args:
            description: Validated input description

        Returns:
            Portfolio specification dictionary
        """
        # Convert to lowercase for case-insensitive matching
        desc_lower = description.lower()

        # Define safe, abstract asset classes only (no real symbols)
        # This prevents any association with actual trading or specific investments
        asset_classes = {
            "equities": "Large-cap equities",
            "bonds": "Government bonds",
            "cash": "Cash equivalents"
        }

        # Rule-based portfolio mapping based on keywords
        # Each portfolio is conservative and educational in nature
        if "growth" in desc_lower or "aggressive" in desc_lower:
            # Growth-oriented but still conservative: equities dominant
            portfolio_name = "Growth Simulation Portfolio"
            allocation = [
                {"asset": asset_classes["equities"], "weight": 70},
                {"asset": asset_classes["bonds"], "weight": 25},
                {"asset": asset_classes["cash"], "weight": 5}
            ]
            rationale = "This simulation portfolio emphasizes equity exposure while maintaining conservative allocations to bonds and cash for stability."

        elif "stability" in desc_lower or "conservative" in desc_lower or "safe" in desc_lower:
            # Stability-focused: bonds and cash dominant
            portfolio_name = "Stability Simulation Portfolio"
            allocation = [
                {"asset": asset_classes["bonds"], "weight": 70},
                {"asset": asset_classes["cash"], "weight": 30}
            ]
            rationale = "This simulation portfolio prioritizes stability through government bonds and cash equivalents, suitable for conservative risk preferences."

        elif "balanced" in desc_lower or "moderate" in desc_lower:
            # Balanced approach: mix of all three asset classes
            portfolio_name = "Balanced Simulation Portfolio"
            allocation = [
                {"asset": asset_classes["equities"], "weight": 50},
                {"asset": asset_classes["bonds"], "weight": 40},
                {"asset": asset_classes["cash"], "weight": 10}
            ]
            rationale = "This simulation portfolio provides balance across equities, bonds, and cash, offering both growth potential and stability."

        else:
            # Default to balanced portfolio for unclear or unspecified requests
            # This ensures safe, predictable behavior for educational purposes
            portfolio_name = "Balanced Simulation Portfolio"
            allocation = [
                {"asset": asset_classes["equities"], "weight": 50},
                {"asset": asset_classes["bonds"], "weight": 40},
                {"asset": asset_classes["cash"], "weight": 10}
            ]
            rationale = "This simulation portfolio provides a balanced approach suitable for general portfolio construction education and research."

        # Create the structured output
        return {
            "portfolio_name": portfolio_name,
            "allocation": allocation,
            "rationale": rationale
        }

    def _log_decision(self, decision_type: str, details: Dict[str, Any]) -> None:
        """
        Log a decision for audit purposes.

        Args:
            decision_type: Type of decision being logged
            details: Decision details and context
        """
        # TODO: Implement proper audit logging with timestamps and hashing
        log_entry = {
            "type": decision_type,
            "details": details,
            "timestamp": None  # TODO: Add actual timestamp
        }
        self.audit_log.append(log_entry)