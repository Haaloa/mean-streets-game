from models.scene import Scene
from models.game_object import GameObject


class Game:

    def __init__(self):
        self._currentScene = Scene("Vardagsrum")
        self._currentScene.add_object(GameObject.create_phone())
        self._currentScene.add_object(GameObject.create_drawer())
        self._currentScene.add_object(GameObject.create_apple())
        self._inventory = []

    def whichSceneAmIIn(self):
        return self._currentScene

    def createInteractionController(self):
        from controllers.interaction_controller import InteractionController
        return InteractionController(self)

    def createConversationController(self):
        return None

    def saveMyProgress(self):
        print("Spelet sparat!")

    def loadMyProgress(self):
        self._inventory = []
        print("Spelet laddat!")