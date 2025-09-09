"""Data models for economic swarm analysis"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class RiskLevel(Enum):
    """Risk level classifications"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Sensitivity(Enum):
    """Sensitivity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    POSITIVE = "positive"  # Benefits from the factor
    NEGATIVE = "negative"  # Harmed by the factor


@dataclass
class EconomicIndicator:
    """Economic indicator with metadata"""
    name: str
    value: float
    unit: str
    trend: str
    risk: RiskLevel
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "trend": self.trend,
            "risk": self.risk.value,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class CompanyExposure:
    """Company exposure to economic factors"""
    ticker: str
    interest_rate_sensitivity: Sensitivity
    inflation_sensitivity: Sensitivity
    volatility_sensitivity: Sensitivity
    debt_to_equity: float
    international_revenue: float
    
    def to_dict(self) -> Dict:
        return {
            "ticker": self.ticker,
            "interest_rate_sensitivity": self.interest_rate_sensitivity.value,
            "inflation_sensitivity": self.inflation_sensitivity.value,
            "volatility_sensitivity": self.volatility_sensitivity.value,
            "debt_to_equity": self.debt_to_equity,
            "international_revenue": self.international_revenue
        }
    
    @property
    def risk_score(self) -> int:
        """Calculate overall risk score"""
        score = 0
        
        # Interest rate risk
        if self.interest_rate_sensitivity == Sensitivity.HIGH:
            score += 3
        elif self.interest_rate_sensitivity == Sensitivity.MEDIUM:
            score += 2
        
        # Inflation risk
        if self.inflation_sensitivity in [Sensitivity.HIGH, Sensitivity.NEGATIVE]:
            score += 2
        elif self.inflation_sensitivity == Sensitivity.MEDIUM:
            score += 1
        
        # Volatility risk
        if self.volatility_sensitivity == Sensitivity.HIGH:
            score += 2
        elif self.volatility_sensitivity == Sensitivity.MEDIUM:
            score += 1
        
        # Debt risk
        if self.debt_to_equity > 2:
            score += 3
        elif self.debt_to_equity > 1:
            score += 1
        
        # International exposure risk
        if self.international_revenue > 0.5:
            score += 1
        
        return score


@dataclass
class RiskAssessment:
    """Risk assessment results"""
    risk_level: RiskLevel
    risk_score: int
    risk_factors: List[str]
    affected_companies: List[str]
    recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "risk_level": self.risk_level.value,
            "risk_score": self.risk_score,
            "risk_factors": self.risk_factors,
            "affected_companies": self.affected_companies,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp.isoformat()
        }


class EconomicContext:
    """Shared context for swarm agents"""
    
    def __init__(self):
        self.indicators: Dict[str, EconomicIndicator] = {}
        self.company_exposures: Dict[str, CompanyExposure] = {}
        self.risk_assessments: List[RiskAssessment] = []
        self.analysis_history: List[Dict] = []
    
    def add_indicator(self, indicator: EconomicIndicator) -> None:
        """Add economic indicator to context"""
        self.indicators[indicator.name] = indicator
        self._log_event("indicator_added", indicator.to_dict())
    
    def add_company_exposure(self, exposure: CompanyExposure) -> None:
        """Add company exposure analysis"""
        self.company_exposures[exposure.ticker] = exposure
        self._log_event("exposure_added", exposure.to_dict())
    
    def add_risk_assessment(self, assessment: RiskAssessment) -> None:
        """Add risk assessment"""
        self.risk_assessments.append(assessment)
        self._log_event("risk_assessed", assessment.to_dict())
    
    def _log_event(self, event_type: str, data: Dict) -> None:
        """Log analysis event"""
        self.analysis_history.append({
            "event": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_high_risk_indicators(self) -> List[EconomicIndicator]:
        """Get indicators with high or critical risk"""
        return [
            ind for ind in self.indicators.values()
            if ind.risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        ]
    
    def get_vulnerable_companies(self) -> List[str]:
        """Get companies with high risk scores"""
        vulnerable = []
        for ticker, exposure in self.company_exposures.items():
            if exposure.risk_score > 5:
                vulnerable.append(ticker)
        return vulnerable
    
    def get_latest_assessment(self) -> Optional[RiskAssessment]:
        """Get most recent risk assessment"""
        return self.risk_assessments[-1] if self.risk_assessments else None
    
    def summary(self) -> Dict:
        """Get context summary"""
        return {
            "indicators_collected": len(self.indicators),
            "companies_analyzed": len(self.company_exposures),
            "risk_assessments": len(self.risk_assessments),
            "high_risk_indicators": len(self.get_high_risk_indicators()),
            "vulnerable_companies": self.get_vulnerable_companies(),
            "latest_risk_level": (
                self.get_latest_assessment().risk_level.value
                if self.get_latest_assessment()
                else None
            ),
            "events_logged": len(self.analysis_history)
        }