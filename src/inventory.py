from src.scene import Scene


class Inventory(Scene):

    def __init__(self):
        super().__init__("Inventory", "Things you have picked up.")

    def add_object(self, obj):
        super().add_object(obj)

    def remove_object(self, obj):
        super().remove_object(obj)

    def is_empty(self):
        return len(self.show_available_things()) == 0
