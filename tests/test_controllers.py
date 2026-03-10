import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.game import Game, InteractionController
from src.scene import Scene
from src.test_scene import TestScene
from src.game_object import GameObject
from src.interaction_strategy import (
    LookAtStrategy, OpenItStrategy, MoveItStrategy,
    TurnItOnStrategy, TurnItOffStrategy, TasteItStrategy,
    PickItUpStrategy, DropItStrategy, InteractionStrategy,
)

def make_test_game():
    """Creates game with test scene"""
    game = Game()
    scene = TestScene()
    game.set_scene(scene)
    ctrl = game.create_interaction_controller()
    return game, scene, ctrl


class TestSelectObject(unittest.TestCase):

    def setUp(self):
        self.game, self.scene, self.ctrl = make_test_game()

    def test_select_existing_object(self):
        # Positive - select existing object
        result = self.ctrl.pick_game_object("test_object")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "test_object")

    def test_can_see_interactions_after_select(self):
        # Interactions visible after selection
        self.ctrl.pick_game_object("test_object")
        types = self.ctrl.get_interaction_types()
        self.assertGreater(len(types), 0)

    def test_new_selection_clears_old(self):
        # New selection clears previous
        self.ctrl.pick_game_object("test_object")
        self.ctrl.choose_interaction("LookAtStrategy")
        self.ctrl.pick_game_object("test_object")
        self.assertIsNone(self.ctrl._selected_strategy)

    def test_select_nonexistent_object(self):
        # Negative - object doesn't exist
        result = self.ctrl.pick_game_object("ghost_lamp")
        self.assertIsNone(result)

    def test_select_with_no_scene(self):
        # Negative - no scene set
        empty_game = Game()
        ctrl = InteractionController(empty_game)
        result = ctrl.pick_game_object("test_object")
        self.assertIsNone(result)

    def test_no_interactions_before_select(self):
        # No interactions before selecting object
        types = self.ctrl.get_interaction_types()
        self.assertEqual(len(types), 0)

    def tearDown(self):
        self.ctrl._selected_object = None
        self.ctrl._selected_strategy = None


class TestChooseInteraction(unittest.TestCase):

    def setUp(self):
        self.game, self.scene, self.ctrl = make_test_game()
        self.ctrl.pick_game_object("test_object")

    def test_choose_by_name(self):
        # Positive - choose by name
        result = self.ctrl.choose_interaction("LookAtStrategy")
        self.assertTrue(result)

    def test_correct_type_chosen(self):
        # Correct type is selected
        self.ctrl.choose_interaction("TurnItOnStrategy")
        self.assertIsInstance(self.ctrl._selected_strategy, TurnItOnStrategy)

    def test_all_8_interactions_work(self):
        # All 8 interactions are choosable
        interactions = ["LookAtStrategy", "OpenItStrategy", "MoveItStrategy",
                       "TurnItOnStrategy", "TurnItOffStrategy", "TasteItStrategy",
                       "PickItUpStrategy", "DropItStrategy"]
        
        for name in interactions:
            self.ctrl.pick_game_object("test_object")
            result = self.ctrl.choose_interaction(name)
            self.assertTrue(result)

    def test_strategy_pattern_verified(self):
        # All strategies inherit from base class
        strategies = [LookAtStrategy, OpenItStrategy, MoveItStrategy,
                     TurnItOnStrategy, TurnItOffStrategy, TasteItStrategy,
                     PickItUpStrategy, DropItStrategy]
        
        for s in strategies:
            self.assertTrue(issubclass(s, InteractionStrategy))

    def test_choose_nonexistent(self):
        # Negative - doesn't exist
        result = self.ctrl.choose_interaction("FlyAwayStrategy")
        self.assertFalse(result)

    def test_choose_without_object(self):
        # Negative - no object selected
        _, _, new_ctrl = make_test_game()
        result = new_ctrl.choose_interaction("LookAtStrategy")
        self.assertFalse(result)

    def tearDown(self):
        self.ctrl._selected_object = None
        self.ctrl._selected_strategy = None


class TestProvideOptions(unittest.TestCase):

    def setUp(self):
        self.game, self.scene, self.ctrl = make_test_game()
        self.ctrl.pick_game_object("test_object")

    def test_options_for_move(self):
        # Positive - move needs direction
        self.ctrl.choose_interaction("MoveItStrategy")
        result = self.ctrl.provide_options("to the left")
        self.assertTrue(result)

    def test_options_in_result(self):
        # Options appear in result
        self.ctrl.choose_interaction("MoveItStrategy")
        self.ctrl.provide_options("to the left")
        result = self.ctrl.perform_interaction()
        self.assertIn("to the left", result)

    def test_options_when_not_needed(self):
        # Negative - not needed
        self.ctrl.choose_interaction("LookAtStrategy")
        result = self.ctrl.provide_options("irrelevant")
        self.assertFalse(result)

    def test_options_without_interaction(self):
        # Negative - no interaction chosen
        result = self.ctrl.provide_options("north")
        self.assertFalse(result)

    def tearDown(self):
        self.ctrl._selected_object = None
        self.ctrl._selected_strategy = None


