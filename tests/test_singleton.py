import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.event_manager import EventManager


class TestSingleton(unittest.TestCase):
    """
    Tests for the Singleton Pattern (Person 3).
    Demonstrates that EventManager always returns the same instance.
    """

    def setUp(self):
        # Reset Singleton before each test
        EventManager._instance = None

    def test_same_instance_returned(self):
        """Singleton - em1 and em2 must be the exact same object."""
        em1 = EventManager.getSharedInstance()
        em2 = EventManager.getSharedInstance()
        self.assertIs(em1, em2)

    def test_shared_state(self):
        """State added via one reference is visible via another."""
        em1 = EventManager.getSharedInstance()
        em1.scheduleEvent("test_condition", "Test message")

        em2 = EventManager.getSharedInstance()
        events = em2.findEventsMatching("test_condition")
        self.assertEqual(len(events), 1)

    def test_schedule_event(self):
        """scheduleEvent() registers an event correctly."""
        em = EventManager.getSharedInstance()
        em.scheduleEvent("pickup_phone", "You found a clue!")
        events = em.findEventsMatching("pickup_phone")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["message"], "You found a clue!")

    def test_trigger_events(self):
        """triggerEventsFor() returns the correct messages."""
        em = EventManager.getSharedInstance()
        em.scheduleEvent("talk_anna", "Anna seems nervous...")
        triggered = em.triggerEventsFor("talk_anna")
        self.assertEqual(len(triggered), 1)
        self.assertIn("Anna", triggered[0])

    def test_trigger_unknown_condition(self):
        """triggerEventsFor() with unknown condition returns empty list."""
        em = EventManager.getSharedInstance()
        triggered = em.triggerEventsFor("does_not_exist")
        self.assertEqual(triggered, [])

    def test_remove_event(self):
        """removeEvent() removes an event correctly."""
        em = EventManager.getSharedInstance()
        em.scheduleEvent("remove_me", "This should be removed")
        em.removeEvent("remove_me")
        events = em.findEventsMatching("remove_me")
        self.assertEqual(len(events), 0)

    def test_direct_instantiation_raises_exception(self):
        """You should not be able to create a second instance directly."""
        EventManager.getSharedInstance()  # create the first instance
        with self.assertRaises(Exception):
            EventManager()  # this should raise an exception

    def tearDown(self):
        EventManager._instance = None


if __name__ == "__main__":
    unittest.main(verbosity=2)
