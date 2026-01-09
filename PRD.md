Foliorank

Product Requirements Document (PRD)
Version: v0.1
Status: Draft
Language: English

⸻

1. Overview

Foliorank is a software system designed to explore, structure, and simulate portfolio compositions using large language models (LLMs) under strict behavioral constraints.

The system focuses on portfolio representation, simulation, comparison, and reproducibility, without performing or facilitating real-world financial transactions.

Foliorank does not provide financial advice, trading execution, or performance guarantees.
All outputs are generated within a controlled, simulation-only environment.

⸻

2. Problem Statement

Many existing tools that involve financial data combine analysis, execution, and recommendation into a single workflow. This coupling makes it difficult to:
  •  Clearly separate simulation from execution
  •  Reproduce decision processes consistently
  •  Compare portfolio constructions under identical conditions
  •  Apply behavioral constraints to LLM-generated outputs

Foliorank addresses this by providing a structured, simulation-only framework that emphasizes transparency, reproducibility, and controlled AI behavior.

⸻

3. Goals

Primary Goals
  •  Enable structured portfolio composition using LLMs
  •  Ensure all AI outputs follow predefined behavioral constraints
  •  Support deterministic, reproducible simulations
  •  Allow comparison and ranking of portfolio artifacts based on observable metrics
  •  Maintain a clear boundary between simulation and real-world execution

Non-Goals
  •  Real trading or broker integration
  •  Investment recommendations or advice
  •  User financial data storage
  •  Profit optimization or performance claims

⸻

4. Core Principles
  1.  Simulation-Only
All portfolio outputs exist only as simulated artifacts.
  2.  Behavioral Control
LLM outputs are constrained by explicit, enforceable rules.
  3.  Reproducibility
Identical inputs must produce identical outputs.
  4.  Neutrality
The system avoids evaluative or prescriptive language.
  5.  Separation of Concerns
SDK, cloud services, and UI have distinct responsibilities.

⸻

5. System Architecture (High-Level)

User Interface (Chat / CLI / Web)
        ↓
Controlled Agent Layer
        ↓
MCP Enforcement Layer
        ↓
Planning & Simulation Engine
        ↓
Audit & Reproducibility Layer


⸻

6. Product Components

6.1 SDK (Open Source)

Purpose
Provide a local or cloud-agnostic framework for controlled portfolio simulation.

Responsibilities
  •  MCP (Model Control Protocol) enforcement
  •  Portfolio schema validation
  •  Deterministic simulation
  •  Audit logging with cryptographic hashes
  •  LLM provider abstraction

Explicit Exclusions
  •  Broker APIs
  •  Exchange connectivity
  •  Execution logic
  •  User account or payment handling

⸻

6.2 MCP (Model Control Protocol)

Purpose
Define and enforce allowed and forbidden AI behaviors.

Key Capabilities
  •  Action whitelisting
  •  Term and pattern filtering
  •  Input/output schema enforcement
  •  Pre- and post-response validation

Design Intent
MCP is an enforcement mechanism, not documentation-only guidance.

⸻

6.3 Simulation Engine

Purpose
Generate reproducible portfolio simulations using versioned market data.

Characteristics
  •  Deterministic execution
  •  No real-time data dependency
  •  Versioned datasets
  •  Output as structured artifacts (JSON)

⸻

6.4 Audit & Reproducibility Layer

Purpose
Ensure traceability and consistency.

Features
  •  SHA256 hashes of inputs and outputs
  •  Timestamped records
  •  Read-only audit logs
  •  No mutable historical state

⸻

6.5 Cloud Services (Optional / Paid)

Purpose
Provide aggregation, comparison, and long-term storage of portfolio artifacts.

Responsibilities
  •  Portfolio ranking and comparison
  •  Simulation result storage
  •  Reporting and visualization
  •  Access control and isolation

Not Required for SDK Usage

⸻

7. User Interaction Model

Interaction Style
  •  Chat-based or CLI-based interaction
  •  Structured prompts mapped to predefined actions
  •  No free-form execution commands

Output Types
  •  Portfolio specifications
  •  Simulation summaries
  •  Comparative metrics
  •  Explanatory descriptions (non-prescriptive)

⸻

8. Data Model (Conceptual)
  •  PortfolioSpec
  •  SimulationResult
  •  AuditEntry
  •  MCPViolationRecord

No personal or financial identifiers are stored.

⸻

9. Compliance & Safety Considerations
  •  No real trading functionality
  •  No financial advice generation
  •  Explicit disclaimers at system boundaries
  •  Behavioral constraints enforced at runtime
  •  Server-side validation as secondary protection

⸻

10. MVP Scope

Included
  •  SDK with MCP enforcement
  •  Deterministic simulation engine
  •  Audit logging
  •  Basic chat/CLI interface
  •  Portfolio comparison logic

Excluded
  •  Mobile apps
  •  Real-time market feeds
  •  Execution services
  •  Payment or subscription systems

⸻

11. Success Criteria
  •  All outputs comply with MCP rules
  •  Reproducible results across environments
  •  Clear separation between simulation and execution
  •  No ambiguous or prescriptive language in outputs
  •  System can be safely open-sourced

⸻

12. Future Considerations (Out of Scope)
  •  External API integrations (read-only)
  •  Advanced visualization tools
  •  Educational content layers
  •  Optional cloud-based extensions

⸻

13. Summary

Foliorank is a controlled, simulation-only framework for exploring portfolio structures using LLMs under explicit behavioral constraints.
Its value lies in structure, reproducibility, and safety, rather than execution or optimization.

⸻