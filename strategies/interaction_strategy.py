from abc import ABC, abstractmethod


class InteractionStrategy(ABC):
    """Abstrakt basklass för alla interaktionsstrategier."""

    @abstractmethod
    def do_it(self, game_object, game, options):
        """
        Utför interaktionen på ett GameObject.

        game_object = objektet som spelaren interagerar med
        game = spelet, om strategin behöver komma åt game state
        options = extra val, t.ex. riktning för Move
        """
        pass

    def need_more_info(self):
        """Returnerar True om strategin behöver extra input."""
        return False

    def ask_for_more_info(self):
        """Returnerar en fråga om extra input behövs."""
        return ""