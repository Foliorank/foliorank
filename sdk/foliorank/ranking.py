"""
Ranking Module

This module provides deterministic comparison and ranking of Foliorank simulation
results. All ranking is based on neutral, simulation-only metrics and produces
explainable, reproducible results for educational and research purposes.

Ranking does not constitute investment advice or recommendations.
"""

import json
import os
from typing import Dict, Any, List, Optional, Tuple
from .export import import_bundle, ExportViolation


class RankingViolation(Exception):
    """
    Exception raised when ranking operations encounter invalid data or
    violations of safety constraints.
    """
    pass


def rank_bundles(
    bundle_input: Dict[str, Any],
    *,
    scoring_profile: str = "v1_balanced",
    top_k: Optional[int] = None
) -> Dict[str, Any]:
    """
    Rank simulation bundles using deterministic scoring and comparison.

    This function validates a rank bundle (containing multiple portfolios),
    computes neutral scores, and produces a ranked comparison suitable
    for educational analysis.

    Args:
        bundle_input: Rank bundle dictionary with schema "rank_bundle_v0.1"
        scoring_profile: Scoring methodology to use (default: "v1_balanced")
        top_k: Return only top K results (None for all)

    Returns:
        Ranking report dictionary with schema "ranking_report_v1"

    Raises:
        RankingViolation: If bundle fails validation or ranking constraints
    """
    if not bundle_input:
        raise RankingViolation("No bundle input provided for ranking")

    if scoring_profile not in ["v1_balanced"]:
        raise RankingViolation(f"Unknown scoring profile: {scoring_profile}")

    # Validate bundle format
    portfolios = _validate_and_extract_bundle(bundle_input)

    if not portfolios:
        raise RankingViolation("No valid portfolios found in bundle")

    # Run simulations and create bundles for each portfolio
    bundles = []
    for portfolio_id, portfolio_spec in portfolios.items():
        # Simulate each portfolio
        from .agent import ControlledAgent
        agent = ControlledAgent()
        simulation_result = agent.simulate(portfolio_spec)

        # Create export bundle format
        bundle = {
            "portfolio_spec": portfolio_spec,
            "simulation_result": simulation_result,
            "audit_hash": f"rank_{portfolio_id}",  # Placeholder hash
            "schema_version": "export_bundle_v1",
            "mcp_version": "v0.1"
        }
        bundles.append(bundle)

    # Validate and filter bundles (though they should all be valid)
    valid_bundles, rejected_bundles = _validate_bundles(bundles)

    if not valid_bundles:
        raise RankingViolation("No valid bundles found for ranking")

    # Compute scores for valid bundles
    scored_items = _compute_scores(valid_bundles, scoring_profile)

    # Sort by total score (deterministic tie-breaking)
    scored_items.sort(key=lambda x: (
        -x["total_score"],  # Higher score first
        -x["score_breakdown"].get("drawdown_score", {}).get("normalized", 0),  # Higher drawdown score first
        x["audit_hash"]  # Lexicographic hash as final tiebreaker
    ))

    # Apply top_k limit if specified
    if top_k is not None:
        scored_items = scored_items[:top_k]

    # Add ranking positions
    for i, item in enumerate(scored_items, 1):
        item["rank"] = i

    # Create ranking report
    report = {
        "schema_version": "ranking_report_v1",
        "scoring_profile": scoring_profile,
        "created_by": "foliorank-sdk",
        "total_candidates": len(bundles),
        "valid_candidates": len(valid_bundles),
        "ranked_items": scored_items,
        "rejected_candidates": rejected_bundles
    }

    return report


