#!/usr/bin/env python3
"""
Demo: Economic Analysis Swarm
Shows multi-agent collaboration with AWS Strands
"""

from agents.economic_swarm import EconomicSwarm
import json


def print_execution_details(details):
    """Pretty print execution details"""
    print("\n🔄 Swarm Execution Details:")
    print(f"  • Agents involved: {', '.join(details['agents_involved'])}")
    print(f"  • Handoffs: {details['handoff_count']}")
    if details['execution_time']:
        print(f"  • Execution time: {details['execution_time']}")


def main():
    """Run economic swarm demonstrations"""
    print("=" * 70)
    print("🔍 AWS Strands - Economic Analysis Swarm Demo")
    print("=" * 70)
    
    try:
        # Initialize swarm
        print("\n⚙️ Initializing Economic Analysis Swarm...")
        swarm = EconomicSwarm(
            max_handoffs=10,
            execution_timeout=300.0,
            use_mcp=True  # Enable MCP for real FRED data
        )
        print("✅ Swarm initialized with 4 specialized agents:")
        print("  • Coordinator - Orchestrates the analysis")
        print("  • Data Collector - Gathers economic indicators (via FRED MCP)")
        print("  • Analyst - Analyzes relationships and impacts")
        print("  • Risk Assessor - Evaluates risks and recommendations")
        print("\n🔌 MCP Integration: Attempting to connect to FRED MCP server...\n")
        
        # Demo 1: Comprehensive Economic Analysis
        print("🤖 Demo 1: Comprehensive Economic Analysis")
        print("-" * 50)
        
        query = """Analyze the current economic environment:
        1. Collect all major economic indicators
        2. Identify which indicators pose the highest risk
        3. Analyze how these risks affect AAPL and JPM
        4. Provide risk assessment and recommendations"""
        
        print(f"Query: {query[:80]}...\n")
        
        result = swarm.analyze(query)
        print("Response:")
        print(result['response'])
        print_execution_details(result['execution_details'])
        if result.get('using_mcp'):
            print("  • Data source: FRED MCP Server (Real-time data)")
        else:
            print("  • Data source: Mock data (MCP unavailable)")
        print()
        
        # Demo 2: Company-Specific Analysis
        print("🤖 Demo 2: Multi-Company Risk Assessment")
        print("-" * 50)
        
        result = swarm.analyze_companies(
            companies=["AAPL", "JPM", "XOM"],
            indicators=["VIXCLS", "DFF", "CPI"]
        )
        
        print("Response:")
        print(result['response'])
        print_execution_details(result['execution_details'])
        print()
        
        # Demo 3: Market Risk Assessment
        print("🤖 Demo 3: Systemic Market Risk Assessment")
        print("-" * 50)
        
        result = swarm.assess_market_risk()
        
        print("Response:")
        print(result['response'])
        print_execution_details(result['execution_details'])
        print()
        
        # Show context summary
        print("📊 Analysis Context Summary")
        print("-" * 50)
        context = swarm.get_context_summary()
        print(json.dumps(context, indent=2))
        
        # Show high-risk indicators
        high_risk = swarm.get_risk_indicators()
        if high_risk:
            print("\n⚠️ High-Risk Indicators:")
            for indicator in high_risk:
                print(f"  • {indicator['name']}: {indicator['value']} {indicator['unit']} "
                      f"(Trend: {indicator['trend']}, Risk: {indicator['risk']})")
        
        # Show vulnerable companies
        vulnerable = swarm.get_vulnerable_companies()
        if vulnerable:
            print(f"\n⚠️ Vulnerable Companies: {', '.join(vulnerable)}")
        
        print("\n" + "=" * 70)
        print("✅ All swarm demos completed successfully!")
        print("\n🎯 Key Features Demonstrated:")
        print("  • Multi-agent collaboration with handoffs")
        print("  • Specialized agents with distinct roles")
        print("  • Shared context across agents")
        print("  • Automatic task delegation")
        print("  • Safety mechanisms (timeouts, handoff limits)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure:")
        print("  1. OPENAI_API_KEY is set in your environment")
        print("  2. You have installed: pip install strands-agents>=1.7.0")


if __name__ == "__main__":
    main()