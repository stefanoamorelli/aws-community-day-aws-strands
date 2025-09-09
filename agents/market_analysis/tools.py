"""Tools for market analysis"""

from strands import tool
from typing import Dict, Optional
from .models import CompanyFinancials, EconomicIndicator


class MarketDataProvider:
    """Provider for market data (simulates MCP servers)"""
    
    def __init__(self):
        self._init_data()
    
    def _init_data(self):
        """Initialize mock data"""
        self.companies = {
            "AAPL": CompanyFinancials(
                ticker="AAPL",
                revenue_billions=383.3,
                eps=6.13,
                debt_to_equity=1.95,
                pe_ratio=30.2,
                profit_margin=25.3,
                roe=147.9
            ),
            "MSFT": CompanyFinancials(
                ticker="MSFT",
                revenue_billions=245.1,
                eps=11.82,
                debt_to_equity=0.58,
                pe_ratio=35.5,
                profit_margin=36.7,
                roe=39.2
            ),
            "GOOGL": CompanyFinancials(
                ticker="GOOGL",
                revenue_billions=307.4,
                eps=5.61,
                debt_to_equity=0.11,
                pe_ratio=24.8,
                profit_margin=27.8,
                roe=30.6
            )
        }
        
        self.indicators = {
            "GDP": EconomicIndicator(
                name="GDP",
                value=27.96,
                unit="Trillion USD",
                trend="growing",
                risk_level="low"
            ),
            "UNRATE": EconomicIndicator(
                name="UNRATE",
                value=3.7,
                unit="Percent",
                trend="stable",
                risk_level="low"
            ),
            "VIXCLS": EconomicIndicator(
                name="VIXCLS",
                value=18.5,
                unit="Index",
                trend="moderate",
                risk_level="medium"
            ),
            "DFF": EconomicIndicator(
                name="DFF",
                value=5.33,
                unit="Percent",
                trend="elevated",
                risk_level="medium"
            ),
            "CPI": EconomicIndicator(
                name="CPI",
                value=318.5,
                unit="Index",
                trend="rising",
                risk_level="medium"
            )
        }
    
    @tool
    def get_company_financials(self, ticker: str) -> Dict:
        """
        Get company financial data (simulates SEC Edgar MCP).
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Financial metrics dictionary
        """
        company = self.companies.get(ticker.upper())
        if company:
            return company.to_dict()
        return {"error": f"No data for {ticker}"}
    
    @tool
    def get_economic_indicator(self, name: str) -> Dict:
        """
        Get economic indicator from FRED (simulates FRED MCP).
        
        Args:
            name: Indicator name (GDP, UNRATE, VIXCLS, DFF, CPI)
        
        Returns:
            Indicator data dictionary
        """
        indicator = self.indicators.get(name.upper())
        if indicator:
            return indicator.to_dict()
        return {"error": f"Unknown indicator {name}"}
    
    @tool
    def analyze_company_correlation(self, ticker: str, indicator: str) -> str:
        """
        Analyze correlation between company and economic indicator.
        
        Args:
            ticker: Company ticker
            indicator: Economic indicator name
        
        Returns:
            Analysis text
        """
        company = self.companies.get(ticker.upper())
        econ = self.indicators.get(indicator.upper())
        
        if not company or not econ:
            return f"Invalid ticker or indicator"
        
        analysis = []
        
        # Interest rate impact
        if indicator.upper() == "DFF" and econ.value > 5:
            if company.is_high_debt:
                analysis.append(
                    f"⚠️ {ticker} has high debt ({company.debt_to_equity:.1f}x) - "
                    f"vulnerable to high rates ({econ.value}%)"
                )
            else:
                analysis.append(
                    f"✅ {ticker} has low debt ({company.debt_to_equity:.1f}x) - "
                    f"resilient to rate hikes"
                )
        
        # Volatility impact
        if indicator.upper() == "VIXCLS":
            if econ.value > 25:
                analysis.append(
                    f"📊 High volatility (VIX: {econ.value}) - "
                    f"consider protective strategies for {ticker}"
                )
            else:
                analysis.append(
                    f"✅ Low volatility (VIX: {econ.value}) - "
                    f"stable environment for {ticker}"
                )
        
        # Inflation impact
        if indicator.upper() == "CPI" and econ.trend == "rising":
            if company.profit_margin > 30:
                analysis.append(
                    f"💪 {ticker} has strong margins ({company.profit_margin:.1f}%) - "
                    f"can absorb inflation pressure"
                )
            else:
                analysis.append(
                    f"⚠️ Rising inflation may pressure {ticker}'s margins "
                    f"({company.profit_margin:.1f}%)"
                )
        
        return " | ".join(analysis) if analysis else f"Neutral relationship between {ticker} and {indicator}"
    
    def get_all_tools(self):
        """Get all tools for the agent"""
        return [
            self.get_company_financials,
            self.get_economic_indicator,
            self.analyze_company_correlation
        ]