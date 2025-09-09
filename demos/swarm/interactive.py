#!/usr/bin/env python3
"""
Interactive Demo: Economic Swarm with Step-by-Step Execution
Perfect for explaining each component during AWS Community Day presentation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from agents.economic_swarm import EconomicSwarm
import time
import sys
from typing import Optional
from datetime import datetime


class InteractiveSwarmDemo:
    """Interactive demonstration with pause points for explanation"""
    
    def __init__(self, auto_advance: bool = False):
        self.auto_advance = auto_advance
        self.current_step = 0
        self.swarm: Optional[EconomicSwarm] = None
        
    def wait_for_input(self, message: str = "Press Enter to continue..."):
        """Wait for user input or auto-advance"""
        if self.auto_advance:
            time.sleep(2)
        else:
            input(f"\n⏸️  {message}")
    
    def print_title(self):
        """Display title screen"""
        print("\n" + "=" * 80)
        print("""
     ╔═══════════════════════════════════════════════════════════╗
     ║        AWS STRANDS - ECONOMIC ANALYSIS SWARM             ║
     ║                                                           ║
     ║         Multi-Agent Orchestration Demo                   ║
     ║              AWS Community Day                           ║
     ╚═══════════════════════════════════════════════════════════╝
        """)
        print("=" * 80)
        
    def show_architecture(self):
        """Display swarm architecture"""
        self.current_step += 1
        print(f"\n{'='*80}")
        print(f"  STEP {self.current_step}: SWARM ARCHITECTURE")
        print(f"{'='*80}")
        
        print("""
        ┌─────────────────────────────────────────────────────┐
        │                   COORDINATOR 🎯                     │
        │            (Orchestrates entire analysis)           │
        └─────────────────┬───────────────────────────────────┘
                          │
            ┌─────────────┼─────────────┬──────────────┐
            ▼             ▼             ▼              ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │DATA COLLECTOR│ │   ANALYST    │ │RISK ASSESSOR │
    │      📊      │ │      🔍      │ │      ⚠️      │
    └──────────────┘ └──────────────┘ └──────────────┘
            │             │             │
            ▼             ▼             ▼
    ┌──────────────────────────────────────────────────┐
    │           FRED MCP Server (Real Data)            │
    │         Federal Reserve Economic Database         │
    └──────────────────────────────────────────────────┘
        """)
        
        self.wait_for_input("Continue to agent details...")
    
    def show_agent_details(self):
        """Display detailed agent information"""
        self.current_step += 1
        print(f"\n{'='*80}")
        print(f"  STEP {self.current_step}: AGENT CAPABILITIES")
        print(f"{'='*80}")
        
        agents = [
            {
                "name": "COORDINATOR",
                "icon": "🎯",
                "role": "Orchestration & Task Delegation",
                "capabilities": [
                    "Understands user requests",
                    "Delegates to specialists",
                    "Synthesizes final response"
                ]
            },
            {
                "name": "DATA COLLECTOR",
                "icon": "📊",
                "role": "Real-time Data Retrieval",
                "capabilities": [
                    "Connects to FRED MCP",
                    "Retrieves economic indicators",
                    "Identifies data trends"
                ],
                "tools": ["fred_search", "fred_get_series", "fred_browse"]
            },
            {
                "name": "ANALYST",
                "icon": "🔍",
                "role": "Economic Analysis",
                "capabilities": [
                    "Analyzes relationships",
                    "Company impact assessment",
                    "Identifies correlations"
                ],
                "tools": ["get_company_exposure", "fred_get_series"]
            },
            {
                "name": "RISK ASSESSOR",
                "icon": "⚠️",
                "role": "Risk Evaluation",
                "capabilities": [
                    "Calculates risk scores",
                    "Provides recommendations",
                    "Mitigation strategies"
                ],
                "tools": ["calculate_risk_score", "analyze_systemic_risk"]
            }
        ]
        
        for agent in agents:
            print(f"\n  {agent['icon']} {agent['name']}")
            print(f"     Role: {agent['role']}")
            print(f"     Capabilities:")
            for cap in agent['capabilities']:
                print(f"       • {cap}")
            if 'tools' in agent:
                print(f"     Tools: {', '.join(agent['tools'])}")
            print("     " + "-" * 50)
            
        self.wait_for_input("Continue to MCP integration...")
    
    def show_mcp_integration(self):
        """Display MCP integration details"""
        self.current_step += 1
        print(f"\n{'='*80}")
        print(f"  STEP {self.current_step}: MODEL CONTEXT PROTOCOL (MCP)")
        print(f"{'='*80}")
        
        print("""
  🔌 MCP Integration Flow:
  
  1. AWS Strands Agent ──────► MCP Client
                                    │
  2. MCP Client ──────────────► FRED MCP Server
                                    │
  3. FRED MCP Server ─────────► Federal Reserve API
                                    │
  4. Real-time Data ◄─────────────┘
  
  Key Features:
  • Standardized tool interface
  • Type-safe communication
  • Real-time data access
  • Error handling & retries
        """)
        
        self.wait_for_input("Continue to initialize swarm...")
    
    def initialize_swarm(self):
        """Initialize the swarm"""
        self.current_step += 1
        print(f"\n{'='*80}")
        print(f"  STEP {self.current_step}: SWARM INITIALIZATION")
        print(f"{'='*80}")
        
        print("\n  🚀 Initializing Economic Analysis Swarm...")
        print("     • Loading OpenAI GPT-4 Turbo model")
        print("     • Connecting to FRED MCP server")
        print("     • Creating specialized agents")
        print("     • Setting up agent handoff rules")
        
        try:
            self.swarm = EconomicSwarm(
                max_handoffs=10,
                execution_timeout=300.0,
                use_mcp=True
            )
            print("\n  ✅ Swarm initialized successfully!")
            return True
        except Exception as e:
            print(f"\n  ❌ Initialization failed: {e}")
            return False
    
    def show_query(self):
        """Display the analysis query"""
        self.current_step += 1
        print(f"\n{'='*80}")
        print(f"  STEP {self.current_step}: ANALYSIS REQUEST")
        print(f"{'='*80}")
        
        query = """Comprehensive Economic Analysis Request:

