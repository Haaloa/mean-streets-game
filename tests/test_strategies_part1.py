import unittest

from strategies.concrete_strategies_part1 import (
    LookStrategy,
    OpenStrategy,
    MoveStrategy,
    TurnOnStrategy
)


class MockGameObject:
    """En enkel fake-klass för att testa strategierna."""

    def __init__(self, name, description=""):
        self.name = name
        self.description = description

        # Egenskaper som strategierna använder
        self.can_open = False
        self.can_move = True
        self.can_turn_on = False
        self.contents = "nothing"
        self.is_on = False


class TestStrategiesPart1(unittest.TestCase):
    """Unit tests för Person 1:s fyra strategier."""

    def setUp(self):
        # Objekt för olika testfall
        self.phone = MockGameObject("phone", "A black rotary phone")
        self.drawer = MockGameObject("drawer", "A wooden drawer")
        self.drawer.can_open = True
        self.drawer.can_move = False
        self.drawer.contents = "a rusty key"

        self.lamp = MockGameObject("lamp", "A desk lamp")
        self.lamp.can_turn_on = True

        self.box = MockGameObject("box", "A heavy wooden box")
        self.box.can_move = True

    def test_look_strategy(self):
        strategy = LookStrategy()
        result = strategy.do_it(self.phone, None, {})

        self.assertEqual(result, "You look at the phone. A black rotary phone")

    def test_open_strategy(self):
        strategy = OpenStrategy()
        result = strategy.do_it(self.drawer, None, {})

        self.assertEqual(result, "You open the drawer and find a rusty key.")

    def test_move_strategy(self):
        strategy = MoveStrategy()

        # Kontrollera att strategin kräver extra info
        self.assertTrue(strategy.need_more_info())
        self.assertEqual(
            strategy.ask_for_more_info(),
            "Which direction do you want to move it?"
        )

        # Testa själva flytten
        result = strategy.do_it(self.box, None, {"direction": "left"})
        self.assertEqual(result, "You move the box left.")

    def test_turnon_strategy(self):
        strategy = TurnOnStrategy()

        # Lampan ska vara av från början
        self.assertFalse(self.lamp.is_on)

        result = strategy.do_it(self.lamp, None, {})

        self.assertEqual(result, "You turn on the lamp.")
        self.assertTrue(self.lamp.is_on)


if __name__ == "__main__":
    unittest.main()