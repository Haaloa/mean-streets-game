"""
GameObject.py - hala kod
Fungerar med zahra Game och InteractionController
"""


class GameObject:
    """En GameObject representerar ett objekt i spelet"""
    
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self._strategies = {}
        
        # Egenskaper
        self.can_open = False
        self.can_move = True
        self.can_turn_on = False
        self.can_turn_off = False
        self.can_taste = False
        self.can_pick_up = True
        
        # Data
        self.contents = "nothing"
        self.taste_description = ""
        self.is_on = False
    
    def add_strategy(self, strategy_name, strategy):
        """Lägg till en strategy till objektet"""
        self._strategies[strategy_name] = strategy
    
    def get_available_strategies(self):
        """Returnera lista av tillgängliga strategies"""
        return list(self._strategies.keys())
    
    def set_interaction_strategy(self, strategy_name, game):
        """Sätt vilken strategy som ska användas"""
        self._current_strategy_name = strategy_name
        self._current_game = game
    
    def execute_interaction(self, options=None):
        """Utför interaktionen"""
        if not hasattr(self, '_current_strategy_name'):
            return "Ingen interaktion vald"
        
        strategy = self._strategies.get(self._current_strategy_name)
        if strategy is None:
            return "Strategin finns inte"
        
        # Anropa strategins do_it metod
        return strategy.do_it(self, self._current_game, options or {})
    
    # === FACTORY METHODS (som static methods) ===
    
    @staticmethod
    def create_phone():
        """Skapar ett telefon-objekt"""
        phone = GameObject("phone", "A black rotary phone from the 1980s")
        phone.can_pick_up = True
        # Strategies läggs till av main programmet
        return phone
    
    @staticmethod
    def create_drawer():
        """Skapar en låda"""
        drawer = GameObject("drawer", "A wooden drawer with brass handles")
        drawer.can_open = True
        drawer.can_pick_up = False
        drawer.can_move = False
        drawer.contents = "a rusty key, an old photograph"
        return drawer
    
    @staticmethod
    def create_apple():
        """Skapar ett äpple"""
        apple = GameObject("apple", "A red, shiny apple")
        apple.can_taste = True
        apple.can_pick_up = True
        apple.taste_description = "Sweet and juicy!"
        return apple
    
    @staticmethod
    def create_lamp():
        """Skapar en lampa"""
        lamp = GameObject("lamp", "A desk lamp")
        lamp.can_turn_on = True
        lamp.can_turn_off = True
        lamp.can_pick_up = True
        lamp.is_on = False
        return lamp