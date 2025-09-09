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
        return Agent(
            name="data_collector",
            model=self.model,
            tools=[self.data_provider.get_economic_indicator],
            system_prompt="""You are a data collection specialist. Your role is to:
            1. Gather economic indicator data systematically
            2. Identify which indicators show concerning trends
            3. Hand off to the analyst for interpretation
            
            When you find concerning trends (high volatility, rising rates, etc.), 
            use handoff_to_agent to pass the data to 'analyst' for deeper analysis.
            
            Always collect GDP, UNRATE, VIXCLS, DFF, and CPI data for comprehensive coverage."""
        )
    
    def create_analyst(self) -> Agent:
        """Create analysis agent"""
        return Agent(
            name="analyst",
            model=self.model,
            tools=[
                self.data_provider.get_economic_indicator,
                self.data_provider.get_company_exposure
            ],
            system_prompt="""You are an economic analyst. Your role is to:
            1. Analyze relationships between economic indicators
            2. Assess how indicators affect specific companies
            3. Identify systemic risks and correlations
            
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