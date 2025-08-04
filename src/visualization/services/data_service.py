"""
Data service for generating and processing dashboard data
"""
import random
import pandas as pd
from typing import Dict, List, Tuple


class DataService:
    """Service class for handling all data operations."""
    
    @staticmethod
    def get_client_growth_data() -> Tuple[List[str], List[int]]:
        """Generate client growth data over time."""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        clients = [11500, 12000, 12250, 12500, 12800, 12847]
        return months, clients
    
    @staticmethod
    def get_revenue_data() -> Tuple[List[str], List[int]]:
        """Generate monthly revenue data."""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [200, 250, 260, 270, 310, 340]
        return months, revenue
    
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
    
    @staticmethod
    def get_economic_trends() -> Tuple[List[str], List[float]]:
        """Generate economic trends over time."""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        economic_data = [100, 102, 104, 103, 105, 107]
        return months, economic_data
    
    @staticmethod
    def get_branch_distribution() -> Tuple[List[str], List[int]]:
        """Generate branch type distribution data."""
        branch_types = ['Main Branch', 'Sub Branch', 'ATM Only', 'Digital Point']
        branch_counts = [random.randint(5, 25) for _ in branch_types]
        return branch_types, branch_counts
    
    @staticmethod
    def get_key_metrics() -> Dict[str, Dict[str, str]]:
        """Generate key metrics for dashboard cards."""
        return {
            'clients': {
                'icon': '👥',
                'title': 'Total Clients',
                'value': '12,847',
                'change': '+5.2% this month'
            },
            'market_share': {
                'icon': '📈',
                'title': 'Market Share',
                'value': '34.2%',
                'change': '+2.1% this quarter'
            },
            'branches': {
                'icon': '🏢',
                'title': 'Active Branches',
                'value': '156',
                'change': '3 new branches'
            },
            'revenue': {
                'icon': '💰',
                'title': 'Revenue',
                'value': '€2.4M',
                'change': '+8.7% vs last month'
            }
        }
    
    @staticmethod
    def generate_export_data() -> pd.DataFrame:
        """Generate data for CSV export."""
        months, clients = DataService.get_client_growth_data()
        _, revenue = DataService.get_revenue_data()
        
        return pd.DataFrame({
            "Month": months,
            "Clients": clients,
            "Revenue": revenue
        })
    
    @staticmethod
    def filter_data_by_segment(data: List, segment: str) -> List:
        """Filter data by client segment."""
        if segment == 'all':
            return data
        # Implement segment-specific filtering logic here
        # This is a placeholder implementation
        return data
    
    @staticmethod
    def sort_data(data: List, sort_type: str) -> List:
        """Sort data based on sort type."""
        if sort_type == 'alpha':
            return sorted(data)
        elif sort_type == 'clients_desc':
            return sorted(data, reverse=True)
        elif sort_type == 'clients_asc':
            return sorted(data)
        return data