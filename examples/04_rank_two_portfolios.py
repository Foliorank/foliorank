#!/usr/bin/env python3
"""
Example 4: Rank two portfolios.

This example demonstrates how to compare and rank multiple simulation
results using Foliorank's deterministic ranking system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sdk'))

from foliorank.agent import ControlledAgent
from foliorank.ranking import rank_bundles

def main():
    print("Foliorank SDK Example 4: Rank Two Portfolios")
    print("=" * 50)

    # Initialize the controlled agent
    agent = ControlledAgent()

    # Create two different portfolios
    print("Creating two portfolios for comparison...")

    portfolio1 = agent.plan("I want aggressive growth with high equity exposure")
    simulation1 = agent.simulate(portfolio1)
    bundle1 = agent.export_last_run()

    # Reset agent state for second portfolio
    agent2 = ControlledAgent()
    portfolio2 = agent2.plan("I prefer conservative stability with bonds")
    simulation2 = agent2.simulate(portfolio2)
    bundle2 = agent2.export_last_run()

    print(f"Portfolio 1: {portfolio1['portfolio_name']}")
    print(f"  Expected return: {simulation1['expected_return']:.1f}%")
    print(f"Portfolio 2: {portfolio2['portfolio_name']}")
    print(f"  Expected return: {simulation2['expected_return']:.1f}%")
    print()

    # Create a rank bundle (canonical format)
    rank_bundle = {
        "version": "v0.1",
        "items": [
            {
                "id": "growth_portfolio",
                "portfolio": portfolio1
            },
            {
                "id": "conservative_portfolio",
                "portfolio": portfolio2
            }
        ]
    }

    # Rank the two portfolios using canonical bundle format
    # Note: CLI also supports single portfolio input (auto-wrapped)
    ranking_report = rank_bundles(rank_bundle)

    print("🎯 Ranking Results:")
    print(f"Total candidates: {ranking_report['total_candidates']}")
    print(f"Valid candidates: {ranking_report['valid_candidates']}")
    print()

    for item in ranking_report['ranked_items']:
        print(f"Rank {item['rank']}: {item['portfolio_name']}")
        print(f"  Score: {item['total_score']:.1f}/100")
        print(f"  Notes: {item['notes']}")
        print()

    if ranking_report['rejected_candidates']:
        print(f"Rejected candidates: {len(ranking_report['rejected_candidates'])}")

    return 0

if __name__ == "__main__":
    exit(main())