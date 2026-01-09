"""
CLI Smoke Tests

This module tests the Foliorank CLI functionality through subprocess calls
to ensure end-to-end operation works correctly.
"""

import sys
import os
import json
import tempfile
import subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_cli_plan_validate_simulate_roundtrip():
    """Test complete CLI roundtrip: plan -> validate -> simulate."""
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as portfolio_file:
        portfolio_path = portfolio_file.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as result_file:
        result_path = result_file.name

    try:
        # Test plan command
        cmd = [
            sys.executable, '-m', 'foliorank.cli',
            'plan', 'balanced portfolio for simulation',
            '--out', portfolio_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..', '..'))
        assert result.returncode == 0, f"Plan command failed: {result.stderr}"

        # Verify portfolio file was created and is valid JSON
        with open(portfolio_path, 'r') as f:
            portfolio_data = json.load(f)

        assert 'portfolio_name' in portfolio_data
        assert 'allocation' in portfolio_data
        print("✓ CLI plan command successful")

        # Test validate command
        cmd = [
            sys.executable, '-m', 'foliorank.cli',
            'validate', '--in', portfolio_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..', '..'))
        assert result.returncode == 0, f"Validate command failed: {result.stderr}"
        print("✓ CLI validate command successful")

        # Test simulate command
        cmd = [
            sys.executable, '-m', 'foliorank.cli',
            'simulate', '--in', portfolio_path, '--out', result_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..', '..'))
        assert result.returncode == 0, f"Simulate command failed: {result.stderr}"

        # Verify simulation result
        with open(result_path, 'r') as f:
            simulation_data = json.load(f)

        assert 'expected_return' in simulation_data
        assert 'volatility' in simulation_data
        assert simulation_data['simulation_version'] == 'v0.1'
        print("✓ CLI simulate command successful")

    finally:
        # Clean up temporary files
        for path in [portfolio_path, result_path]:
            if os.path.exists(path):
                os.unlink(path)


def test_cli_rank_two_results():
    """Test CLI ranking using canonical bundle format."""
    # Create a rank bundle with two portfolios
    rank_bundle = {
        "version": "v0.1",
        "items": [
            {
                "id": "high_return",
                "portfolio": {
                    "portfolio_name": "High Return Portfolio",
                    "allocation": [
                        {"asset": "Large-cap equities", "weight": 70},
                        {"asset": "Government bonds", "weight": 25},
                        {"asset": "Cash equivalents", "weight": 5}
                    ],
                    "rationale": "Portfolio focused on equity exposure"
                }
            },
            {
                "id": "conservative",
                "portfolio": {
                    "portfolio_name": "Conservative Portfolio",
                    "allocation": [
                        {"asset": "Government bonds", "weight": 70},
                        {"asset": "Cash equivalents", "weight": 30}
                    ],
                    "rationale": "Conservative bond-focused portfolio"
                }
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as bundle_file:
        bundle_path = bundle_file.name
        json.dump(rank_bundle, bundle_file)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as ranking_file:
        ranking_path = ranking_file.name

    try:
        # Test rank command
        cmd = [
            sys.executable, '-m', 'foliorank.cli',
            'rank', '--in', bundle_path, '--out', ranking_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..', '..'))
        assert result.returncode == 0, f"Rank command failed: {result.stderr}"

        # Verify ranking result
        with open(ranking_path, 'r') as f:
            ranking_data = json.load(f)

        assert ranking_data['schema_version'] == 'ranking_report_v1'
        assert ranking_data['total_candidates'] == 2
        assert len(ranking_data['ranked_items']) == 2

        # Check that ranking is deterministic
        items = ranking_data['ranked_items']
        assert all('rank' in item for item in items)
        assert all('total_score' in item for item in items)

        # High return should rank higher than conservative
        high_return_item = next(item for item in items if 'High Return' in item['portfolio_name'])
        conservative_item = next(item for item in items if 'Conservative' in item['portfolio_name'])
        assert high_return_item['rank'] < conservative_item['rank']  # Lower rank number = better

        print("✓ CLI rank command successful")

    finally:
        # Clean up temporary files
        for path in [bundle_path, ranking_path]:
            if os.path.exists(path):
                os.unlink(path)


def test_cli_validation_failure():
    """Test that CLI validation properly rejects invalid portfolios."""
    # Create invalid portfolio (weights don't sum to 100)
    invalid_portfolio = {
        'portfolio_name': 'Invalid Portfolio',
        'allocation': [
            {'asset': 'Large-cap equities', 'weight': 50},
            {'asset': 'Government bonds', 'weight': 30}  # Only 80 total
        ],
        'rationale': 'This is invalid'
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as portfolio_file:
        portfolio_path = portfolio_file.name
        json.dump(invalid_portfolio, portfolio_file)

    try:
        # Test validate command on invalid portfolio
        cmd = [
            sys.executable, '-m', 'foliorank.cli',
            'validate', '--in', portfolio_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..', '..'))
        assert result.returncode != 0, "Validate should have failed for invalid portfolio"
        print("✓ CLI validation correctly rejects invalid portfolios")

    finally:
        os.unlink(portfolio_path)


if __name__ == "__main__":
    test_cli_plan_validate_simulate_roundtrip()
    test_cli_rank_two_results()
    test_cli_validation_failure()

    print("\n🎉 All CLI tests passed!")