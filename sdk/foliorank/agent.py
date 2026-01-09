"""
Controlled Agent Module

This module provides the ControlledAgent class for AI-assisted portfolio planning
under strict behavioral constraints. The agent processes natural language inputs
and generates structured portfolio specifications for simulation purposes.
"""

from typing import Dict, Any, Optional
import asyncio


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
        No real trading, execution, or financial advice is provided.

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
            ValueError: If description cannot be processed or violates constraints
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

        # Validate weights sum to exactly 100 (safety check)
        total_weight = sum(item["weight"] for item in allocation)
        if total_weight != 100:
            raise ValueError(f"Portfolio weights must sum to 100, got {total_weight}")

        # Create the structured output
        portfolio_spec = {
            "portfolio_name": portfolio_name,
            "allocation": allocation,
            "rationale": rationale
        }

        # Log the decision for audit purposes
        self._log_decision("portfolio_planning", {
            "input": description,
            "output": portfolio_spec
        })

        return portfolio_spec

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