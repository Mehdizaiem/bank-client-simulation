# tests/simulation/test_event_system.py
"""
Test suite for Event System
Author: Maryem - Simulation Interface Lead
"""

import unittest
import sys
import os
from datetime import datetime, timedelta
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from simulation.event_system import EventSystem, BaseEvent
from simulation.event_types import (
    MarketingCampaignEvent, BranchClosureEvent, ProductLaunchEvent,
    CompetitorActionEvent, EconomicShockEvent, create_event
)

class TestEventSystem(unittest.TestCase):
    """Test cases for EventSystem class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.event_system = EventSystem()
        self.sample_events = []
        
        # Create sample events
        self.marketing_event = MarketingCampaignEvent(
            step=5,
            target_segment="young_professionals",
            campaign_type="digital_banking_promotion",
            intensity=0.8,
            budget=50000.0
        )
        
        self.branch_event = BranchClosureEvent(
            step=10,
            location="Sfax",
            alternative_branches=["Sousse", "Monastir"],
            compensation_offered=True
        )
        
        self.product_event = ProductLaunchEvent(
            step=7,
            product_type="mobile_wallet",
            target_market="retail",
            pricing=10.0,
            digital_only=True
        )
    
    def test_event_system_initialization(self):
        """Test EventSystem initializes correctly"""
        self.assertEqual(len(self.event_system.event_queue), 0)
        self.assertEqual(len(self.event_system.processed_events), 0)
        self.assertEqual(len(self.event_system.failed_events), 0)
        self.assertEqual(self.event_system.current_step, 0)
        self.assertFalse(self.event_system.is_running)
    
    def test_event_injection(self):
        """Test event injection functionality"""
        # Test successful injection
        result = self.event_system.inject_event(self.marketing_event)
        self.assertTrue(result)
        self.assertEqual(len(self.event_system.event_queue), 1)
        
        # Test batch injection
        events = [self.branch_event, self.product_event]
        count = self.event_system.inject_events_batch(events)
        self.assertEqual(count, 2)
        self.assertEqual(len(self.event_system.event_queue), 3)
    
    def test_event_ordering(self):
        """Test events are ordered correctly by step"""
        # Inject events out of order
        events = [
            BranchClosureEvent(step=15, location="Tunis"),
            MarketingCampaignEvent(step=3, target_segment="seniors", 
                                 campaign_type="savings", intensity=0.5),
            ProductLaunchEvent(step=8, product_type="credit_card", target_market="corporate")
        ]
        
        for event in events:
            self.event_system.inject_event(event)
        
        # Check ordering
        queue_steps = [event.step for event in self.event_system.event_queue]
        self.assertEqual(queue_steps, sorted(queue_steps))
    
    def test_handler_registration(self):
        """Test event handler registration"""
        def dummy_handler(event):
            pass
        
        # Register handler
        self.event_system.register_event_handler("MarketingCampaignEvent", dummy_handler)
        self.assertIn("MarketingCampaignEvent", self.event_system.event_handlers)
        self.assertEqual(len(self.event_system.event_handlers["MarketingCampaignEvent"]), 1)
        
        # Register another handler for same event type
        def another_handler(event):
            pass
        
        self.event_system.register_event_handler("MarketingCampaignEvent", another_handler)
        self.assertEqual(len(self.event_system.event_handlers["MarketingCampaignEvent"]), 2)
    
    def test_event_processing(self):
        """Test event processing functionality"""
        # Set up handler
        processed_events = []
        
        def marketing_handler(event):
            processed_events.append(event)
        
        self.event_system.register_event_handler("MarketingCampaignEvent", marketing_handler)
        
        # Inject events
        self.event_system.inject_event(self.marketing_event)  # step 5
        self.event_system.inject_event(self.branch_event)     # step 10
        
        # Process step 5 - should process marketing event
        processed = self.event_system.process_events(5)
        self.assertEqual(len(processed), 1)
        self.assertEqual(processed[0].event_type, "MarketingCampaignEvent")
        self.assertEqual(len(processed_events), 1)
        self.assertEqual(len(self.event_system.event_queue), 1)  # branch event still pending
        
        # Process step 10 - should process branch event (no handler, but should not fail)
        processed = self.event_system.process_events(10)
        self.assertEqual(len(processed), 1)
        self.assertEqual(processed[0].event_type, "BranchClosureEvent")
        self.assertEqual(len(self.event_system.event_queue), 0)  # all events processed
    
    def test_event_summary(self):
        """Test event summary functionality"""
        # Add some events
        self.event_system.inject_event(self.marketing_event)
        self.event_system.inject_event(self.branch_event)
        
        summary = self.event_system.get_event_summary()
        
        self.assertEqual(summary["total_events"], 2)
        self.assertEqual(summary["pending_events"], 2)
        self.assertEqual(summary["processed_events"], 0)
        self.assertEqual(summary["failed_events"], 0)
        self.assertIn("MarketingCampaignEvent", summary["event_types"])
        self.assertIn("BranchClosureEvent", summary["event_types"])
    
    def test_event_filtering(self):
        """Test event filtering by type and step"""
        # Add events
        self.event_system.inject_event(self.marketing_event)  # step 5
        self.event_system.inject_event(self.branch_event)     # step 10
        
        # Test step filtering
        step_5_events = self.event_system.get_pending_events(step_filter=5)
        self.assertEqual(len(step_5_events), 1)
        self.assertEqual(step_5_events[0].event_type, "MarketingCampaignEvent")
        
        # Test type filtering
        marketing_events = self.event_system.get_events_by_type("MarketingCampaignEvent")
        self.assertEqual(len(marketing_events["pending"]), 1)
        self.assertEqual(len(marketing_events["processed"]), 0)
    
    def test_system_validation(self):
        """Test system state validation"""
        # Clean system should be valid
        validation = self.event_system.validate_system_state()
        self.assertTrue(validation["valid"])
        self.assertEqual(len(validation["issues"]), 0)
        
        # Add valid events
        self.event_system.inject_event(self.marketing_event)
        validation = self.event_system.validate_system_state()
        self.assertTrue(validation["valid"])

class TestEventTypes(unittest.TestCase):
    """Test cases for specific event types"""
    
    def test_marketing_campaign_event(self):
        """Test MarketingCampaignEvent creation and properties"""
        event = MarketingCampaignEvent(
            step=5,
            target_segment="young_professionals",
            campaign_type="digital_promotion",
            intensity=0.8,
            duration=15,
            budget=75000.0
        )
        
        self.assertEqual(event.step, 5)
        self.assertEqual(event.target_segment, "young_professionals")
        self.assertEqual(event.campaign_type, "digital_promotion")
        self.assertEqual(event.intensity, 0.8)
        self.assertEqual(event.duration, 15)
        self.assertEqual(event.budget, 75000.0)
        self.assertEqual(event.event_type, "MarketingCampaignEvent")
    
    def test_branch_closure_event(self):
        """Test BranchClosureEvent creation and properties"""
        event = BranchClosureEvent(
            step=12,
            location="Sfax",
            alternative_branches=["Sousse", "Monastir"],
            compensation_offered=True
        )
        
        self.assertEqual(event.step, 12)
        self.assertEqual(event.location, "Sfax")
        self.assertEqual(event.alternative_branches, ["Sousse", "Monastir"])
        self.assertTrue(event.compensation_offered)
        self.assertEqual(event.event_type, "BranchClosureEvent")
    
    def test_event_factory(self):
        """Test event factory function"""
        event = create_event(
            "CompetitorActionEvent",
            step=8,
            competitor_name="BIAT",
            action_type="rate_reduction",
            affected_region="Tunis",
            impact_intensity=0.7
        )
        
        self.assertEqual(event.event_type, "CompetitorActionEvent")
        self.assertEqual(event.step, 8)
        self.assertEqual(event.competitor_name, "BIAT")
    
    def test_invalid_event_factory(self):
        """Test factory function with invalid event type"""
        with self.assertRaises(ValueError):
            create_event("InvalidEventType", step=1)

class TestIntegrationScenarios(unittest.TestCase):
    """Integration tests for complex scenarios"""
    
    def setUp(self):
        self.event_system = EventSystem()
        self.processed_events = []
        
        # Set up handlers
        def generic_handler(event):
            self.processed_events.append(f"Processed {event.event_type} at step {event.step}")
        
        # Register handlers for all event types
        event_types = [
            "MarketingCampaignEvent", "BranchClosureEvent", "ProductLaunchEvent",
            "CompetitorActionEvent", "EconomicShockEvent", "RegulatoryChangeEvent"
        ]
        
        for event_type in event_types:
            self.event_system.register_event_handler(event_type, generic_handler)
    
    def test_complex_scenario_processing(self):
        """Test processing a complex scenario with multiple event types"""
        # Create a complex scenario
        events = [
            MarketingCampaignEvent(step=1, target_segment="youth", 
                                 campaign_type="digital", intensity=0.6),
            CompetitorActionEvent(step=3, competitor_name="BIAT", 
                                action_type="branch_opening", affected_region="Tunis"),
            ProductLaunchEvent(step=5, product_type="crypto_wallet", target_market="tech_savvy"),
            EconomicShockEvent(step=7, shock_type="inflation", severity=0.4),
            BranchClosureEvent(step=10, location="Sfax"),
        ]
        
        # Inject all events
        for event in events:
            self.event_system.inject_event(event)
        
        # Process simulation over 12 steps
        all_processed = []
        for step in range(1, 13):
            processed = self.event_system.process_events(step)
            all_processed.extend(processed)
        
        # Verify all events were processed
        self.assertEqual(len(all_processed), 5)
        self.assertEqual(len(self.processed_events), 5)
        self.assertEqual(len(self.event_system.event_queue), 0)
        
        # Verify processing order
        processed_steps = [event.step for event in all_processed]
        self.assertEqual(processed_steps, [1, 3, 5, 7, 10])

def run_demo():
    """Run a demonstration of the event system"""
    print("=" * 60)
    print("BANK CLIENT SIMULATION - EVENT SYSTEM DEMO")
    print("=" * 60)
    
    # Initialize system
    event_system = EventSystem()
    
    # Set up handlers
    def marketing_handler(event):
        print(f"📢 MARKETING: {event.campaign_type} campaign targeting {event.target_segment}")
        print(f"   Intensity: {event.intensity}, Budget: {event.budget} TND")
    
    def branch_handler(event):
        print(f"🏢 BRANCH: Closing branch in {event.location}")
        if event.alternative_branches:
            print(f"   Alternatives: {', '.join(event.alternative_branches)}")
    
    def product_handler(event):
        print(f"🚀 PRODUCT: Launching {event.product_type} for {event.target_market}")
        print(f"   Digital only: {event.digital_only}, Price: {event.pricing} TND")
    
    def competitor_handler(event):
        print(f"⚔️  COMPETITOR: {event.competitor_name} doing {event.action_type}")
        print(f"   Region: {event.affected_region}, Impact: {event.impact_intensity}")
    
    def economic_handler(event):
        print(f"📈 ECONOMIC: {event.shock_type} with severity {event.severity}")
        if event.affected_sectors:
            print(f"   Affected sectors: {', '.join(event.affected_sectors)}")
    
    # Register handlers
    event_system.register_event_handler("MarketingCampaignEvent", marketing_handler)
    event_system.register_event_handler("BranchClosureEvent", branch_handler)
    event_system.register_event_handler("ProductLaunchEvent", product_handler)
    event_system.register_event_handler("CompetitorActionEvent", competitor_handler)
    event_system.register_event_handler("EconomicShockEvent", economic_handler)
    
    # Create scenario events
    events = [
        MarketingCampaignEvent(
            step=2, target_segment="young_professionals", 
            campaign_type="mobile_banking_push", intensity=0.8, budget=100000
        ),
        CompetitorActionEvent(
            step=4, competitor_name="BIAT", action_type="rate_cut", 
            affected_region="Tunis", impact_intensity=0.7
        ),
        ProductLaunchEvent(
            step=6, product_type="contactless_payment", target_market="retail",
            pricing=5.0, digital_only=False
        ),
        BranchClosureEvent(
            step=8, location="Sfax", alternative_branches=["Sousse", "Monastir"],
            compensation_offered=True
        ),
        EconomicShockEvent(
            step=10, shock_type="currency_devaluation", severity=0.6,
            affected_sectors=["import", "tourism"], duration=30
        )
    ]
    
    # Inject events
    print("\n📥 INJECTING EVENTS...")
    for event in events:
        event_system.inject_event(event)
    
    print(f"✅ Injected {len(events)} events")
    print("\n📊 SYSTEM SUMMARY:")
    summary = event_system.get_event_summary()
    print(f"   Total events: {summary['total_events']}")
    print(f"   Event types: {list(summary['event_types'].keys())}")
    
    # Simulate processing over time
    print("\n🚀 STARTING SIMULATION...")
    print("=" * 60)
    
    for step in range(1, 15):
        print(f"\n⏰ STEP {step}")
        print("-" * 30)
        
        processed = event_system.process_events(step)
        if processed:
            for event in processed:
                # Handlers already printed the details
                pass
        else:
            print("   📋 No events this step")
    
    # Final summary
    print("\n" + "=" * 60)
    print("📈 FINAL SIMULATION SUMMARY")
    print("=" * 60)
    
    final_summary = event_system.get_event_summary()
    print(f"✅ Processed events: {final_summary['processed_events']}")
    print(f"❌ Failed events: {final_summary['failed_events']}")
    print(f"⏳ Pending events: {final_summary['pending_events']}")
    
    # Export history
    filename = event_system.export_event_history("demo_event_history.json")
    print(f"💾 Event history exported to: {filename}")


if __name__ == "__main__":
    # Run tests
    print("Running Event System Tests...")
    unittest.main(verbosity=2, exit=False)
    
    # Run demo
    print("\n" + "=" * 80)
    run_demo()