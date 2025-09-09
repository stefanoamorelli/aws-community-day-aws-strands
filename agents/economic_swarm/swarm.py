"""Economic Analysis Swarm implementation"""

from strands.multiagent.swarm import Swarm
from strands.models.openai import OpenAIModel
from typing import Optional, Dict, Any
import os
from .agents import AgentFactory
from .tools import EconomicDataProvider
from .models import EconomicContext


class EconomicSwarm:
    """Economic Analysis Swarm with multiple specialized agents"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_handoffs: int = 10,
        max_iterations: int = 15,
        execution_timeout: float = 300.0,
        node_timeout: float = 60.0,
        use_mcp: bool = True
    ):
        """
        Initialize Economic Analysis Swarm.
        
        Args:
            api_key: OpenAI API key (uses env var if not provided)
            model_id: Model to use for all agents
            temperature: Model temperature
            max_handoffs: Maximum agent handoffs
            max_iterations: Maximum total iterations
            execution_timeout: Total execution timeout in seconds
            node_timeout: Per-agent timeout in seconds
            use_mcp: Whether to use MCP server for FRED data
        """
        self.context = EconomicContext()
        self.use_mcp = use_mcp
        self.data_provider = EconomicDataProvider(self.context, use_mcp=use_mcp)
        self.model = self._create_model(api_key, model_id, temperature)
        self.agent_factory = AgentFactory(self.model, self.data_provider)
        self.swarm = self._create_swarm(
            max_handoffs, max_iterations, execution_timeout, node_timeout
        )
    
    def _create_model(self, api_key: str, model_id: str, temperature: float) -> OpenAIModel:
        """Create OpenAI model instance"""
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OpenAI API key required")
        
        return OpenAIModel(
            client_args={"api_key": key},
            model_id=model_id,
            temperature=temperature
        )
    
    def _create_swarm(
        self,
        max_handoffs: int,
        max_iterations: int,
        execution_timeout: float,
        node_timeout: float
    ) -> Swarm:
        """Create the swarm with all agents"""
        agents = self.agent_factory.create_all_agents()
        
        return Swarm(
            agents,  # Pass as list, not keyword argument
            max_handoffs=max_handoffs,
            max_iterations=max_iterations,
            execution_timeout=execution_timeout,
            node_timeout=node_timeout
        )
    
    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Run economic analysis on the query.
        
        Args:
            query: Analysis request
        
        Returns:
            Analysis results with context
        """
        # If using MCP, we need to run within context
        if self.use_mcp and self.data_provider.mcp_client:
            try:
                with self.data_provider.mcp_client:
                    # Get FRED tools while in context
                    self.data_provider.fred_tools = self.data_provider.mcp_client.list_tools_sync()
                    print(f"✅ Connected to FRED MCP - {len(self.data_provider.fred_tools)} tools available")
                    
                    # Recreate agents with MCP tools
                    self.agent_factory = AgentFactory(self.model, self.data_provider)
                    # Store original parameters
                    self.swarm = self._create_swarm(10, 15, 300.0, 60.0)
                    
                    # Execute swarm within MCP context
                    result = self.swarm(query)
            except Exception as e:
                print(f"⚠️ MCP execution failed: {e}")
                print("   Falling back to mock data")
                self.data_provider.use_mcp = False
                self.agent_factory = AgentFactory(self.model, self.data_provider)
                self.swarm = self._create_swarm(10, 15, 300.0, 60.0)
                result = self.swarm(query)
        else:
            # Execute without MCP
            result = self.swarm(query)
        
        # Return results with context
        return {
            "response": str(result),
            "status": result.status.value if hasattr(result, 'status') else "completed",
            "context": self.context.summary(),
            "execution_details": self._extract_execution_details(result),
            "using_mcp": self.use_mcp and bool(self.data_provider.fred_tools)
        }
    
    def _extract_execution_details(self, result) -> Dict:
        """Extract execution details from swarm result"""
        details = {
            "handoff_count": 0,
            "agents_involved": [],
            "execution_time": None
        }
        
        if hasattr(result, 'node_history'):
            details["agents_involved"] = [node.node_id for node in result.node_history]
            details["handoff_count"] = len(result.node_history) - 1
        
        if hasattr(result, 'execution_time'):
            details["execution_time"] = f"{result.execution_time / 1000:.2f}s"
        
        return details
    
    def analyze_companies(self, companies: list, indicators: Optional[list] = None) -> Dict[str, Any]:
        """
        Analyze specific companies against economic indicators.
        
        Args:
            companies: List of company tickers
            indicators: Optional list of specific indicators
        
        Returns:
            Analysis results
        """
        indicator_list = indicators or ["GDP", "UNRATE", "VIXCLS", "DFF", "CPI"]
        
        query = f"""Analyze the following companies: {', '.join(companies)}
        1. Collect these economic indicators: {', '.join(indicator_list)}
        2. Assess how each indicator affects each company
        3. Calculate risk scores for each company
        4. Provide specific recommendations for each company
        5. Identify which company is best positioned"""
        
        return self.analyze(query)
    
    def assess_market_risk(self) -> Dict[str, Any]:
        """
        Perform comprehensive market risk assessment.
        
        Returns:
            Market risk analysis
        """
        query = """Perform comprehensive market risk assessment:
        1. Collect all major economic indicators
        2. Identify systemic risks in the current environment
        3. Analyze impact on major sectors
        4. Calculate overall market risk level
        5. Provide defensive strategies and recommendations"""
        
        return self.analyze(query)
    
    def get_context_summary(self) -> Dict:
        """
        Get summary of analysis context.
        
        Returns:
            Context summary
        """
        return self.context.summary()
    
    def get_risk_indicators(self) -> list:
        """
        Get high-risk economic indicators.
        
        Returns:
            List of high-risk indicators
        """
        return [
            ind.to_dict() for ind in self.context.get_high_risk_indicators()
        ]
    
    def get_vulnerable_companies(self) -> list:
        """
        Get companies with high risk exposure.
        
        Returns:
            List of vulnerable companies
        """
        return self.context.get_vulnerable_companies()