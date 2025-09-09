#!/usr/bin/env python3
"""
Simple tests that demonstrate testability of our components
These tests ACTUALLY PASS with our real implementations
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.market_analysis.models import CompanyFinancials, EconomicIndicator
from agents.market_analysis.tools import MarketDataProvider
from agents.portfolio_risk.portfolio import Portfolio, Position


class TestMarketAnalysisModels(unittest.TestCase):
    """Test market analysis models - pure data classes"""
    
    def test_company_financials_creation(self):
        """Test creating company financials - simple DTO"""
        financials = CompanyFinancials(
            ticker="AAPL",
            revenue_billions=383.3,
            eps=6.13,
            debt_to_equity=1.95,
            pe_ratio=30.2,
            profit_margin=25.3,
            roe=147.9
        )
        
        # All fields accessible
        self.assertEqual(financials.ticker, "AAPL")
        self.assertEqual(financials.revenue_billions, 383.3)
        self.assertEqual(financials.pe_ratio, 30.2)
    
    def test_company_financials_to_dict(self):
        """Test serialization - no external dependencies"""
        financials = CompanyFinancials(
            ticker="MSFT",
            revenue_billions=245.1,
            eps=11.82,
            debt_to_equity=0.58,
            pe_ratio=35.5,
            profit_margin=36.7,
            roe=39.2
        )
        
        data = financials.to_dict()
        
        # Verify all fields present
        self.assertEqual(data["ticker"], "MSFT")
        self.assertEqual(data["revenue_billions"], 245.1)
        self.assertEqual(data["pe_ratio"], 35.5)
    
    def test_is_high_debt_property(self):
        """Test computed property - pure logic"""
        low_debt = CompanyFinancials("LOW", 100, 5, 0.5, 20, 15, 25)
        high_debt = CompanyFinancials("HIGH", 100, 5, 2.0, 20, 15, 25)
        
        self.assertFalse(low_debt.is_high_debt)
        self.assertTrue(high_debt.is_high_debt)
    
    def test_peg_ratio_calculation(self):
        """Test PEG ratio property - pure calculation"""
        financials = CompanyFinancials("TEST", 100, 5, 1.0, 30.0, 20, 30)
        
        # PEG with default growth (15%)
        peg = financials.peg_ratio
        self.assertAlmostEqual(peg, 2.0, places=1)  # 30 / 15


class TestMarketDataProvider(unittest.TestCase):
    """Test market data provider - tool isolation"""
    
    def test_provider_initialization(self):
        """Test creating provider - no external dependencies"""
        provider = MarketDataProvider()
        
        # Should have mock data
        self.assertIsNotNone(provider.companies)
        self.assertIsNotNone(provider.indicators)
    
    def test_get_company_financials(self):
        """Test getting company data - returns mock data"""
        provider = MarketDataProvider()
        
        # Get known company
        result = provider.get_company_financials("AAPL")
        
        self.assertIn("ticker", result)
        self.assertEqual(result["ticker"], "AAPL")
    
    def test_get_economic_indicator(self):
        """Test getting indicator - predictable output"""
        provider = MarketDataProvider()
        
        # Get known indicator
        result = provider.get_economic_indicator("GDP")
        
        self.assertIn("name", result)
        self.assertEqual(result["name"], "GDP")
    
    def test_get_all_tools(self):
        """Test tool registration - verifies decorator works"""
        provider = MarketDataProvider()
        tools = provider.get_all_tools()
        
        # Should have multiple tools
        self.assertGreater(len(tools), 0)
        
        # Each should be callable
        for tool in tools:
            self.assertTrue(callable(tool))


class TestPortfolio(unittest.TestCase):
    """Test portfolio entity - state management"""
    
    def test_portfolio_creation(self):
        """Test creating portfolio - clean initialization"""
        portfolio = Portfolio()
        
        self.assertEqual(len(portfolio.positions), 0)
        self.assertEqual(portfolio.total_value, 0)
    
    def test_add_position(self):
        """Test adding position - state mutation"""
        portfolio = Portfolio()
        
        # Add position (symbol, shares, buy_price, current_price)
        position = portfolio.add_position("AAPL", 100, 150.0, 155.0)
        
        # Should return the Position object
        self.assertIsInstance(position, Position)
        self.assertEqual(position.symbol, "AAPL")
        
        # Position should be added to list
        self.assertEqual(len(portfolio.positions), 1)
        self.assertEqual(portfolio.positions[0].shares, 100)
    
    def test_portfolio_value_calculation(self):
        """Test value calculation - aggregation logic"""
        portfolio = Portfolio()
        portfolio.add_position("AAPL", 100, 150.0, 160.0)
        portfolio.add_position("MSFT", 50, 300.0, 310.0)
        
        # Total value should be sum
        expected = (100 * 160.0) + (50 * 310.0)
        self.assertEqual(portfolio.total_value, expected)
    
    def test_portfolio_independence(self):
        """Test portfolio instances are independent"""
        portfolio1 = Portfolio()
        portfolio2 = Portfolio()
        
        portfolio1.add_position("AAPL", 100, 150.0, 155.0)
        
        # Portfolio2 should be unaffected
        self.assertEqual(len(portfolio1.positions), 1)
        self.assertEqual(len(portfolio2.positions), 0)


class TestIntegration(unittest.TestCase):
    """Test component integration - shows how pieces work together"""
    
    def test_market_data_with_models(self):
        """Test provider returns proper model structures"""
        provider = MarketDataProvider()
        
        # Get company data
        data = provider.get_company_financials("AAPL")
        
        # Can create model from data
        financials = CompanyFinancials(**{
            k: data.get(k, data.get("metrics", {}).get(k, 0))
            for k in ["ticker", "revenue_billions", "eps", "debt_to_equity", 
                     "pe_ratio", "profit_margin", "roe"]
        })
        
        self.assertEqual(financials.ticker, "AAPL")
    
    def test_portfolio_with_positions(self):
        """Test portfolio manages positions correctly"""
        portfolio = Portfolio()
        
        # Add multiple positions
        portfolio.add_position("AAPL", 100, 150.0, 155.0)
        portfolio.add_position("MSFT", 50, 300.0, 305.0)
        
        # Each position is a Position object
        for position in portfolio.positions:
            self.assertIsInstance(position, Position)
            self.assertIn(position.symbol, ["AAPL", "MSFT"])


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)