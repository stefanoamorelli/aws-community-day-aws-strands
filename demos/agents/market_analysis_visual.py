#!/usr/bin/env python3
"""
Visual Demo: Market Analysis Agent
Enhanced visualization for AWS Community Day presentation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from agents.market_analysis import MarketAnalysisAgent
import time
from typing import Dict, Any


class MarketAnalysisVisualizer:
    """Visual presentation of market analysis"""
    
    def __init__(self):
        self.agent = None
        
    def print_header(self, title: str, icon: str = "📊"):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"  {icon} {title}")
        print("=" * 70)
    
    def print_data_table(self, title: str, data: Dict[str, Any]):
        """Print data in table format"""
        print(f"\n  {title}:")
        print("  " + "─" * 50)
        
        max_key_len = max(len(k) for k in data.keys())
        for key, value in data.items():
            if isinstance(value, float):
                print(f"  │ {key:{max_key_len}} │ {value:>12.2f} │")
            else:
                print(f"  │ {key:{max_key_len}} │ {value:>12} │")
        print("  " + "─" * 50)
    
    def show_market_indicators(self, indicators: Dict[str, float]):
        """Display market indicators with visual bars"""
        print("\n  📈 Market Indicators:")
        print("  " + "─" * 60)
        
        for name, value in indicators.items():
            # Create visual bar
            normalized = min(max(value / 100, 0), 1)  # Normalize to 0-1
            bar_length = int(normalized * 30)
            bar = "█" * bar_length + "░" * (30 - bar_length)
            
            # Determine color/status
            if value > 70:
                status = "🔴 HIGH"
            elif value > 40:
                status = "🟡 MODERATE"
            else:
                status = "🟢 LOW"
            
            print(f"  {name:20} [{bar}] {value:6.2f} {status}")
        print()
    
    def show_company_analysis(self, symbol: str, analysis: Dict[str, Any]):
        """Display company analysis with visual elements"""
        print(f"\n  🏢 Company Analysis: {symbol}")
        print("  " + "═" * 60)
        
        # Financial metrics
        print("\n  📊 Financial Metrics:")
        metrics = {
            "P/E Ratio": analysis.get("pe_ratio", 25.3),
            "Market Cap": f"${analysis.get('market_cap', 3000)}B",
            "Revenue Growth": f"{analysis.get('revenue_growth', 12.5)}%",
            "Profit Margin": f"{analysis.get('profit_margin', 21.4)}%"
        }
        
        for metric, value in metrics.items():
            print(f"    • {metric:20} {value}")
        
        # Risk indicators
        print("\n  ⚠️ Risk Assessment:")
        risks = analysis.get("risks", {
            "Market Risk": 0.6,
            "Liquidity Risk": 0.3,
            "Credit Risk": 0.4,
            "Operational Risk": 0.5
        })
        
        for risk_type, level in risks.items():
            bar_length = int(level * 20)
            bar = "▓" * bar_length + "░" * (20 - bar_length)
            percentage = int(level * 100)
            print(f"    {risk_type:20} [{bar}] {percentage}%")
        
        # Recommendation
        print("\n  💡 Recommendation:")
        rec = analysis.get("recommendation", "HOLD")
        if rec == "BUY":
            print(f"    🟢 {rec} - Strong fundamentals, good entry point")
        elif rec == "HOLD":
            print(f"    🟡 {rec} - Maintain position, monitor closely")
        else:
            print(f"    🔴 {rec} - Consider reducing exposure")
    
    def show_correlation_matrix(self):
        """Display correlation matrix visually"""
        print("\n  📊 Asset Correlation Matrix:")
        print("  " + "─" * 60)
        
        assets = ["AAPL", "GOOGL", "MSFT", "SPY", "GLD"]
        print("        ", end="")
        for asset in assets:
            print(f"{asset:8}", end="")
        print()
        
        correlations = [
            [1.00, 0.82, 0.78, 0.85, -0.12],
            [0.82, 1.00, 0.91, 0.88, -0.08],
            [0.78, 0.91, 1.00, 0.92, -0.15],
            [0.85, 0.88, 0.92, 1.00, -0.20],
            [-0.12, -0.08, -0.15, -0.20, 1.00]
        ]
        
        for i, asset in enumerate(assets):
            print(f"  {asset:6}", end="")
            for j, corr in enumerate(correlations[i]):
                # Color code correlation
                if corr > 0.8:
                    symbol = "██"  # Strong positive
                elif corr > 0.5:
                    symbol = "▓▓"  # Moderate positive
                elif corr > 0:
                    symbol = "░░"  # Weak positive
                elif corr > -0.5:
                    symbol = "░░"  # Weak negative
                else:
                    symbol = "▒▒"  # Strong negative
                print(f"  {symbol:2} ", end="")
            print()
        
        print("\n  Legend: ██ Strong+ ▓▓ Moderate+ ░░ Weak ▒▒ Negative")
    
    def animate_analysis_flow(self):
        """Animate the analysis process"""
        print("\n  🔄 Analysis Pipeline:")
        print("  " + "─" * 60)
        
        steps = [
            ("📥 Data Collection", "Gathering market data from multiple sources"),
            ("🔍 Pattern Analysis", "Identifying trends and anomalies"),
            ("📊 Statistical Processing", "Calculating indicators and metrics"),
            ("🧮 Risk Calculation", "Evaluating portfolio exposure"),
            ("💡 Recommendation Engine", "Generating actionable insights")
        ]
        
        for icon_step, description in steps:
            print(f"\n  {icon_step}")
            print(f"    └─► {description}", end="")
            
            # Progress animation
            for _ in range(3):
                time.sleep(0.3)
                print(".", end="", flush=True)
            print(" ✓")
    
    def run_demo(self):
        """Run the complete visual demonstration"""
        
        # Title
        print("\n" + "🌟" * 35)
        print("\n       AWS STRANDS - MARKET ANALYSIS AGENT")
        print("         Visual Demonstration for AWS Community Day")
        print("\n" + "🌟" * 35)
        
        # Initialize agent
        self.print_header("AGENT INITIALIZATION", "🚀")
        print("\n  Setting up Market Analysis Agent...")
        print("    • Model: OpenAI GPT-4 Turbo")
        print("    • Tools: 5 specialized market analysis tools")
        print("    • Data Sources: Mock market data (for demo stability)")
        
        try:
            self.agent = MarketAnalysisAgent()
            print("\n  ✅ Agent initialized successfully!")
        except Exception as e:
            print(f"\n  ❌ Error initializing agent: {e}")
            print("  Please ensure OPENAI_API_KEY is set")
            return
        
        # Show analysis pipeline
        self.print_header("ANALYSIS PIPELINE", "🔄")
        self.animate_analysis_flow()
        
        # Query 1: Get market indicators
        self.print_header("MARKET INDICATORS", "📈")
        print("\n  🤖 Querying agent for market indicators...")
        
        query1 = """Get economic indicators: VIXCLS (volatility), DFF (interest rate), and CPI.
        Format the response with current values and risk levels."""
        
        try:
            result1 = self.agent.analyze(query1)
            response1 = result1.message["content"][0]["text"] if hasattr(result1, "message") else str(result1)
            print("\n  Agent Response:")
            print("  " + "-" * 60)
            for line in response1.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        # Company analysis
        self.print_header("COMPANY ANALYSIS", "🏢")
        
        companies = ["AAPL", "MSFT", "GOOGL"]
        for symbol in companies:
            print(f"\n  🤖 Analyzing {symbol}...")
            
            query = f"""Analyze {symbol}:
            1. Get financial metrics (P/E ratio, profit margin, debt/equity, ROE)
            2. Assess risk level based on debt and valuation
            3. Provide BUY/HOLD/SELL recommendation with reasoning"""
            
            try:
                result = self.agent.analyze(query)
                response = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
                print(f"\n  📊 {symbol} Analysis:")
                print("  " + "=" * 60)
                for line in response.split('\n'):
                    if line.strip():
                        print(f"  {line}")
                print()
                time.sleep(0.5)
            except Exception as e:
                print(f"\n  ❌ Error analyzing {symbol}: {e}")
        
        # Company comparison
        self.print_header("COMPANY COMPARISON", "🔗")
        
        print("\n  🤖 Comparing companies...")
        comparison_query = """Compare AAPL, MSFT, and GOOGL on:
        1. Valuation metrics (P/E ratios)
        2. Financial health (debt/equity ratios)
        3. Profitability (margins and ROE)
        Which is the best investment opportunity and why?"""
        
        try:
            result = self.agent.analyze(comparison_query)
            comparison = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Comparison Results:")
            print("  " + "-" * 60)
            for line in comparison.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        # Economic impact assessment
        self.print_header("ECONOMIC IMPACT ASSESSMENT", "🌍")
        
        print("\n  🤖 Assessing economic impact on tech sector...")
        impact_query = """How do current economic indicators affect tech companies?
        Consider interest rates (DFF), volatility (VIXCLS), and inflation (CPI).
        What are the main risks and opportunities?"""
        
        try:
            result = self.agent.analyze(impact_query)
            impact = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Economic Impact Analysis:")
            print("  " + "-" * 60)
            for line in impact.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        # Investment recommendations
        self.print_header("INVESTMENT RECOMMENDATIONS", "📡")
        
        print("\n  🤖 Generating investment recommendations...")
        rec_query = """Based on the financial data and economic indicators:
        1. Which of these companies (AAPL, MSFT, GOOGL) offers the best risk/reward?
        2. What's your recommendation for portfolio allocation?
        3. What are the top 3 risks to watch?"""
        
        try:
            result = self.agent.analyze(rec_query)
            recommendations = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Investment Strategy:")
            print("  " + "=" * 60)
            for line in recommendations.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        # Valuation analysis
        self.print_header("VALUATION ANALYSIS", "⚠️")
        
        print("\n  🤖 Calculating valuations...")
        val_query = """For AAPL:
        1. Calculate PEG ratio assuming 15% growth
        2. Is it overvalued or undervalued at current P/E?
        3. What's a fair price target?"""
        
        try:
            result = self.agent.analyze(val_query)
            valuation = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Valuation Assessment:")
            print("  " + "-" * 60)
            for line in valuation.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        # Final summary
        self.print_header("EXECUTIVE SUMMARY", "💡")
        
        print("\n  🤖 Generating executive summary...")
        summary_query = """Provide a brief executive summary:
        1. Overall market conditions
        2. Best investment opportunity from the analyzed companies
        3. Key risks to monitor
        4. One actionable recommendation"""
        
        try:
            result = self.agent.analyze(summary_query)
            summary = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Summary:")
            print("  " + "=" * 60)
            for line in summary.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        # AWS Strands features
        self.print_header("AWS STRANDS FEATURES DEMONSTRATED", "✨")
        
        features = [
            "Clean, reusable agent architecture",
            "Type-safe tool integration",
            "Real-time market data processing",
            "Advanced risk calculations",
            "Automated signal generation",
            "Portfolio optimization algorithms"
        ]
        
        print("\n  Capabilities Showcased:")
        for feature in features:
            print(f"    ✓ {feature}")
            time.sleep(0.15)
        
        # Footer
        print("\n" + "=" * 70)
        print("  End of Market Analysis Agent Demonstration")
        print("  Thank you for attending AWS Community Day!")
        print("=" * 70)
        print("\n" + "🌟" * 35 + "\n")


def main():
    """Run visual market analysis demo"""
    demo = MarketAnalysisVisualizer()
    demo.run_demo()


if __name__ == "__main__":
    main()