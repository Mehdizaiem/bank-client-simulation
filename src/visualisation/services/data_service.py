"""
Data service for generating and processing bank simulation data
"""
import random
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any


class DataService:
    """Service class for handling all simulation data operations."""
    
    # Static data for consistent simulation results
    TUNISIAN_GOVERNORATES = [
        "Tunis", "Ariana", "Ben Arous", "Manouba", "Sfax", "Sousse", 
        "Nabeul", "Bizerte", "Kairouan", "Gabès", "Médenine", "Monastir",
        "Mahdia", "Kasserine", "Sidi Bouzid", "Gafsa"
    ]
    
    CLIENT_SEGMENTS = ["Retail", "Corporate", "SME", "High Net Worth", "Government"]
    BRANCH_TYPES = ["Full Service", "Express", "Corporate Center", "Digital Hub", "ATM Point"]
    
    @staticmethod
    def get_simulation_metrics() -> Dict[str, Dict[str, str]]:
        """Generate simulation-specific key metrics."""
        return {
            'active_agents': {
                'icon': '🤖',
                'title': 'Active AI Agents',
                'value': '50,247',
                'change': 'Simulating behavior'
            },
            'accuracy': {
                'icon': '🎯',
                'title': 'Simulation Accuracy',
                'value': '94.7%',
                'change': '+2.1% vs baseline'
            },
            'events_processed': {
                'icon': '⚡',
                'title': 'Events Processed',
                'value': '1,247,830',
                'change': 'Last 24 hours'
            },
            'branches_modeled': {
                'icon': '🏦',
                'title': 'Branches Modeled',
                'value': '156',
                'change': 'Across 24 governorates'
            }
        }
    
    @staticmethod
    def get_agent_behavior_data(client_filter: str = 'all', region_filter: str = 'all') -> Tuple[List[str], Dict[str, List[int]]]:
        """Generate AI agent behavior patterns data."""
        time_steps = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6']
        
        # Simulate different behavior patterns based on client segments
        behavior_data = {
            'Digital Adoption': [45, 52, 58, 63, 67, 72],
            'Branch Visits': [100, 95, 88, 82, 78, 75],
            'Product Uptake': [12, 18, 25, 31, 35, 42],
            'Churn Risk': [8, 7, 6, 6, 5, 5]
        }
        
        # Apply filters
        if client_filter != 'all':
            # Modify data based on client segment
            multiplier = {'retail': 1.0, 'corporate': 0.7, 'sme': 1.2, 'hnw': 0.5}.get(client_filter, 1.0)
            for key in behavior_data:
                behavior_data[key] = [int(val * multiplier) for val in behavior_data[key]]
        
        return time_steps, behavior_data
    
    @staticmethod
    def get_scenario_impact_data() -> Tuple[List[str], List[float]]:
        """Generate scenario impact analysis data."""
        scenarios = ['Branch Closure', 'Fee Reduction', 'Digital Launch', 'Competition', 'Economic Shock']
        impacts = [random.uniform(-15, 25) for _ in scenarios]  # Impact percentage
        return scenarios, impacts
    
    @staticmethod
    def get_agent_distribution_data(region_filter: str = 'all') -> Tuple[List[str], List[int]]:
        """Generate agent distribution across Tunisia."""
        if region_filter == 'all':
            governorates = DataService.TUNISIAN_GOVERNORATES[:8]  # Top 8 for display
        elif region_filter == 'north':
            governorates = ["Tunis", "Ariana", "Ben Arous", "Bizerte", "Nabeul"]
        elif region_filter == 'central':
            governorates = ["Sousse", "Monastir", "Mahdia", "Kairouan"]
        elif region_filter == 'south':
            governorates = ["Sfax", "Gabès", "Médenine", "Gafsa"]
        else:
            governorates = ["Tunis", "Sfax", "Sousse", "Ariana"]
        
        # Generate agent counts (representing simulated clients)
        agent_counts = [random.randint(1500, 5000) for _ in governorates]
        return governorates, agent_counts
    
    @staticmethod
    def get_market_response_data() -> Tuple[List[str], List[float]]:
        """Generate market response to events data."""
        events = ['Product Launch', 'Price Change', 'Branch Opening', 'Marketing Campaign', 'Competitor Action']
        responses = [random.uniform(0.5, 2.5) for _ in events]  # Response multiplier
        return events, responses
    
    @staticmethod
    def get_economic_scenario_data(event_type: str, severity: int, time_horizon: str) -> Tuple[List[str], List[float]]:
        """Generate economic scenario simulation data."""
        if time_horizon == '3m':
            time_data = ['Month 1', 'Month 2', 'Month 3']
        elif time_horizon == '6m':
            time_data = ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6']
        elif time_horizon == '1y':
            time_data = ['Q1', 'Q2', 'Q3', 'Q4']
        else:
            time_data = ['Year 1', 'Year 2']
        
        # Generate impact based on event type and severity
        base_impact = {
            'currency': [100, 85, 78, 82, 88, 95],
            'interest': [100, 102, 105, 103, 101, 100],
            'inflation': [100, 95, 88, 83, 85, 90],
            'gdp': [100, 98, 96, 99, 103, 106],
            'political': [100, 92, 85, 88, 94, 98],
            'oil': [100, 88, 82, 85, 91, 96]
        }.get(event_type, [100, 95, 90, 85, 88, 92])
        
        # Apply severity multiplier
        severity_factor = severity / 5.0  # Normalize to 0-2 range
        scenario_impact = [val * (1 + (severity_factor - 1) * 0.3) for val in base_impact[:len(time_data)]]
        
        return time_data, scenario_impact
    
    @staticmethod
    def get_client_economic_response_data(event_type: str) -> Tuple[List[str], List[float]]:
        """Generate client response to economic events by segment."""
        segments = DataService.CLIENT_SEGMENTS
        
        # Different segments respond differently to economic events
        response_patterns = {
            'currency': [0.8, 1.2, 1.0, 0.9, 1.1],  # Corporate most affected
            'interest': [1.1, 0.9, 1.0, 0.8, 1.0],  # Retail most affected
            'inflation': [1.2, 0.8, 1.0, 0.7, 0.9],  # Retail most affected
            'gdp': [0.9, 1.1, 1.0, 1.2, 1.0],       # HNW and Corporate benefit
            'political': [1.0, 0.9, 0.95, 0.8, 1.2], # Government most affected
            'oil': [1.0, 1.1, 1.0, 0.9, 1.0]        # Corporate affected
        }
        
        responses = response_patterns.get(event_type, [1.0] * len(segments))
        return segments, responses
    
    @staticmethod
    def get_regional_economic_impact_data(event_type: str) -> Tuple[List[str], List[float]]:
        """Generate regional economic impact data."""
        regions = ["Greater Tunis", "Sfax Region", "Sousse-Monastir", "Northern Coast", "Interior", "South"]
        
        # Different regions have different economic sensitivities
        regional_impacts = {
            'currency': [0.9, 1.2, 1.0, 0.8, 1.1, 1.0],  # Sfax (export) most affected
            'interest': [1.0, 1.0, 1.1, 0.9, 0.8, 0.9],  # Tourism areas affected
            'inflation': [1.1, 1.0, 1.1, 1.2, 1.3, 1.2], # Rural areas more affected
            'gdp': [1.2, 1.1, 1.0, 0.9, 0.8, 0.8],       # Urban areas benefit more
            'political': [1.1, 0.9, 1.0, 1.0, 1.2, 1.1], # Interior most affected
            'oil': [1.0, 1.1, 1.0, 1.0, 1.2, 1.1]        # Transport-dependent areas
        }
        
        impacts = regional_impacts.get(event_type, [1.0] * len(regions))
        return regions, impacts
    
    @staticmethod
    def get_portfolio_risk_data(event_type: str) -> Tuple[List[str], List[float]]:
        """Generate portfolio risk analysis data."""
        risk_categories = ["Credit Risk", "Market Risk", "Operational Risk", "Liquidity Risk", "Country Risk"]
        
        # Risk levels change based on economic event
        risk_patterns = {
            'currency': [1.2, 1.5, 1.0, 1.3, 1.4],
            'interest': [1.3, 1.2, 1.0, 1.1, 1.1],
            'inflation': [1.1, 1.3, 1.1, 1.2, 1.2],
            'gdp': [1.4, 1.1, 1.0, 1.0, 1.2],
            'political': [1.2, 1.3, 1.4, 1.3, 1.8],
            'oil': [1.1, 1.2, 1.1, 1.1, 1.3]
        }
        
        risk_levels = risk_patterns.get(event_type, [1.0] * len(risk_categories))
        return risk_categories, risk_levels
    
    @staticmethod
    def get_tunisia_map_data(map_view: str) -> Dict[str, Any]:
        """Generate Tunisia map visualization data."""
        governorates = DataService.TUNISIAN_GOVERNORATES
        
        if map_view == 'clients':
            values = [random.randint(500, 5000) for _ in governorates]
            metric = "Client Count"
        elif map_view == 'branches':
            values = [random.randint(3, 25) for _ in governorates]
            metric = "Branch Count"
        elif map_view == 'penetration':
            values = [random.uniform(10, 45) for _ in governorates]
            metric = "Market Penetration %"
        else:  # potential
            values = [random.uniform(0.5, 3.0) for _ in governorates]
            metric = "Growth Potential"
        
        return {
            'governorates': governorates,
            'values': values,
            'metric': metric
        }
    
    @staticmethod
    def get_economic_indicators_tunisia() -> Dict[str, Any]:
        """Get current Tunisian economic indicators for simulation."""
        return {
            'central_bank_rate': 8.0,
            'usd_tnd_rate': 3.18,
            'inflation_rate': 7.3,
            'gdp_growth': 2.1,
            'unemployment_rate': 15.2,
            'external_debt': 87.4,  # % of GDP
            'last_updated': '2025-08-04'
        }
    
    @staticmethod
    def get_real_time_simulation_status() -> Dict[str, Any]:
        """Get real-time simulation engine status."""
        return {
            'engine_status': 'Running',
            'active_agents': random.randint(48000, 52000),
            'scenarios_running': random.randint(3, 8),
            'last_update': '2 minutes ago',
            'cpu_usage': random.uniform(45, 75),
            'memory_usage': random.uniform(60, 85),
            'queue_size': random.randint(0, 15)
        }
    
    @staticmethod
    def generate_simulation_export_data() -> pd.DataFrame:
        """Generate comprehensive simulation data for export."""
        # Generate sample simulation results
        governorates = DataService.TUNISIAN_GOVERNORATES
        data = []
        
        for gov in governorates:
            data.append({
                'Governorate': gov,
                'Active_Agents': random.randint(500, 5000),
                'Digital_Adoption_Rate': random.uniform(40, 90),
                'Branch_Count': random.randint(2, 20),
                'Market_Share': random.uniform(10, 45),
                'Client_Satisfaction': random.uniform(7.0, 9.5),
                'Revenue_Per_Client': random.uniform(150, 450),
                'Churn_Risk': random.uniform(2, 12)
            })
        
        return pd.DataFrame(data)
    
    # Legacy methods for compatibility
    @staticmethod
    def get_key_metrics() -> Dict[str, Dict[str, str]]:
        """Get key metrics (legacy compatibility)."""
        return DataService.get_simulation_metrics()
    
    
    @staticmethod
    def get_client_segmentation_data() -> Tuple[List[str], List[int]]:
        """Generate client segmentation data."""
        segments = ["Retail", "Corporate", "SME", "Private"]
        sizes = [62, 20, 10, 8]
        return segments, sizes
    
    @staticmethod
    def get_governorate_data() -> Tuple[List[str], List[int]]:
        """Generate data for Tunisian governorates."""
        governorates = ["Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte", "Ariana"]
        counts = [3200, 2100, 1850, 1300, 1400, 1600]
        return governorates, counts
    
    @staticmethod
    def get_economic_indicators() -> Tuple[List[str], List[float]]:
        """Generate economic indicators data."""
        indicators = ['GDP Growth', 'Inflation', 'Unemployment', 'Consumer Confidence']
        values = [random.uniform(1, 8) for _ in indicators]
        return indicators, values