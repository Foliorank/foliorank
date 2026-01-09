"""
Data Schemas Module

This module defines data structures and validation schemas for portfolio
specifications and simulation results. All schemas emphasize data integrity,
structure validation, and clear documentation without referencing external
data sources or execution systems.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
import os


@dataclass
class PortfolioSpecification:
    """
    Structured representation of a portfolio specification.

    This class defines the expected structure for portfolio configurations
    used in simulation environments. All fields are validated for type
    and structural integrity.

    Attributes:
        description: Natural language description of the portfolio
        structure: Dictionary defining portfolio composition and weights
        constraints: Applied behavioral and structural constraints
        metadata: Additional specification metadata
    """
    description: str
    structure: Dict[str, Any]
    constraints: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    def validate(self) -> bool:
        """
        Validate the portfolio specification structure.

        Returns:
            True if specification is valid, False otherwise

        Raises:
            ValueError: If validation fails with specific error details
        """
        # TODO: Implement comprehensive validation logic
        # TODO: Check required fields are present
        # TODO: Validate data types and ranges
        # TODO: Ensure constraint compatibility
        return True


@dataclass
class SimulationResult:
    """
    Structured representation of simulation execution results.

    This class defines the expected structure for simulation outputs,
    including performance metrics, analysis data, and audit information.

    Attributes:
        portfolio_spec: Original portfolio specification used
        config: Simulation configuration applied
        metrics: Performance and analysis metrics
        analysis: Detailed simulation analysis data
        audit_info: Audit trail and validation information
    """
    portfolio_spec: PortfolioSpecification
    config: Dict[str, Any]
    metrics: Dict[str, Any]
    analysis: Dict[str, Any]
    audit_info: Dict[str, Any]

    def validate(self) -> bool:
        """
        Validate the simulation result structure.

        Returns:
            True if result is valid, False otherwise

        Raises:
            ValueError: If validation fails with specific error details
        """
        # TODO: Implement result validation logic
        # TODO: Check all required fields are present
        # TODO: Validate metric calculations
        # TODO: Ensure audit trail integrity
        return True


# Schema validation constants
REQUIRED_PORTFOLIO_FIELDS = [
    "description",
    "structure",
    "constraints"
]

REQUIRED_SIMULATION_FIELDS = [
    "portfolio_spec",
    "config",
    "metrics",
    "analysis",
    "audit_info"
]

# Portfolio Schema Validator
class PortfolioValidator:
    """
    Validates portfolio specifications against the defined JSON schema.

    This validator ensures that all portfolio outputs conform to the
    required structure and safety constraints for simulation-only operation.
    """

    def __init__(self):
        self.schema_path = os.path.join(os.path.dirname(__file__), "portfolio.json")
        with open(self.schema_path, 'r') as f:
            self.schema = json.load(f)

    def validate(self, portfolio: Dict[str, Any]) -> None:
        """
        Validate a portfolio specification against the schema.

        Args:
            portfolio: Portfolio dictionary to validate

        Raises:
            ValueError: If portfolio fails schema validation
        """
        # Check required top-level fields
        required_fields = self.schema["required"]
        for field in required_fields:
            if field not in portfolio:
                raise ValueError(f"Missing required field: {field}")

        # Validate portfolio_name
        if not isinstance(portfolio["portfolio_name"], str) or len(portfolio["portfolio_name"]) == 0:
            raise ValueError("portfolio_name must be non-empty string")

        # Validate allocation array
        allocation = portfolio["allocation"]
        if not isinstance(allocation, list) or len(allocation) == 0:
            raise ValueError("allocation must be non-empty array")

        total_weight = 0
        for item in allocation:
            if not isinstance(item, dict):
                raise ValueError("allocation items must be objects")

            # Check required fields in allocation items
            if "asset" not in item or "weight" not in item:
                raise ValueError("allocation items must have 'asset' and 'weight' fields")

            asset = item["asset"]
            weight = item["weight"]

            # Validate asset is string
            if not isinstance(asset, str) or len(asset) == 0:
                raise ValueError("asset must be non-empty string")

            # Validate weight is number between 0-100
            if not isinstance(weight, (int, float)) or weight < 0 or weight > 100:
                raise ValueError(f"weight must be number between 0-100, got {weight}")

            total_weight += weight

        # Validate total weight equals exactly 100
        if abs(total_weight - 100) > 0.001:  # Allow for floating point precision
            raise ValueError(f"Allocation weights must sum to exactly 100, got {total_weight}")

        # Validate rationale
        if not isinstance(portfolio["rationale"], str) or len(portfolio["rationale"]) == 0:
            raise ValueError("rationale must be non-empty string")


# Global validator instance
portfolio_validator = PortfolioValidator()