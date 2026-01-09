Foliorank SDK v0.1

API Specification (Simulation-Only)

Status
  •  Version: v0.1.0
  •  Scope: Simulation-only
  •  Execution: Not supported
  •  Intended use: Research, experimentation, and structured analysis

⸻

1. Overview

Foliorank SDK is a Python-based framework for constructing, simulating, and inspecting portfolio configurations using large language models (LLMs) under strict behavioral constraints.

The SDK is designed to:
  •  Produce structured portfolio specifications
  •  Run deterministic simulations on historical data
  •  Generate explanatory and analytical outputs
  •  Maintain complete reproducibility and auditability

The SDK explicitly does not perform real-world trading activities.

⸻

2. Design Principles
  •  Simulation-only: No real execution paths exist.
  •  Behavioral constraints: All LLM interactions are governed by MCP rules.
  •  Determinism: Identical inputs must produce identical outputs.
  •  Reproducibility: All decisions are logged with cryptographic hashes.
  •  Separation of concerns: Planning, simulation, and auditing are isolated.

⸻

3. Core Components

3.1 ControlledAgent

The primary interface for interacting with the SDK.

class ControlledAgent:
    async def plan(prompt: str) -> PortfolioSpec
    async def simulate(portfolio: PortfolioSpec, dataset_version: str) -> SimulationResult
    async def analyze_market(prompt: str, dataset_version: str) -> AnalysisOutput
    async def explain(portfolio: PortfolioSpec) -> ExplanationOutput

All methods:
  •  Pass through MCP pre-checks
  •  Produce schema-validated outputs
  •  Trigger audit logging

⸻

3.2 Mission Control Protocol (MCP)

A mandatory behavioral control layer.

Allowed actions
  •  portfolio_design
  •  market_analysis
  •  simulation
  •  explanation
  •  audit

Disallowed actions
  •  Any form of real-world execution
  •  Any recommendation or advisory language
  •  Any performance guarantee
  •  Any broker, exchange, or transaction reference

Violations result in:
  •  Action rejection
  •  Safe fallback output
  •  Audit record creation

⸻

3.3 Simulation Engine
  •  Operates on versioned historical datasets
  •  Deterministic by default
  •  Produces structured metrics (returns, volatility, allocation changes)
  •  No forward-looking or predictive claims

⸻

3.4 Audit & Reproducibility

Every interaction generates:
  •  Input hash (SHA-256)
  •  Output hash (SHA-256)
  •  MCP validation result
  •  Timestamp

This enables:
  •  Replay
  •  Verification
  •  External inspection

⸻

4. Data Model (Simplified)

{
  "portfolio": {
    "assets": [
      { "symbol": "XYZ", "weight": 0.25 }
    ],
    "constraints": {
      "max_weight": 0.3
    }
  }
}

All schemas are versioned and validated at runtime.

⸻

5. Explicit Non-Goals

The SDK does not:
  •  Connect to brokers or exchanges
  •  Execute or schedule trades
  •  Store user financial data
  •  Provide recommendations or guarantees
  •  Optimize for real-world outcomes

⸻

6. Compliance Note

Foliorank SDK is a technical simulation framework.
Any integration with external systems occurs outside this SDK and is not part of its scope.

⸻