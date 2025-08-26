"""
FastAPI endpoint for serving simulation results to dashboard
"""
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
import json
import asyncio
from datetime import datetime
from pathlib import Path

from src.integration.simulation_controller import SimulationController

app = FastAPI(title="Bank Simulation API", version="1.0.0")

# Enable CORS for dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global controller instance
controller = SimulationController()

@app.get("/")
def read_root():
    """API health check"""
    return {"status": "active", "service": "Bank Simulation API"}

@app.post("/simulation/initialize")
async def initialize_simulation(config: Dict[str, Any]):
    """
    Initialize a new simulation
    
    Body:
    {
        "scenario": "branch_closure_scenario",  # optional
        "config": {
            "num_agents": 1000,
            "time_steps": 100,
            "retail_ratio": 0.8
        }
    }
    """
    try:
        scenario = config.get("scenario")
        custom_config = config.get("config", {})
        
        model = controller.initialize_simulation(
            scenario_name=scenario,
            custom_config=custom_config
        )
        
        return {
            "status": "initialized",
            "scenario": scenario or "basic_simulation",
            "total_agents": len(model.agents),
            "configuration": custom_config
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simulation/run")
async def run_simulation(params: Dict[str, Any]):
    """
    Run the initialized simulation
    
    Body:
    {
        "steps": 100,  # optional, uses config default
        "output_frequency": 10
    }
    """
    try:
        steps = params.get("steps")
        output_frequency = params.get("output_frequency", 10)
        
        results = controller.run_simulation(
            steps=steps,
            output_frequency=output_frequency
        )
        
        return {
            "status": "completed",
            "summary": {
                "total_steps": results['metadata']['total_steps'],
                "start_time": results['metadata']['start_time'],
                "end_time": results['metadata']['end_time']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/simulation/results")
async def get_simulation_results():
    """Get the latest simulation results formatted for dashboard"""
    try:
        if not controller.simulation_results:
            raise HTTPException(status_code=404, detail="No simulation results available")
        
        dashboard_data = controller._prepare_dashboard_data()
        return dashboard_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/simulation/scenarios")
async def list_available_scenarios():
    """List all available simulation scenarios"""
    try:
        scenarios_path = Path("configs/scenario_templates")
        scenarios = []
        
        for scenario_file in scenarios_path.glob("*.json"):
            with open(scenario_file, 'r') as f:
                data = json.load(f)
                scenarios.append({
                    "filename": scenario_file.name,
                    "name": data['scenario_metadata']['name'],
                    "description": data['scenario_metadata']['description'],
                    "duration": data['simulation_parameters']['duration_steps']
                })
        
        return {"scenarios": scenarios}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.websocket("/simulation/stream")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time simulation updates"""
    await websocket.accept()
    try:
        while True:
            # Send updates every second during simulation
            if controller.current_model:
                metrics = controller._collect_metrics(controller.current_model.schedule.steps)
                await websocket.send_json({
                    "type": "metrics_update",
                    "data": metrics
                })
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.post("/simulation/scenario/create")
async def create_custom_scenario(scenario_data: Dict[str, Any]):
    """Create a custom scenario from dashboard input"""
    try:
        # Extract scenario parameters
        name = scenario_data['name']
        description = scenario_data['description']
        events = scenario_data['events']
        
        # Create scenario using ScenarioManager
        filepath = controller.scenario_manager.create_scenario_template(
            name=name,
            description=description,
            events=events,
            duration=scenario_data.get('duration', 100),
            population=scenario_data.get('population', 1000)
        )
        
        return {
            "status": "created",
            "scenario_file": filepath,
            "name": name
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))