"""
Data Management Utilities
Create: utils/data_utils.py
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """Centralized data management for the banking simulation dashboard"""
    
    def __init__(self):
        self.data_cache = {}
        self.last_refresh = None
        
    def get_data_sources(self):
        """Get all available data sources and their status"""
        sources = {
            'simulation_bundle': {
                'path': 'output/dashboard_exports/dashboard_bundle_enhanced.json',
                'type': 'json',
                'status': 'unknown'
            },
            'agents_data': {
                'path': 'output/dashboard_exports/agents_data_enhanced.csv', 
                'type': 'csv',
                'status': 'unknown'
            },
            'retail_training': {
                'path': 'data/ctgan/training_data/retail_training_data_20250807_154910.csv',
                'type': 'csv',
                'status': 'unknown'
            },
            'corporate_training': {
                'path': 'data/ctgan/training_data/corporate_training_data_20250807_155356.csv',
                'type': 'csv', 
                'status': 'unknown'
            },
            'simulation_metrics': {
                'path': 'output/dashboard_exports/simulation_metrics_enhanced.json',
                'type': 'json',
                'status': 'unknown'
            },
            'agent_analytics': {
                'path': 'output/dashboard_exports/agent_analytics_enhanced.json',
                'type': 'json',
                'status': 'unknown'
            }
        }
        
        # Check status of each source
        for source_name, source_info in sources.items():
            path = Path(source_info['path'])
            if path.exists():
                source_info['status'] = 'available'
                source_info['last_modified'] = datetime.fromtimestamp(path.stat().st_mtime).isoformat()
                source_info['size_kb'] = round(path.stat().st_size / 1024, 2)
            else:
                source_info['status'] = 'missing'
                
        return sources
    
    def load_all_data(self, force_refresh=False):
        """Load all available data sources"""
        if not force_refresh and self.data_cache and self.last_refresh:
            # Return cached data if available and not forcing refresh
            return self.data_cache
            
        logger.info("Loading all data sources...")
        data = {}
        
        sources = self.get_data_sources()
        
        for source_name, source_info in sources.items():
            if source_info['status'] == 'available':
                try:
                    if source_info['type'] == 'json':
                        data[source_name] = self._load_json_file(source_info['path'])
                    elif source_info['type'] == 'csv':
                        data[source_name] = self._load_csv_file(source_info['path'])
                    logger.info(f"Successfully loaded {source_name}")
                except Exception as e:
                    logger.error(f"Error loading {source_name}: {e}")
                    data[source_name] = None
            else:
                data[source_name] = None
                
        self.data_cache = data
        self.last_refresh = datetime.now()
        return data
    
    def _load_json_file(self, path):
        """Load JSON file"""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_csv_file(self, path):
        """Load CSV file with proper handling"""
        return pd.read_csv(path, encoding='utf-8')
    
    def get_current_kpis(self):
        """Extract current KPIs from loaded data"""
        data = self.load_all_data()
        
        # Try to get from simulation bundle first
        if data.get('simulation_bundle'):
            try:
                quick_stats = data['simulation_bundle']['quick_stats']['headline_numbers']
                return {
                    'total_clients': quick_stats.get('total_clients', 0),
                    'active_clients': quick_stats.get('active_clients', 0),
                    'satisfaction_score': quick_stats.get('satisfaction_score', 0),
                    'digital_adoption': quick_stats.get('digital_adoption', 0),
                    'retention_rate': quick_stats.get('retention_rate', 0)
                }
            except KeyError:
                pass
        
        # Fallback calculations from other sources
        kpis = {'total_clients': 0, 'active_clients': 0, 'satisfaction_score': 0, 
                'digital_adoption': 0, 'retention_rate': 0}
        
        if data.get('agents_data') is not None:
            agents_df = data['agents_data']
            kpis['total_clients'] = len(agents_df)
            kpis['active_clients'] = len(agents_df[agents_df['status'] == 'active']) if 'status' in agents_df.columns else len(agents_df)
            
            if 'satisfaction_level' in agents_df.columns:
                kpis['satisfaction_score'] = round(agents_df['satisfaction_level'].mean() * 100, 1)
                
            kpis['retention_rate'] = round((kpis['active_clients'] / kpis['total_clients']) * 100, 1) if kpis['total_clients'] > 0 else 100
        
        return kpis
    
    def get_segmentation_data(self):
        """Get segmentation data for charts"""
        data = self.load_all_data()
        
        segmentation = {
            'by_governorate': {},
            'by_type': {},
            'by_satisfaction_tier': {},
            'by_value_tier': {},
            'by_channel': {}
        }
        
        # Try agent analytics first
        if data.get('agent_analytics'):
            try:
                analytics = data['agent_analytics']['segmentation']
                segmentation.update(analytics)
                return segmentation
            except KeyError:
                pass
        
        # Try simulation bundle
        if data.get('simulation_bundle') and 'agent_analytics' in data['simulation_bundle']:
            try:
                analytics = data['simulation_bundle']['agent_analytics']['segmentation']
                segmentation.update(analytics)
                return segmentation
            except KeyError:
                pass
        
        # Fallback to agents data calculation
        if data.get('agents_data') is not None:
            agents_df = data['agents_data']
            
            if 'governorate' in agents_df.columns:
                segmentation['by_governorate'] = agents_df['governorate'].value_counts().to_dict()
                
            if 'client_type' in agents_df.columns:
                segmentation['by_type'] = agents_df['client_type'].value_counts().to_dict()
                
            if 'satisfaction_level' in agents_df.columns:
                # Create satisfaction tiers
                agents_df['satisfaction_tier'] = pd.cut(
                    agents_df['satisfaction_level'], 
                    bins=[0, 0.4, 0.7, 1.0], 
                    labels=['low', 'medium', 'high']
                )
                segmentation['by_satisfaction_tier'] = agents_df['satisfaction_tier'].value_counts().to_dict()
        
        return segmentation
    
    def get_time_series_data(self):
        """Get time series data for evolution charts"""
        data = self.load_all_data()
        
        # Try simulation bundle first
        if data.get('simulation_bundle') and 'simulation_metrics' in data['simulation_bundle']:
            try:
                metrics = data['simulation_bundle']['simulation_metrics']['time_series']
                return metrics
            except KeyError:
                pass
        
        # Try simulation metrics file
        if data.get('simulation_metrics'):
            try:
                return data['simulation_metrics']['time_series']
            except KeyError:
                pass
                
        return None
    
    def get_training_data_insights(self):
        """Get insights from training data"""
        data = self.load_all_data()
        insights = {}
        
        # Retail training insights
        if data.get('retail_training') is not None:
            retail_df = data['retail_training']
            
            insights['retail'] = {
                'age_group_distribution': retail_df['age_group'].value_counts().to_dict() if 'age_group' in retail_df.columns else {},
                'income_quintile_distribution': retail_df['income_quintile'].value_counts().to_dict() if 'income_quintile' in retail_df.columns else {},
                'digital_adoption_by_age': retail_df.groupby('age_group')['digital_adoption'].mean().to_dict() if all(col in retail_df.columns for col in ['age_group', 'digital_adoption']) else {},
                'satisfaction_by_age': retail_df.groupby('age_group')['satisfaction_score'].mean().to_dict() if all(col in retail_df.columns for col in ['age_group', 'satisfaction_score']) else {}
            }
        
        # Corporate training insights
        if data.get('corporate_training') is not None:
            corporate_df = data['corporate_training']
            
            insights['corporate'] = {
                'sector_distribution': corporate_df['business_sector'].value_counts().to_dict() if 'business_sector' in corporate_df.columns else {},
                'size_distribution': corporate_df['company_size'].value_counts().to_dict() if 'company_size' in corporate_df.columns else {},
                'digital_maturity_by_sector': corporate_df.groupby('business_sector')['digital_maturity_score'].mean().to_dict() if all(col in corporate_df.columns for col in ['business_sector', 'digital_maturity_score']) else {},
                'revenue_by_sector': corporate_df.groupby('business_sector')['annual_revenue'].mean().to_dict() if all(col in corporate_df.columns for col in ['business_sector', 'annual_revenue']) else {}
            }
        
        return insights
    
    def check_simulation_output_exists(self):
        """Check if simulation output files exist"""
        output_dir = Path('output/dashboard_exports')
        if not output_dir.exists():
            return False, "Output directory does not exist"
            
        required_files = [
            'dashboard_bundle_enhanced.json',
            'simulation_metrics_enhanced.json', 
            'agent_analytics_enhanced.json'
        ]
        
        missing_files = []
        for filename in required_files:
            if not (output_dir / filename).exists():
                missing_files.append(filename)
        
        if missing_files:
            return False, f"Missing files: {', '.join(missing_files)}"
        
        return True, "All simulation output files present"
    
    def get_data_freshness(self):
        """Get information about data freshness"""
        sources = self.get_data_sources()
        freshness_info = {
            'most_recent': None,
            'oldest': None,
            'sources_count': {'available': 0, 'missing': 0},
            'details': {}
        }
        
        available_sources = {k: v for k, v in sources.items() if v['status'] == 'available'}
        
        if available_sources:
            # Find most recent and oldest
            modification_times = []
            for source_name, source_info in available_sources.items():
                mod_time = datetime.fromisoformat(source_info['last_modified'])
                modification_times.append((source_name, mod_time))
                
            modification_times.sort(key=lambda x: x[1])
            
            freshness_info['oldest'] = {
                'source': modification_times[0][0],
                'timestamp': modification_times[0][1].isoformat()
            }
            freshness_info['most_recent'] = {
                'source': modification_times[-1][0], 
                'timestamp': modification_times[-1][1].isoformat()
            }
        
        freshness_info['sources_count']['available'] = len([s for s in sources.values() if s['status'] == 'available'])
        freshness_info['sources_count']['missing'] = len([s for s in sources.values() if s['status'] == 'missing'])
        freshness_info['details'] = sources
        
        return freshness_info

# Global data manager instance
data_manager = DataManager()

def get_data_manager():
    """Get the global data manager instance"""
    return data_manager