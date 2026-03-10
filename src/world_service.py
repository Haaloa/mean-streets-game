class WorldService:
    def __init__(self):
        self._scenes = []
        self._active_scene = None

    def register_scene(self, scene):
        self._scenes.append(scene)

    def set_active_scene(self, scene):
        self._active_scene = scene

    def get_active_scene(self):
        return self._active_scene

    def get_all_scenes(self):
        return list(self._scenes)



# class WorldService:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance._scenes = []
#             cls._instance._active_scene = None
#         return cls._instance

#     def register_scene(self, scene):
#         if scene not in self._scenes:
#             self._scenes.append(scene)

#     def get_all_scenes(self):
#         return list(self._scenes)

#     def set_active_scene(self, scene):
#         self._active_scene = scene

#     def get_active_scene(self):
#         return self._active_scene
