import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.game import Game
from src.interaction_controller import InteractionController
from src.character_controller import CharacterInteractionController
from src.scene import Scene
from src.test_scene import TestScene
from src.game_object import GameObject
from src.character import Character
from src.game_plot import GamePlot
from src.world_service import WorldService
from src.inventory import Inventory
from src.event_manager import EventManager
from src.interaction_strategy import (
    LookAtStrategy, OpenItStrategy, MoveItStrategy,
    TurnItOnStrategy, TurnItOffStrategy, TasteItStrategy,
    PickItUpStrategy, DropItStrategy, InteractionStrategy,
)


# ── Helper functions ───────────────────────────────────────────────────────────

def make_game_with_test_scene():
    """Creates a Game with a simple test scene."""
    game = Game()
    scene = TestScene()
    game.set_scene(scene)
    ctrl = game.create_interaction_controller()
    return game, scene, ctrl


def make_character_setup():
    """Creates a simple setup for character interaction tests."""
    world_service = WorldService()
    game_plot = GamePlot()
    inventory = Inventory()

    scene = Scene("test_scene")
    anna = Character("Anna", "A nervous woman.")
    anna.add_response("murder", "I saw someone running!")
    anna.add_response("phone", "That phone belonged to the victim.")

    gift = GameObject("clue note", "An important note.")
    gift.add_strategy(LookAtStrategy())
    anna.set_gift_object(gift)

    scene.add_character(anna)
    world_service.register_scene(scene)
    world_service.set_active_scene(scene)

    ctrl = CharacterInteractionController(world_service, game_plot, inventory)
    return ctrl, inventory


# ══════════════════════════════════════════════════════════════════════════════
# USE CASE 1: INTERACT WITH OBJECT
# ══════════════════════════════════════════════════════════════════════════════

class TestSelectObject(unittest.TestCase):
    """Tests for step 1: selecting an object."""

    def setUp(self):
        self.game, self.scene, self.ctrl = make_game_with_test_scene()
        EventManager._instance = None

    def test_select_existing_object(self):
        result = self.ctrl.pick_game_object("test_object")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "test_object")

    def test_can_see_interactions_after_select(self):
        self.ctrl.pick_game_object("test_object")
        types = self.ctrl.get_interaction_types()
        self.assertGreater(len(types), 0)

    def test_new_selection_clears_strategy(self):
        self.ctrl.pick_game_object("test_object")
        self.ctrl.choose_interaction("LookAtStrategy")
        self.ctrl.pick_game_object("test_object")
        self.assertIsNone(self.ctrl._selected_strategy)

    def test_select_nonexistent_object(self):
        result = self.ctrl.pick_game_object("invisible_lamp")
        self.assertIsNone(result)

    def test_select_with_no_scene(self):
        empty_game = Game()
        empty_game.set_scene(None)
        ctrl = InteractionController(empty_game)
        result = ctrl.pick_game_object("test_object")
        self.assertIsNone(result)

    def test_no_interactions_before_select(self):
        types = self.ctrl.get_interaction_types()
        self.assertEqual(len(types), 0)

    def tearDown(self):
        EventManager._instance = None


class TestChooseInteraction(unittest.TestCase):
    """Tests for step 2: choosing which interaction to perform."""

    def setUp(self):
        self.game, self.scene, self.ctrl = make_game_with_test_scene()
        self.ctrl.pick_game_object("test_object")
        EventManager._instance = None

    def test_choose_by_name(self):
        result = self.ctrl.choose_interaction("LookAtStrategy")
        self.assertTrue(result)

    def test_correct_type_chosen(self):
        self.ctrl.choose_interaction("TurnItOnStrategy")
        self.assertIsInstance(self.ctrl._selected_strategy, TurnItOnStrategy)

    def test_all_8_interactions_work(self):
        interactions = [
            "LookAtStrategy", "OpenItStrategy", "MoveItStrategy",
            "TurnItOnStrategy", "TurnItOffStrategy", "TasteItStrategy",
            "PickItUpStrategy", "DropItStrategy",
        ]
        for name in interactions:
            self.ctrl.pick_game_object("test_object")
            result = self.ctrl.choose_interaction(name)
            self.assertTrue(result, f"{name} failed")

    def test_strategy_pattern_verified(self):
        """Verifies Strategy Pattern - all strategies are subclasses of InteractionStrategy."""
        strategies = [
            LookAtStrategy, OpenItStrategy, MoveItStrategy,
            TurnItOnStrategy, TurnItOffStrategy, TasteItStrategy,
            PickItUpStrategy, DropItStrategy,
        ]
        for s in strategies:
            self.assertTrue(issubclass(s, InteractionStrategy))

    def test_choose_nonexistent(self):
        result = self.ctrl.choose_interaction("FlyAwayStrategy")
        self.assertFalse(result)

    def test_choose_without_object(self):
        _, _, new_ctrl = make_game_with_test_scene()
        result = new_ctrl.choose_interaction("LookAtStrategy")
        self.assertFalse(result)

    def tearDown(self):
        EventManager._instance = None


