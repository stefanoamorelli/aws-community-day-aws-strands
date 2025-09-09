#!/usr/bin/env python3
"""
Demo: Portfolio Risk Assessment Agent
Shows clean OOP design with state management
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from agents.portfolio_risk import PortfolioRiskAgent


def main():
    """Run portfolio risk demonstrations"""
    print("=" * 70)
    print("💼 AWS Strands - Portfolio Risk Agent Demo")
    print("=" * 70)
    
    try:
        # Initialize agent
        agent = PortfolioRiskAgent()
        print("\n✅ Portfolio Risk Agent initialized with OpenAI\n")
        
        # Build sample portfolio
        print("📊 Building sample portfolio...")
        print("-" * 50)
        
        positions = [
            ("AAPL", 100, 150, 185),   # Apple
            ("MSFT", 50, 320, 380),     # Microsoft
            ("NVDA", 40, 450, 850),     # NVIDIA
            ("GOOGL", 30, 130, 145),    # Google
            ("JPM", 25, 140, 155)       # JP Morgan
        ]
        
        agent.add_positions(positions)
        
        for symbol, shares, buy, current in positions:
            pos = agent.portfolio.get_position(symbol)
            print(f"{symbol:5} | {shares:3} shares | "
                  f"Value: ${pos.value:,.0f} | "
                  f"P&L: ${pos.pnl:+,.0f} ({pos.return_pct:+.1f}%)")
        
        summary = agent.portfolio.summary()
        print(f"\nTotal Portfolio Value: ${summary['total_value']:,.2f}")
        print(f"Total P&L: ${summary['total_pnl']:+,.2f} ({summary['total_return_pct']:+.1f}%)")
        print()
        
        # Demo 1: Comprehensive Risk Analysis
        print("📈 Demo 1: Comprehensive Risk Analysis")
        print("-" * 50)
        
        response = agent.analyze_risk()
        print(response)
        print()
        
        # Demo 2: Risk Report
        print("📈 Demo 2: Professional Risk Report")
        print("-" * 50)
        
        response = agent.get_risk_report()
        print(response)
        print()
        
        # Demo 3: Rebalancing Recommendations
        print("📈 Demo 3: Portfolio Rebalancing")
        print("-" * 50)
        
        response = agent.recommend_rebalancing()
        print(response)
        print()
        
        # Demo 4: Scenario Comparison
        print("📈 Demo 4: Risk Scenario Analysis")
        print("-" * 50)
        
        response = agent.compare_risk_scenarios(
            ["market_crash", "recession", "inflation"]
        )
        print(response)
        
        print("\n" + "=" * 70)
        print("✅ All portfolio risk demos completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure OPENAI_API_KEY is set in your environment")


if __name__ == "__main__":
    main()