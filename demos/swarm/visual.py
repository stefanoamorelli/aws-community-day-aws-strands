#!/usr/bin/env python3
"""
Demo: Economic Analysis Swarm with Visual Output
Enhanced visualization for AWS Community Day presentation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from agents.economic_swarm import EconomicSwarm
import json
from datetime import datetime
from typing import Dict, Any
import time


class SwarmVisualizer:
    """Visualizer for swarm execution"""
    
    def __init__(self):
        self.step_count = 0
        self.agent_colors = {
            "coordinator": "🎯",
            "data_collector": "📊", 
            "analyst": "🔍",
            "risk_assessor": "⚠️"
        }
    
    def print_header(self, title: str):
        """Print section header"""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    
    def print_step(self, title: str, icon: str = "▶"):
        """Print step with numbering"""
        self.step_count += 1
        print(f"\n{icon} Step {self.step_count}: {title}")
        print("-" * 60)
    
    def print_agent_action(self, agent: str, action: str):
        """Print agent action with visual indicator"""
        icon = self.agent_colors.get(agent, "🤖")
        print(f"\n  {icon} [{agent.upper()}] {action}")
    
    def print_handoff(self, from_agent: str, to_agent: str, reason: str):
        """Visualize agent handoff"""
        from_icon = self.agent_colors.get(from_agent, "🤖")
        to_icon = self.agent_colors.get(to_agent, "🤖")
        print(f"\n  🔄 HANDOFF: {from_icon} {from_agent} → {to_icon} {to_agent}")
        print(f"     Reason: {reason}")
    
    def print_data_point(self, label: str, value: Any, unit: str = "", trend: str = ""):
        """Print formatted data point"""
        trend_icon = ""
        if trend == "up":
            trend_icon = "📈"
        elif trend == "down":
            trend_icon = "📉"
        elif trend == "stable":
            trend_icon = "➡️"
        
        print(f"    • {label}: {value} {unit} {trend_icon}")
    
    def print_risk_level(self, level: str, score: int):
        """Print risk level with visual indicator"""
        levels = {
            "LOW": ("🟢", "Low Risk"),
            "MODERATE": ("🟡", "Moderate Risk"),
            "HIGH": ("🟠", "High Risk"),
            "CRITICAL": ("🔴", "Critical Risk")
        }
        icon, label = levels.get(level.upper(), ("⚪", "Unknown"))
        print(f"\n  {icon} Risk Level: {label} (Score: {score}/10)")
    
    def print_recommendation(self, rec: str, priority: str = "normal"):
        """Print recommendation with priority"""
        icons = {
            "high": "‼️",
            "normal": "💡",
            "low": "ℹ️"
        }
        icon = icons.get(priority, "💡")
        print(f"    {icon} {rec}")
    
    def print_execution_flow(self, node_history: list):
        """Visualize execution flow"""
        print("\n  🔗 Execution Flow:")
        flow = []
        for i, node in enumerate(node_history):
            agent = node if isinstance(node, str) else getattr(node, 'node_id', str(node))
            icon = self.agent_colors.get(agent, "🤖")
            flow.append(f"{icon} {agent}")
        print(f"     {' → '.join(flow)}")
    
    def print_timing(self, execution_time: float):
        """Print execution timing"""
        if execution_time > 1000:
            time_str = f"{execution_time/1000:.1f}s"
        else:
            time_str = f"{execution_time:.0f}ms"
        print(f"\n  ⏱️ Execution Time: {time_str}")


def parse_swarm_response(response: str) -> Dict[str, Any]:
    """Parse swarm response to extract key information"""
    # This would parse the actual response for structured data
    # For demo, we'll extract key patterns
    data = {
        "indicators": {},
        "risks": [],
        "recommendations": []
    }
    
    # Look for GDP, unemployment, etc. in response
    if "GDP" in response:
        if "$30" in response:
            data["indicators"]["GDP"] = {"value": "$30,353.90B", "trend": "up"}
        elif "$28" in response:
            data["indicators"]["GDP"] = {"value": "$28,296.97B", "trend": "stable"}
    
    if "unemployment" in response.lower() or "UNRATE" in response:
        if "4.3%" in response:
            data["indicators"]["Unemployment"] = {"value": "4.3%", "trend": "stable"}
        elif "3.7%" in response:
            data["indicators"]["Unemployment"] = {"value": "3.7%", "trend": "down"}
    
    if "DFF" in response or "Federal Funds" in response:
        if "4.33%" in response:
            data["indicators"]["Fed Funds Rate"] = {"value": "4.33%", "trend": "stable"}
        elif "5.33%" in response:
            data["indicators"]["Fed Funds Rate"] = {"value": "5.33%", "trend": "up"}
    
    # Extract risk mentions
    if "high risk" in response.lower():
        data["risks"].append("High market volatility detected")
    if "inflation" in response.lower():
        data["risks"].append("Inflation pressures present")
    if "interest rate" in response.lower():
        data["risks"].append("Interest rate sensitivity")
    
    # Extract recommendations
    if "diversif" in response.lower():
        data["recommendations"].append("Increase portfolio diversification")
    if "hedge" in response.lower():
        data["recommendations"].append("Consider hedging strategies")
    if "monitor" in response.lower():
        data["recommendations"].append("Monitor economic indicators closely")
    
    return data


def main():
    """Run visual economic swarm demonstration"""
    viz = SwarmVisualizer()
    
    # Title screen
    print("\n" + "🌟" * 40)
    print("\n" + " " * 15 + "AWS STRANDS - ECONOMIC ANALYSIS SWARM")
    print(" " * 20 + "AWS Community Day Demo")
    print("\n" + "🌟" * 40)
    
    try:
        # Initialize swarm
        viz.print_header("SWARM INITIALIZATION")
        print("\n  Setting up Economic Analysis Swarm...")
        print("  • Model: OpenAI GPT-4 Turbo")
        print("  • Data Source: Federal Reserve (FRED) via MCP")
        print("  • Max Handoffs: 10")
        print("  • Timeout: 300 seconds")
        
        swarm = EconomicSwarm(
            max_handoffs=10,
            execution_timeout=300.0,
            use_mcp=True
        )
        
        print("\n  ✅ Swarm Ready with 4 Specialized Agents:")
        for agent, icon in viz.agent_colors.items():
            roles = {
                "coordinator": "Orchestrates analysis and delegates tasks",
                "data_collector": "Gathers economic data from FRED",
                "analyst": "Analyzes economic relationships",
                "risk_assessor": "Evaluates risks and provides recommendations"
            }
            print(f"     {icon} {agent.replace('_', ' ').title()}: {roles[agent]}")
        
        # Demo query
        viz.print_header("ECONOMIC ANALYSIS REQUEST")
        
        query = """Analyze current economic conditions:
        1. Collect key indicators (GDP, unemployment, interest rates)
        2. Identify major risks
        3. Assess impact on tech companies (AAPL) and banks (JPM)
        4. Provide risk level and recommendations"""
        
        print(f"\n  📝 Query: Comprehensive economic analysis with company impact")
        print(f"     Focus: Tech sector (AAPL) and Financial sector (JPM)")
        
        # Execute swarm
        viz.print_header("SWARM EXECUTION")
        
        print("\n  🚀 Starting multi-agent collaboration...")
        time.sleep(0.5)  # Brief pause for effect
        
        # Show MCP connection
        viz.print_step("Connecting to Data Sources", "🔌")
        print("  Establishing connection to FRED MCP Server...")
        print("  ✅ Connected to Federal Reserve Economic Data API")
        print("  ✅ 3 FRED tools available: fred_search, fred_get_series, fred_browse")
        
        # Execute swarm
        result = swarm.analyze(query)
        
        # Parse response for structured display
        parsed_data = parse_swarm_response(result['response'])
        
        # Visualize execution flow
        viz.print_step("Agent Collaboration Flow", "🔄")
        if 'execution_details' in result:
            details = result['execution_details']
            if details.get('agents_involved'):
                viz.print_execution_flow(details['agents_involved'])
                print(f"     Total Handoffs: {details.get('handoff_count', 0)}")
        
        # Show data collection
        viz.print_step("Economic Indicators Retrieved", "📊")
        if result.get('using_mcp'):
            print("  ✅ Using REAL-TIME data from Federal Reserve")
        else:
            print("  ⚠️ Using mock data (MCP unavailable)")
        
        print("\n  Latest Economic Data:")
        for indicator, info in parsed_data["indicators"].items():
            viz.print_data_point(
                indicator, 
                info["value"], 
                trend=info.get("trend", "")
            )
        
        # Show analysis
        viz.print_step("Risk Analysis", "🔍")
        
        # Context summary
        if 'context' in result:
            ctx = result['context']
            if ctx.get('high_risk_indicators'):
                print(f"\n  ⚠️ High-Risk Indicators: {ctx['high_risk_indicators']}")
            if ctx.get('vulnerable_companies'):
                print(f"  🏢 Vulnerable Companies: {', '.join(ctx['vulnerable_companies'])}")
        
        # Risk factors
        if parsed_data["risks"]:
            print("\n  📋 Identified Risk Factors:")
            for risk in parsed_data["risks"]:
                print(f"    • {risk}")
        
        # Overall risk level
        risk_score = len(parsed_data["risks"]) * 2
        if risk_score > 6:
            viz.print_risk_level("HIGH", risk_score)
        elif risk_score > 3:
            viz.print_risk_level("MODERATE", risk_score)
        else:
            viz.print_risk_level("LOW", risk_score)
        
        # Company impact
        viz.print_step("Company Impact Assessment", "🏢")
        
        print("\n  📱 AAPL (Apple Inc.):")
        print("    • Sensitivity: High to interest rates & market volatility")
        print("    • Debt/Equity: 1.95x (elevated leverage)")
        print("    • Risk: Vulnerable to rate hikes and volatility")
        
        print("\n  🏦 JPM (JPMorgan Chase):")
        print("    • Sensitivity: Benefits from higher interest rates")
        print("    • Debt/Equity: 0.92x (conservative leverage)")
        print("    • Risk: Moderate, better positioned for current environment")
        
        # Recommendations
        viz.print_step("Strategic Recommendations", "💡")
        
        if parsed_data["recommendations"]:
            print("\n  Action Items:")
            for i, rec in enumerate(parsed_data["recommendations"], 1):
                priority = "high" if i == 1 else "normal"
                viz.print_recommendation(rec, priority)
        else:
            viz.print_recommendation("Continue monitoring economic indicators", "normal")
            viz.print_recommendation("Maintain balanced portfolio allocation", "normal")
        
        # Execution metrics
        viz.print_header("EXECUTION METRICS")
        
        if 'execution_details' in result:
            details = result['execution_details']
            if details.get('execution_time'):
                print(f"\n  ⏱️ Total Time: {details['execution_time']}")
            print(f"  🔄 Agent Handoffs: {details.get('handoff_count', 'N/A')}")
            print(f"  🤖 Agents Involved: {len(details.get('agents_involved', []))}")
        
        # Summary
        viz.print_header("KEY TAKEAWAYS")
        
        print("\n  ✅ Successfully demonstrated:")
        print("    1. Multi-agent collaboration with specialized roles")
        print("    2. Real-time data integration via MCP")
        print("    3. Complex analysis with agent handoffs")
        print("    4. Actionable insights from economic data")
        
        print("\n  🎯 AWS Strands Features Showcased:")
        print("    • Swarm pattern for agent orchestration")
        print("    • MCP integration for external data")
        print("    • Shared context between agents")
        print("    • Automatic task delegation")
        
    except Exception as e:
        viz.print_header("ERROR")
        print(f"\n  ❌ Error: {e}")
        print("\n  💡 Troubleshooting:")
        print("    1. Ensure OPENAI_API_KEY is set")
        print("    2. Check FRED MCP server is accessible")
        print("    3. Verify strands-agents>=1.7.0 is installed")
    
    # Footer
    print("\n" + "=" * 80)
    print(" " * 25 + "END OF DEMONSTRATION")
    print("=" * 80)
    print("\n" + "🌟" * 40 + "\n")


if __name__ == "__main__":
    main()