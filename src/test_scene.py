from src.scene import Scene
from src.game_object import GameObject
from src.interaction_strategy import (
    LookAtStrategy, OpenItStrategy, MoveItStrategy,
    TurnItOnStrategy, TurnItOffStrategy, TasteItStrategy,
    PickItUpStrategy, DropItStrategy,
)


class TestScene(Scene):
    """
    A test scene that always contains a test_object with all 8 strategies.
    Used in unit tests to avoid setting up the full game world.
    """

    def __init__(self):
        super().__init__("test_scene")
        obj = GameObject("test_object", "A generic test object.")
        obj.add_strategy(LookAtStrategy())
        obj.add_strategy(OpenItStrategy())
        obj.add_strategy(MoveItStrategy())
        obj.add_strategy(TurnItOnStrategy())
        obj.add_strategy(TurnItOffStrategy())
        obj.add_strategy(TasteItStrategy())
        obj.add_strategy(PickItUpStrategy())
        obj.add_strategy(DropItStrategy())
        self.add_object(obj)
