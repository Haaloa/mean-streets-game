class EventManager:
    """
    Singleton Pattern - guarantees only ONE instance exists in the entire system.
    All game events are handled in one place.

    Usage:
        em = EventManager.getSharedInstance()
        em.scheduleEvent("pickup_phone", "You found an important clue!")
        em.triggerEventsFor("pickup_phone")
    """

    _instance = None

    @classmethod
    def getSharedInstance(cls):
        """Always returns the same instance (Singleton)."""
        if cls._instance is None:
            cls._instance = EventManager()
        return cls._instance

    def __init__(self):
        if EventManager._instance is not None:
            raise Exception("EventManager is a Singleton! Use getSharedInstance().")
        self._events = []

    def scheduleEvent(self, condition, message):
        """Register an event to be triggered when a certain condition is met."""
        self._events.append({"condition": condition, "message": message})

    def triggerEventsFor(self, condition):
        """Trigger all events matching the condition. Returns a list of messages."""
        triggered = []
        for event in self._events:
            if event["condition"] == condition:
                triggered.append(event["message"])
        return triggered

    def findEventsMatching(self, condition):
        """Return all events matching the condition (without triggering them)."""
        return [e for e in self._events if e["condition"] == condition]

    def removeEvent(self, condition):
        """Remove all events with a given condition."""
        self._events = [e for e in self._events if e["condition"] != condition]
