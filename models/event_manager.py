"""
EventManager.py - rana kod
Singleton Pattern
"""


class EventManager:
    """EventManager är en Singleton - bara EN instans kan finnas"""
    
    _instance = None
    
    @classmethod
    def getSharedInstance(cls):
        """Hämta den enda instansen av EventManager"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Privat constructor - använd getSharedInstance() istället"""
        if EventManager._instance is not None:
            raise Exception("EventManager är en Singleton! Använd getSharedInstance()")
        self.events = []
        self.event_queue = []
    
    def scheduleEvent(self, condition, event):
        """Skapa ett nytt event"""
        new_event = {
            "condition": condition,
            "event": event
        }
        self.events.append(new_event)
    
    def findEventsMatching(self, condition):
        """Hitta alla events som matchar en condition"""
        matching = []
        for event in self.events:
            if event["condition"] == condition:
                matching.append(event)
        return matching
    
    def triggerEventsFor(self, condition):
        """Trigga alla events för en condition"""
        triggered = []
        for event in self.events:
            if event["condition"] == condition:
                triggered.append(event["event"])
                self.event_queue.append(event["event"])
        return triggered
    
    def removeEvent(self, event_to_remove):
        """Ta bort ett event"""
        self.events = [e for e in self.events if e["event"] != event_to_remove]