
class InteractionController:
    def __init__(self, game):
        self._game = game
        self._selected_object = None
        self._selected_strategy = None

    def pick_game_object(self, object_name):
        scene = self._game.which_scene_am_i_in()
        if scene is None:
            return None

        obj = scene.find_object(object_name)
        if obj is None:
            return None

        self._selected_object = obj
        self._selected_strategy = None
        return obj

    def get_interaction_types(self):
        if self._selected_object is None:
            return []
        return [type(strategy).__name__ for strategy in self._selected_object.what_can_i_do()]

    def choose_interaction(self, type_name):
        if self._selected_object is None:
            return False

        for strategy in self._selected_object.what_can_i_do():
            if strategy.__class__.__name__ == type_name:
                self._selected_strategy = strategy
                return True

        return False

    def provide_options(self, options):
        if self._selected_strategy is None:
            return False

        if hasattr(self._selected_strategy, "needs_options") and self._selected_strategy.needs_options():
            self._selected_strategy.set_options(options)
            return True

        return False

    def perform_interaction(self):
        if self._selected_object is None or self._selected_strategy is None:
            return "No interaction to perform."

        return self._selected_strategy.interact(self._selected_object)

    def cancel_interaction(self):
        self._selected_object = None
        self._selected_strategy = None



# from src.scene import GameObjectRepository


# class InteractionController:
#     def __init__(self, world_service, inventory):
#         self._world_service = world_service
#         self._inventory = inventory
#         self._repo = GameObjectRepository()
#         self._selected_object = None
#         self._selected_strategy = None

#     def pick_game_object(self, object_name):
#         scene = self._world_service.get_active_scene()
#         if scene is None:
#             return None
#         obj = self._repo.find_game_object(object_name, scene)
#         if obj is None:
#             return None
#         self._selected_object = obj
#         self._selected_strategy = None
#         return obj

#     def get_interaction_types(self):
#         if self._selected_object is None:
#             return []
#         return self._selected_object.what_can_i_do()

#     def choose_interaction(self, type_name):
#         if self._selected_object is None:
#             return False
#         for strategy in self._selected_object.what_can_i_do():
#             if strategy.__class__.__name__ == type_name:
#                 self._selected_strategy = strategy
#                 self._selected_object.change_how_to_interact(strategy)
#                 return True
#         return False

#     def provide_options(self, options):
#         if self._selected_strategy is None:
#             return False
#         if hasattr(self._selected_strategy, 'set_options'):
#             self._selected_strategy.set_options(options)
#         return True

#     def perform_interaction(self):
#         if self._selected_object is None or self._selected_strategy is None:
#             return "No interaction to perform."
#         result = self._selected_object.do_interaction()
#         scene = self._world_service.get_active_scene()
#         if self._selected_strategy.__class__.__name__ == "PickItUpStrategy":
#             if scene and self._selected_object in scene.show_available_things():
#                 scene.remove_object(self._selected_object)
#                 self._inventory.add_object(self._selected_object)
#         elif self._selected_strategy.__class__.__name__ == "DropItStrategy":
#             if self._selected_object in self._inventory.show_available_things():
#                 self._inventory.remove_object(self._selected_object)
#                 if scene:
#                     scene.add_object(self._selected_object)
#         return result

#     def cancel_interaction(self):
#         self._selected_object = None
#         self._selected_strategy = None
