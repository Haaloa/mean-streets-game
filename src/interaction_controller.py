from src.event_manager import EventManager


class InteractionController:
    """
    Use Case Controller for 'Interact with Object'.
    Handles the full flow: select object -> select interaction -> perform.
    Matches class diagram: pick_game_object, choose_interaction,
    provide_options, perform_interaction, cancel_interaction.
    """

    def __init__(self, game):
        self._game = game
        self._selected_object = None
        self._selected_strategy = None

    def pick_game_object(self, object_name):
        """Step 1: Select which object the player wants to interact with."""
        scene = self._game.which_scene_am_i_in()
        if scene is None:
            return None

        obj = scene.find_object(object_name)
        if obj is None:
            return None

        self._selected_object = obj
        self._selected_strategy = None  # reset strategy on new selection
        return obj

    def get_interaction_types(self):
        """Return a list of available interaction names for the selected object."""
        if self._selected_object is None:
            return []
        return [
            type(strategy).__name__
            for strategy in self._selected_object.what_can_i_do()
        ]

    def choose_interaction(self, interaction_type):
        """Step 2: Select which interaction to perform."""
        if self._selected_object is None:
            return False

        for strategy in self._selected_object.what_can_i_do():
            if strategy.__class__.__name__ == interaction_type:
                self._selected_strategy = strategy
                self._selected_object.change_how_to_interact(strategy)
                return True

        return False

    def provide_options(self, user_input):
        """Step 3 (optional): Provide extra information, e.g. direction for Move."""
        if self._selected_strategy is None:
            return False

        if self._selected_strategy.needs_options():
            self._selected_strategy.set_options(user_input)
            return True

        return False

    def perform_interaction(self):
        """Step 4: Execute the selected interaction via GameObject (Strategy Pattern)."""
        if self._selected_object is None or self._selected_strategy is None:
            return "No interaction to perform."

        # Delegate to GameObject which delegates to Strategy (matches class diagram)
        result = self._selected_object.do_interaction()

        # Trigger events via Singleton (EventManager)
        em = EventManager.getSharedInstance()
        triggered = em.triggerEventsFor(f"interact_{self._selected_object.name}")
        if triggered:
            result += f"\n  [{triggered[0]}]"

        return result

    def cancel_interaction(self):
        """Cancel the current interaction and reset state."""
        self._selected_object = None
        self._selected_strategy = None
