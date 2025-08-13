"""
Simulation Reporter for Bank Client Simulation
Handles reporting and output generation for simulations
"""
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

class SimulationReporter:
    """Handles simulation reporting and output generation"""
    
    def __init__(self, output_dir: str = "simulation_outputs"):
        """Initialize reporter with output directory"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger('SimulationReporter')
        
        # Store reports
        self.reports = []
        self.current_report = None
    
    def start_report(self, scenario_name: str, metadata: Dict[str, Any] = None):
        """Start a new report for a scenario"""
        self.current_report = {
            'scenario_name': scenario_name,
            'start_time': datetime.now().isoformat(),
            'metadata': metadata or {},
            'metrics': [],
            'events': [],
            'final_results': {}
        }
        self.logger.info(f"Started report for scenario: {scenario_name}")
    
    def add_metric(self, step: int, metric_name: str, value: float):
        """Add a metric measurement to the current report"""
        if self.current_report:
            self.current_report['metrics'].append({
                'step': step,
                'metric': metric_name,
                'value': value,
                'timestamp': datetime.now().isoformat()
            })
    
    def add_event(self, step: int, event_type: str, description: str, impact: Dict[str, Any] = None):
        """Add an event record to the current report"""
        if self.current_report:
            self.current_report['events'].append({
                'step': step,
                'event_type': event_type,
                'description': description,
                'impact': impact or {},
                'timestamp': datetime.now().isoformat()
            })
    
    def finalize_report(self, final_metrics: Dict[str, Any], outcome_validation: List[Dict] = None):
        """Finalize the current report with final results"""
        if self.current_report:
            self.current_report['end_time'] = datetime.now().isoformat()
            self.current_report['final_results'] = final_metrics
            self.current_report['outcome_validation'] = outcome_validation or []
            
            # Save report
            self.save_report(self.current_report)
            self.reports.append(self.current_report)
            
            self.logger.info(f"Finalized report for scenario: {self.current_report['scenario_name']}")
            self.current_report = None
    
    def save_report(self, report: Dict[str, Any], format: str = 'json'):
        """Save a report to file"""
        scenario_name = report['scenario_name'].replace(' ', '_').lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = self.output_dir / f"{scenario_name}_report_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.info(f"Report saved to: {filename}")
            return filename
        
        elif format == 'csv':
            # Save metrics as CSV
            if report['metrics']:
                df = pd.DataFrame(report['metrics'])
                filename = self.output_dir / f"{scenario_name}_metrics_{timestamp}.csv"
                df.to_csv(filename, index=False)
                self.logger.info(f"Metrics saved to: {filename}")
                return filename
        
        return None
    
    def generate_summary(self, reports: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a summary across multiple reports"""
        reports_to_summarize = reports or self.reports
        
        if not reports_to_summarize:
            return {}
        
        summary = {
            'total_scenarios': len(reports_to_summarize),
            'scenarios': [],
            'aggregate_metrics': {}
        }
        
        for report in reports_to_summarize:
            scenario_summary = {
                'name': report['scenario_name'],
                'start_time': report.get('start_time'),
                'end_time': report.get('end_time'),
                'events_count': len(report.get('events', [])),
                'final_metrics': report.get('final_results', {})
            }
            summary['scenarios'].append(scenario_summary)
        
        return summary
    
    def export_dashboard_data(self) -> Dict[str, Any]:
        """Export data formatted for dashboard visualization"""
        dashboard_data = {
            'scenarios': [],
            'metrics_timeline': [],
            'events_timeline': []
        }
        
        for report in self.reports:
            # Add scenario info
            dashboard_data['scenarios'].append({
                'name': report['scenario_name'],
                'start': report.get('start_time'),
                'end': report.get('end_time')
            })
            
            # Add metrics timeline
            for metric in report.get('metrics', []):
                dashboard_data['metrics_timeline'].append({
                    'scenario': report['scenario_name'],
                    'step': metric['step'],
                    'metric': metric['metric'],
                    'value': metric['value']
                })
            
            # Add events timeline
            for event in report.get('events', []):
                dashboard_data['events_timeline'].append({
                    'scenario': report['scenario_name'],
                    'step': event['step'],
                    'type': event['event_type'],
                    'description': event['description']
                })
        
        return dashboard_data