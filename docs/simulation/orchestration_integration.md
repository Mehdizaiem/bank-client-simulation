# Orchestration Integration Guide

## Overview
This document outlines the integration points for the Simulation Orchestration & Control system developed in Week 3.

## Integration Points

### 1. Agent Data (Mehdi)
- **Format**: pandas DataFrame
- **Required Columns**: `unique_id`, `demographics`, `channel_preference`
- **Optional Columns**: `satisfaction_level`, `status` (will be initialized to 0.5 and 'active' if missing)
- **Method**: Pass to `SimulationOrchestrator.initialize_simulation(agent_data)`
- **Example**:
  ```python
  import pandas as pd
  agent_data = pd.DataFrame({
      'unique_id': [1, 2, 3],
      'demographics': ['Tunis_Male', 'Tunis_Female', 'Sfax_Male'],
      'channel_preference': ['mobile', 'branch', 'web']
  })
  orchestrator.initialize_simulation(agent_data)