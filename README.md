Foliorank (Public Repository)

What is Foliorank?

Foliorank is an open-source framework for simulating and analyzing portfolio configurations using large language models under strict behavioral constraints.

The project focuses on:
  •  Structured portfolio representation
  •  Deterministic simulation
  •  Reproducible outputs
  •  Transparent audit trails

⸻

What this project does
  •  Converts natural language inputs into structured portfolio specifications
  •  Simulates portfolios using historical datasets
  •  Produces analytical and explanatory outputs
  •  Enforces strict action constraints through MCP
  •  Logs all decisions for reproducibility

⸻

What this project does NOT do
  •  Execute real-world transactions
  •  Connect to brokers or exchanges
  •  Provide recommendations or advice
  •  Guarantee outcomes
  •  Store sensitive personal data

⸻

Architecture (High Level)

User Input
   ↓
ControlledAgent
   ↓
MCP Validation
   ↓
Planner / Simulator
   ↓
Structured Output
   ↓
Audit Log (Hash + Timestamp)


⸻

Installation

pip install foliorank


⸻

Example (Simulation Only)

from foliorank import ControlledAgent

agent = ControlledAgent()

portfolio = await agent.plan(
    "Create a diversified portfolio for simulation purposes"
)

result = await agent.simulate(portfolio, dataset_version="v1.0")


⸻

Intended Audience
  •  Researchers
  •  Developers exploring LLM-driven systems
  •  Educational environments
  •  Experimental analysis workflows

⸻

License

MIT License

⸻