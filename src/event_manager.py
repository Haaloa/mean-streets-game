# class EventManager:
#     _instance = None
    
#     @classmethod
#     def getSharedInstance(cls):
#         if cls._instance is None:
#             cls._instance = cls()
#         return cls._instance
    
#     def __init__(self):
#         if EventManager._instance is not None:
#             raise Exception("EventManager is a Singleton! Use getSharedInstance()")
#         self.events = []
#         self.event_queue = []
    
#     def scheduleEvent(self, condition, event):
#         new_event = {
#             "condition": condition,
#             "event": event
#         }
#         self.events.append(new_event)
    
#     def findEventsMatching(self, condition):
#         matching = []
#         for event in self.events:
#             if event["condition"] == condition:
#                 matching.append(event)
#         return matching
    
#     def triggerEventsFor(self, condition):
#         triggered = []
#         for event in self.events:
#             if event["condition"] == condition:
#                 triggered.append(event["event"])
#                 self.event_queue.append(event["event"])
#         return triggered
    
#     def removeEvent(self, event_to_remove):
#         self.events = [e for e in self.events if e["event"] != event_to_remove]
