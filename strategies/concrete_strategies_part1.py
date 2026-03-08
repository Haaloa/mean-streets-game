from strategies.interaction_strategy import InteractionStrategy


class LookStrategy(InteractionStrategy):
    """Strategi för att titta på ett objekt."""

    def do_it(self, game_object, game, options):
        # Returnerar objektets namn och beskrivning
        return f"You look at the {game_object.name}. {game_object.description}"


class OpenStrategy(InteractionStrategy):
    """Strategi för att öppna ett objekt."""

    def do_it(self, game_object, game, options):
        # Kontrollera om objektet går att öppna
        if not game_object.can_open:
            return f"You cannot open the {game_object.name}."

        # Om objektet går att öppna visar vi innehållet
        return f"You open the {game_object.name} and find {game_object.contents}."


class MoveStrategy(InteractionStrategy):
    """Strategi för att flytta ett objekt. Kräver extra info, t.ex. riktning."""

    def do_it(self, game_object, game, options):
        # Kontrollera om objektet går att flytta
        if not game_object.can_move:
            return f"The {game_object.name} cannot be moved."

        # Hämta riktning från options
        direction = options.get("direction")

        if not direction:
            return f"You move the {game_object.name}."

        return f"You move the {game_object.name} {direction}."

    def need_more_info(self):
        # Move behöver extra info, till exempel left/right
        return True

    def ask_for_more_info(self):
        return "Which direction do you want to move it?"


class TurnOnStrategy(InteractionStrategy):
    """Strategi för att slå på ett objekt."""

    def do_it(self, game_object, game, options):
        # Kontrollera om objektet går att slå på
        if not game_object.can_turn_on:
            return f"You cannot turn on the {game_object.name}."

        # Om objektet redan är på
        if game_object.is_on:
            return f"The {game_object.name} is already on."

        # Ändra state
        game_object.is_on = True
        return f"You turn on the {game_object.name}."