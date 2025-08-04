"""
Event Types for Bank Client Simulation
Author: Maryem - Simulation Interface Lead
Week: 1 - Event Types Definition
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime
from abc import ABC
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
        self.parameters = {
            "target_segment": self.target_segment,
            "campaign_type": self.campaign_type,
            "intensity": self.intensity,
            "duration": self.duration,
            "budget": self.budget,
            "channels": self.channels or [],
            "message": self.message
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketingCampaignEvent':
        params = data.get("parameters", {})
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "MarketingCampaignEvent"),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            target_segment=params.get("target_segment", ""),
            campaign_type=params.get("campaign_type", ""),
            intensity=params.get("intensity", 0.0),
            duration=params.get("duration", 0),
            budget=params.get("budget", 0.0),
            channels=params.get("channels", []),
            message=params.get("message", ""),
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
        self.parameters = {
            "location": self.location,
            "alternative_branches": self.alternative_branches or [],
            "compensation_offered": self.compensation_offered,
            "closure_date": self.closure_date,
            "digital_migration_support": self.digital_migration_support,
            "staff_reallocation": self.staff_reallocation,
            "reason": self.reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BranchClosureEvent':
        params = data.get("parameters", {})
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "BranchClosureEvent"),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            location=params.get("location", ""),
            alternative_branches=params.get("alternative_branches", []),
            compensation_offered=params.get("compensation_offered", False),
            closure_date=params.get("closure_date", ""),
            digital_migration_support=params.get("digital_migration_support", False),
            staff_reallocation=params.get("staff_reallocation", ""),
            reason=params.get("reason", ""),
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

    def __post_init__(self):
        super().__post_init__()
        self.parameters = {
            "product_type": self.product_type,
            "target_market": self.target_market,
            "pricing": self.pricing,
            "digital_only": self.digital_only
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductLaunchEvent':
        params = data.get("parameters", {})
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "ProductLaunchEvent"),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            product_type=params.get("product_type", ""),
            target_market=params.get("target_market", ""),
            pricing=params.get("pricing", 0.0),
            digital_only=params.get("digital_only", False),
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

    def __post_init__(self):
        super().__post_init__()
        self.parameters = {
            "competitor_name": self.competitor_name,
            "action_type": self.action_type,
            "affected_region": self.affected_region,
            "impact_intensity": self.impact_intensity,
            "duration": self.duration,
            "competitor_offer": self.competitor_offer
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompetitorActionEvent':
        params = data.get("parameters", {})
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "CompetitorActionEvent"),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            competitor_name=params.get("competitor_name", ""),
            action_type=params.get("action_type", ""),
            affected_region=params.get("affected_region", ""),
            impact_intensity=params.get("impact_intensity", 0.0),
            duration=params.get("duration", 0),
            competitor_offer=params.get("competitor_offer", ""),
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
        self.parameters = {
            "shock_type": self.shock_type,
            "severity": self.severity,
            "affected_sectors": self.affected_sectors or [],
            "duration": self.duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EconomicShockEvent':
        params = data.get("parameters", {})
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "EconomicShockEvent"),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            shock_type=params.get("shock_type", ""),
            severity=params.get("severity", 0.0),
            affected_sectors=params.get("affected_sectors", []),
            duration=params.get("duration", 0),
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
        self.parameters = {
            "regulation_type": self.regulation_type,
            "affected_products": self.affected_products or [],
            "compliance_deadline": self.compliance_deadline,
            "impact_severity": self.impact_severity
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RegulatoryChangeEvent':
        params = data.get("parameters", {})
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "RegulatoryChangeEvent"),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            regulation_type=params.get("regulation_type", ""),
            affected_products=params.get("affected_products", []),
            compliance_deadline=params.get("compliance_deadline", ""),
            impact_severity=params.get("impact_severity", 0.0),
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
        self.parameters = {
            "service_type": self.service_type,
            "channel": self.channel,
            "user_experience_score": self.user_experience_score,
            "rollout_phases": self.rollout_phases,
            "target_regions": self.target_regions or [],
            "features": self.features or []
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DigitalTransformationEvent':
        params = data.get("parameters", {})
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "DigitalTransformationEvent"),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            service_type=params.get("service_type", ""),
            channel=params.get("channel", ""),
            user_experience_score=params.get("user_experience_score", 0.0),
            rollout_phases=params.get("rollout_phases", 1),
            target_regions=params.get("target_regions", []),
            features=params.get("features", []),
            status=data.get("status", "pending"),
            metadata=data.get("metadata", {})
        )

@dataclass
class LoanOfferEvent(BaseEvent):
    """Event for loan offer simulations"""
    amount: float = 0.0
    interest_rate: float = 0.0
    term_months: int = 0
    target_income_level: str = ""
    eligibility_criteria: Dict[str, Any] = None

    def __post_init__(self):
        super().__post_init__()
        self.parameters = {
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "term_months": self.term_months,
            "target_income_level": self.target_income_level,
            "eligibility_criteria": self.eligibility_criteria or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LoanOfferEvent':
        params = data.get("parameters", {})
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "LoanOfferEvent"),
            step=data.get("step", 0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            amount=params.get("amount", 0.0),
            interest_rate=params.get("interest_rate", 0.0),
            term_months=params.get("term_months", 0),
            target_income_level=params.get("target_income_level", ""),
            eligibility_criteria=params.get("eligibility_criteria", {}),
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
        "DigitalTransformationEvent": DigitalTransformationEvent,
        "LoanOfferEvent": LoanOfferEvent
    }
    
    if event_type not in event_classes:
        raise ValueError(f"Unknown event type: {event_type}")
    
    # Pass all kwargs directly, allowing field initialization
    return event_classes[event_type](**kwargs)