def _validate_and_extract_bundle(bundle_input: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Validate rank bundle format and extract portfolios.

    Returns:
        Dictionary mapping portfolio IDs to portfolio specs
    """
    # Check basic structure
    if not isinstance(bundle_input, dict):
        raise RankingViolation("Bundle input must be a dictionary")

    if bundle_input.get("version") != "v0.1":
        raise RankingViolation("Unsupported bundle version")

    items = bundle_input.get("items", [])
    if not isinstance(items, list) or len(items) == 0:
        raise RankingViolation("Bundle must contain at least one item")

    portfolios = {}
    for item in items:
        if not isinstance(item, dict):
            raise RankingViolation("Bundle items must be dictionaries")

        portfolio_id = item.get("id")
        portfolio_spec = item.get("portfolio")

        if not portfolio_id or not portfolio_spec:
            raise RankingViolation("Bundle items must have 'id' and 'portfolio' fields")

        portfolios[portfolio_id] = portfolio_spec

    return portfolios


def _validate_bundles(bundles: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Validate bundles and separate valid from rejected ones.

    Returns:
        Tuple of (valid_bundles, rejected_bundles_with_reasons)
    """
    valid_bundles = []
    rejected_bundles = []

    for i, bundle in enumerate(bundles):
        try:
            # Try to import (validates structure and safety)
            validated_bundle = import_bundle(bundle)
            valid_bundles.append(validated_bundle)
        except ExportViolation as e:
            rejected_bundles.append({
                "bundle_index": i,
                "reason": str(e),
                "reason_code": "validation_failed"
            })
        except Exception as e:
            rejected_bundles.append({
                "bundle_index": i,
                "reason": f"Unexpected error: {str(e)}",
                "reason_code": "unexpected_error"
            })

    return valid_bundles, rejected_bundles


def _compute_scores(bundles: List[Dict[str, Any]], profile: str) -> List[Dict[str, Any]]:
    """
    Compute scores for valid bundles using the specified scoring profile.
    """
    if profile == "v1_balanced":
        return _compute_v1_balanced_scores(bundles)
    else:
        raise RankingViolation(f"Unsupported scoring profile: {profile}")


def _compute_v1_balanced_scores(bundles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Compute scores using v1_balanced profile.

    Scoring weights (must sum to 1.0):
    - return_score: 0.4 (higher better)
    - risk_score: 0.3 (lower volatility better)
    - drawdown_score: 0.2 (lower drawdown better)
    - stability_score: 0.05 (lower extreme swings better)
    - completeness_score: 0.05 (all metrics present)
    """
    weights = {
        "return_score": 0.4,
        "risk_score": 0.3,
        "drawdown_score": 0.2,
        "stability_score": 0.05,
        "completeness_score": 0.05
    }

    scored_items = []

    # Extract raw metrics for normalization
    raw_metrics = {
        "returns": [],
        "volatilities": [],
        "drawdowns": [],  # Placeholder - not in current simulation_result
        "stability_scores": []  # Placeholder - computed from volatility
    }

    for bundle in bundles:
        sim_result = bundle["simulation_result"]
        expected_return = sim_result.get("expected_return", 0)
        volatility = sim_result.get("volatility", 0)

        # Collect raw metrics for normalization
        raw_metrics["returns"].append(expected_return)
        raw_metrics["volatilities"].append(volatility)
        raw_metrics["drawdowns"].append(0)  # Placeholder
        raw_metrics["stability_scores"].append(1 / (1 + volatility))  # Inverse volatility

    # Compute normalization ranges
    norm_ranges = {}
    for key, values in raw_metrics.items():
        if values:
            min_val = min(values)
            max_val = max(values)
            # Handle edge case: all identical values
            if min_val == max_val:
                norm_ranges[key] = (min_val, max_val, "identical")
            else:
                norm_ranges[key] = (min_val, max_val, "normal")
        else:
            norm_ranges[key] = (0, 1, "empty")

    # Score each bundle
    for bundle in bundles:
        sim_result = bundle["simulation_result"]
        expected_return = sim_result.get("expected_return", 0)
        volatility = sim_result.get("volatility", 0)

        # Compute individual scores
        scores = {}

        # Return score (higher better) - normalize to 0-1
        ret_min, ret_max, ret_status = norm_ranges["returns"]
        if ret_status == "identical":
            scores["return_score"] = {"raw": expected_return, "normalized": 0.5}
        else:
            scores["return_score"] = {
                "raw": expected_return,
                "normalized": (expected_return - ret_min) / (ret_max - ret_min)
            }

        # Risk score (lower volatility better) - invert and normalize
        vol_min, vol_max, vol_status = norm_ranges["volatilities"]
        if vol_status == "identical":
            scores["risk_score"] = {"raw": volatility, "normalized": 0.5}
        else:
            # Invert: lower volatility = higher score
            risk_normalized = 1 - ((volatility - vol_min) / (vol_max - vol_min))
            scores["risk_score"] = {"raw": volatility, "normalized": risk_normalized}

        # Drawdown score (placeholder - lower drawdown better)
        scores["drawdown_score"] = {"raw": 0, "normalized": 0.5}  # Placeholder

        # Stability score (lower volatility swings better)
        stab_min, stab_max, stab_status = norm_ranges["stability_scores"]
        stability_raw = 1 / (1 + volatility)
        if stab_status == "identical":
            scores["stability_score"] = {"raw": stability_raw, "normalized": 0.5}
        else:
            scores["stability_score"] = {
                "raw": stability_raw,
                "normalized": (stability_raw - stab_min) / (stab_max - stab_min)
            }

        # Completeness score (all metrics present)
        required_metrics = ["expected_return", "volatility", "time_horizon", "simulation_version"]
        completeness = sum(1 for m in required_metrics if m in sim_result) / len(required_metrics)
        scores["completeness_score"] = {"raw": completeness, "normalized": completeness}

        # Compute total score and breakdown
        total_score = 0
        score_breakdown = {}

        for metric_name, score_data in scores.items():
            weight = weights.get(metric_name, 0)
            contribution = score_data["normalized"] * weight
            total_score += contribution

            score_breakdown[metric_name] = {
                "raw": score_data["raw"],
                "normalized": score_data["normalized"],
                "weight": weight,
                "contribution": contribution
            }

        # Scale total_score to 0-100
        total_score *= 100

        # Generate neutral notes
        notes = _generate_neutral_notes(bundle, total_score)

        scored_item = {
            "audit_hash": bundle["audit_hash"],
            "portfolio_name": bundle["portfolio_spec"]["portfolio_name"],
            "total_score": round(total_score, 2),
            "score_breakdown": score_breakdown,
            "notes": notes
        }

        scored_items.append(scored_item)

    return scored_items


def _generate_neutral_notes(bundle: Dict[str, Any], total_score: float) -> str:
    """
    Generate neutral, non-prescriptive notes about the portfolio ranking.

    Avoids any language that could be interpreted as advice or recommendations.
    """
    portfolio_name = bundle["portfolio_spec"]["portfolio_name"]
    sim_result = bundle["simulation_result"]

    notes = f"Portfolio '{portfolio_name}' achieved a ranking score of {total_score:.1f}. "

    expected_return = sim_result.get("expected_return", 0)
    volatility = sim_result.get("volatility", 0)

    notes += f"Simulation showed expected return of {expected_return:.1f}% with volatility of {volatility:.1f}%. "

    notes += "This ranking reflects simulation-based comparison metrics."

    return notes