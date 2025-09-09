"""Market Analysis Agent implementation"""

from strands import Agent
from strands_tools import calculator
from strands.models.openai import OpenAIModel
from typing import Optional, List, Any
from .tools import MarketDataProvider


class MarketAnalysisAgent:
    """Market Analysis Agent with financial tools"""
    
    SYSTEM_PROMPT = """You are a market analyst specializing in financial analysis. 
    Use the tools to get data and provide insights. Be concise and data-driven. 
    Always cite specific numbers from the tools. Focus on:
    - Company financial health and valuations
    - Economic indicator impacts
    - Risk assessment and correlations
    - Investment recommendations based on data"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        additional_tools: Optional[List[Any]] = None
    ):
        """
        Initialize Market Analysis Agent.
        
        Args:
            api_key: OpenAI API key (uses env var if not provided)
            model_id: Model to use
            temperature: Model temperature
            additional_tools: Extra tools to add
        """
        self.data_provider = MarketDataProvider()
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
        tools = self.data_provider.get_all_tools() + [calculator]
        if additional_tools:
            tools.extend(additional_tools)
        
        return Agent(
            model=self.model,
            tools=tools,
            system_prompt=self.SYSTEM_PROMPT
        )
    
    def analyze(self, query: str) -> str:
        """
        Analyze market query.
        
        Args:
            query: Market analysis question
        
        Returns:
            Analysis response
        """
        return self.agent(query)
    
    def compare_companies(self, tickers: List[str], metrics: List[str]) -> str:
        """
        Compare multiple companies on specific metrics.
        
        Args:
            tickers: List of company tickers
            metrics: Metrics to compare (e.g., ["debt", "pe_ratio", "margins"])
        
        Returns:
            Comparison analysis
        """
        query = f"Compare {', '.join(tickers)} on these metrics: {', '.join(metrics)}. "
        query += "Provide specific numbers and identify which company is best positioned."
        return self.analyze(query)
    
    def assess_economic_impact(self, ticker: str, indicators: List[str]) -> str:
        """
        Assess economic indicators' impact on a company.
        
        Args:
            ticker: Company ticker
            indicators: Economic indicators to analyze
        
        Returns:
            Impact assessment
        """
        query = f"Analyze how {ticker} is affected by these economic indicators: {', '.join(indicators)}. "
        query += "Use correlation analysis and provide specific recommendations."
        return self.analyze(query)
    
    def calculate_valuation(self, ticker: str, growth_rate: float) -> str:
        """
        Calculate company valuation metrics.
        
        Args:
            ticker: Company ticker
            growth_rate: Expected growth rate
        
        Returns:
            Valuation analysis
        """
        query = f"Calculate valuation metrics for {ticker} assuming {growth_rate}% growth. "
        query += "Include P/E ratio, PEG ratio, and whether it's attractive at current levels."
        return self.analyze(query)