class Scene:
    """Represents a location in the game with objects and characters."""

    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self._objects = []
        self._characters = []

    def add_object(self, obj):
        self._objects.append(obj)

    def remove_object(self, obj):
        if obj in self._objects:
            self._objects.remove(obj)

    def add_character(self, character):
        self._characters.append(character)

    def show_available_things(self):
        return list(self._objects)

    def get_characters(self):
        return list(self._characters)

    def is_thing_here(self, name):
        return any(obj.name == name for obj in self._objects)

    def find_object(self, name):
        for obj in self._objects:
            if obj.name == name:
                return obj
        return None
