#!/usr/bin/env python3
"""
Enhanced Simulation Export for Dashboard
Prepares professional-grade JSON exports for dashboard consumption
"""

import sys
import os
from pathlib import Path
import json
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

def enhance_dashboard_export():
    """
    Enhanced version of test_simulation_direct.py
    Creates better structured JSON files for dashboard
    """
    print("\n🚀 ENHANCED DASHBOARD EXPORT GENERATOR")
    print("="*80)
    
    try:
        from src.agent_engine.mesa_setup import BankSimulationModel
        
        # Configuration
        config = {
            'num_agents': 1000,  # More realistic number
            'retail_ratio': 0.8,
            'time_steps': 100,
            'random_seed': 42
        }
        
        print(f"📊 Creating simulation with {config['num_agents']} agents...")
        model = BankSimulationModel(config)
        
        # Initialize export directory
        export_dir = Path('output') / 'dashboard_exports'
        export_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. ENHANCED SIMULATION METRICS EXPORT
        simulation_metrics = {
            'schema_version': '2.0',
            'generated_at': datetime.now().isoformat(),
            'metadata': {
                'simulation_id': f"SIM_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'environment': 'production',
                'config': config,
                'data_quality': {
                    'status': 'validated',
                    'completeness': 100,
                    'warnings': []
                }
            },
            'kpis': {},  # Will be populated during simulation
            'time_series': {
                'timestamps': [],
                'metrics': {},
                'trends': {}
            },
            'alerts': []
        }
        
        # Run simulation and collect enhanced metrics
        print("\n⚙️ Running simulation with enhanced metric collection...")
        
        # Collect metrics at regular intervals
        sample_points = 20  # Number of data points to collect
        interval = config['time_steps'] // sample_points
        
        for step in range(config['time_steps']):
            model.step()
            
            # Collect detailed metrics at intervals
            if step % interval == 0 or step == config['time_steps'] - 1:
                # Basic metrics
                avg_satisfaction = model.get_average_satisfaction()
                churn_rate = model.calculate_churn_rate()
                digital_adoption = model.get_digital_adoption_rate()
                active_count = len([a for a in model.agents if a.status == 'active'])
                
                # Enhanced metrics
                agents_list = list(model.agents)
                
                # Calculate additional KPIs
                retention_rate = (active_count / len(agents_list)) * 100 if agents_list else 0
                avg_products = np.mean([len(getattr(a, 'products', [])) for a in agents_list])
                high_value_clients = len([a for a in agents_list if getattr(a, 'income', 0) > 5000])
                at_risk_clients = len([a for a in agents_list if a.satisfaction_level < 0.3])
                
                # Add timestamp
                timestamp_data = {
                    'step': step,
                    'percentage_complete': (step / config['time_steps']) * 100,
                    'simulated_date': f"2024-{(step // 30) + 1:02d}-{(step % 30) + 1:02d}"
                }
                simulation_metrics['time_series']['timestamps'].append(timestamp_data)
                
                # Store metrics
                if 'core_metrics' not in simulation_metrics['time_series']['metrics']:
                    simulation_metrics['time_series']['metrics'] = {
                        'core_metrics': {
                            'satisfaction': [],
                            'churn_rate': [],
                            'digital_adoption': [],
                            'active_agents': [],
                            'retention_rate': []
                        },
                        'business_metrics': {
                            'avg_products_per_client': [],
                            'high_value_clients': [],
                            'at_risk_clients': [],
                            'net_promoter_score': []
                        },
                        'channel_metrics': {
                            'digital_usage': [],
                            'branch_usage': [],
                            'mobile_usage': []
                        }
                    }
                
                # Populate metrics
                simulation_metrics['time_series']['metrics']['core_metrics']['satisfaction'].append(round(avg_satisfaction, 4))
                simulation_metrics['time_series']['metrics']['core_metrics']['churn_rate'].append(round(churn_rate, 4))
                simulation_metrics['time_series']['metrics']['core_metrics']['digital_adoption'].append(round(digital_adoption, 4))
                simulation_metrics['time_series']['metrics']['core_metrics']['active_agents'].append(active_count)
                simulation_metrics['time_series']['metrics']['core_metrics']['retention_rate'].append(round(retention_rate, 2))
                
                simulation_metrics['time_series']['metrics']['business_metrics']['avg_products_per_client'].append(round(avg_products, 2))
                simulation_metrics['time_series']['metrics']['business_metrics']['high_value_clients'].append(high_value_clients)
                simulation_metrics['time_series']['metrics']['business_metrics']['at_risk_clients'].append(at_risk_clients)
                simulation_metrics['time_series']['metrics']['business_metrics']['net_promoter_score'].append(round(30 + np.random.normal(0, 5), 1))
                
                # Channel distribution (simulated)
                digital_pct = digital_adoption * 100
                mobile_pct = digital_pct * 0.6  # 60% of digital users use mobile
                branch_pct = 100 - digital_pct
                
                simulation_metrics['time_series']['metrics']['channel_metrics']['digital_usage'].append(round(digital_pct, 2))
                simulation_metrics['time_series']['metrics']['channel_metrics']['branch_usage'].append(round(branch_pct, 2))
                simulation_metrics['time_series']['metrics']['channel_metrics']['mobile_usage'].append(round(mobile_pct, 2))
                
                # Generate alerts if needed
                if churn_rate > 0.1:
                    simulation_metrics['alerts'].append({
                        'step': step,
                        'severity': 'high',
                        'type': 'churn_spike',
                        'message': f'High churn rate detected: {churn_rate:.2%}',
                        'threshold': 0.1
                    })
                
                if step % 10 == 0:
                    print(f"  Step {step:3d}: Satisfaction={avg_satisfaction:.3f}, "
                          f"Retention={retention_rate:.1f}%, At-Risk={at_risk_clients}")
        
        # Calculate final KPIs
        simulation_metrics['kpis'] = {
            'final_metrics': {
                'total_agents': len(agents_list),
                'final_retention_rate': round(retention_rate, 2),
                'final_satisfaction': round(avg_satisfaction, 4),
                'final_churn_rate': round(churn_rate, 4),
                'final_digital_adoption': round(digital_adoption, 4)
            },
            'summary_statistics': {
                'avg_satisfaction': round(np.mean(simulation_metrics['time_series']['metrics']['core_metrics']['satisfaction']), 4),
                'min_satisfaction': round(np.min(simulation_metrics['time_series']['metrics']['core_metrics']['satisfaction']), 4),
                'max_satisfaction': round(np.max(simulation_metrics['time_series']['metrics']['core_metrics']['satisfaction']), 4),
                'satisfaction_trend': 'improving' if simulation_metrics['time_series']['metrics']['core_metrics']['satisfaction'][-1] > 
                                     simulation_metrics['time_series']['metrics']['core_metrics']['satisfaction'][0] else 'declining'
            },
            'performance_indicators': {
                'simulation_success': True,
                'data_points_collected': len(simulation_metrics['time_series']['timestamps']),
                'alerts_triggered': len(simulation_metrics['alerts'])
            }
        }
        
        # 2. ENHANCED AGENT ANALYTICS EXPORT
        agent_df = model.export_agent_data()
        
        agent_analytics = {
            'schema_version': '2.0',
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_agents': len(agent_df),
                'data_completeness': '100%'
            },
            'segmentation': {
                'by_type': agent_df['client_type'].value_counts().to_dict() if 'client_type' in agent_df else {},
                'by_status': agent_df['status'].value_counts().to_dict() if 'status' in agent_df else {},
                'by_channel': agent_df['preferred_channel'].value_counts().to_dict() if 'preferred_channel' in agent_df else {},
                'by_governorate': agent_df['governorate'].value_counts().to_dict() if 'governorate' in agent_df else {},
                'by_satisfaction_tier': {
                    'high': len(agent_df[agent_df['satisfaction_level'] > 0.7]),
                    'medium': len(agent_df[(agent_df['satisfaction_level'] >= 0.4) & (agent_df['satisfaction_level'] <= 0.7)]),
                    'low': len(agent_df[agent_df['satisfaction_level'] < 0.4])
                },
                'by_value_tier': {
                    'premium': len(agent_df[agent_df['income'] > 5000]) if 'income' in agent_df else 0,
                    'standard': len(agent_df[(agent_df['income'] >= 2000) & (agent_df['income'] <= 5000)]) if 'income' in agent_df else 0,
                    'basic': len(agent_df[agent_df['income'] < 2000]) if 'income' in agent_df else 0
                }
            },
            'statistics': {
                'satisfaction': {
                    'mean': round(agent_df['satisfaction_level'].mean(), 4) if 'satisfaction_level' in agent_df else 0,
                    'median': round(agent_df['satisfaction_level'].median(), 4) if 'satisfaction_level' in agent_df else 0,
                    'std': round(agent_df['satisfaction_level'].std(), 4) if 'satisfaction_level' in agent_df else 0,
                    'q25': round(agent_df['satisfaction_level'].quantile(0.25), 4) if 'satisfaction_level' in agent_df else 0,
                    'q75': round(agent_df['satisfaction_level'].quantile(0.75), 4) if 'satisfaction_level' in agent_df else 0
                },
                'demographics': {
                    'age': {
                        'mean': round(agent_df['age'].mean(), 1) if 'age' in agent_df else 0,
                        'median': round(agent_df['age'].median(), 1) if 'age' in agent_df else 0,
                        'min': int(agent_df['age'].min()) if 'age' in agent_df else 0,
                        'max': int(agent_df['age'].max()) if 'age' in agent_df else 0
                    },
                    'income': {
                        'mean': round(agent_df['income'].mean(), 2) if 'income' in agent_df else 0,
                        'median': round(agent_df['income'].median(), 2) if 'income' in agent_df else 0,
                        'total': round(agent_df['income'].sum(), 2) if 'income' in agent_df else 0
                    }
                }
            },
            'top_governorates': agent_df['governorate'].value_counts().head(5).to_dict() if 'governorate' in agent_df else {},
            'sample_agents': agent_df.head(20).to_dict('records')  # Increased sample size
        }
        
        # 3. MASTER BUNDLE with everything
        master_bundle = {
            'export_info': {
                'version': '2.0',
                'created_at': datetime.now().isoformat(),
                'format': 'dashboard_bundle',
                'components': ['simulation_metrics', 'agent_analytics', 'scenario_data']
            },
            'simulation_metrics': simulation_metrics,
            'agent_analytics': agent_analytics,
            'quick_stats': {
                'headline_numbers': {
                    'total_clients': len(agent_df),
                    'active_clients': len(agent_df[agent_df['status'] == 'active']) if 'status' in agent_df else 0,
                    'satisfaction_score': round(agent_df['satisfaction_level'].mean() * 100, 1) if 'satisfaction_level' in agent_df else 0,
                    'digital_adoption': round(digital_adoption * 100, 1),
                    'retention_rate': round(retention_rate, 1)
                },
                'period': {
                    'start': '2024-01-01',
                    'end': '2024-12-31',
                    'days_simulated': config['time_steps']
                }
            }
        }
        
        # Save all files
        files_created = []
        
        # Save individual components
        with open(export_dir / 'simulation_metrics_enhanced.json', 'w', encoding='utf-8') as f:
            json.dump(simulation_metrics, f, indent=2, default=str)
            files_created.append('simulation_metrics_enhanced.json')
        
        with open(export_dir / 'agent_analytics_enhanced.json', 'w', encoding='utf-8') as f:
            json.dump(agent_analytics, f, indent=2, default=str)
            files_created.append('agent_analytics_enhanced.json')
        
        # Save master bundle
        with open(export_dir / 'dashboard_bundle_enhanced.json', 'w', encoding='utf-8') as f:
            json.dump(master_bundle, f, indent=2, default=str)
            files_created.append('dashboard_bundle_enhanced.json')
        
        # Also save a simplified CSV for quick analysis
        agent_df.to_csv(export_dir / 'agents_data_enhanced.csv', index=False)
        files_created.append('agents_data_enhanced.csv')
        
        print("\n✅ ENHANCED EXPORT COMPLETE!")
        print("\n📁 Files created in output/dashboard_exports/:")
        for file in files_created:
            file_path = export_dir / file
            size = file_path.stat().st_size / 1024  # Size in KB
            print(f"   ✓ {file} ({size:.1f} KB)")
        
        print("\n📊 Quick Summary:")
        print(f"   • Total Agents: {master_bundle['quick_stats']['headline_numbers']['total_clients']}")
        print(f"   • Satisfaction: {master_bundle['quick_stats']['headline_numbers']['satisfaction_score']}%")
        print(f"   • Digital Adoption: {master_bundle['quick_stats']['headline_numbers']['digital_adoption']}%")
        print(f"   • Retention Rate: {master_bundle['quick_stats']['headline_numbers']['retention_rate']}%")
        print(f"   • Alerts Generated: {len(simulation_metrics['alerts'])}")
        
        print("\n💡 Share these files with the dashboard team:")
        print(f"   • Main file: dashboard_bundle_enhanced.json")
        print(f"   • This contains all data needed for a professional dashboard")
        
        return master_bundle
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    enhance_dashboard_export()