class TestPerformInteraction(unittest.TestCase):

    def setUp(self):
        self.game, self.scene, self.ctrl = make_test_game()

    def _setup(self, name):
        self.ctrl.pick_game_object("test_object")
        self.ctrl.choose_interaction(name)

    def test_look_shows_description(self):
        # Look shows description
        self._setup("LookAtStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("test_object", result)

    def test_look_shows_off_default(self):
        # Starts as "off"
        self._setup("LookAtStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("off", result.lower())

    def test_turn_on_changes_state(self):
        # Turn on changes state
        self._setup("TurnItOnStrategy")
        self.ctrl.perform_interaction()
        self.assertTrue(self.ctrl._selected_object.is_on)

    def test_look_shows_on_after_turn_on(self):
        # Look shows "on" after turn on
        self._setup("TurnItOnStrategy")
        self.ctrl.perform_interaction()
        self._setup("LookAtStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("on", result.lower())

    def test_turn_off_changes_state(self):
        # Turn off changes state
        self._setup("TurnItOnStrategy")
        self.ctrl.perform_interaction()
        self._setup("TurnItOffStrategy")
        self.ctrl.perform_interaction()
        self.assertFalse(self.ctrl._selected_object.is_on)

    def test_look_shows_off_after_turn_off(self):
        # Look shows "off" after turn off
        self._setup("TurnItOnStrategy")
        self.ctrl.perform_interaction()
        self._setup("TurnItOffStrategy")
        self.ctrl.perform_interaction()
        self._setup("LookAtStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("off", result.lower())

    def test_open_works(self):
        self._setup("OpenItStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("open", result.lower())

    def test_taste_works(self):
        self._setup("TasteItStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("taste", result.lower())

    def test_pick_up_works(self):
        self._setup("PickItUpStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("pick up", result.lower())

    def test_drop_works(self):
        self._setup("DropItStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("drop", result.lower())

    def test_perform_without_object(self):
        # Negative - no object
        result = self.ctrl.perform_interaction()
        self.assertEqual(result, "No interaction to perform.")

    def test_perform_without_interaction(self):
        # Negative - no interaction
        self.ctrl.pick_game_object("test_object")
        result = self.ctrl.perform_interaction()
        self.assertEqual(result, "No interaction to perform.")

    def tearDown(self):
        self.ctrl._selected_object = None
        self.ctrl._selected_strategy = None


class TestCancelInteraction(unittest.TestCase):

    def setUp(self):
        self.game, self.scene, self.ctrl = make_test_game()

    def test_cancel_resets(self):
        # Cancel resets everything
        self.ctrl.pick_game_object("test_object")
        self.ctrl.choose_interaction("LookAtStrategy")
        self.ctrl.cancel_interaction()
        
        self.assertIsNone(self.ctrl._selected_object)
        self.assertIsNone(self.ctrl._selected_strategy)

    def test_cant_perform_after_cancel(self):
        # Can't perform after cancel
        self.ctrl.pick_game_object("test_object")
        self.ctrl.choose_interaction("LookAtStrategy")
        self.ctrl.cancel_interaction()
        result = self.ctrl.perform_interaction()
        self.assertEqual(result, "No interaction to perform.")

    def tearDown(self):
        self.ctrl._selected_object = None
        self.ctrl._selected_strategy = None


class TestTestScene(unittest.TestCase):

    def setUp(self):
        self.scene = TestScene()

    def test_has_test_object(self):
        # Test scene has test object
        self.assertTrue(self.scene.is_thing_here("test_object"))

    def test_object_has_all_interactions(self):
        # Test object has all 8
        obj = self.scene.find_object("test_object")
        self.assertEqual(len(obj.what_can_i_do()), 8)

    def test_plain_scene_empty(self):
        # Plain scene starts empty
        plain = Scene("plain")
        self.assertEqual(len(plain.show_available_things()), 0)


class TestGame(unittest.TestCase):

    def test_create_controller(self):
        # Game creates controller
        game = Game()
        ctrl = game.create_interaction_controller()
        self.assertIsInstance(ctrl, InteractionController)

    def test_which_scene(self):
        # Returns current scene
        game = Game()
        scene = TestScene()
        game.set_scene(scene)
        self.assertIs(game.which_scene_am_i_in(), scene)


if __name__ == "__main__":
    unittest.main(verbosity=2)
