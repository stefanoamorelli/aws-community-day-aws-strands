"""Portfolio data models and management"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class RiskLevel(Enum):
    """Risk level categories"""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Position:
    """Portfolio position with analytics"""
    symbol: str
    shares: int
    buy_price: float
    current_price: float
    
    @property
    def value(self) -> float:
        """Current position value"""
        return self.shares * self.current_price
    
    @property
    def cost_basis(self) -> float:
        """Total cost basis"""
        return self.shares * self.buy_price
    
    @property
    def pnl(self) -> float:
        """Profit and loss"""
        return self.value - self.cost_basis
    
    @property
    def return_pct(self) -> float:
        """Return percentage"""
        if self.buy_price == 0:
            return 0
        return ((self.current_price / self.buy_price) - 1) * 100
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "symbol": self.symbol,
            "shares": self.shares,
            "buy_price": self.buy_price,
            "current_price": self.current_price,
            "value": round(self.value, 2),
            "pnl": round(self.pnl, 2),
            "return_pct": round(self.return_pct, 2)
        }


class Portfolio:
    """Portfolio management with analytics"""
    
    def __init__(self):
        self.positions: List[Position] = []
        self._risk_metrics: Optional[Dict] = None
    
    def add_position(
        self,
        symbol: str,
        shares: int,
        buy_price: float,
        current_price: float
    ) -> Position:
        """Add a position to portfolio"""
        position = Position(symbol, shares, buy_price, current_price)
        self.positions.append(position)
        self._risk_metrics = None  # Invalidate cache
        return position
    
    def remove_position(self, symbol: str) -> bool:
        """Remove a position by symbol"""
        initial_count = len(self.positions)
        self.positions = [p for p in self.positions if p.symbol != symbol]
        self._risk_metrics = None  # Invalidate cache
        return len(self.positions) < initial_count
    
    @property
    def total_value(self) -> float:
        """Total portfolio value"""
        return sum(p.value for p in self.positions)
    
    @property
    def total_cost_basis(self) -> float:
        """Total cost basis"""
        return sum(p.cost_basis for p in self.positions)
    
    @property
    def total_pnl(self) -> float:
        """Total profit and loss"""
        return sum(p.pnl for p in self.positions)
    
    @property
    def total_return_pct(self) -> float:
        """Total return percentage"""
        if self.total_cost_basis == 0:
            return 0
        return ((self.total_value / self.total_cost_basis) - 1) * 100
    
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position by symbol"""
        for position in self.positions:
            if position.symbol == symbol:
                return position
        return None
    
    def concentration(self) -> Dict:
        """Calculate concentration metrics"""
        if not self.positions or self.total_value == 0:
            return {
                "max": 0,
                "symbol": None,
                "value": 0,
                "positions": {}
            }
        
        max_pos = max(self.positions, key=lambda p: p.value)
        concentrations = {
            p.symbol: round(p.value / self.total_value * 100, 2)
            for p in self.positions
        }
        
        return {
            "max": round(max_pos.value / self.total_value * 100, 2),
            "symbol": max_pos.symbol,
            "value": round(max_pos.value, 2),
            "positions": concentrations
        }
    
    def diversification_score(self) -> float:
        """
        Calculate diversification score (0-100).
        Higher score means better diversification.
        """
        if len(self.positions) <= 1:
            return 0.0
        
        conc = self.concentration()
        max_concentration = conc["max"]
        
        # Perfect diversification would be 100/n percent for each position
        ideal_concentration = 100 / len(self.positions)
        
        # Score based on how close we are to ideal
        score = max(0, 100 - abs(max_concentration - ideal_concentration) * 2)
        return round(score, 2)
    
    def summary(self) -> Dict:
        """Get portfolio summary"""
        return {
            "total_value": round(self.total_value, 2),
            "total_cost_basis": round(self.total_cost_basis, 2),
            "total_pnl": round(self.total_pnl, 2),
            "total_return_pct": round(self.total_return_pct, 2),
            "position_count": len(self.positions),
            "diversification_score": self.diversification_score(),
            "positions": [p.to_dict() for p in self.positions]
        }