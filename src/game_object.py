
class GameObject:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self._strategies = []
        self._current_strategy = None
        self.is_on = False

    def add_strategy(self, strategy):
        self._strategies.append(strategy)

    def add_interaction(self, strategy):
        self.add_strategy(strategy)

    def what_can_i_do(self):
        return list(self._strategies)

    def change_how_to_interact(self, strategy):
        self._current_strategy = strategy

    def do_interaction(self):
        if self._current_strategy is None:
            return "No interaction selected."
        return self._current_strategy.interact(self)
    
# class GameObject:
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description
#         self._strategies = []
#         self._current_strategy = None
#         self.is_on = False

#     def add_strategy(self, strategy):
#         self._strategies.append(strategy)

#     def what_can_i_do(self):
#         return list(self._strategies)

#     def change_how_to_interact(self, strategy):
#         self._current_strategy = strategy

#     def do_interaction(self):
#         if self._current_strategy is None:
#             return "No interaction selected."
#         return self._current_strategy.do_it(self)
