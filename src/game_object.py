class GameObject:
    """
    Context class in the Strategy Pattern.
    Holds a list of strategies and delegates interactions to them.
    """

    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.is_on = False
        self._strategies = []
        self._current_strategy = None

    def add_strategy(self, strategy):
        """Add an interaction strategy to this object."""
        self._strategies.append(strategy)

    def what_can_i_do(self):
        """Return the list of available strategies (matches class diagram)."""
        return list(self._strategies)

    def change_how_to_interact(self, strategy):
        """Set the active strategy (matches class diagram)."""
        self._current_strategy = strategy

    def do_interaction(self):
        """Execute the selected interaction (matches class diagram)."""
        if self._current_strategy is None:
            return "No interaction selected."
        return self._current_strategy.interact(self)
