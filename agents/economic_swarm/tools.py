"""Tools for economic swarm analysis with MCP integration"""

from strands import tool
from typing import Dict, List, Optional, Any
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
from .models import (
    EconomicIndicator, CompanyExposure, RiskAssessment,
    RiskLevel, Sensitivity, EconomicContext
)


class EconomicDataProvider:
    """Provider for economic data and analysis tools with MCP integration"""
    
    def __init__(self, context: EconomicContext, use_mcp: bool = True):
        self.context = context
        self.use_mcp = use_mcp
        self.mcp_client: Optional[MCPClient] = None
        self.fred_tools = []
        
        if use_mcp:
            self._init_mcp()
        else:
            self._init_data()
    
    def _init_mcp(self):
        """Initialize MCP connection to FRED server"""
        import os
        
        # Create MCP client for FRED server
        fred_api_key = os.environ.get("FRED_API_KEY", "")
        
        self.mcp_client = MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command="/usr/bin/node",
                    args=["/home/amorelli/development/fred-mcp-server/build/index.js"],
                    env={"FRED_API_KEY": fred_api_key}
                )
            )
        )
        
        # Will get tools when entering context
        print("✅ FRED MCP server configured (will connect on use)")
    
    def _init_data(self):
        """Initialize mock data sources (fallback when MCP not available)"""
        self.indicator_data = {
            "GDP": {"value": 27.96, "unit": "Trillion USD", "trend": "growing", "risk": "low"},
            "UNRATE": {"value": 3.7, "unit": "Percent", "trend": "stable", "risk": "low"},
            "VIXCLS": {"value": 35.2, "unit": "Index", "trend": "elevated", "risk": "high"},
            "DFF": {"value": 5.33, "unit": "Percent", "trend": "high", "risk": "medium"},
            "CPI": {"value": 318.5, "unit": "Index", "trend": "rising", "risk": "medium"}
        }
        
        self.company_data = {
            "AAPL": {
                "interest_rate_sensitivity": "high",
                "inflation_sensitivity": "medium",
                "volatility_sensitivity": "high",
                "debt_to_equity": 1.95,
                "international_revenue": 0.58
            },
            "JPM": {
                "interest_rate_sensitivity": "positive",
                "inflation_sensitivity": "low",
                "volatility_sensitivity": "medium",
                "debt_to_equity": 0.92,
                "international_revenue": 0.23
            },
            "XOM": {
                "interest_rate_sensitivity": "low",
                "inflation_sensitivity": "positive",
                "volatility_sensitivity": "medium",
                "debt_to_equity": 0.41,
                "international_revenue": 0.65
            }
        }
    
    @tool
    def get_economic_indicator(self, indicator: str) -> Dict:
        """
        Get economic indicator data (simulates FRED MCP).
        
        Args:
            indicator: Indicator name (GDP, UNRATE, VIXCLS, DFF, CPI)
        
        Returns:
            Indicator data with value and trend
        """
        data = self.indicator_data.get(indicator.upper(), {
            "value": 0, "unit": "Unknown", "trend": "unknown", "risk": "unknown"
        })
        
        # Create indicator object and add to context
        if indicator.upper() in self.indicator_data:
            ind = EconomicIndicator(
                name=indicator.upper(),
                value=data["value"],
                unit=data["unit"],
                trend=data["trend"],
                risk=RiskLevel(data["risk"])
            )
            self.context.add_indicator(ind)
        
        return data
    
    @tool
    def get_company_exposure(self, company: str) -> Dict:
        """
        Get company's exposure to economic factors.
        
        Args:
            company: Company ticker
        
        Returns:
            Exposure metrics
        """
        data = self.company_data.get(company.upper(), {
            "interest_rate_sensitivity": "unknown",
            "inflation_sensitivity": "unknown",
            "volatility_sensitivity": "unknown",
            "debt_to_equity": 1.0,
            "international_revenue": 0.3
        })
        
        # Create exposure object and add to context
        if company.upper() in self.company_data:
            # Map string sensitivities to enum
            sensitivity_map = {
                "low": Sensitivity.LOW,
                "medium": Sensitivity.MEDIUM,
                "high": Sensitivity.HIGH,
                "positive": Sensitivity.POSITIVE,
                "negative": Sensitivity.NEGATIVE
            }
            
            exposure = CompanyExposure(
                ticker=company.upper(),
                interest_rate_sensitivity=sensitivity_map.get(
                    data["interest_rate_sensitivity"], Sensitivity.MEDIUM
                ),
                inflation_sensitivity=sensitivity_map.get(
                    data["inflation_sensitivity"], Sensitivity.MEDIUM
                ),
                volatility_sensitivity=sensitivity_map.get(
                    data["volatility_sensitivity"], Sensitivity.MEDIUM
                ),
                debt_to_equity=data["debt_to_equity"],
                international_revenue=data["international_revenue"]
            )
            self.context.add_company_exposure(exposure)
        
        return data
    
    @tool
    def calculate_risk_score(self, factors: List[str]) -> Dict:
        """
        Calculate overall risk score based on factors.
        
        Args:
            factors: List of risk factors to consider
        
        Returns:
            Risk assessment
        """
        score = 0
        details = []
        
        for factor in factors:
            factor_lower = factor.lower()
            if "high" in factor_lower or "critical" in factor_lower:
                score += 3
                details.append(f"High risk: {factor}")
            elif "medium" in factor_lower or "moderate" in factor_lower:
                score += 2
                details.append(f"Medium risk: {factor}")
            elif "low" in factor_lower:
                score += 1
                details.append(f"Low risk: {factor}")
        
        # Determine risk level
        if score > 8:
            risk_level = RiskLevel.CRITICAL
            recommendation = "Immediate action needed - reduce exposure"
        elif score > 5:
            risk_level = RiskLevel.HIGH
            recommendation = "Monitor closely and consider hedging"
        elif score > 3:
            risk_level = RiskLevel.MEDIUM
            recommendation = "Monitor and prepare contingency plans"
        else:
            risk_level = RiskLevel.LOW
            recommendation = "Maintain current strategy"
        
        # Get affected companies
        affected = self.context.get_vulnerable_companies()
        
        # Create risk assessment
        assessment = RiskAssessment(
            risk_level=risk_level,
            risk_score=score,
            risk_factors=details,
            affected_companies=affected,
            recommendations=[recommendation]
        )
        self.context.add_risk_assessment(assessment)
        
        return {
            "score": score,
            "level": risk_level.value,
            "details": details,
            "recommendation": recommendation,
            "affected_companies": affected
        }
    
    @tool
    def analyze_systemic_risk(self) -> Dict:
        """
        Analyze systemic risk across indicators and companies.
        
        Returns:
            Systemic risk analysis
        """
        # Analyze indicators
        high_risk_indicators = self.context.get_high_risk_indicators()
        
        # Analyze companies
        vulnerable_companies = self.context.get_vulnerable_companies()
        
        # Calculate systemic risk
        systemic_score = len(high_risk_indicators) * 2 + len(vulnerable_companies)
        
        if systemic_score > 6:
            systemic_level = "CRITICAL"
            actions = [
                "Reduce overall portfolio exposure",
                "Implement defensive strategies",
                "Increase cash allocation"
            ]
        elif systemic_score > 3:
            systemic_level = "ELEVATED"
            actions = [
                "Review and adjust positions",
                "Consider protective hedges",
                "Monitor daily"
            ]
        else:
            systemic_level = "NORMAL"
            actions = [
                "Maintain positions",
                "Regular monitoring",
                "Stay informed"
            ]
        
        return {
            "systemic_level": systemic_level,
            "systemic_score": systemic_score,
            "high_risk_indicators": [ind.name for ind in high_risk_indicators],
            "vulnerable_companies": vulnerable_companies,
            "recommended_actions": actions,
            "context_summary": self.context.summary()
        }
    
    def get_mcp_tools(self):
        """Get FRED MCP tools if available"""
        if self.mcp_client and not self.fred_tools:
            try:
                # Must use within context manager
                with self.mcp_client:
                    self.fred_tools = self.mcp_client.list_tools_sync()
                    print(f"✅ Connected to FRED MCP server - {len(self.fred_tools)} tools available")
            except Exception as e:
                print(f"⚠️ Could not connect to FRED MCP: {e}")
                print("   Falling back to mock data")
                self.use_mcp = False
                self.fred_tools = []
        return self.fred_tools
    
    def get_all_tools(self):
        """Get all tools for agents"""
        tools = [
            self.get_company_exposure,
            self.calculate_risk_score,
            self.analyze_systemic_risk
        ]
        
        if self.use_mcp:
            # Add MCP tools if available
            mcp_tools = self.get_mcp_tools()
            if mcp_tools:
                tools.extend(mcp_tools)
            else:
                # Fallback to mock indicator tool
                tools.insert(0, self.get_economic_indicator)
        else:
            # Use mock indicator tool
            tools.insert(0, self.get_economic_indicator)
        
        return tools