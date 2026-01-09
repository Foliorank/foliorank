# Foliorank SDK Examples

This document lists the example scripts included with Foliorank SDK, demonstrating key functionality for newcomers.

## Overview

All examples are simulation-only and educational in nature. They demonstrate the complete pipeline from natural language input through MCP validation, schema checking, deterministic simulation, and result comparison.

## Example Scripts

### 01_plan_from_text.py
**Demonstrates**: Converting natural language to structured portfolio specifications
- Shows MCP enforcement on user input
- Displays schema validation
- Outputs neutral, educational rationale

**Run**:
```bash
python examples/01_plan_from_text.py
```

**Expected Output**:
```
Foliorank SDK Example 1: Plan from Text
==================================================
Input description: I want a balanced portfolio for long-term simulation purposes

✅ Portfolio planning successful!

Generated portfolio:
  Name: Balanced Simulation Portfolio
  Allocation:
    - Large-cap equities: 50%
    - Government bonds: 40%
    - Cash equivalents: 10%
  Rationale: This simulation portfolio provides balance across equity, bond, and cash asset classes for moderate risk and return expectations.
```

### 02_simulate_from_template.py
**Demonstrates**: Loading portfolio templates and running deterministic simulations
- Shows template validation
- Demonstrates reproducible simulation results
- Displays performance metrics

**Run**:
```bash
python examples/02_simulate_from_template.py
```

**Expected Output**:
```
Foliorank SDK Example 2: Simulate from Template
==================================================
Loaded template: Balanced Simulation Portfolio

✅ Template import successful!

Simulation results:
  Expected return: 4.8%
  Volatility: 9.6%
  Time horizon: long_term
  Version: v0.1
```

### 03_export_import_roundtrip.py
**Demonstrates**: Safe export and import of simulation results
- Shows complete audit trail preservation
- Demonstrates bundle validation
- Illustrates file-based storage/sharing

**Run**:
```bash
python examples/03_export_import_roundtrip.py
```

**Expected Output**:
```
Foliorank SDK Example 3: Export/Import Roundtrip
==================================================
Created portfolio: Conservative Simulation Portfolio

Ran simulation with results:
  Expected return: 3.5%

✅ Exported results to bundle
  Bundle keys: ['portfolio_spec', 'simulation_result', 'audit_hash', 'schema_version', 'mcp_version']

Saved bundle to temporary file: ...

✅ Imported bundle successfully!
Imported data matches original:
  Portfolio: Conservative Simulation Portfolio
  Simulation return: 3.5%
  Audit hash: ...
```

### 04_rank_two_portfolios.py
**Demonstrates**: Comparing and ranking simulation results using canonical rank bundle format
- Shows deterministic scoring algorithm
- Displays neutral comparison language
- Illustrates ranking report structure
- Uses the preferred rank bundle JSON format

**Rank Input Formats Supported**:
1. **Canonical Bundle Format** (preferred):
   ```json
   {
     "version": "v0.1",
     "items": [
       {"id": "portfolio_1", "portfolio": <portfolio_spec>},
       {"id": "portfolio_2", "portfolio": <portfolio_spec>}
     ]
   }
   ```
2. **Single Portfolio** (auto-wrapped): CLI automatically wraps single portfolio specs into bundle format

**Run**:
```bash
python examples/04_rank_two_portfolios.py
```

**Expected Output**:
```
Foliorank SDK Example 4: Rank Two Portfolios
==================================================
Creating two portfolios for comparison...
Portfolio 1: Growth Simulation Portfolio
  Expected return: 5.7%
Portfolio 2: Conservative Simulation Portfolio
  Expected return: 3.5%

🎯 Ranking Results:
Total candidates: 2
Valid candidates: 2

Rank 1: Growth Simulation Portfolio
  Score: 55.0/100
  Notes: Portfolio 'Growth Simulation Portfolio' achieved a ranking score of 55.0. Simulation showed expected return of 5.7% with volatility of 11.8%. This ranking reflects simulation-based comparison metrics.

Rank 2: Conservative Simulation Portfolio
  Score: 50.0/100
  Notes: Portfolio 'Conservative Simulation Portfolio' achieved a ranking score of 50.0. Simulation showed expected return of 3.5% with volatility of 6.0%. This ranking reflects simulation-based comparison metrics.
```

## Template Files

The SDK includes pre-built portfolio templates in `sdk/foliorank/templates/`:

- `balanced.json`: Moderate risk-return profile
- `growth.json`: Higher equity exposure
- `conservative.json`: Stability-focused with bonds/cash

These templates can be loaded and modified for custom simulations.

## CLI Usage

For command-line usage, see the main README.md Quickstart section. The CLI provides the same functionality as the Python examples but in a scriptable format.

## Notes

- All examples are deterministic - running them multiple times produces identical results
- No network calls or external dependencies are required
- All operations are simulation-only and educational in nature
- Asset classes remain abstract (no real financial symbols)