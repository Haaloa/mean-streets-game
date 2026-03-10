from src.scene import Scene
from src.inventory import Inventory
from src.world_service import WorldService
from src.game_plot import GamePlot
from src.event_manager import EventManager
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
    """
    Main controller for the game.
    Tracks game state and delegates to controllers (Use Case Controller Pattern).
    HIGH COHESION: Game only manages game state, not the details of each use case.
    """

    def __init__(self):
        self._inventory = Inventory()
        self._world_service = WorldService()
        self._game_plot = GamePlot()

        # Singleton - one EventManager for the entire game
        self._event_manager = EventManager.getSharedInstance()

        self._character_ctrl = CharacterInteractionController(
            self._world_service,
            self._game_plot,
            self._inventory,
        )

        self._setup_world()

    def _setup_world(self):
        """Build the game world with objects, characters and events."""

        # -- Scene --
        start_scene = Scene(
            name="Stortorget",
            description=(
                "You are standing at Stortorget in Karlskrona. "
                "The cobblestones are wet from last night's rain. "
                "A bronze statue stands in the centre of the square."
            ),
        )

        # -- Objects --
        statue = GameObject("statue", "A bronze statue of Karl XI on horseback. Looks very old.")
        statue.add_strategy(LookAtStrategy())
        statue.add_strategy(TasteItStrategy())

        phone = GameObject("phone", "A smartphone lying on the ground. The screen is cracked.")
        phone.add_strategy(LookAtStrategy())
        phone.add_strategy(PickItUpStrategy())
        phone.add_strategy(TurnItOnStrategy())
        phone.add_strategy(TurnItOffStrategy())

        bench = GameObject("bench", "A wooden bench in the park. Someone left a newspaper on it.")
        bench.add_strategy(LookAtStrategy())
        bench.add_strategy(MoveItStrategy())

        start_scene.add_object(statue)
        start_scene.add_object(phone)
        start_scene.add_object(bench)

        # -- Character --
        anna = Character(name="Anna", description="A nervous woman in a red coat.")
        anna.add_response("murder", "I saw someone running from the alley last night. I was too scared to look closely.")
        anna.add_response("phone", "That phone? I think it belonged to the victim. I saw him drop it.")
        anna.add_response("statue", "People meet here all the time. I saw two men arguing near the statue yesterday.")
        anna.add_response("hello", "Oh! You startled me. Are you from the police?")
        anna.add_response("clue", "Check the alley behind the bakery. I think they went that way.")

        clue_note = GameObject("clue note", "A crumpled piece of paper: 'Meet me at the pier. Midnight. -V'")
        clue_note.add_strategy(LookAtStrategy())
        clue_note.add_strategy(PickItUpStrategy())
        anna.set_gift_object(clue_note)

        start_scene.add_character(anna)

        # -- Inventory --
        notebook = GameObject("notebook", "Your detective notebook. Several pages are already filled in.")
        notebook.add_strategy(LookAtStrategy())
        notebook.add_strategy(OpenItStrategy())
        self._inventory.add_object(notebook)

        # -- Register scenes --
        self._world_service.register_scene(start_scene)
        self._world_service.register_scene(self._inventory)
        self._world_service.set_active_scene(start_scene)

        # -- Register events via EventManager (Singleton) --
        em = EventManager.getSharedInstance()
        em.scheduleEvent("interact_phone", "Clue: The phone may contain important information!")
        em.scheduleEvent("interact_statue", "You study the statue carefully...")
        em.scheduleEvent("talk_anna", "Anna seems to have more to say...")

    # -- Use case: Interact with Object --
    def which_scene_am_i_in(self):
        return self._world_service.get_active_scene()

    def set_scene(self, scene):
        """Used in tests to set a custom scene."""
        self._world_service.set_active_scene(scene)

    def create_interaction_controller(self):
        """Creates a new InteractionController (new instance per interaction = no state leak)."""
        return InteractionController(self)

    # -- Use case: Interact with Character --
    def initiate_conversation(self, character_name):
        return self._character_ctrl.initiate_conversation(character_name)

    def send_query(self, query):
        return self._character_ctrl.send_query(query)

    def accept_game_object(self):
        return self._character_ctrl.accept_game_object()

    def end_conversation(self):
        return self._character_ctrl.end_conversation()

    # -- Navigation --
    def go_to_scene(self, scene_name):
        for scene in self._world_service.get_all_scenes():
            if scene.name.lower() == scene_name.lower():
                self._world_service.set_active_scene(scene)
                return True
        return False

    def get_all_scenes(self):
        return self._world_service.get_all_scenes()

    # -- Properties --
    @property
    def inventory(self):
        return self._inventory

    @property
    def character_ctrl(self):
        return self._character_ctrl

    @property
    def game_plot(self):
        return self._game_plot
