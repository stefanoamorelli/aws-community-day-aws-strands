# AWS Strands Demos

## Overview
This directory contains demonstration scripts for AWS Community Day presentation, showcasing AWS Strands multi-agent capabilities.

## Directory Structure

```
demos/
├── swarm/              # Economic Swarm demos (multi-agent orchestration)
│   ├── basic.py        # Simple swarm execution
│   ├── visual.py       # Enhanced visualization
│   ├── live.py         # Live presentation version
│   ├── interactive.py  # Step-by-step interactive demo
│   └── realtime.py     # Real-time monitoring
│
└── agents/             # Individual agent demos
    ├── market_analysis.py         # Basic market analysis
    ├── market_analysis_visual.py  # Visual market analysis
    ├── portfolio_risk.py          # Basic risk assessment
    └── portfolio_risk_visual.py   # Visual risk dashboard
```

## Economic Swarm Demos

### What Question Does the Swarm Answer?

**Main Query**: "Analyze the current economic environment and assess how it impacts specific companies (AAPL and JPM), then provide risk assessment and investment recommendations"

**Sub-questions**:
1. What are the current economic indicators? (GDP, unemployment, interest rates)
2. What risks do these indicators present?
3. How do these risks affect tech (AAPL) vs financial (JPM) sectors?
4. What investment actions should be taken?

### Swarm Demos

#### 1. Basic Demo (`demos/swarm/basic.py`)
- Simplest implementation
- Shows core swarm functionality
- Good for understanding basics

```bash
python demos/swarm/basic.py
```

#### 2. Visual Demo (`demos/swarm/visual.py`)
- Enhanced output formatting
- Clear data visualization
- Shows agent handoffs

```bash
python demos/swarm/visual.py
```

#### 3. Live Demo (`demos/swarm/live.py`)
- Typewriter effects
- Dramatic presentation style
- Perfect for live talks

```bash
python demos/swarm/live.py
```

#### 4. Interactive Demo (`demos/swarm/interactive.py`)
- Step-by-step execution
- Pause points for explanation
- Educational walkthrough

```bash
# Interactive mode (press Enter to advance)
python demos/swarm/interactive.py

# Auto mode (2-second delays)
python demos/swarm/interactive.py --auto
```

#### 5. Real-time Demo (`demos/swarm/realtime.py`)
- Live progress monitoring
- Activity matrix visualization
- Risk dashboard

```bash
python demos/swarm/realtime.py
```

## Individual Agent Demos

### Market Analysis Agent
Demonstrates clean, reusable agent architecture for financial analysis.

```bash
# Basic version
python demos/agents/market_analysis.py

# Visual version with dashboards
python demos/agents/market_analysis_visual.py
```

### Portfolio Risk Agent
Shows OOP design with state management for risk assessment.

```bash
# Basic version
python demos/agents/portfolio_risk.py

# Visual version with risk metrics
python demos/agents/portfolio_risk_visual.py
```

## Key Features Demonstrated

### 1. Multi-Agent Orchestration
- Coordinator delegates tasks to specialists
- Agents hand off work based on expertise
- Shared context between agents

### 2. Real Data Integration
- FRED MCP server for economic data
- Real-time Federal Reserve statistics
- Fallback to mock data if unavailable

### 3. Agent Collaboration Flow
```
User Query → Coordinator → Data Collector → FRED API
                ↓              ↓
           Risk Assessor ← Analyst
                ↓
          User Response
```

### 4. AWS Strands Capabilities
- Clean agent architecture
- Tool integration via decorators
- Type-safe communication
- State management
- Error handling

## Requirements

1. **Environment Variables**:
   ```bash
   export OPENAI_API_KEY="your-key"
   export FRED_API_KEY="your-fred-key"  # Optional
   ```

2. **FRED MCP Server** (for real data):
   - Server should be running at `/home/amorelli/development/fred-mcp-server/build/index.js`
   - Falls back to mock data if unavailable

3. **Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Presentation Tips

1. **Start with Interactive Demo** - Explains architecture step-by-step
2. **Show Visual Demo** - Demonstrates actual execution with clear output
3. **Use Live Demo** - For dramatic effect during key points
4. **Show Individual Agents** - To explain modularity and reusability

## Troubleshooting

- **"OpenAI API key required"**: Set `OPENAI_API_KEY` environment variable
- **FRED data shows mock values**: FRED MCP server not running or accessible
- **Import errors**: Run from project root or ensure proper Python path

## Summary

These demos showcase AWS Strands' ability to:
- Orchestrate multiple specialized AI agents
- Integrate real-world data sources via MCP
- Solve complex analytical problems through collaboration
- Provide actionable insights for real-world decisions
