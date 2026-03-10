from abc import ABC, abstractmethod


class InteractionStrategy(ABC):
    """
    Abstract base class for the Strategy Pattern.
    All concrete strategies must implement interact(obj).
    needs_options() returns True if the strategy requires extra input (e.g. direction).
    """

    @abstractmethod
    def interact(self, obj):
        pass

    def needs_options(self):
        return False


class LookAtStrategy(InteractionStrategy):
    """Look at an object - shows its description and current state."""

    def interact(self, obj):
        extra = ""
        if hasattr(obj, "is_on"):
            extra = " It is currently " + ("on." if obj.is_on else "off.")
        return f"You look at {obj.name}. {obj.description}{extra}"


class OpenItStrategy(InteractionStrategy):
    """Open an object."""

    def interact(self, obj):
        return f"You open {obj.name}."


class MoveItStrategy(InteractionStrategy):
    """Move an object - requires a direction as extra input."""

    def __init__(self):
        self._direction = ""

    def needs_options(self):
        return True

    def set_options(self, direction):
        self._direction = direction

    def interact(self, obj):
        direction = f" {self._direction}" if self._direction else ""
        return f"You move {obj.name}{direction}."


class TurnItOnStrategy(InteractionStrategy):
    """Turn on an object - sets is_on to True."""

    def interact(self, obj):
        obj.is_on = True
        return f"You turn on {obj.name}."


class TurnItOffStrategy(InteractionStrategy):
    """Turn off an object - sets is_on to False."""

    def interact(self, obj):
        obj.is_on = False
        return f"You turn off {obj.name}."


class TasteItStrategy(InteractionStrategy):
    """Taste an object."""

    def interact(self, obj):
        return f"You taste {obj.name}. An unusual choice."


class PickItUpStrategy(InteractionStrategy):
    """Pick up an object."""

    def interact(self, obj):
        return f"You pick up {obj.name}."


class DropItStrategy(InteractionStrategy):
    """Drop an object."""

    def interact(self, obj):
        return f"You drop {obj.name} on the ground."
