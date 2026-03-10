
from abc import ABC, abstractmethod


class InteractionStrategy(ABC):
    @abstractmethod
    def interact(self, obj):
        pass

    def needs_options(self):
        return False

    # Alias för klassdiagrammet
    def doIt(self, obj):
        return self.interact(obj)

    def needMoreInfo(self):
        return self.needs_options()

    def askForMoreInfo(self):
        return ""


class LookAtStrategy(InteractionStrategy):
    def interact(self, obj):
        extra = ""
        if hasattr(obj, "is_on"):
            extra = " It is currently " + ("on." if obj.is_on else "off.")
        return f"You look at the {obj.name}. {obj.description}{extra}"


class OpenItStrategy(InteractionStrategy):
    def interact(self, obj):
        return f"You open the {obj.name}."


class MoveItStrategy(InteractionStrategy):
    def __init__(self):
        self.options = ""

    def set_options(self, val):
        self.options = val

    def needs_options(self):
        return True

    def askForMoreInfo(self):
        return "Which direction?"

    # Alias för klassdiagrammet
    def setDirection(self, direction):
        self.set_options(direction)

    def interact(self, obj):
        direction = f" {self.options}" if self.options else ""
        return f"You move the {obj.name}{direction}."


class TurnItOnStrategy(InteractionStrategy):
    def interact(self, obj):
        obj.is_on = True
        return f"You turn on the {obj.name}."


class TurnItOffStrategy(InteractionStrategy):
    def interact(self, obj):
        obj.is_on = False
        return f"You turn off the {obj.name}."


class TasteItStrategy(InteractionStrategy):
    def interact(self, obj):
        return f"You taste the {obj.name}. Weird choice."


class PickItUpStrategy(InteractionStrategy):
    def interact(self, obj):
        return f"You pick up the {obj.name}."


class DropItStrategy(InteractionStrategy):
    def interact(self, obj):
        return f"You drop the {obj.name} on the ground."
    
# from abc import ABC, abstractmethod


# class InteractionStrategy(ABC):
#     @abstractmethod
#     def do_it(self, obj):
#         pass

#     @abstractmethod
#     def needs_more_info(self):
#         pass


# class LookAtStrategy(InteractionStrategy):
#     def do_it(self, obj):
#         extra = ""
#         if hasattr(obj, "is_on"):
#             extra = " It is currently " + ("on." if obj.is_on else "off.")
#         return f"You look at the {obj.name}. {obj.description}{extra}"

#     def needs_more_info(self):
#         return False


# class OpenItStrategy(InteractionStrategy):
#     def do_it(self, obj):
#         return f"You open the {obj.name}."

#     def needs_more_info(self):
#         return False


# class MoveItStrategy(InteractionStrategy):
#     def __init__(self):
#         self.options = ""

#     def set_options(self, val):
#         self.options = val

#     def do_it(self, obj):
#         dir = f" {self.options}" if self.options else ""
#         return f"You move the {obj.name}{dir}."

#     def needs_more_info(self):
#         return True


# class TurnItOnStrategy(InteractionStrategy):
#     def do_it(self, obj):
#         obj.is_on = True
#         return f"You turn on the {obj.name}."

#     def needs_more_info(self):
#         return False


# class TurnItOffStrategy(InteractionStrategy):
#     def do_it(self, obj):
#         obj.is_on = False
#         return f"You turn off the {obj.name}."

#     def needs_more_info(self):
#         return False


# class TasteItStrategy(InteractionStrategy):
#     def do_it(self, obj):
#         return f"You taste the {obj.name}. Weird choice."

#     def needs_more_info(self):
#         return False


# class PickItUpStrategy(InteractionStrategy):
#     def do_it(self, obj):
#         return f"You pick up the {obj.name}."

#     def needs_more_info(self):
#         return False


# class DropItStrategy(InteractionStrategy):
#     def do_it(self, obj):
#         return f"You drop the {obj.name} on the ground."

#     def needs_more_info(self):
#         return False
