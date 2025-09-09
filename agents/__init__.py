"""AWS Strands Agent Modules

Clean, reusable agent implementations for AWS Community Day presentation.
"""

from .market_analysis import MarketAnalysisAgent
from .portfolio_risk import PortfolioRiskAgent
from .economic_swarm import EconomicSwarm

__version__ = "1.0.0"

__all__ = [
    "MarketAnalysisAgent",
    "PortfolioRiskAgent",
    "EconomicSwarm"
]