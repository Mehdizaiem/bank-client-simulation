"""
Event Types for Bank Client Simulation
Author: Maryem - Simulation Interface Lead
Week: 1 - Event Types Definition
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from .event_system import BaseEvent

@dataclass
class MarketingCampaignEvent(BaseEvent):
    """Event for marketing campaign simulations"""
    target_segment: str = ""
    campaign_type: str = ""
    intensity: float = 0.0
    duration: int = 0
    budget: float = 0.0
    channels: List[str] = None
    message: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.channels = self.channels or []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketingCampaignEvent':
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            target_segment=data.get("parameters", {}).get("target_segment", ""),
            campaign_type=data.get("parameters", {}).get("campaign_type", ""),
            intensity=data.get("parameters", {}).get("intensity", 0.0),
            duration=data.get("parameters", {}).get("duration", 0),
            budget=data.get("parameters", {}).get("budget", 0.0),
            channels=data.get("parameters", {}).get("channels", []),
            message=data.get("parameters", {}).get("message", ""),
            status=data.get("status", "pending"),
            metadata=data.get("metadata", {})
        )

@dataclass
class BranchClosureEvent(BaseEvent):
    """Event for branch closure simulations"""
    location: str = ""
    alternative_branches: List[str] = None
    compensation_offered: bool = False
    closure_date: str = ""
    digital_migration_support: bool = False
    staff_reallocation: str = ""
    reason: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.alternative_branches = self.alternative_branches or []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BranchClosureEvent':
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            location=data.get("parameters", {}).get("location", ""),
            alternative_branches=data.get("parameters", {}).get("alternative_branches", []),
            compensation_offered=data.get("parameters", {}).get("compensation_offered", False),
            closure_date=data.get("parameters", {}).get("closure_date", ""),
            digital_migration_support=data.get("parameters", {}).get("digital_migration_support", False),
            staff_reallocation=data.get("parameters", {}).get("staff_reallocation", ""),
            reason=data.get("parameters", {}).get("reason", ""),
            status=data.get("status", "pending"),
            metadata=data.get("metadata", {})
        )

@dataclass
class ProductLaunchEvent(BaseEvent):
    """Event for new product launch simulations"""
    product_type: str = ""
    target_market: str = ""
    pricing: float = 0.0
    digital_only: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductLaunchEvent':
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            product_type=data.get("parameters", {}).get("product_type", ""),
            target_market=data.get("parameters", {}).get("target_market", ""),
            pricing=data.get("parameters", {}).get("pricing", 0.0),
            digital_only=data.get("parameters", {}).get("digital_only", False),
            status=data.get("status", "pending"),
            metadata=data.get("metadata", {})
        )

@dataclass
class CompetitorActionEvent(BaseEvent):
    """Event for competitor action simulations"""
    competitor_name: str = ""
    action_type: str = ""
    affected_region: str = ""
    impact_intensity: float = 0.0
    duration: int = 0
    competitor_offer: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompetitorActionEvent':
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            competitor_name=data.get("parameters", {}).get("competitor_name", ""),
            action_type=data.get("parameters", {}).get("action_type", ""),
            affected_region=data.get("parameters", {}).get("affected_region", ""),
            impact_intensity=data.get("parameters", {}).get("impact_intensity", 0.0),
            duration=data.get("parameters", {}).get("duration", 0),
            competitor_offer=data.get("parameters", {}).get("competitor_offer", ""),
            status=data.get("status", "pending"),
            metadata=data.get("metadata", {})
        )

@dataclass
class EconomicShockEvent(BaseEvent):
    """Event for macroeconomic shock simulations"""
    shock_type: str = ""
    severity: float = 0.0
    affected_sectors: List[str] = None
    duration: int = 0

    def __post_init__(self):
        super().__post_init__()
        self.affected_sectors = self.affected_sectors or []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EconomicShockEvent':
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            shock_type=data.get("parameters", {}).get("shock_type", ""),
            severity=data.get("parameters", {}).get("severity", 0.0),
            affected_sectors=data.get("parameters", {}).get("affected_sectors", []),
            duration=data.get("parameters", {}).get("duration", 0),
            status=data.get("status", "pending"),
            metadata=data.get("metadata", {})
        )

@dataclass
class RegulatoryChangeEvent(BaseEvent):
    """Event for regulatory change simulations"""
    regulation_type: str = ""
    affected_products: List[str] = None
    compliance_deadline: str = ""
    impact_severity: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        self.affected_products = self.affected_products or []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RegulatoryChangeEvent':
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            regulation_type=data.get("parameters", {}).get("regulation_type", ""),
            affected_products=data.get("parameters", {}).get("affected_products", []),
            compliance_deadline=data.get("parameters", {}).get("compliance_deadline", ""),
            impact_severity=data.get("parameters", {}).get("impact_severity", 0.0),
            status=data.get("status", "pending"),
            metadata=data.get("metadata", {})
        )

@dataclass
class DigitalTransformationEvent(BaseEvent):
    """Event for digital transformation initiatives"""
    service_type: str = ""
    channel: str = ""
    user_experience_score: float = 0.0
    rollout_phases: int = 1
    target_regions: List[str] = None
    features: List[str] = None

    def __post_init__(self):
        super().__post_init__()
        self.target_regions = self.target_regions or []
        self.features = self.features or []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DigitalTransformationEvent':
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            service_type=data.get("parameters", {}).get("service_type", ""),
            channel=data.get("parameters", {}).get("channel", ""),
            user_experience_score=data.get("parameters", {}).get("user_experience_score", 0.0),
            rollout_phases=data.get("parameters", {}).get("rollout_phases", 1),
            target_regions=data.get("parameters", {}).get("target_regions", []),
            features=data.get("parameters", {}).get("features", []),
            status=data.get("status", "pending"),
            metadata=data.get("metadata", {})
        )

def create_event(event_type: str, **kwargs) -> BaseEvent:
    """Factory function for creating events dynamically"""
    event_classes = {
        "MarketingCampaignEvent": MarketingCampaignEvent,
        "BranchClosureEvent": BranchClosureEvent,
        "ProductLaunchEvent": ProductLaunchEvent,
        "CompetitorActionEvent": CompetitorActionEvent,
        "EconomicShockEvent": EconomicShockEvent,
        "RegulatoryChangeEvent": RegulatoryChangeEvent,
        "DigitalTransformationEvent": DigitalTransformationEvent
    }
    
    if event_type not in event_classes:
        raise ValueError(f"Unknown event type: {event_type}")
    
    return event_classes[event_type](**kwargs)