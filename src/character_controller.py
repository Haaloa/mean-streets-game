from src.character import CharacterInterface


class CharacterInteractionController:
    def __init__(self, world_service, game_plot, inventory):
        self._world_service = world_service
        self._game_plot = game_plot
        self._inventory = inventory
        self._interface = CharacterInterface()

    def initiate_conversation(self, character_name):
        scene = self._world_service.get_active_scene()
        if scene is None:
            return False

        for character in scene.get_characters():
            if character.name.lower() == character_name.lower():
                self._interface.connect(character)
                return True

        return False

    def send_query(self, query):
        stage = self._game_plot.get_current_stage()
        return self._interface.send_query(query, stage)

    def accept_game_object(self):
        if not self._interface.is_connected:
            return None

        character = self._interface.active_character
        stage = self._game_plot.get_current_stage()
        obj = character.create_game_object(stage)

        if obj:
            self._inventory.add_object(obj)
            return obj.name

        return None

    def end_conversation(self):
        if not self._interface.is_connected:
            return

        character = self._interface.active_character
        stage = self._game_plot.get_current_stage()
        record = character.end_conversation(stage)
        self._game_plot.add_conversation_record(record)
        self._interface.disconnect()

    @property
    def is_in_conversation(self):
        return self._interface.is_connected



# from src.character import CharacterInterface


# class CharacterInteractionController:
#     def __init__(self, world_service, game_plot, inventory):
#         self._world_service = world_service
#         self._game_plot = game_plot
#         self._inventory = inventory
#         self._interface = CharacterInterface()

#     def initiate_conversation(self, character_name):
#         scene = self._world_service.get_active_scene()
#         if scene is None:
#             return False
#         chars = scene.get_characters()
#         for c in chars:
#             if c.name.lower() == character_name.lower():
#                 self._interface.connect(c)
#                 return True
#         return False

#     def send_query(self, query):
#         stage = self._game_plot.get_current_stage()
#         return self._interface.send_query(query, stage)

#     def accept_game_object(self):
#         if not self._interface.is_connected:
#             return None
#         char = self._interface.active_character
#         stage = self._game_plot.get_current_stage()
#         obj = char.create_game_object(stage)
#         if obj:
#             self._inventory.add_object(obj)
#             return obj.name
#         return None

#     def end_conversation(self):
#         if not self._interface.is_connected:
#             return
#         char = self._interface.active_character
#         stage = self._game_plot.get_current_stage()
#         record = char.end_conversation(stage)
#         self._game_plot.add_conversation_record(record)
#         self._interface.disconnect()

#     @property
#     def is_in_conversation(self):
#         return self._interface.is_connected
