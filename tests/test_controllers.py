import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.game import Game
from controllers.interaction_controller import InteractionController


class TestGameHighCohesion(unittest.TestCase):

    def test_game_high_cohesion(self):
        game = Game()
        public_methods = [
            m for m in dir(game)
            if callable(getattr(game, m)) and not m.startswith('_')
        ]
        self.assertLessEqual(len(public_methods), 7)

    def test_game_has_correct_method_names(self):
        game = Game()
        self.assertTrue(hasattr(game, 'whichSceneAmIIn'))
        self.assertTrue(hasattr(game, 'createInteractionController'))
        self.assertTrue(hasattr(game, 'saveMyProgress'))
        self.assertTrue(hasattr(game, 'loadMyProgress'))

    def test_game_starts_with_scene(self):
        game = Game()
        scene = game.whichSceneAmIIn()
        self.assertIsNotNone(scene)


class TestCreateController(unittest.TestCase):

    def test_create_controller(self):
        game = Game()
        controller = game.createInteractionController()
        self.assertIsInstance(controller, InteractionController)

    def test_new_controller_each_time(self):
        game = Game()
        controller1 = game.createInteractionController()
        controller2 = game.createInteractionController()
        self.assertIsNot(controller1, controller2)


class TestPickGameObject(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.controller = self.game.createInteractionController()

    def test_pick_object_that_exists(self):
        result = self.controller.pickGameObject("Telefon")
        self.assertTrue(result)

    def test_pick_object_that_does_not_exist(self):
        result = self.controller.pickGameObject("Flygande matta")
        self.assertFalse(result)


class TestChooseInteraction(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.controller = self.game.createInteractionController()

    def test_choose_interaction_without_object(self):
        result = self.controller.chooseInteraction("look")
        self.assertFalse(result)

    def test_choose_valid_interaction(self):
        self.controller.pickGameObject("Telefon")
        result = self.controller.chooseInteraction("look")
        self.assertTrue(result)


class TestFullInteractionFlow(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.controller = self.game.createInteractionController()

    def test_full_flow(self):
        self.assertTrue(self.controller.pickGameObject("Telefon"))
        self.assertTrue(self.controller.chooseInteraction("look"))
        result = self.controller.performInteraction()
        self.assertIsNotNone(result)

    def test_cancel_resets_everything(self):
        self.controller.pickGameObject("Telefon")
        self.controller.chooseInteraction("look")
        self.controller.cancelInteraction()
        self.assertIsNone(self.controller._selectedObject)
        self.assertIsNone(self.controller._selectedStrategy)

    def test_perform_without_selection_returns_none(self):
        result = self.controller.performInteraction()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)