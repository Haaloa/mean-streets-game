class WorldService:
    """Manages all scenes and tracks the currently active scene."""

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
