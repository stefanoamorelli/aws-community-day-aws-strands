#!/usr/bin/env python3
"""
Visual Demo: Portfolio Risk Assessment Agent
Enhanced visualization showing risk metrics and portfolio analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from agents.portfolio_risk import PortfolioRiskAgent
import time
from typing import Dict, List, Tuple
import random


class PortfolioRiskVisualizer:
    """Visual presentation of portfolio risk assessment"""
    
    def __init__(self):
        self.agent = None
        
    def print_header(self, title: str, icon: str = "💼"):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"  {icon} {title}")
        print("=" * 70)
    
    def show_portfolio_composition(self, positions: List[Tuple[str, float, float]]):
        """Display portfolio composition as pie chart"""
        print("\n  📊 Portfolio Composition:")
        print("  " + "─" * 60)
        
        total = sum(shares * price for _, shares, price in positions)
        
        print("\n  Asset Allocation:")
        for symbol, shares, price in positions:
            value = shares * price
            percentage = (value / total) * 100
            
            # Create visual bar
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            
            print(f"  {symbol:6} {bar:25} {percentage:5.1f}% (${value:,.0f})")
        
        print(f"\n  Total Portfolio Value: ${total:,.2f}")
    
    def show_risk_metrics(self, metrics: Dict[str, float]):
        """Display risk metrics with visual indicators"""
        print("\n  📈 Risk Metrics Dashboard:")
        print("  " + "═" * 60)
        
        risk_levels = {
            "Value at Risk (95%)": (metrics.get("var_95", -2.5), "percent"),
            "Conditional VaR": (metrics.get("cvar", -3.8), "percent"),
            "Sharpe Ratio": (metrics.get("sharpe", 1.65), "ratio"),
            "Sortino Ratio": (metrics.get("sortino", 2.10), "ratio"),
            "Beta": (metrics.get("beta", 1.15), "ratio"),
            "Max Drawdown": (metrics.get("max_drawdown", -15.2), "percent")
        }
        
        for metric_name, (value, metric_type) in risk_levels.items():
            # Determine status
            if metric_name == "Sharpe Ratio":
                if value > 2:
                    status = "🟢 Excellent"
                elif value > 1:
                    status = "🟡 Good"
                else:
                    status = "🔴 Poor"
            elif metric_name == "Value at Risk (95%)":
                if value > -2:
                    status = "🟢 Low Risk"
                elif value > -5:
                    status = "🟡 Moderate"
                else:
                    status = "🔴 High Risk"
            elif metric_name == "Beta":
                if abs(value - 1) < 0.2:
                    status = "🟡 Market"
                elif value > 1:
                    status = "🔴 Aggressive"
                else:
                    status = "🟢 Defensive"
            else:
                status = ""
            
            # Format value
            if metric_type == "percent":
                value_str = f"{value:+.2f}%"
            else:
                value_str = f"{value:.2f}"
            
            print(f"  │ {metric_name:25} │ {value_str:>10} │ {status:12} │")
        
        print("  " + "═" * 60)
    
    def show_stress_test_results(self):
        """Display stress test scenarios"""
        print("\n  🔬 Stress Test Scenarios:")
        print("  " + "─" * 60)
        
        scenarios = [
            ("Market Crash (-20%)", -18.5, "🔴"),
            ("Interest Rate Spike (+2%)", -8.2, "🟡"),
            ("Inflation Surge (+3%)", -5.7, "🟡"),
            ("Tech Bubble Burst", -22.3, "🔴"),
            ("Energy Crisis", -12.1, "🟠"),
            ("Black Swan Event", -35.2, "🔴")
        ]
        
        print("\n  Scenario                    Impact    Visual")
        print("  " + "─" * 50)
        
        for scenario, impact, indicator in scenarios:
            # Create impact bar
            bar_length = int(abs(impact) / 2)
            bar = "▓" * min(bar_length, 20)
            
            print(f"  {scenario:25} {impact:>7.1f}%  {indicator} {bar}")
            time.sleep(0.2)
        
        print("\n  💡 Recommendation: Implement hedging strategies for high-impact scenarios")
    
    def show_correlation_heatmap(self):
        """Display portfolio correlation heatmap"""
        print("\n  🔗 Portfolio Correlation Matrix:")
        print("  " + "─" * 60)
        
        assets = ["AAPL", "MSFT", "JPM", "XOM", "GLD"]
        
        # Header
        print("        ", end="")
        for asset in assets:
            print(f"{asset:7}", end="")
        print("\n  " + "─" * 50)
        
        # Correlation data
        correlations = [
            [1.00, 0.75, 0.45, 0.30, -0.15],
            [0.75, 1.00, 0.52, 0.28, -0.10],
            [0.45, 0.52, 1.00, 0.65, -0.05],
            [0.30, 0.28, 0.65, 1.00, 0.12],
            [-0.15, -0.10, -0.05, 0.12, 1.00]
        ]
        
        for i, asset in enumerate(assets):
            print(f"  {asset:5}", end="")
            for corr in correlations[i]:
                # Color-code correlation
                if corr >= 0.7:
                    cell = "███"  # High correlation
                elif corr >= 0.3:
                    cell = "▓▓▓"  # Medium correlation
                elif corr >= 0:
                    cell = "░░░"  # Low correlation
                else:
                    cell = "   "  # Negative correlation
                print(f"  {cell:3}", end="")
            print()
        
        print("\n  Legend: ███ High (>0.7)  ▓▓▓ Medium (0.3-0.7)  ░░░ Low (0-0.3)")
        print("  ⚠️ Warning: High correlations reduce diversification benefits")
    
    def animate_risk_evolution(self):
        """Animate risk evolution over time"""
        print("\n  📈 Portfolio Risk Evolution (Last 30 Days):")
        print("  " + "─" * 60)
        
        days = 30
        risk_values = []
        
        # Generate risk evolution
        current_risk = 10
        for _ in range(days):
            change = random.uniform(-2, 2)
            current_risk = max(0, min(20, current_risk + change))
            risk_values.append(current_risk)
        
        # Display as ASCII chart
        height = 10
        print()
        for h in range(height, -1, -1):
            print(f"  {h*2:3}% |", end="")
            for risk in risk_values:
                if risk >= h * 2:
                    print("█", end="")
                else:
                    print(" ", end="")
            print()
        
        print("       +" + "─" * days)
        print("        " + "Day 1" + " " * (days - 10) + "Day 30")
        
        # Current status
        final_risk = risk_values[-1]
        trend = "📈" if risk_values[-1] > risk_values[-7] else "📉"
        print(f"\n  Current Risk Level: {final_risk:.1f}% {trend}")
    
    def show_optimization_results(self):
        """Display portfolio optimization results"""
        print("\n  🎯 Portfolio Optimization Results:")
        print("  " + "═" * 60)
        
        print("\n  Current vs Optimized Portfolio:")
        print("  " + "─" * 50)
        
        comparison = [
            ("Expected Return", "12.5%", "15.8%", "🟢"),
            ("Volatility", "18.2%", "14.6%", "🟢"),
            ("Sharpe Ratio", "1.45", "2.18", "🟢"),
            ("Max Drawdown", "-22%", "-15%", "🟢"),
            ("VaR (95%)", "-3.2%", "-2.1%", "🟢")
        ]
        
        print(f"  {'Metric':20} {'Current':>12} {'Optimized':>12} {'Status':>10}")
        print("  " + "─" * 50)
        
        for metric, current, optimized, status in comparison:
            print(f"  {metric:20} {current:>12} {optimized:>12} {status:>10}")
            time.sleep(0.2)
        
        print("\n  💡 Recommended Rebalancing:")
        rebalancing = [
            ("AAPL", 25, 20, "Reduce 5%"),
            ("MSFT", 20, 18, "Reduce 2%"),
            ("JPM", 15, 22, "Increase 7%"),
            ("XOM", 10, 8, "Reduce 2%"),
            ("GLD", 5, 7, "Increase 2%"),
            ("Cash", 25, 25, "Maintain")
        ]
        
        print("\n  Asset    Current  Target  Action")
        print("  " + "─" * 40)
        for asset, current, target, action in rebalancing:
            print(f"  {asset:8} {current:>5}%  {target:>5}%  {action}")
    
    def show_risk_alerts(self):
        """Display risk alerts and warnings"""
        print("\n  ⚠️ Risk Alerts:")
        print("  " + "─" * 60)
        
        alerts = [
            ("🔴 HIGH", "Concentration Risk", "AAPL position exceeds 25% of portfolio"),
            ("🟡 MEDIUM", "Correlation Risk", "Tech holdings highly correlated (>0.8)"),
            ("🟡 MEDIUM", "Volatility Spike", "VIX increased 15% in last 5 days"),
            ("🟢 LOW", "Liquidity Risk", "All positions highly liquid"),
            ("🔴 HIGH", "Drawdown Alert", "Portfolio down 8% from recent high")
        ]
        
        for level, risk_type, description in alerts:
            print(f"\n  {level:12} {risk_type:20}")
            print(f"     └─► {description}")
            time.sleep(0.3)
    
    def run_demo(self):
        """Run the complete visual demonstration"""
        
        # Title
        print("\n" + "💎" * 35)
        print("\n       AWS STRANDS - PORTFOLIO RISK ASSESSMENT")
        print("         Visual Risk Analytics Dashboard")
        print("\n" + "💎" * 35)
        
        # Initialize
        self.print_header("AGENT INITIALIZATION", "🚀")
        print("\n  Setting up Portfolio Risk Agent...")
        print("    • Model: OpenAI GPT-4 Turbo")
        print("    • Tools: Advanced risk analytics suite")
        print("    • Metrics: VaR, CVaR, Sharpe, Sortino, Beta")
        
        try:
            self.agent = PortfolioRiskAgent()
            print("\n  ✅ Agent initialized successfully!")
        except Exception as e:
            print(f"\n  ❌ Error initializing agent: {e}")
            print("  Please ensure OPENAI_API_KEY is set")
            return
        
        # Add positions to portfolio
        self.print_header("PORTFOLIO SETUP", "📊")
        print("\n  Adding positions to portfolio...")
        
        positions = [
            ("AAPL", 100, 185.50),
            ("MSFT", 75, 420.25),
            ("JPM", 200, 165.80),
            ("XOM", 150, 105.20),
            ("GLD", 50, 195.30)
        ]
        
        # Add positions using agent
        for symbol, shares, price in positions:
            self.agent.add_position(symbol, shares, price)
            print(f"    ✓ Added {shares} shares of {symbol} at ${price}")
        
        # Display composition
        self.show_portfolio_composition(positions)
        
        # Get portfolio summary from agent
        print("\n  🤖 Analyzing portfolio composition...")
        
        try:
            result = self.agent.analyze("Summarize the current portfolio: total value, number of positions, and sector allocation.")
            summary = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Portfolio Summary:")
            print("  " + "-" * 60)
            for line in summary.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        time.sleep(1)
        
        # Risk metrics
        self.print_header("RISK METRICS", "📈")
        
        print("\n  🤖 Calculating risk metrics...")
        
        risk_query = """Calculate the following risk metrics for the portfolio:
        1. Value at Risk (95% confidence)
        2. Sharpe ratio (assume 2% risk-free rate)
        3. Maximum drawdown estimate
        4. Portfolio beta
        Provide specific numbers and interpretation."""
        
        try:
            result = self.agent.analyze(risk_query)
            risk_analysis = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Risk Analysis Results:")
            print("  " + "=" * 60)
            for line in risk_analysis.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error calculating risk metrics: {e}")
        
        time.sleep(1)
        
        # Concentration risk
        self.print_header("CONCENTRATION RISK ANALYSIS", "🔗")
        
        print("\n  🤖 Analyzing concentration risk...")
        
        concentration_query = """Analyze concentration risk in the portfolio:
        1. What percentage does each position represent?
        2. Are there any positions that are too large (>25%)?
        3. How well diversified is the portfolio across sectors?
        4. What are the correlation risks?"""
        
        try:
            result = self.agent.analyze(concentration_query)
            concentration = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Concentration Analysis:")
            print("  " + "-" * 60)
            for line in concentration.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        time.sleep(1)
        
        # Stress testing
        self.print_header("STRESS TESTING", "🔬")
        
        print("\n  🤖 Running stress test scenarios...")
        
        stress_query = """Run stress tests on the portfolio for these scenarios:
        1. Market crash: -20% equity market decline
        2. Interest rate shock: +2% rate increase
        3. Tech sector collapse: -30% for tech stocks
        What would be the portfolio impact in each scenario?"""
        
        try:
            result = self.agent.analyze(stress_query)
            stress_results = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Stress Test Results:")
            print("  " + "=" * 60)
            for line in stress_results.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error running stress tests: {e}")
        
        time.sleep(1)
        
        # Risk comparison
        self.print_header("RISK COMPARISON", "📉")
        
        print("\n  🤖 Comparing portfolio risk to benchmarks...")
        
        benchmark_query = """Compare this portfolio's risk profile to:
        1. S&P 500 index (SPY)
        2. A 60/40 stocks/bonds portfolio
        3. A pure tech portfolio
        Which has better risk-adjusted returns?"""
        
        try:
            result = self.agent.analyze(benchmark_query)
            comparison = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Benchmark Comparison:")
            print("  " + "-" * 60)
            for line in comparison.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        time.sleep(1)
        
        # Optimization
        self.print_header("PORTFOLIO OPTIMIZATION", "🎯")
        
        print("\n  🤖 Optimizing portfolio allocation...")
        
        optimize_query = """Suggest portfolio optimization:
        1. What changes would improve the Sharpe ratio?
        2. How can we reduce risk without sacrificing too much return?
        3. Should we rebalance any positions?
        4. What's the optimal allocation for these holdings?"""
        
        try:
            result = self.agent.analyze(optimize_query)
            optimization = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Optimization Recommendations:")
            print("  " + "=" * 60)
            for line in optimization.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        time.sleep(1)
        
        # Risk alerts
        self.print_header("RISK MONITORING", "🚨")
        
        print("\n  🤖 Identifying risk alerts...")
        
        alert_query = """Identify the top risk alerts for this portfolio:
        1. What are the biggest risks right now?
        2. Are there any red flags in the allocation?
        3. What should we monitor most closely?
        4. What protective actions should we consider?"""
        
        try:
            result = self.agent.analyze(alert_query)
            alerts = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Risk Alerts:")
            print("  " + "=" * 60)
            for line in alerts.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
        
        # Summary
        self.print_header("EXECUTIVE SUMMARY", "📋")
        
        print("\n  🤖 Generating executive summary...")
        
        summary_query = """Provide an executive summary of the portfolio risk assessment:
        1. Overall portfolio health score (1-10)
        2. Top 3 strengths
        3. Top 3 weaknesses
        4. Most important action items
        5. Expected return vs risk trade-off assessment"""
        
        try:
            result = self.agent.analyze(summary_query)
            summary = result.message["content"][0]["text"] if hasattr(result, "message") else str(result)
            print("\n  Executive Summary:")
            print("  " + "=" * 60)
            for line in summary.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        except Exception as e:
            print(f"\n  ❌ Error generating summary: {e}")
        
        # AWS Strands features
        self.print_header("AWS STRANDS CAPABILITIES", "✨")
        
        features = [
            "Advanced risk calculations (VaR, CVaR, Greeks)",
            "Monte Carlo simulation for stress testing",
            "Portfolio optimization algorithms",
            "Real-time risk monitoring and alerts",
            "State management for portfolio tracking",
            "Clean OOP architecture for extensibility"
        ]
        
        print("\n  Features Demonstrated:")
        for feature in features:
            print(f"    ✓ {feature}")
            time.sleep(0.15)
        
        # Footer
        print("\n" + "=" * 70)
        print("  End of Portfolio Risk Assessment Demonstration")
        print("  Thank you for attending AWS Community Day!")
        print("=" * 70)
        print("\n" + "💎" * 35 + "\n")


def main():
    """Run visual portfolio risk demo"""
    demo = PortfolioRiskVisualizer()
    demo.run_demo()


if __name__ == "__main__":
    main()