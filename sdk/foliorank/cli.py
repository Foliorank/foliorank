#!/usr/bin/env python3
"""
Foliorank CLI - Simulation-only portfolio research toolkit.

This CLI provides simulation-only tools for portfolio construction,
analysis, and comparison. All operations are deterministic and
educational in nature. No real trading, execution, or investment
advice is provided.

Usage:
    foliorank plan "description" --out portfolio.json
    foliorank simulate --in portfolio.json --out result.json
    foliorank rank --a result_a.json --b result_b.json --out ranking.json
    foliorank validate --in portfolio.json
"""

import argparse
import json
import sys
import os
from typing import Dict, Any, Optional

from .agent import ControlledAgent
from .ranking import rank_bundles
from .export import ExportViolation


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Foliorank SDK - Simulation-only portfolio research toolkit",
        epilog="All operations are simulation-only and for educational purposes only."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Plan command
    plan_parser = subparsers.add_parser('plan', help='Plan portfolio from text description')
    plan_parser.add_argument('description', help='Natural language portfolio description')
    plan_parser.add_argument('--out', required=True, help='Output portfolio JSON file')

    # Simulate command
    sim_parser = subparsers.add_parser('simulate', help='Run simulation on portfolio')
    sim_parser.add_argument('--in', dest='input_file', required=True, help='Input portfolio JSON file')
    sim_parser.add_argument('--out', required=True, help='Output simulation result JSON file')

    # Rank command
    rank_parser = subparsers.add_parser('rank', help='Rank portfolios for comparison')
    rank_parser.add_argument('--in', dest='input_file', required=True, help='Input rank bundle JSON file (or single portfolio for auto-wrap)')
    rank_parser.add_argument('--out', required=True, help='Output ranking JSON file')

    # Validate command
    val_parser = subparsers.add_parser('validate', help='Validate portfolio specification')
    val_parser.add_argument('--in', dest='input_file', required=True, help='Portfolio JSON file to validate')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == 'plan':
            return cmd_plan(args.description, args.out)
        elif args.command == 'simulate':
            return cmd_simulate(args.input_file, args.out)
        elif args.command == 'rank':
            return cmd_rank(args.input_file, args.out)
        elif args.command == 'validate':
            return cmd_validate(args.input_file)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_plan(description: str, output_file: str) -> int:
    """Plan portfolio from text description."""
    print(f"Planning portfolio from: {description}")

    agent = ControlledAgent()
    portfolio = agent.plan(description)

    # Save to file
    with open(output_file, 'w') as f:
        json.dump(portfolio, f, indent=2)

    print(f"✅ Portfolio saved to {output_file}")
    print(f"   Name: {portfolio['portfolio_name']}")
    return 0


def cmd_simulate(input_file: str, output_file: str) -> int:
    """Run simulation on portfolio."""
    print(f"Loading portfolio from: {input_file}")

    # Load portfolio
    with open(input_file, 'r') as f:
        portfolio_data = json.load(f)

    # Validate portfolio first
    from .schemas import portfolio_validator
    portfolio_validator.validate(portfolio_data)

    # Run simulation
    agent = ControlledAgent()
    simulation_result = agent.simulate(portfolio_data)

    # Save result
    with open(output_file, 'w') as f:
        json.dump(simulation_result, f, indent=2)

    print(f"✅ Simulation completed, results saved to {output_file}")
    print(f"   Expected return: {simulation_result['expected_return']:.1f}%")
    return 0


def cmd_rank(input_file: str, output_file: str) -> int:
    """Rank portfolios using a rank bundle or single portfolio."""
    print(f"Loading rank input from: {input_file}")

    # Load input file
    with open(input_file, 'r') as f:
        input_data = json.load(f)

    # Determine if this is a rank bundle or single portfolio
    bundle_input = _prepare_rank_bundle(input_data)

    # Rank portfolios
    ranking_report = rank_bundles(bundle_input)

    # Save ranking
    with open(output_file, 'w') as f:
        json.dump(ranking_report, f, indent=2)

    print(f"✅ Ranking completed, results saved to {output_file}")
    print(f"   Ranked {ranking_report['valid_candidates']} portfolios")

    # Show top result
    if ranking_report['ranked_items']:
        top = ranking_report['ranked_items'][0]
        print(f"   Top result: {top['portfolio_name']} (Score: {top['total_score']:.1f})")
    return 0


def _prepare_rank_bundle(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare rank bundle from input data.

    If input is already a rank bundle (has 'version' and 'items'), return as-is.
    If input is a single portfolio spec, wrap it into a bundle format.
    """
    # Check if it's already a rank bundle
    if (isinstance(input_data, dict) and
        input_data.get("version") == "v0.1" and
        "items" in input_data):
        return input_data

    # Assume it's a single portfolio spec - wrap into bundle format
    print("   Detected single portfolio input, auto-wrapping into bundle format")

    bundle = {
        "version": "v0.1",
        "items": [
            {
                "id": "portfolio_1",
                "portfolio": input_data
            }
        ]
    }

    return bundle


def cmd_validate(input_file: str) -> int:
    """Validate portfolio specification."""
    print(f"Validating portfolio from: {input_file}")

    try:
        with open(input_file, 'r') as f:
            portfolio_data = json.load(f)

        # Validate portfolio structure directly
        from .schemas import portfolio_validator
        portfolio_validator.validate(portfolio_data)

        print("✅ Portfolio validation successful")
        return 0

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"❌ Validation failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())