from abc import ABC, abstractmethod

class InteractionStrategy(ABC):
    @abstractmethod
    def do_it(self, game_object, game, options):
        pass
    
    @abstractmethod
    def need_more_info(self):
        pass
    
    def ask_for_more_info(self):
        return ""
