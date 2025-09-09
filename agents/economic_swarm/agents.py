"""Agent factory for economic swarm"""

from strands import Agent
from strands.models.openai import OpenAIModel
from typing import List, Optional
from .tools import EconomicDataProvider


class AgentFactory:
    """Factory for creating specialized agents"""
    
    def __init__(self, model: OpenAIModel, data_provider: EconomicDataProvider):
        self.model = model
        self.data_provider = data_provider
    
    def create_coordinator(self) -> Agent:
        """Create coordinator agent"""
        return Agent(
            name="coordinator",
            model=self.model,
            tools=[],
            system_prompt="""You are the swarm coordinator. Your role is to:
            1. Understand the user's request
            2. Delegate tasks to appropriate specialists
            3. Synthesize findings into a coherent response
            
            Available specialists:
            - data_collector: Gathers economic data
            - analyst: Analyzes economic relationships
            - risk_assessor: Evaluates risks and provides recommendations
            
            Start by using handoff_to_agent to delegate to the appropriate specialist.
            Ensure all aspects of the user's request are addressed."""
        )
    
    def create_data_collector(self) -> Agent:
        """Create data collection agent"""
        # Get appropriate tools (MCP or mock)
        tools = []
        if self.data_provider.use_mcp and self.data_provider.fred_tools:
            # Use MCP FRED tools
            tools = self.data_provider.fred_tools
        else:
            # Use mock tool
            tools = [self.data_provider.get_economic_indicator]
        
        return Agent(
            name="data_collector",
            model=self.model,
            tools=tools,
            system_prompt="""You are a data collection specialist with access to Federal Reserve Economic Data (FRED). Your role is to:
            1. Gather economic indicator data systematically using FRED MCP tools
            2. Identify which indicators show concerning trends  
            3. Hand off to the analyst for interpretation
            
            FRED MCP tools available:
            - fred_search: Search for economic series by keywords (e.g., search for "GDP", "unemployment")
            - fred_get_series: Get actual data for a series ID (e.g., "GDP", "UNRATE", "CPIAUCSL")
            - fred_browse: Browse categories to find relevant series
            
            Key series IDs to collect data for:
            - GDP: Gross Domestic Product (use fred_get_series with series_id="GDP")
            - UNRATE: Unemployment Rate (use fred_get_series with series_id="UNRATE")
            - DFF: Federal Funds Rate (use fred_get_series with series_id="DFF")
            - CPIAUCSL: Consumer Price Index (use fred_get_series with series_id="CPIAUCSL")
            - For volatility: Search for "VIX" or "volatility index"
            
            First use fred_get_series to get the latest values for these key indicators, then analyze trends.
            When you find concerning trends, use handoff_to_agent to pass to 'analyst'."""
        )
    
    def create_analyst(self) -> Agent:
        """Create analysis agent"""
        # Get appropriate tools (MCP or mock)
        tools = [self.data_provider.get_company_exposure]
        if self.data_provider.use_mcp and self.data_provider.fred_tools:
            # Add MCP FRED tools
            tools.extend(self.data_provider.fred_tools)
        else:
            # Add mock tool
            tools.insert(0, self.data_provider.get_economic_indicator)
        
        return Agent(
            name="analyst",
            model=self.model,
            tools=tools,
            system_prompt="""You are an economic analyst with access to FRED data. Your role is to:
            1. Analyze relationships between economic indicators
            2. Assess how indicators affect specific companies
            3. Identify systemic risks and correlations
            
            Use FRED MCP tools to get additional data as needed:
            - fred_get_series: Get time series data (e.g., series_id="GDP", "UNRATE", "DFF")
            - fred_search: Find related economic series
            
            Also use get_company_exposure to analyze company-specific impacts.
            
            When you identify high-risk situations, use handoff_to_agent 
            to pass your analysis to 'risk_assessor' for final evaluation.
            
            Focus on cause-and-effect relationships and quantitative analysis."""
        )
    
    def create_risk_assessor(self) -> Agent:
        """Create risk assessment agent"""
        return Agent(
            name="risk_assessor",
            model=self.model,
            tools=[
                self.data_provider.calculate_risk_score,
                self.data_provider.get_company_exposure,
                self.data_provider.analyze_systemic_risk
            ],
            system_prompt="""You are a risk assessment specialist. Your role is to:
            1. Calculate overall risk scores
            2. Provide actionable recommendations
            3. Prioritize risks by severity
            4. Suggest specific mitigation strategies
            
            When you need more data, use handoff_to_agent to request 
            additional information from 'data_collector'.
            
            Always provide clear, actionable recommendations with specific steps."""
        )
    
    def create_all_agents(self) -> List[Agent]:
        """Create all agents for the swarm"""
        return [
            self.create_coordinator(),
            self.create_data_collector(),
            self.create_analyst(),
            self.create_risk_assessor()
        ]