"""Data models for market analysis"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class CompanyFinancials:
    """Company financial metrics"""
    ticker: str
    revenue_billions: float
    eps: float
    debt_to_equity: float
    pe_ratio: float
    profit_margin: float
    roe: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticker": self.ticker,
            "revenue_billions": self.revenue_billions,
            "eps": self.eps,
            "debt_to_equity": self.debt_to_equity,
            "pe_ratio": self.pe_ratio,
            "profit_margin": self.profit_margin,
            "roe": self.roe
        }
    
    @property
    def peg_ratio(self, growth_rate: float = 15.0) -> float:
        """Calculate PEG ratio given growth rate"""
        if growth_rate == 0:
            return float('inf')
        return self.pe_ratio / growth_rate
    
    @property
    def is_high_debt(self) -> bool:
        """Check if company has high debt levels"""
        return self.debt_to_equity > 1.5


@dataclass
class EconomicIndicator:
    """Economic indicator data"""
    name: str
    value: float
    unit: str
    trend: str
    risk_level: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "trend": self.trend
        }
        if self.risk_level:
            result["risk"] = self.risk_level
        return result
    
    @property
    def is_elevated(self) -> bool:
        """Check if indicator shows elevated risk"""
        return self.trend in ["elevated", "high", "rising"]
    
    @property
    def risk_score(self) -> int:
        """Get numeric risk score"""
        risk_map = {"low": 1, "medium": 2, "high": 3}
        return risk_map.get(self.risk_level, 0)