# src/simulation/event_types.py - UPDATED VERSION

"""
UPDATED Event Types for Bank Client Simulation
Author: Maryem - Simulation Interface Lead
Week: 1 - Event Types Definition (ENHANCED)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime
from abc import ABC
from .event_system import BaseEvent

@dataclass
class MarketingCampaignEvent(BaseEvent):
    """Event for marketing campaign simulations - ENHANCED"""
    target_segment: str = ""
    campaign_type: str = ""
    intensity: float = 0.0
    duration: int = 0
    budget: float = 0.0
    channels: List[str] = None
    message: str = ""
    
    # Additional flexible parameters
    message_theme: str = ""
    promotional_offer: str = ""
    social_proof_strategy: str = ""
    loyalty_program: str = ""
    defensive_offer: str = ""
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        super().__post_init__()
        self.parameters = {
            "target_segment": self.target_segment,
            "campaign_type": self.campaign_type,
            "intensity": self.intensity,
            "duration": self.duration,
            "budget": self.budget,
            "channels": self.channels or [],
            "message": self.message,
            "message_theme": self.message_theme,
            "promotional_offer": self.promotional_offer,
            "social_proof_strategy": self.social_proof_strategy,
            "loyalty_program": self.loyalty_program,
            "defensive_offer": self.defensive_offer,
            **self.extra_params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketingCampaignEvent':
        params = data.get("parameters", {})
        
        # Extract known parameters
        known_params = {
            'event_id': data.get("event_id", str(uuid.uuid4())),
            'event_type': data.get("event_type", "MarketingCampaignEvent"),
            'step': data.get("step", 0),
            'timestamp': datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            'target_segment': params.get("target_segment", ""),
            'campaign_type': params.get("campaign_type", ""),
            'intensity': params.get("intensity", 0.0),
            'duration': params.get("duration", 0),
            'budget': params.get("budget", 0.0),
            'channels': params.get("channels", []),
            'message': params.get("message", ""),
            'message_theme': params.get("message_theme", ""),
            'promotional_offer': params.get("promotional_offer", ""),
            'social_proof_strategy': params.get("social_proof_strategy", ""),
            'loyalty_program': params.get("loyalty_program", ""),
            'defensive_offer': params.get("defensive_offer", ""),
            'status': data.get("status", "pending"),
            'metadata': data.get("metadata", {})
        }
        
        # Put any remaining parameters in extra_params
        extra_params = {k: v for k, v in params.items() if k not in known_params}
        known_params['extra_params'] = extra_params
        
        return cls(**known_params)

@dataclass
class BranchClosureEvent(BaseEvent):
    """Event for branch closure simulations - ENHANCED"""
    location: str = ""
    alternative_branches: List[str] = None
    compensation_offered: bool = False
    closure_date: str = ""
    digital_migration_support: bool = False
    staff_reallocation: str = ""
    reason: str = ""
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        super().__post_init__()
        self.parameters = {
            "location": self.location,
            "alternative_branches": self.alternative_branches or [],
            "compensation_offered": self.compensation_offered,
            "closure_date": self.closure_date,
            "digital_migration_support": self.digital_migration_support,
            "staff_reallocation": self.staff_reallocation,
            "reason": self.reason,
            **self.extra_params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BranchClosureEvent':
        params = data.get("parameters", {})
        
        known_params = {
            'event_id': data.get("event_id", str(uuid.uuid4())),
            'event_type': data.get("event_type", "BranchClosureEvent"),
            'step': data.get("step", 0),
            'timestamp': datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            'location': params.get("location", ""),
            'alternative_branches': params.get("alternative_branches", []),
            'compensation_offered': params.get("compensation_offered", False),
            'closure_date': params.get("closure_date", ""),
            'digital_migration_support': params.get("digital_migration_support", False),
            'staff_reallocation': params.get("staff_reallocation", ""),
            'reason': params.get("reason", ""),
            'status': data.get("status", "pending"),
            'metadata': data.get("metadata", {})
        }
        
        extra_params = {k: v for k, v in params.items() if k not in known_params}
        known_params['extra_params'] = extra_params
        
        return cls(**known_params)

@dataclass
class ProductLaunchEvent(BaseEvent):
    """Event for new product launch simulations - ENHANCED"""
    product_type: str = ""
    target_market: str = ""
    pricing: float = 0.0
    digital_only: bool = False
    launch_governorates: List[str] = None
    gamification_elements: List[str] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        super().__post_init__()
        self.parameters = {
            "product_type": self.product_type,
            "target_market": self.target_market,
            "pricing": self.pricing,
            "digital_only": self.digital_only,
            "launch_governorates": self.launch_governorates or [],
            "gamification_elements": self.gamification_elements or [],
            **self.extra_params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductLaunchEvent':
        params = data.get("parameters", {})
        
        known_params = {
            'event_id': data.get("event_id", str(uuid.uuid4())),
            'event_type': data.get("event_type", "ProductLaunchEvent"),
            'step': data.get("step", 0),
            'timestamp': datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            'product_type': params.get("product_type", ""),
            'target_market': params.get("target_market", ""),
            'pricing': params.get("pricing", 0.0),
            'digital_only': params.get("digital_only", False),
            'launch_governorates': params.get("launch_governorates", []),
            'gamification_elements': params.get("gamification_elements", []),
            'status': data.get("status", "pending"),
            'metadata': data.get("metadata", {})
        }
        
        extra_params = {k: v for k, v in params.items() if k not in known_params}
        known_params['extra_params'] = extra_params
        
        return cls(**known_params)

@dataclass
class DigitalTransformationEvent(BaseEvent):
    """Event for digital transformation initiatives - ENHANCED"""
    service_type: str = ""
    channel: str = ""
    user_experience_score: float = 0.0
    rollout_phases: int = 1
    target_regions: List[str] = None
    features: List[str] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        super().__post_init__()
        self.parameters = {
            "service_type": self.service_type,
            "channel": self.channel,
            "user_experience_score": self.user_experience_score,
            "rollout_phases": self.rollout_phases,
            "target_regions": self.target_regions or [],
            "features": self.features or [],
            **self.extra_params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DigitalTransformationEvent':
        params = data.get("parameters", {})
        
        known_params = {
            'event_id': data.get("event_id", str(uuid.uuid4())),
            'event_type': data.get("event_type", "DigitalTransformationEvent"),
            'step': data.get("step", 0),
            'timestamp': datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            'service_type': params.get("service_type", ""),
            'channel': params.get("channel", ""),
            'user_experience_score': params.get("user_experience_score", 0.0),
            'rollout_phases': params.get("rollout_phases", 1),
            'target_regions': params.get("target_regions", []),
            'features': params.get("features", []),
            'status': data.get("status", "pending"),
            'metadata': data.get("metadata", {})
        }
        
        extra_params = {k: v for k, v in params.items() if k not in known_params}
        known_params['extra_params'] = extra_params
        
        return cls(**known_params)
    
@dataclass
class CompetitorActionEvent(BaseEvent):
    """Event for competitor action simulations - ENHANCED"""
    competitor_name: str = ""
    action_type: str = ""
    affected_region: str = ""
    impact_intensity: float = 0.0
    duration: int = 0
    competitor_offer: str = ""
    competitor_strategy: str = ""
    extra_params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EconomicShockEvent(BaseEvent):
    """Event for macroeconomic shock simulations - ENHANCED"""
    shock_type: str = ""
    severity: float = 0.0
    affected_sectors: List[str] = None
    duration: int = 0
    extra_params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegulatoryChangeEvent(BaseEvent):
    """Event for regulatory change simulations - ENHANCED"""
    regulation_type: str = ""
    affected_products: List[str] = None
    compliance_deadline: str = ""
    impact_severity: float = 0.0
    compliance_cost: float = 0.0
    implementation_period: int = 0
    regulatory_requirements: List[str] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

# Update the create_event function to be more flexible
def create_event(event_type: str, **kwargs) -> BaseEvent:
    """Factory function for creating events dynamically - ENHANCED"""
    event_classes = {
        "MarketingCampaignEvent": MarketingCampaignEvent,
        "BranchClosureEvent": BranchClosureEvent,
        "ProductLaunchEvent": ProductLaunchEvent,
        "CompetitorActionEvent": CompetitorActionEvent,
        "EconomicShockEvent": EconomicShockEvent,
        "RegulatoryChangeEvent": RegulatoryChangeEvent,
        "DigitalTransformationEvent": DigitalTransformationEvent,
    }
    
    if event_type not in event_classes:
        raise ValueError(f"Unknown event type: {event_type}")
    
    event_class = event_classes[event_type]
    
    # Filter kwargs to only include valid parameters for the class
    import inspect
    signature = inspect.signature(event_class.__init__)
    valid_params = set(signature.parameters.keys()) - {'self'}
    
    # Separate valid parameters from extra ones
    valid_kwargs = {k: v for k, v in kwargs.items() if k in valid_params}
    extra_kwargs = {k: v for k, v in kwargs.items() if k not in valid_params}
    
    # Add extra parameters to extra_params if the class supports it
    if 'extra_params' in valid_params and extra_kwargs:
        valid_kwargs['extra_params'] = extra_kwargs
    
    return event_class(**valid_kwargs)