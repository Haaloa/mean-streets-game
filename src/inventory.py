from src.scene import Scene


class Inventory(Scene):
    """The player's inventory - a special scene belonging to the player."""

    def __init__(self):
        super().__init__("Inventory", "Items you have picked up.")

    def is_empty(self):
        return len(self.show_available_things()) == 0