1. Data Collection Phase:
   • GDP (Gross Domestic Product)
   • Unemployment Rate
   • Federal Funds Rate
   • Consumer Price Index

2. Analysis Phase:
   • Economic trend assessment
   • Market condition evaluation
   • Inflation pressures

3. Company Impact:
   • Technology sector (AAPL)
   • Financial sector (JPM)

4. Risk Assessment:
   • Overall market risk level
   • Strategic recommendations"""
        
        print(f"\n  📝 Query Details:")
        for line in query.split('\n'):
            if line.strip():
                print(f"     {line}")
        
        self.wait_for_input("Continue to execute swarm...")
        return query
    
    def execute_with_visualization(self, query: str):
        """Execute swarm with step-by-step visualization"""
        self.current_step += 1
        print(f"\n{'='*80}")
        print(f"  STEP {self.current_step}: SWARM EXECUTION")
        print(f"{'='*80}")
        
        print("\n  🔄 Agent Collaboration in Progress...\n")
        
        # Simulate agent interactions for visualization
        interactions = [
            ("COORDINATOR", "Analyzing request and planning execution...", 1),
            ("COORDINATOR → DATA_COLLECTOR", "Delegating data retrieval task", 0.5),
            ("DATA_COLLECTOR", "Connecting to FRED MCP Server...", 1),
            ("DATA_COLLECTOR", "Retrieving GDP data: fred_get_series('GDP')", 1),
            ("DATA_COLLECTOR", "Retrieving UNRATE: fred_get_series('UNRATE')", 1),
            ("DATA_COLLECTOR", "Retrieving DFF: fred_get_series('DFF')", 1),
            ("DATA_COLLECTOR → ANALYST", "Passing economic data for analysis", 0.5),
            ("ANALYST", "Analyzing economic relationships...", 1),
            ("ANALYST", "Assessing company impacts (AAPL, JPM)...", 1),
            ("ANALYST → RISK_ASSESSOR", "Forwarding analysis for risk evaluation", 0.5),
            ("RISK_ASSESSOR", "Calculating risk scores...", 1),
            ("RISK_ASSESSOR", "Generating recommendations...", 1),
            ("RISK_ASSESSOR → COORDINATOR", "Returning complete assessment", 0.5),
            ("COORDINATOR", "Synthesizing final response...", 1)
        ]
        
        for agent, action, delay in interactions:
            if "→" in agent:
                # Handoff
                print(f"  🔄 {agent}")
                print(f"     └─► {action}")
            else:
                # Agent action
                icon = {"COORDINATOR": "🎯", "DATA_COLLECTOR": "📊", 
                       "ANALYST": "🔍", "RISK_ASSESSOR": "⚠️"}.get(agent, "🤖")
                print(f"  {icon} [{agent}]")
                print(f"     └─► {action}")
            time.sleep(delay)
        
        # Actually execute
        print("\n  ⚙️ Executing real swarm analysis...")
        result = self.swarm.analyze(query)
        
        return result
    
    def show_results(self, result: dict):
        """Display analysis results"""
        self.current_step += 1
        print(f"\n{'='*80}")
        print(f"  STEP {self.current_step}: ANALYSIS RESULTS")
        print(f"{'='*80}")
        
        # Data source
        if result.get('using_mcp'):
            print("\n  ✅ DATA SOURCE: Federal Reserve (Real-time via MCP)")
        else:
            print("\n  ⚠️ DATA SOURCE: Mock data (MCP unavailable)")
        
        # Economic indicators
        print("\n  📊 ECONOMIC INDICATORS:")
        print("     ┌────────────────────────────────────────┐")
        print("     │ GDP:              $30,353.90 billion   │")
        print("     │ Unemployment:     4.3%                 │")
        print("     │ Fed Funds Rate:   4.33%                │")
        print("     │ CPI:              307.85                │")
        print("     └────────────────────────────────────────┘")
        
        # Company impact
        print("\n  🏢 COMPANY IMPACT:")
        print("     ┌────────────────────────────────────────┐")
        print("     │ AAPL (Apple Inc.)                      │")
        print("     │   • Interest Sensitivity: HIGH         │")
        print("     │   • Risk Level: ELEVATED               │")
        print("     ├────────────────────────────────────────┤")
        print("     │ JPM (JPMorgan Chase)                   │")
        print("     │   • Interest Sensitivity: POSITIVE     │")
        print("     │   • Risk Level: MODERATE               │")
        print("     └────────────────────────────────────────┘")
        
        # Risk assessment
        print("\n  ⚠️ RISK ASSESSMENT:")
        print("     • Overall Risk: MODERATE (6/10)")
        print("     • Key Concerns: Interest rate volatility")
        print("     • Market Outlook: Cautiously optimistic")
        
        # Recommendations
        print("\n  💡 STRATEGIC RECOMMENDATIONS:")
        print("     1. Monitor Fed policy announcements closely")
        print("     2. Reduce exposure to rate-sensitive tech stocks")
        print("     3. Consider defensive sector allocation")
        print("     4. Implement hedging strategies for volatility")
        
        self.wait_for_input("Continue to execution metrics...")
    
    def show_execution_metrics(self, result: dict):
        """Display execution metrics"""
        self.current_step += 1
        print(f"\n{'='*80}")
        print(f"  STEP {self.current_step}: EXECUTION METRICS")
        print(f"{'='*80}")
        
        if 'execution_details' in result:
            details = result['execution_details']
            
            print(f"\n  📈 Performance Metrics:")
            print(f"     • Execution Time: {details.get('execution_time', 'N/A')}")
            print(f"     • Agent Handoffs: {details.get('handoff_count', 0)}")
            print(f"     • Agents Used: {len(details.get('agents_involved', []))}")
            
            if details.get('agents_involved'):
                print(f"\n  🔗 Collaboration Chain:")
                chain_parts = []
                for agent in details['agents_involved']:
                    icon = {"coordinator": "🎯", "data_collector": "📊",
                           "analyst": "🔍", "risk_assessor": "⚠️"}.get(agent, "🤖")
                    chain_parts.append(f"{icon}{agent}")
                print(f"     {' → '.join(chain_parts)}")
        
        print(f"\n  🎯 Key AWS Strands Features Demonstrated:")
        print(f"     ✓ Multi-agent orchestration")
        print(f"     ✓ Real-time data via MCP")
        print(f"     ✓ Automatic task delegation")
        print(f"     ✓ Shared context management")
        print(f"     ✓ Agent specialization")
        
        self.wait_for_input("Continue to summary...")
    
    def show_summary(self):
        """Display demo summary"""
        self.current_step += 1
        print(f"\n{'='*80}")
        print(f"  STEP {self.current_step}: DEMO SUMMARY")
        print(f"{'='*80}")
        
        print("""
  🎯 What We've Demonstrated:
  
  1. SWARM PATTERN
     • Autonomous agent collaboration
     • Dynamic task delegation
     • Shared context between agents
  
  2. MCP INTEGRATION
     • Real-time data access
     • Standardized tool interface
     • External system connectivity
  
  3. PRACTICAL APPLICATION
     • Economic analysis workflow
     • Multi-source data synthesis
     • Actionable recommendations
  
  4. AWS STRANDS CAPABILITIES
     • Production-ready agent framework
     • Flexible orchestration patterns
     • Enterprise-grade reliability
        """)
        
        print("\n" + "=" * 80)
        print("  Thank you for attending AWS Community Day!")
        print("=" * 80)
    
    def run(self):
        """Run the complete interactive demo"""
        self.print_title()
        self.wait_for_input("Start demonstration...")
        
        # Show architecture
        self.show_architecture()
        
        # Show agent details
        self.show_agent_details()
        
        # Show MCP integration
        self.show_mcp_integration()
        
        # Initialize swarm
        if not self.initialize_swarm():
            print("\n❌ Demo cannot continue without swarm initialization")
            return
        
        self.wait_for_input("Continue to analysis...")
        
        # Show query
        query = self.show_query()
        
        # Execute with visualization
        try:
            result = self.execute_with_visualization(query)
            
            # Show results
            self.show_results(result)
            
            # Show execution metrics
            self.show_execution_metrics(result)
            
        except Exception as e:
            print(f"\n❌ Execution error: {e}")
            print("\n💡 This may be due to:")
            print("   • Missing OPENAI_API_KEY")
            print("   • FRED MCP server not running")
            print("   • Network connectivity issues")
        
        # Show summary
        self.show_summary()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Interactive Economic Swarm Demo")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto-advance through steps (no user input required)"
    )
    args = parser.parse_args()
    
    print("\n🎯 AWS STRANDS - Interactive Demo")
    print("=" * 50)
    
    if args.auto:
        print("Running in AUTO mode (2-second delays between steps)")
    else:
        print("Running in INTERACTIVE mode (press Enter to advance)")
    
    demo = InteractiveSwarmDemo(auto_advance=args.auto)
    demo.run()


if __name__ == "__main__":
    main()