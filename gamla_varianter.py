# ═══════════════════════════════════════════════════════════════════════════════
# OLD VARIANTS - saved for reference
# These implementations were removed from the main code but can be used
# if you want to extend or change the design later.
# ═══════════════════════════════════════════════════════════════════════════════


# ── ALTERNATIVE: WorldService as Singleton (via __new__) ─────────────────────
# The old version used __new__ to implement Singleton in WorldService.
# The current version uses a plain class because we chose to demonstrate
# the Singleton pattern only via EventManager (matches the class diagram).
#
# class WorldService:
#     _instance = None
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance._scenes = []
#             cls._instance._active_scene = None
#         return cls._instance
#
#     def register_scene(self, scene):
#         if scene not in self._scenes:
#             self._scenes.append(scene)
#
#     def get_all_scenes(self):
#         return list(self._scenes)
#
#     def set_active_scene(self, scene):
#         self._active_scene = scene
#
#     def get_active_scene(self):
#         return self._active_scene


# ── ALTERNATIVE: GameObject without change_how_to_interact / do_interaction ──
# This version was missing the two methods present in the class diagram.
# InteractionController called the strategy directly instead of via GameObject.
# Drawback: GameObject is no longer the <<context>> in the Strategy Pattern.
#
# class GameObject:
#     def __init__(self, name, description=""):
#         self.name = name
#         self.description = description
#         self._strategies = []
#         self.is_on = False
#
#     def add_strategy(self, strategy):
#         self._strategies.append(strategy)
#
#     def add_interaction(self, strategy):
#         self.add_strategy(strategy)
#
#     def what_can_i_do(self):
#         return list(self._strategies)


# ── ALTERNATIVE: InteractionStrategy with do_it() and needs_more_info() ──────
# An earlier version used these method names instead of interact() and needs_options().
# Changed to better match the class diagram.
#
# class InteractionStrategy(ABC):
#     @abstractmethod
#     def do_it(self, obj):
#         pass
#
#     @abstractmethod
#     def needs_more_info(self):
#         pass


# ── ALTERNATIVE: InteractionController with world_service + inventory ─────────
# An earlier version took world_service and inventory directly as arguments
# instead of the game object. Changed to simplify and match the diagram.
#
# class InteractionController:
#     def __init__(self, world_service, inventory):
#         self._world_service = world_service
#         self._inventory = inventory
#         self._repo = GameObjectRepository()
#         self._selected_object = None
#         self._selected_strategy = None


# ── ALTERNATIVE: GameObjectRepository ────────────────────────────────────────
# Helper class for finding objects in scenes. Removed when InteractionController
# was simplified to use scene.find_object() directly.
#
# class GameObjectRepository:
#     def find_game_object(self, name, scene):
#         return scene.find_object(name)
#
#     def get_all_objects(self, scene):
#         return scene.show_available_things()


# ── ALTERNATIVE: Scene with is_available() ───────────────────────────────────
# Checked if an element (object or character) was present in the scene.
# Removed because is_thing_here() and get_characters() cover the need.
#
# def is_available(self, element_name):
#     for o in self._objects:
#         if o.name == element_name:
#             return True
#     for c in self._characters:
#         if c.name == element_name:
#             return True
#     return False
