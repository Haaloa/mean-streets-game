"""
Scene.py - hala kod
Fungerar med zahra Game och InteractionController
"""


class Scene:
    """En Scene representerar en plats i spelet"""
    
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.objects = {}
    
    def add_object(self, game_object):
        """Lägg till ett objekt i denna Scene"""
        self.objects[game_object.name] = game_object
    
    def remove_object(self, game_object):
        """Ta bort ett objekt från denna Scene"""
        if game_object.name in self.objects:
            del self.objects[game_object.name]
    
    def get_object(self, name):
        """Hämta ett objekt från denna Scene (returnerar None om det inte finns)"""
        return self.objects.get(name)
    
    def get_available_objects(self):
        """Lista alla objekt som finns i denna Scene"""
        return list(self.objects.keys())
    
    def has_object(self, name):
        """Kolla om ett objekt finns i denna Scene"""
        return name in self.objects