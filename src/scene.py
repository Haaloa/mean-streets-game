class Scene:
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

    def add_character(self, c):
        self._characters.append(c)

    def show_available_things(self):
        return list(self._objects)

    def get_characters(self):
        return list(self._characters)

    def is_thing_here(self, name):
        for o in self._objects:
            if o.name == name:
                return True
        return False

    def find_object(self, name):
        for obj in self._objects:
            if obj.name == name:
                return obj
        return None

    def is_available(self, element_name):
        for o in self._objects:
            if o.name == element_name:
                return True
        for c in self._characters:
            if c.name == element_name:
                return True
        return False


# class Scene:
#     def __init__(self, name, description=""):
#         self.name = name
#         self.description = description
#         self._objects = []
#         self._characters = []

#     def add_object(self, obj):
#         self._objects.append(obj)

#     def remove_object(self, obj):
#         if obj in self._objects:
#             self._objects.remove(obj)

#     def add_character(self, c):
#         self._characters.append(c)

#     def show_available_things(self):
#         return list(self._objects)

#     def get_characters(self):
#         return list(self._characters)

#     def is_thing_here(self, name):
#         for o in self._objects:
#             if o.name == name:
#                 return True
#         return False

#     def find_object(self, name):
#         for obj in self._objects:
#             if obj.name == name:
#                 return obj
#         return None

#     def is_available(self, element_name):
#         for o in self._objects:
#             if o.name == element_name:
#                 return True
#         for c in self._characters:
#             if c.name == element_name:
#                 return True
#         return False


# class GameObjectRepository:
#     def find_game_object(self, name, scene):
#         return scene.find_object(name)

#     def get_all_objects(self, scene):
#         return scene.show_available_things()