class TestProvideOptions(unittest.TestCase):
    """Tests for step 3: providing extra options (e.g. direction)."""

    def setUp(self):
        self.game, self.scene, self.ctrl = make_game_with_test_scene()
        self.ctrl.pick_game_object("test_object")
        EventManager._instance = None

    def test_options_for_move(self):
        self.ctrl.choose_interaction("MoveItStrategy")
        result = self.ctrl.provide_options("to the left")
        self.assertTrue(result)

    def test_options_in_result(self):
        self.ctrl.choose_interaction("MoveItStrategy")
        self.ctrl.provide_options("to the left")
        result = self.ctrl.perform_interaction()
        self.assertIn("to the left", result)

    def test_options_when_not_needed(self):
        self.ctrl.choose_interaction("LookAtStrategy")
        result = self.ctrl.provide_options("irrelevant")
        self.assertFalse(result)

    def test_options_without_interaction(self):
        result = self.ctrl.provide_options("north")
        self.assertFalse(result)

    def tearDown(self):
        EventManager._instance = None


class TestPerformInteraction(unittest.TestCase):
    """Tests for step 4: performing the interaction."""

    def setUp(self):
        self.game, self.scene, self.ctrl = make_game_with_test_scene()
        EventManager._instance = None

    def _setup(self, name):
        self.ctrl.pick_game_object("test_object")
        self.ctrl.choose_interaction(name)

    def test_look_shows_description(self):
        self._setup("LookAtStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("test_object", result)

    def test_look_shows_off_default(self):
        self._setup("LookAtStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("off", result.lower())

    def test_turn_on_changes_state(self):
        self._setup("TurnItOnStrategy")
        self.ctrl.perform_interaction()
        self.assertTrue(self.ctrl._selected_object.is_on)

    def test_look_shows_on_after_turn_on(self):
        self._setup("TurnItOnStrategy")
        self.ctrl.perform_interaction()
        self._setup("LookAtStrategy")
        result = self.ctrl.perform_interaction()
        self.assertIn("on", result.lower())

    def test_turn_off_changes_state(self):
        self._setup("TurnItOnStrategy")
        self.ctrl.perform_interaction()
        self._setup("TurnItOffStrategy")
        self.ctrl.perform_interaction()
        self.assertFalse(self.ctrl._selected_object.is_on)

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
        result = self.ctrl.perform_interaction()
        self.assertEqual(result, "No interaction to perform.")

    def test_perform_without_interaction(self):
        self.ctrl.pick_game_object("test_object")
        result = self.ctrl.perform_interaction()
        self.assertEqual(result, "No interaction to perform.")

    def tearDown(self):
        EventManager._instance = None


class TestCancelInteraction(unittest.TestCase):
    """Tests for cancel_interaction."""

    def setUp(self):
        self.game, self.scene, self.ctrl = make_game_with_test_scene()
        EventManager._instance = None

    def test_cancel_resets(self):
        self.ctrl.pick_game_object("test_object")
        self.ctrl.choose_interaction("LookAtStrategy")
        self.ctrl.cancel_interaction()
        self.assertIsNone(self.ctrl._selected_object)
        self.assertIsNone(self.ctrl._selected_strategy)

    def test_cant_perform_after_cancel(self):
        self.ctrl.pick_game_object("test_object")
        self.ctrl.choose_interaction("LookAtStrategy")
        self.ctrl.cancel_interaction()
        result = self.ctrl.perform_interaction()
        self.assertEqual(result, "No interaction to perform.")

    def tearDown(self):
        EventManager._instance = None


# ══════════════════════════════════════════════════════════════════════════════
# USE CASE 2: INTERACT WITH CHARACTER
# ══════════════════════════════════════════════════════════════════════════════

class TestInitiateConversation(unittest.TestCase):
    """Tests for step 1: starting a conversation."""

    def setUp(self):
        self.ctrl, self.inventory = make_character_setup()

    def test_start_conversation_with_existing_character(self):
        result = self.ctrl.initiate_conversation("Anna")
        self.assertTrue(result)

    def test_start_conversation_case_insensitive(self):
        result = self.ctrl.initiate_conversation("anna")
        self.assertTrue(result)

    def test_start_conversation_with_unknown_character(self):
        result = self.ctrl.initiate_conversation("Bob")
        self.assertFalse(result)

    def test_is_in_conversation_after_start(self):
        self.ctrl.initiate_conversation("Anna")
        self.assertTrue(self.ctrl.is_in_conversation)

    def test_not_in_conversation_before_start(self):
        self.assertFalse(self.ctrl.is_in_conversation)


class TestSendQuery(unittest.TestCase):
    """Tests for step 2: sending queries to a character."""

    def setUp(self):
        self.ctrl, self.inventory = make_character_setup()
        self.ctrl.initiate_conversation("Anna")

    def test_response_to_keyword_murder(self):
        response = self.ctrl.send_query("murder")
        self.assertIn("running", str(response))

    def test_response_to_keyword_phone(self):
        response = self.ctrl.send_query("phone")
        self.assertIn("victim", str(response))

    def test_default_response_for_unknown_keyword(self):
        response = self.ctrl.send_query("xyz_unknown")
        self.assertIsNotNone(response)
        self.assertGreater(len(str(response)), 0)

    def test_response_is_not_empty(self):
        response = self.ctrl.send_query("hello")
        self.assertIsNotNone(str(response))


class TestAcceptGameObject(unittest.TestCase):
    """Tests for step 3: receiving an item from a character."""

    def setUp(self):
        self.ctrl, self.inventory = make_character_setup()
        self.ctrl.initiate_conversation("Anna")

    def test_accept_game_object(self):
        item = self.ctrl.accept_game_object()
        self.assertEqual(item, "clue note")

    def test_item_is_added_to_inventory(self):
        self.ctrl.accept_game_object()
        self.assertTrue(self.inventory.is_thing_here("clue note"))

    def test_no_item_without_conversation(self):
        new_ctrl, _ = make_character_setup()
        item = new_ctrl.accept_game_object()
        self.assertIsNone(item)


class TestEndConversation(unittest.TestCase):
    """Tests for step 4: ending a conversation."""

    def setUp(self):
        self.ctrl, self.inventory = make_character_setup()
        self.ctrl.initiate_conversation("Anna")

    def test_not_in_conversation_after_end(self):
        self.ctrl.end_conversation()
        self.assertFalse(self.ctrl.is_in_conversation)

    def test_end_without_active_conversation_does_not_crash(self):
        new_ctrl, _ = make_character_setup()
        try:
            new_ctrl.end_conversation()
        except Exception:
            self.fail("end_conversation() crashed without an active conversation")


# ══════════════════════════════════════════════════════════════════════════════
# HELPER TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestTestScene(unittest.TestCase):

    def setUp(self):
        EventManager._instance = None

    def test_has_test_object(self):
        scene = TestScene()
        self.assertTrue(scene.is_thing_here("test_object"))

    def test_object_has_all_interactions(self):
        scene = TestScene()
        obj = scene.find_object("test_object")
        self.assertEqual(len(obj.what_can_i_do()), 8)

    def test_plain_scene_empty(self):
        plain = Scene("plain")
        self.assertEqual(len(plain.show_available_things()), 0)

    def tearDown(self):
        EventManager._instance = None


class TestGame(unittest.TestCase):

    def setUp(self):
        EventManager._instance = None

    def test_create_controller(self):
        game = Game()
        ctrl = game.create_interaction_controller()
        self.assertIsInstance(ctrl, InteractionController)

    def test_which_scene(self):
        game = Game()
        scene = TestScene()
        game.set_scene(scene)
        self.assertIs(game.which_scene_am_i_in(), scene)

    def tearDown(self):
        EventManager._instance = None


if __name__ == "__main__":
    unittest.main(verbosity=2)
