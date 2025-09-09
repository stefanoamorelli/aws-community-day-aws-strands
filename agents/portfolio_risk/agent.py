"""Portfolio Risk Assessment Agent implementation"""

from strands import Agent
from strands_tools import calculator
from strands.models.openai import OpenAIModel
from typing import Optional, List, Tuple, Any
from .portfolio import Portfolio
from .tools import RiskCalculator


class PortfolioRiskAgent:
    """Portfolio Risk Assessment Agent"""
    
    SYSTEM_PROMPT = """You are a portfolio risk analyst specializing in risk assessment and management. 
    Analyze portfolios and calculate risk metrics. Use the tools to:
    - Calculate Value at Risk (VaR) at different confidence levels
    - Assess concentration risk and diversification
    - Compute risk-adjusted returns (Sharpe ratio)
    - Run stress tests for various scenarios
    - Provide actionable risk management recommendations
    Be concise, data-driven, and focus on practical risk mitigation strategies."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        additional_tools: Optional[List[Any]] = None
    ):
        """
        Initialize Portfolio Risk Agent.
        
        Args:
            api_key: OpenAI API key (uses env var if not provided)
            model_id: Model to use
            temperature: Model temperature
            additional_tools: Extra tools to add
        """
        self.portfolio = Portfolio()
        self.risk_calculator = RiskCalculator(self.portfolio)
        self.model = self._create_model(api_key, model_id, temperature)
        self.agent = self._create_agent(additional_tools)
    
    def _create_model(self, api_key: str, model_id: str, temperature: float) -> OpenAIModel:
        """Create OpenAI model instance"""
        import os
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OpenAI API key required")
        
        return OpenAIModel(
            client_args={"api_key": key},
            model_id=model_id,
            temperature=temperature
        )
    
    def _create_agent(self, additional_tools: Optional[List[Any]] = None) -> Agent:
        """Create the agent with tools"""
        tools = self.risk_calculator.get_all_tools() + [calculator]
        if additional_tools:
            tools.extend(additional_tools)
        
        return Agent(
            model=self.model,
            tools=tools,
            system_prompt=self.SYSTEM_PROMPT
        )
    
    def add_position(
        self,
        symbol: str,
        shares: int,
        buy_price: float,
        current_price: float
    ) -> None:
        """
        Add a position to the portfolio.
        
        Args:
            symbol: Stock ticker
            shares: Number of shares
            buy_price: Purchase price per share
            current_price: Current price per share
        """
        self.portfolio.add_position(symbol, shares, buy_price, current_price)
    
    def add_positions(self, positions: List[Tuple[str, int, float, float]]) -> None:
        """
        Add multiple positions.
        
        Args:
            positions: List of (symbol, shares, buy_price, current_price) tuples
        """
        for symbol, shares, buy_price, current_price in positions:
            self.add_position(symbol, shares, buy_price, current_price)
    
    def analyze_risk(self, query: Optional[str] = None) -> str:
        """
        Analyze portfolio risk.
        
        Args:
            query: Specific risk analysis question (optional)
        
        Returns:
            Risk analysis response
        """
        if not query:
            query = """Perform comprehensive risk analysis:
            1. Calculate VaR at 95% and 99% confidence
            2. Assess concentration risk
            3. Calculate Sharpe ratio
            4. Run market crash stress test
            5. Provide top 3 risk management recommendations"""
        
        return self.agent(query)
    
    def get_risk_report(self) -> str:
        """
        Generate comprehensive risk report.
        
        Returns:
            Detailed risk report
        """
        query = """Generate a professional risk report including:
        1. Executive Summary of key risks
        2. VaR analysis at multiple confidence levels
        3. Concentration and diversification assessment
        4. Risk-adjusted performance metrics
        5. Stress test results for recession scenario
        6. Specific actionable recommendations with priority levels"""
        
        return self.analyze_risk(query)
    
    def recommend_rebalancing(self) -> str:
        """
        Get rebalancing recommendations.
        
        Returns:
            Rebalancing suggestions
        """
        query = """Analyze the portfolio and provide rebalancing recommendations:
        1. Identify overweight and underweight positions
        2. Suggest specific trades to improve diversification
        3. Calculate the impact on concentration risk
        4. Prioritize recommendations by importance"""
        
        return self.analyze_risk(query)
    
    def compare_risk_scenarios(self, scenarios: List[str]) -> str:
        """
        Compare multiple risk scenarios.
        
        Args:
            scenarios: List of scenarios to test
        
        Returns:
            Scenario comparison
        """
        scenario_list = ", ".join(scenarios)
        query = f"""Run and compare these stress test scenarios: {scenario_list}.
        For each scenario:
        1. Calculate portfolio impact
        2. Identify most vulnerable positions
        3. Suggest hedging strategies
        Compare results and recommend the best defensive strategy."""
        
        return self.analyze_risk(query)
    
    def clear_portfolio(self) -> None:
        """Clear all positions from portfolio"""
        self.portfolio = Portfolio()
        self.risk_calculator = RiskCalculator(self.portfolio)