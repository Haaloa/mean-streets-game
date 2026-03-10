from src.scene import Scene
from src.game_object import GameObject
from src.interaction_strategy import (
    LookAtStrategy,
    OpenItStrategy,
    MoveItStrategy,
    TurnItOnStrategy,
    TurnItOffStrategy,
    TasteItStrategy,
    PickItUpStrategy,
    DropItStrategy
)


class TestScene(Scene):

    def __init__(self):

        super().__init__("test scene")

        test_object = GameObject("test_object", "This is a test object.")

        test_object.add_strategy(LookAtStrategy())
        test_object.add_strategy(OpenItStrategy())
        test_object.add_strategy(MoveItStrategy())
        test_object.add_strategy(TurnItOnStrategy())
        test_object.add_strategy(TurnItOffStrategy())
        test_object.add_strategy(TasteItStrategy())
        test_object.add_strategy(PickItUpStrategy())
        test_object.add_strategy(DropItStrategy())

        self.add_object(test_object)