"""Risk calculation tools for portfolio analysis"""

from strands import tool
from typing import Dict, List, Optional
from .portfolio import Portfolio, RiskLevel
import math


class RiskCalculator:
    """Risk calculation tools for portfolios"""
    
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio
    
    @tool
    def calculate_var(self, confidence: float = 0.95, volatility: float = 0.02) -> Dict:
        """
        Calculate Value at Risk.
        
        Args:
            confidence: Confidence level (0.95 or 0.99)
            volatility: Daily volatility (default 2%)
        
        Returns:
            VaR metrics
        """
        if self.portfolio.total_value == 0:
            return {"error": "Empty portfolio"}
        
        # Z-scores for confidence levels
        z_scores = {0.95: 1.65, 0.99: 2.33}
        z = z_scores.get(confidence, 1.65)
        
        var = self.portfolio.total_value * volatility * z
        
        return {
            "portfolio_value": round(self.portfolio.total_value, 2),
            "var": round(var, 2),
            "confidence": f"{confidence*100:.0f}%",
            "volatility": f"{volatility*100:.1f}%",
            "interpretation": f"With {confidence*100:.0f}% confidence, daily loss won't exceed ${var:,.2f}"
        }
    
    @tool
    def assess_concentration_risk(self) -> Dict:
        """
        Assess portfolio concentration risk.
        
        Returns:
            Concentration risk assessment
        """
        conc = self.portfolio.concentration()
        
        # Determine risk level
        max_conc = conc["max"]
        if max_conc > 40:
            risk_level = RiskLevel.CRITICAL
        elif max_conc > 30:
            risk_level = RiskLevel.HIGH
        elif max_conc > 20:
            risk_level = RiskLevel.MODERATE
        else:
            risk_level = RiskLevel.LOW
        
        # Generate recommendations
        recommendations = []
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append(f"⚠️ Reduce {conc['symbol']} position - too concentrated ({max_conc:.1f}%)")
            recommendations.append("Add more diversified holdings")
            recommendations.append("Consider position size limits (e.g., max 20% per position)")
        elif risk_level == RiskLevel.MODERATE:
            recommendations.append("Monitor concentration levels")
            recommendations.append("Consider rebalancing quarterly")
        else:
            recommendations.append("✅ Portfolio well diversified")
            recommendations.append("Maintain current allocation strategy")
        
        return {
            "max_concentration": f"{max_conc:.1f}%",
            "largest_position": conc['symbol'],
            "risk_level": risk_level.value,
            "diversification_score": self.portfolio.diversification_score(),
            "position_weights": conc["positions"],
            "recommendations": recommendations
        }
    
    @tool
    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.04) -> Dict:
        """
        Calculate Sharpe ratio.
        
        Args:
            risk_free_rate: Annual risk-free rate (default 4%)
        
        Returns:
            Sharpe ratio metrics
        """
        portfolio_return = self.portfolio.total_return_pct / 100
        
        # Calculate standard deviation of returns (simplified)
        # In production, this would use historical data
        returns = [p.return_pct / 100 for p in self.portfolio.positions]
        mean_return = sum(returns) / len(returns) if returns else 0
        
        if len(returns) > 1:
            variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
            std_dev = math.sqrt(variance)
        else:
            std_dev = 0
        
        if std_dev == 0:
            sharpe = 0
        else:
            sharpe = (portfolio_return - risk_free_rate) / std_dev
        
        interpretation = ""
        if sharpe > 2:
            interpretation = "Excellent risk-adjusted returns"
        elif sharpe > 1:
            interpretation = "Good risk-adjusted returns"
        elif sharpe > 0:
            interpretation = "Positive but modest risk-adjusted returns"
        else:
            interpretation = "Poor risk-adjusted returns"
        
        return {
            "sharpe_ratio": round(sharpe, 2),
            "portfolio_return": f"{portfolio_return*100:.2f}%",
            "risk_free_rate": f"{risk_free_rate*100:.2f}%",
            "volatility": f"{std_dev*100:.2f}%",
            "interpretation": interpretation
        }
    
    @tool
    def stress_test(self, scenario: str = "market_crash") -> Dict:
        """
        Run stress test scenarios.
        
        Args:
            scenario: Test scenario (market_crash, recession, inflation)
        
        Returns:
            Stress test results
        """
        scenarios = {
            "market_crash": {
                "name": "Market Crash (-30%)",
                "factor": 0.7,
                "description": "Severe market downturn"
            },
            "recession": {
                "name": "Recession (-15%)",
                "factor": 0.85,
                "description": "Economic recession"
            },
            "inflation": {
                "name": "High Inflation (-10%)",
                "factor": 0.9,
                "description": "High inflation environment"
            }
        }
        
        test = scenarios.get(scenario, scenarios["market_crash"])
        
        current_value = self.portfolio.total_value
        stressed_value = current_value * test["factor"]
        loss = current_value - stressed_value
        loss_pct = (1 - test["factor"]) * 100
        
        # Position-level impact
        position_impacts = []
        for pos in self.portfolio.positions:
            stressed_pos_value = pos.value * test["factor"]
            pos_loss = pos.value - stressed_pos_value
            position_impacts.append({
                "symbol": pos.symbol,
                "current_value": round(pos.value, 2),
                "stressed_value": round(stressed_pos_value, 2),
                "loss": round(pos_loss, 2)
            })
        
        return {
            "scenario": test["name"],
            "description": test["description"],
            "current_portfolio_value": round(current_value, 2),
            "stressed_portfolio_value": round(stressed_value, 2),
            "total_loss": round(loss, 2),
            "loss_percentage": f"{loss_pct:.1f}%",
            "position_impacts": position_impacts
        }
    
    @tool
    def get_portfolio_summary(self) -> Dict:
        """
        Get complete portfolio summary with risk metrics.
        
        Returns:
            Portfolio summary
        """
        summary = self.portfolio.summary()
        
        # Add risk metrics
        summary["risk_metrics"] = {
            "var_95": self.calculate_var(0.95),
            "concentration": self.assess_concentration_risk(),
            "sharpe_ratio": self.calculate_sharpe_ratio()
        }
        
        return summary
    
    def get_all_tools(self):
        """Get all tools for the agent"""
        return [
            self.calculate_var,
            self.assess_concentration_risk,
            self.calculate_sharpe_ratio,
            self.stress_test,
            self.get_portfolio_summary
        ]