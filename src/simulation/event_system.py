"""
FIXED Core Event System for Bank Client Simulation
Author: Maryem - Simulation Interface Lead
Week: 1 - Event System Architecture (FIXED VERSION)
"""

from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import uuid
from datetime import datetime
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BaseEvent(ABC):
    """Base class for all simulation events"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    step: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"  # pending, processing, completed, failed
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.event_type:
            self.event_type = self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "step": self.step,
            "timestamp": self.timestamp.isoformat(),
            "parameters": self.parameters,
            "status": self.status,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseEvent':
        """Create event from dictionary"""
        # This will be implemented by subclasses
        raise NotImplementedError("Subclasses must implement from_dict")

class EventSystem:
    """
    FIXED Core event system for managing simulation events
    Handles event injection, processing, and coordination
    """
    
    def __init__(self):
        self.event_queue: List[BaseEvent] = []
        self.event_handlers: Dict[str, List[Callable]] = {
            "MarketingCampaignEvent": [self.handle_marketing_campaign],
            "BranchClosureEvent": [self.handle_branch_closure],
            "DigitalTransformationEvent": [self.handle_digital_transformation],
            "CompetitorActionEvent": [self.handle_competitor_action],
            "EconomicShockEvent": [self.handle_economic_shock],
            "RegulatoryChangeEvent": [self.handle_regulatory_change],
            "ProductLaunchEvent": [self.handle_product_launch],
        }
        self.processed_events: List[BaseEvent] = []
        self.failed_events: List[BaseEvent] = []
        self.current_step: int = 0
        self.is_running: bool = False
        self.event_history: List[Dict[str, Any]] = []
        self._processed_event_ids: set = set()  # Track processed events to prevent duplicates
        
        # Log initialization
        logger.info("Event system initialized with registered handlers")

    def register_event_handler(self, event_type: str, handler: Callable[[BaseEvent], None]):
        """
        Register handlers for different event types
        
        Args:
            event_type: String identifier for event type
            handler: Function that takes BaseEvent and returns None
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        self.event_handlers[event_type].append(handler)
        logger.info(f"Registered handler for event type: {event_type}")
        
    def unregister_event_handler(self, event_type: str, handler: Callable):
        """Remove a specific handler for an event type"""
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type].remove(handler)
                logger.info(f"Unregistered handler for event type: {event_type}")
            except ValueError:
                logger.warning(f"Handler not found for event type: {event_type}")
    
    def inject_event(self, event: BaseEvent) -> bool:
        """
        Add event to simulation queue
        
        Args:
            event: BaseEvent instance to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate event
            if not isinstance(event, BaseEvent):
                raise ValueError("Event must be instance of BaseEvent")
            
            if event.step < 0:
                raise ValueError("Event step cannot be negative")
            
            # Check for duplicate event IDs
            if event.event_id in self._processed_event_ids:
                logger.warning(f"Event {event.event_id} already processed, skipping")
                return False
            
            # Check if event already in queue
            existing_ids = {e.event_id for e in self.event_queue}
            if event.event_id in existing_ids:
                logger.warning(f"Event {event.event_id} already in queue, skipping")
                return False
            
            # Add to queue
            self.event_queue.append(event)
            
            # Sort queue by step to ensure proper execution order
            self.event_queue.sort(key=lambda x: (x.step, x.timestamp))
            
            logger.info(f"Injected event: {event.event_type} scheduled for step {event.step}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to inject event {event.event_type}: {str(e)}")
            return False
    
    def inject_events_batch(self, events: List[BaseEvent]) -> int:
        """Inject multiple events at once"""
        successful = 0
        for event in events:
            if self.inject_event(event):
                successful += 1
        
        logger.info(f"Batch injected {successful}/{len(events)} events")
        return successful
    
    def process_events(self, current_step: int) -> List[BaseEvent]:
        """
        FIXED: Process events for current simulation step
        
        Args:
            current_step: Current simulation step
            
        Returns:
            List of events processed in this step
        """
        self.current_step = current_step
        events_to_process = []
        remaining_events = []
        
        # Separate events for this step vs future steps
        for event in self.event_queue:
            if event.step <= current_step and event.event_id not in self._processed_event_ids:
                events_to_process.append(event)
            elif event.step > current_step:
                remaining_events.append(event)
            # Skip events that were already processed
        
        # Update the queue to only contain future events
        self.event_queue = remaining_events
        processed_this_step = []
        
        # Process each event exactly once
        for event in events_to_process:
            try:
                # Double-check we haven't processed this event already
                if event.event_id in self._processed_event_ids:
                    continue
                    
                event.status = "processing"
                self._execute_event(event)
                event.status = "completed"
                
                # Mark as processed
                self._processed_event_ids.add(event.event_id)
                self.processed_events.append(event)
                processed_this_step.append(event)
                
                # Add to history
                self.event_history.append({
                    "step": current_step,
                    "event": event.to_dict(),
                    "processed_at": datetime.now().isoformat()
                })
                
                logger.info(f"Processed event {event.event_type} at step {current_step}")
                
            except Exception as e:
                event.status = "failed"
                event.metadata["error"] = str(e)
                self.failed_events.append(event)
                self._processed_event_ids.add(event.event_id)  # Mark as processed to avoid retry
                logger.error(f"Error processing event {event.event_type}: {str(e)}")
        
        return processed_this_step
    
    def _execute_event(self, event: BaseEvent):
        """Execute a single event by calling its handlers"""
        event_type = event.event_type
        
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Handler failed for {event_type}: {str(e)}")
                    raise
        else:
            logger.warning(f"No handlers registered for event type {event_type}")
    
    def get_pending_events(self, step_filter: Optional[int] = None) -> List[BaseEvent]:
        """Get list of pending events, optionally filtered by step"""
        if step_filter is None:
            return self.event_queue.copy()
        return [e for e in self.event_queue if e.step == step_filter]
    
    def get_processed_events(self, step_filter: Optional[int] = None) -> List[BaseEvent]:
        """Get list of processed events, optionally filtered by step"""
        if step_filter is None:
            return self.processed_events.copy()
        return [e for e in self.processed_events if e.step == step_filter]
    
    def get_failed_events(self) -> List[BaseEvent]:
        """Get list of failed events"""
        return self.failed_events.copy()
    
    def clear_events(self, include_history: bool = False):
        """Clear all events (use with caution)"""
        self.event_queue.clear()
        self.processed_events.clear()
        self.failed_events.clear()
        self._processed_event_ids.clear()
        
        if include_history:
            self.event_history.clear()
        
        logger.info("All events cleared from system")
    
    def get_event_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of event system state"""
        all_events = self.event_queue + self.processed_events + self.failed_events
        
        type_counts = {}
        status_counts = {"pending": 0, "completed": 0, "failed": 0}
        
        for event in all_events:
            # Count by type
            event_type = event.event_type
            type_counts[event_type] = type_counts.get(event_type, 0) + 1
            
            # Count by status
            if event in self.event_queue:
                status_counts["pending"] += 1
            elif event in self.processed_events:
                status_counts["completed"] += 1
            elif event in self.failed_events:
                status_counts["failed"] += 1
        
        return {
            "total_events": len(all_events),
            "current_step": self.current_step,
            "event_types": type_counts,
            "status_breakdown": status_counts,
            "pending_events": len(self.event_queue),
            "processed_events": len(self.processed_events),
            "failed_events": len(self.failed_events),
            "registered_handlers": {k: len(v) for k, v in self.event_handlers.items()},
            "unique_processed_events": len(self._processed_event_ids)
        }
    
    def export_event_history(self, filename: str = None) -> str:
        """Export event history to JSON file"""
        if filename is None:
            filename = f"event_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "summary": self.get_event_summary(),
            "event_history": self.event_history
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Event history exported to {filename}")
        return filename
    
    def get_events_by_type(self, event_type: str) -> Dict[str, List[BaseEvent]]:
        """Get all events of a specific type, grouped by status"""
        result = {
            "pending": [],
            "processed": [],
            "failed": []
        }
        
        for event in self.event_queue:
            if event.event_type == event_type:
                result["pending"].append(event)
        
        for event in self.processed_events:
            if event.event_type == event_type:
                result["processed"].append(event)
        
        for event in self.failed_events:
            if event.event_type == event_type:
                result["failed"].append(event)
        
        return result
    
    def get_events_at_step(self, step: int) -> List[BaseEvent]:
        """Return all events scheduled or processed exactly at the given step."""
        events = []
        events.extend([e for e in self.event_queue if e.step == step])
        events.extend([e for e in self.processed_events if e.step == step])
        events.extend([e for e in self.failed_events if e.step == step])
        return events
    
    def validate_system_state(self) -> Dict[str, Any]:
        """Validate the current state of the event system"""
        issues = []
        warnings = []
        
        # Check for duplicate event IDs
        all_events = self.event_queue + self.processed_events + self.failed_events
        event_ids = [e.event_id for e in all_events]
        if len(event_ids) != len(set(event_ids)):
            issues.append("Duplicate event IDs detected")
        
        # Check for events with invalid steps
        invalid_step_events = [e for e in all_events if e.step < 0]
        if invalid_step_events:
            issues.append(f"{len(invalid_step_events)} events have negative step values")
        
        # Check for unhandled event types
        event_types = set(e.event_type for e in all_events)
        unhandled_types = event_types - set(self.event_handlers.keys())
        if unhandled_types:
            warnings.append(f"Unhandled event types: {list(unhandled_types)}")
        
        # Check consistency between processed events and tracking set
        processed_ids_in_list = {e.event_id for e in self.processed_events}
        if processed_ids_in_list != self._processed_event_ids:
            issues.append("Inconsistency between processed events list and tracking set")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "total_events": len(all_events),
            "unique_event_types": len(event_types),
            "processed_tracking_count": len(self._processed_event_ids)
        }

    def handle_marketing_campaign(self, event: BaseEvent) -> None:
        intensity = event.parameters.get("intensity", 0.0)
        effect = min(1.0, intensity * 1.2)
        event.metadata["results"] = {"client_retention_rate": effect}
        logger.info(f"MarketingCampaignEvent: Boosting retention by {effect} at step {self.current_step}")
        # Note: This should update a global state or return results; for now, logging the effect

    def handle_branch_closure(self, event: BaseEvent) -> None:
        event.metadata["results"] = {"churned_agents": 50}
        logger.info(f"BranchClosureEvent: Triggering churn of 50 agents at step {self.current_step}")
        # Note: Should update churned_agents; logging for now

    def handle_digital_transformation(self, event: BaseEvent) -> None:
        user_experience_score = event.parameters.get("user_experience_score", 0.0)
        effect = user_experience_score * 0.5
        event.metadata["results"] = {"digital_adoption_increase": effect}
        logger.info(f"DigitalTransformationEvent: Increasing adoption by {effect} at step {self.current_step}")
        # Note: Should update digital_adoption_increase; logging for now

    def handle_competitor_action(self, event: BaseEvent) -> None:
        impact_intensity = event.parameters.get("impact_intensity", 0.0)
        effect = max(0.0, 1.0 - impact_intensity * 0.5)
        event.metadata["results"] = {"client_retention_rate": effect}
        logger.info(f"CompetitorActionEvent: Reducing retention by {1.0 - effect} at step {self.current_step}")
        # Note: Should update client_retention_rate; logging for now

    def handle_economic_shock(self, event: BaseEvent):
        logger.info(f"EconomicShockEvent: Severity {event.parameters.get('severity', 0.0)} at step {event.step}")
        event.metadata["results"] = {
            "impact_factor": event.parameters.get("severity", 0.0)
        }

    def handle_regulatory_change(self, event: BaseEvent):
        logger.info(f"RegulatoryChangeEvent: Impact severity {event.parameters.get('impact_severity', 0.0)} at step {event.step}")
        event.metadata["results"] = {
            "regulatory_impact": event.parameters.get("impact_severity", 0.0)
        }

    def handle_product_launch(self, event: BaseEvent):
        logger.info(f"ProductLaunchEvent: Launching in {event.parameters.get('launch_governorates', [])} at step {event.step}")
        event.metadata["results"] = {
            "launch_regions": event.parameters.get("launch_governorates", [])
        }
