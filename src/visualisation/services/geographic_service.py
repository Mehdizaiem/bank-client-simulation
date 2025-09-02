"""
Geographic Service - Simplified for single simulation approach
"""

from __future__ import annotations

import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


class GeographicService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._load_real_data()

    def _load_real_data(self) -> None:
        """Load simulation data from output directory"""
        try:
            self.simulation_data = self._load_simulation_data()
            self.training_data = self._load_training_data()
            self.logger.info("Data loading - Simulation: %s, Training: %s", 
                           bool(self.simulation_data), self.training_data is not None)
        except Exception as e:
            self.logger.error("Error loading data: %s", e)
            self.simulation_data = None
            self.training_data = None

    def _load_simulation_data(self) -> Optional[Dict[str, Any]]:
        """Load simulation results from output/dashboard_exports"""
        try:
            output_dir = Path("output/dashboard_exports")
            
            # Try enhanced bundle first
            bundle = output_dir / "dashboard_bundle_enhanced.json"
            if bundle.exists():
                return json.loads(bundle.read_text(encoding="utf-8"))
            
            # Try standard bundle
            bundle = output_dir / "dashboard_bundle.json"
            if bundle.exists():
                return json.loads(bundle.read_text(encoding="utf-8"))
            
            # Try individual metrics file
            sim_file = output_dir / "simulation_metrics_enhanced.json" 
            if sim_file.exists():
                return json.loads(sim_file.read_text(encoding="utf-8"))
                
            # Try standard metrics
            sim_file = output_dir / "simulation_metrics.json"
            if sim_file.exists():
                return json.loads(sim_file.read_text(encoding="utf-8"))
                
        except Exception as e:
            self.logger.error("Error reading simulation data: %s", e)
        return None

    def _load_training_data(self) -> Optional[pd.DataFrame]:
        """Load training data from data/ctgan/training_data"""
        try:
            data_dir = Path("data/ctgan/training_data")
            
            # Try specific retail training file
            retail_1000 = data_dir / "retail_training_data_20250807_154910.csv"
            if retail_1000.exists():
                df = pd.read_csv(retail_1000)
                return self._process_training_data(df)
            
            # Try any CSV in training data directory
            csvs = list(data_dir.glob("*.csv"))
            if csvs:
                df = pd.read_csv(csvs[0])
                return self._process_training_data(df)
                
        except Exception as e:
            self.logger.error("Error reading training data: %s", e)
        return None

    def _process_training_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process training data to standardize column names and values"""
        # Map numeric governorate codes to names if needed
        if "governorate" in df.columns and df["governorate"].dtype in ['int64', 'float64']:
            gov_map = {
                0: "Tunis", 1: "Ariana", 2: "Ben Arous", 3: "Manouba", 
                4: "Nabeul", 5: "Sfax", 6: "Sousse", 7: "Monastir",
                8: "Mahdia", 9: "Kairouan", 10: "Bizerte", 11: "Gafsa"
            }
            df["governorate"] = df["governorate"].map(gov_map).fillna("Unknown")
        
        return df

    def get_agent_data(self) -> Optional[pd.DataFrame]:
        """Get agent data, preferring simulation output over training data"""
        try:
            # First try to get agents data from CSV export
            agents_csv = Path("output/dashboard_exports/agents_data_enhanced.csv")
            if agents_csv.exists():
                df = pd.read_csv(agents_csv)
                self.logger.info("Loaded agents CSV with %d rows and columns: %s", len(df), list(df.columns))
                return df
            
            # Try standard agents file
            agents_csv = Path("output/dashboard_exports/agents_data.csv")
            if agents_csv.exists():
                df = pd.read_csv(agents_csv)
                self.logger.info("Loaded standard agents CSV with %d rows", len(df))
                return df
                
        except Exception as e:
            self.logger.error("Error loading agents CSV: %s", e)

        try:
            # Try to extract from JSON simulation data
            if self.simulation_data and "agent_analytics" in self.simulation_data:
                sample = self.simulation_data["agent_analytics"].get("sample_agents", [])
                if sample:
                    df = pd.DataFrame(sample)
                    self.logger.info("Extracted %d agents from JSON simulation data", len(df))
                    return df
        except Exception as e:
            self.logger.error("Error extracting agents from JSON: %s", e)

        # Fallback to training data
        if self.training_data is not None:
            self.logger.info("Using training data as fallback with %d rows", len(self.training_data))
            return self.training_data
            
        self.logger.warning("No agent data available")
        return None

    def run_simulation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run test_simulation_direct.py with the given configuration"""
        try:
            script_path = Path("test_simulation_direct.py")
            if not script_path.exists():
                return {
                    "success": False,
                    "error": "test_simulation_direct.py not found in project root. Make sure the simulation script exists."
                }
            
            # Build command for simulation
            cmd = [
                sys.executable, 
                str(script_path),
                "--num_agents", str(config.get("num_agents", 800)),
                "--retail_ratio", str(config.get("retail_ratio", 0.75)),
                "--time_steps", str(config.get("time_steps", 100)),
                "--scenario", config.get("scenario", "normal"),
                "--random_seed", str(config.get("random_seed", 42))
            ]
            
            # Add optional parameters
            if config.get("target_region"):
                cmd.extend(["--target_region", config["target_region"]])
            if config.get("target_segment"):
                cmd.extend(["--target_segment", config["target_segment"]])
            
            self.logger.info("Running simulation: %s", " ".join(cmd))
            print(f"Starting simulation with {config.get('num_agents', 800)} agents...")
            print(f"Scenario: {config.get('scenario', 'normal')}")
            print("This may take 1-2 minutes...")
            
            # Execute simulation
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                self.logger.info("Simulation completed successfully")
                print("Simulation completed successfully!")
                
                # Reload data after simulation
                self._load_real_data()
                
                return {
                    "success": True,
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else None,
                    "config": config,
                    "files_created": self._get_output_files(),
                    "message": "Simulation completed - data ready for analysis"
                }
            else:
                error_msg = f"Simulation failed (exit code {result.returncode})"
                if result.stderr:
                    error_msg += f": {result.stderr}"
                
                self.logger.error("Simulation failed: %s", error_msg)
                return {
                    "success": False,
                    "error": error_msg,
                    "output": result.stdout,
                    "config": config
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Simulation timed out after 10 minutes. Try reducing the number of agents or time steps."
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Python executable not found. Check your Python installation."
            }
        except Exception as e:
            self.logger.error("Unexpected error running simulation: %s", e)
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def _get_output_files(self) -> List[str]:
        """Get list of files created in output directory"""
        try:
            output_dir = Path("output/dashboard_exports")
            if output_dir.exists():
                files = [f.name for f in output_dir.iterdir() if f.is_file()]
                self.logger.info("Output files created: %s", files)
                return files
        except Exception as e:
            self.logger.error("Error listing output files: %s", e)
        return []

    def get_available_regions(self) -> List[str]:
        """Get list of available regions from actual data"""
        df = self.get_agent_data()
        if df is None or df.empty:
            return []
        
        if "governorate" in df.columns:
            regions = df["governorate"].dropna().unique().tolist()
            return [str(r) for r in regions if str(r) != 'nan']
        return []

    def get_simulation_summary(self) -> Dict[str, Any]:
        """Get comprehensive simulation summary"""
        try:
            if not self.simulation_data:
                return {"error": "No simulation data available"}
            
            # Extract key metrics
            simulation_metrics = self.simulation_data.get('simulation_metrics', {})
            agent_analytics = self.simulation_data.get('agent_analytics', {})
            
            # Final KPIs
            kpis = simulation_metrics.get('kpis', {})
            final_metrics = kpis.get('final_metrics', {})
            
            # Time series data
            time_series = simulation_metrics.get('time_series', {})
            
            # Agent data
            agent_data = self.get_agent_data()
            agent_count = len(agent_data) if agent_data is not None else 0
            
            summary = {
                "simulation_completed": True,
                "agent_count": agent_count,
                "final_metrics": final_metrics,
                "time_series_available": bool(time_series.get('timestamps')),
                "regions_available": self.get_available_regions(),
                "data_sources": {
                    "simulation_json": bool(self.simulation_data),
                    "agent_csv": agent_data is not None,
                    "training_data": self.training_data is not None
                },
                "key_metrics": {
                    "satisfaction": final_metrics.get('final_satisfaction', 0),
                    "retention": final_metrics.get('final_retention_rate', 0),
                    "churn": final_metrics.get('final_churn_rate', 0),
                    "digital_adoption": final_metrics.get('final_digital_adoption', 0)
                }
            }
            
            return summary
            
        except Exception as e:
            self.logger.error("Error creating simulation summary: %s", e)
            return {"error": f"Error creating summary: {e}"}

    def validate_simulation_data(self) -> Dict[str, Any]:
        """Validate that simulation data is complete and usable"""
        validation = {
            "valid": True,
            "issues": [],
            "data_sources": {},
            "recommendations": []
        }
        
        try:
            # Check simulation JSON
            if not self.simulation_data:
                validation["issues"].append("No simulation JSON data found")
                validation["recommendations"].append("Run a fresh simulation")
            else:
                validation["data_sources"]["json"] = "✓ Available"
                
                # Check for key sections
                required_sections = ['simulation_metrics', 'agent_analytics']
                for section in required_sections:
                    if section not in self.simulation_data:
                        validation["issues"].append(f"Missing {section} in simulation data")
            
            # Check agent data
            agent_data = self.get_agent_data()
            if agent_data is None:
                validation["issues"].append("No agent data available")
                validation["recommendations"].append("Verify simulation output files")
            else:
                validation["data_sources"]["agents"] = f"✓ {len(agent_data)} records"
                
                # Check required columns
                required_cols = ['governorate']
                missing_cols = [col for col in required_cols if col not in agent_data.columns]
                if missing_cols:
                    validation["issues"].append(f"Missing columns: {missing_cols}")
            
            # Check training data fallback
            if self.training_data is not None:
                validation["data_sources"]["training"] = f"✓ {len(self.training_data)} fallback records"
            else:
                validation["data_sources"]["training"] = "✗ Not available"
            
            validation["valid"] = len(validation["issues"]) == 0
            
        except Exception as e:
            validation["valid"] = False
            validation["issues"].append(f"Validation error: {e}")
        
        return validation

    def get_scenario_info(self) -> Dict[str, Any]:
        """Get information about available scenarios"""
        return {
            "available_scenarios": {
                "normal": "Standard market conditions with typical customer behavior",
                "digital": "Digital transformation focus - increased online adoption",
                "downturn": "Economic downturn scenario - cost-conscious behavior",
                "marketing": "Active marketing campaign - increased engagement",
                "service": "Service quality improvement initiative"
            },
            "default_scenario": "normal",
            "scenario_impacts": {
                "normal": {"satisfaction": 0.0, "retention": 0.0, "cost": 1.0},
                "digital": {"satisfaction": 0.1, "retention": 0.05, "cost": 0.8},
                "downturn": {"satisfaction": -0.1, "retention": -0.08, "cost": 1.2},
                "marketing": {"satisfaction": 0.05, "retention": 0.03, "cost": 1.1},
                "service": {"satisfaction": 0.15, "retention": 0.1, "cost": 1.05}
            }
        }