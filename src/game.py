from src.scene import Scene
from src.inventory import Inventory
from src.world_service import WorldService
from src.game_plot import GamePlot
from src.interaction_controller import InteractionController
from src.character_controller import CharacterInteractionController
from src.character import Character
from src.game_object import GameObject
from src.interaction_strategy import (
    LookAtStrategy, OpenItStrategy, MoveItStrategy,
    TurnItOnStrategy, TurnItOffStrategy, TasteItStrategy,
    PickItUpStrategy, DropItStrategy,
)


class Game:
    def __init__(self):
        self._inventory = Inventory()
        self._world_service = WorldService()
        self._game_plot = GamePlot()

        self._interaction_ctrl = InteractionController(
            self._world_service, self._inventory
        )
        self._character_ctrl = CharacterInteractionController(
            self._world_service, self._game_plot, self._inventory
        )

        self._setup_world()

    def _setup_world(self):
        startScene = Scene(
            name="Stortorget",
            description=(
                "You are standing at Stortorget in Karlskrona. "
                "The cobblestones are slick from last night's rain. "
                "A bronze statue stands in the center of the square."
            )
        )

        statue = GameObject("statue", "A bronze statue of Karl XI on horseback. Looks very old.")
        statue.add_strategy(LookAtStrategy())
        statue.add_strategy(TasteItStrategy())

        phone = GameObject("phone", "A smartphone lying on the ground. The screen is cracked.")
        phone.add_strategy(LookAtStrategy())
        phone.add_strategy(PickItUpStrategy())
        phone.add_strategy(TurnItOnStrategy())
        phone.add_strategy(TurnItOffStrategy())

        bench = GameObject("bench", "A wooden park bench. Someone left a newspaper on it.")
        bench.add_strategy(LookAtStrategy())
        bench.add_strategy(MoveItStrategy())

        startScene.add_object(statue)
        startScene.add_object(phone)
        startScene.add_object(bench)

        witness = Character(
            name="Anna",
            description="A nervous-looking woman in a red coat."
        )
        witness.add_response("murder", "I saw someone running from the alley last night. I was too scared to look closely.")
        witness.add_response("phone", "That phone? I think it belonged to the victim. I saw him drop it.")
        witness.add_response("statue", "People meet here all the time. I saw two men arguing near it yesterday.")
        witness.add_response("hello", "Oh! You scared me. Are you with the police?")
        witness.add_response("who", "My name is Anna. I live just around the corner.")
        witness.add_response("clue", "Check the alley behind the bakery. I think they went that way.")

        clue_note = GameObject("clue note", "A crumpled note: 'Meet me at the docks. Midnight. -V'")
        clue_note.add_strategy(LookAtStrategy())
        clue_note.add_strategy(PickItUpStrategy())
        witness.set_gift_object(clue_note)

        startScene.add_character(witness)

        notebook = GameObject("notebook", "Your detective's notebook. Several pages already filled.")
        notebook.add_strategy(LookAtStrategy())
        notebook.add_strategy(OpenItStrategy())
        self._inventory.add_object(notebook)

        self._world_service.register_scene(startScene)
        self._world_service.register_scene(self._inventory)
        self._world_service.set_active_scene(startScene)

    def which_scene_am_i_in(self):
        return self._world_service.get_active_scene()

    def go_to_scene(self, scene_name):
        for scene in self._world_service.get_all_scenes():
            if scene.name.lower() == scene_name.lower():
                self._world_service.set_active_scene(scene)
                return True
        return False

    def get_all_scenes(self):
        return self._world_service.get_all_scenes()

    def create_interaction_controller(self):
        return self._interaction_ctrl

    def initiate_conversation(self, character_name):
        return self._character_ctrl.initiate_conversation(character_name)

    def send_query(self, query):
        return self._character_ctrl.send_query(query)

    def accept_game_object(self):
        return self._character_ctrl.accept_game_object()

    def end_conversation(self):
        return self._character_ctrl.end_conversation()

    @property
    def inventory(self):
        return self._inventory

    @property
    def interaction_ctrl(self):
        return self._interaction_ctrl

    @property
    def character_ctrl(self):
        return self._character_ctrl

    @property
    def game_plot(self):
        return self._game_plot
