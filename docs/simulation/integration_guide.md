# Event System Integration Guide
*Author: Maryem - Simulation Interface Lead*

## Overview
This document provides integration guidelines for connecting the Event System with other simulation components.

## For Hamza (Agent Engine Integration)

### Registering Agent Event Handlers
```python
from simulation.event_system import EventSystem
from simulation.event_types import MarketingCampaignEvent

# In your agent initialization
event_system = EventSystem()

def handle_marketing_campaign(event: MarketingCampaignEvent):
    # Update agent behavior based on campaign
    for agent in agents:
        if agent.segment == event.target_segment:
            agent.respond_to_campaign(event)

# Register handler
event_system.register_event_handler("MarketingCampaignEvent", handle_marketing_campaign)
```

### Required Agent Methods
Your agent classes should implement these methods to respond to events:

```python
class RetailClientAgent:
    def respond_to_campaign(self, campaign_event):
        """Handle marketing campaign events"""
        pass
    
    def handle_branch_closure(self, closure_event):
        """Handle branch closure events"""
        pass
    
    def evaluate_new_product(self, product_event):
        """Handle product launch events"""
        pass
```

## For Nessrine (Visualization Integration)

### Subscribing to Event Data
```python
# Get real-time event data for visualization
def get_visualization_data(event_system):
    summary = event_system.get_event_summary()
    recent_events = event_system.get_processed_events()[-10:]  # Last 10 events
    
    return {
        'summary': summary,
        'recent_events': [event.to_dict() for event in recent_events],
        'event_timeline': generate_timeline(recent_events)
    }
```

### Event Data Structure for Charts
Each event provides this data structure:
```python
{
    "event_id": "uuid-string",
    "event_type": "MarketingCampaignEvent",
    "step": 15,
    "timestamp": "2024-01-15T10:30:00",
    "parameters": {
        "target_segment": "young_professionals",
        "intensity": 0.8,
        "budget": 50000
    },
    "status": "completed"
}
```

## For Mehdi (Data Generation Integration)

### Agent Initialization with Events
```python
# Your synthetic data should include event responsiveness parameters
client_data = {
    'demographics': {...},
    'event_responsiveness': {
        'marketing_sensitivity': 0.7,
        'loyalty_factor': 0.8,
        'digital_adoption_rate': 0.6
    }
}

# Initialize agents with event system reference
agent = RetailClientAgent(client_data, event_system)
```

## Event System API Reference

### Core Methods
- `inject_event(event)` - Add event to queue
- `process_events(step)` - Process events for current step  
- `register_event_handler(type, handler)` - Register event handler
- `get_event_summary()` - Get system statistics
- `export_event_history(filename)` - Export event log

### Event Types Available
1. **MarketingCampaignEvent** - Campaign simulations
2. **BranchClosureEvent** - Branch strategy testing
3. **ProductLaunchEvent** - New product rollouts
4. **CompetitorActionEvent** - Market competition
5. **EconomicShockEvent** - Macroeconomic impacts
6. **RegulatoryChangeEvent** - Compliance scenarios
7. **DigitalTransformationEvent** - Digital initiatives

### Error Handling
All event processing includes comprehensive error handling:
- Invalid events are logged and skipped
- Handler exceptions don't crash the system
- Failed events are tracked separately
- System validation checks for integrity

## Testing Integration

### Shared Test Data
Use these test events for integration testing:
```python
test_events = [
    MarketingCampaignEvent(step=5, target_segment="test", campaign_type="test", intensity=0.5),
    BranchClosureEvent(step=10, location="TestCity"),
    ProductLaunchEvent(step=15, product_type="test_product", target_market="test")
]
```

### Integration Test Checklist
- [ ] Events trigger agent behavior changes
- [ ] Visualization updates reflect processed events
- [ ] Event data persists across simulation runs
- [ ] Error handling works for malformed events
- [ ] Performance acceptable with 1000+ agents + events

## Performance Considerations
- Event queue automatically sorts by step (O(n log n))
- Handler execution is O(n) where n = number of handlers
- Memory usage: ~1KB per event with full metadata
- Recommended: Process events in batches for large simulations

## Support and Debugging
- Enable logging: `logging.getLogger('simulation.event_system').setLevel(logging.DEBUG)`
- Use `validate_system_state()` for health checks
- Export event history for debugging: `export_event_history()`
- Monitor system summary for performance metrics

## Next Steps (Week 2)
1. Scenario template loading system
2. Advanced event validation
3. Event dependency management
4. Real-time event injection via UI