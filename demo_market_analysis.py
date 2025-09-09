#!/usr/bin/env python3
"""
Demo: Market Analysis Agent
Shows clean, reusable agent architecture with AWS Strands
"""

from agents.market_analysis import MarketAnalysisAgent


def main():
    """Run market analysis demonstrations"""
    print("=" * 70)
    print("🚀 AWS Strands - Market Analysis Agent Demo")
    print("=" * 70)
    
    try:
        # Initialize agent
        agent = MarketAnalysisAgent()
        print("\n✅ Market Analysis Agent initialized with OpenAI\n")
        
        # Demo 1: Basic Analysis
        print("📊 Demo 1: Company Valuation Analysis")
        print("-" * 50)
        
        query = """Get financial data for AAPL and current interest rate (DFF).
        Calculate AAPL's PEG ratio assuming 15% growth.
        Is AAPL attractive at current valuations?"""
        
        response = agent.analyze(query)
        print(response)
        print()
        
        # Demo 2: Company Comparison
        print("📊 Demo 2: Multi-Company Comparison")
        print("-" * 50)
        
        response = agent.compare_companies(
            tickers=["AAPL", "MSFT", "GOOGL"],
            metrics=["debt_to_equity", "pe_ratio", "profit_margin", "roe"]
        )
        print(response)
        print()
        
        # Demo 3: Economic Impact Assessment
        print("📊 Demo 3: Economic Impact on Company")
        print("-" * 50)
        
        response = agent.assess_economic_impact(
            ticker="AAPL",
            indicators=["DFF", "VIXCLS", "CPI"]
        )
        print(response)
        print()
        
        # Demo 4: Valuation Calculation
        print("📊 Demo 4: Detailed Valuation Metrics")
        print("-" * 50)
        
        response = agent.calculate_valuation(
            ticker="MSFT",
            growth_rate=12.0
        )
        print(response)
        
        print("\n" + "=" * 70)
        print("✅ All market analysis demos completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure OPENAI_API_KEY is set in your environment")


if __name__ == "__main__":
    main()