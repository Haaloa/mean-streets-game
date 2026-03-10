from src.scene import Scene
from src.game_object import GameObject
from src.interaction_strategy import (
    LookAtStrategy, OpenItStrategy, MoveItStrategy,
    TurnItOnStrategy, TurnItOffStrategy, TasteItStrategy,
    PickItUpStrategy, DropItStrategy
)


class TestScene(Scene):
    def __init__(self):
        super().__init__("test scene")

        test_object = GameObject("test_object", "This is a test object.")
        test_object.add_interaction(LookAtStrategy())
        test_object.add_interaction(OpenItStrategy())
        test_object.add_interaction(MoveItStrategy())
        test_object.add_interaction(TurnItOnStrategy())
        test_object.add_interaction(TurnItOffStrategy())
        test_object.add_interaction(TasteItStrategy())
        test_object.add_interaction(PickItUpStrategy())
        test_object.add_interaction(DropItStrategy())

        self.add_object(test_object)