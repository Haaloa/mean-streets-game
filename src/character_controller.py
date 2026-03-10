from src.character import CharacterInterface
from src.event_manager import EventManager


class CharacterInteractionController:
    """
    Use Case Controller for 'Interact with Character'.
    Handles the full conversation flow: start -> query -> receive item -> end.
    """

    def __init__(self, world_service, game_plot, inventory):
        self._world_service = world_service
        self._game_plot = game_plot
        self._inventory = inventory
        self._interface = CharacterInterface()

    def initiate_conversation(self, character_name):
        """Start a conversation with a character in the active scene."""
        scene = self._world_service.get_active_scene()
        if scene is None:
            return False

        for character in scene.get_characters():
            if character.name.lower() == character_name.lower():
                self._interface.connect(character)
                return True

        return False

    def send_query(self, query):
        """Send a message to the character and receive a response."""
        stage = self._game_plot.get_current_stage()
        response = self._interface.send_query(query, stage)

        # Trigger events via Singleton (EventManager)
        if self._interface.active_character:
            em = EventManager.getSharedInstance()
            char_name = self._interface.active_character.name.lower()
            em.triggerEventsFor(f"talk_{char_name}")

        return response

    def accept_game_object(self):
        """Receive an item from the character - added to inventory."""
        if not self._interface.is_connected:
            return None

        character = self._interface.active_character
        stage = self._game_plot.get_current_stage()
        obj = character.create_game_object(stage)

        if obj:
            self._inventory.add_object(obj)
            return obj.name

        return None

    def end_conversation(self):
        """End the conversation and save a conversation record."""
        if not self._interface.is_connected:
            return

        character = self._interface.active_character
        stage = self._game_plot.get_current_stage()
        record = character.end_conversation(stage)
        self._game_plot.add_conversation_record(record)
        self._interface.disconnect()

    @property
    def is_in_conversation(self):
        return self._interface.is_connected
