from strategies.interaction_strategy import InteractionStrategy

class TurnOffStrategy(InteractionStrategy):
    def do_it(self, game_object, game, options):
        if not hasattr(game_object, 'can_turn_off') or not game_object.can_turn_off:
            return f"You can't turn off the {game_object.name}."
        game_object.is_on = False
        return f"You turn off the {game_object.name}."
    
    def need_more_info(self):
        return False

class TasteStrategy(InteractionStrategy):
    def do_it(self, game_object, game, options):
        if not hasattr(game_object, 'can_taste') or not game_object.can_taste:
            return f"You probably shouldn't taste the {game_object.name}."
        if hasattr(game_object, 'taste_description') and game_object.taste_description:
            return f"You taste the {game_object.name}. {game_object.taste_description}"
        return f"You taste the {game_object.name}. It doesn't taste like much."
    
    def need_more_info(self):
        return False

class PickItUpStrategy(InteractionStrategy):
    def do_it(self, game_object, game, options):
        if not hasattr(game_object, 'can_pick_up') or not game_object.can_pick_up:
            return f"You can't pick up the {game_object.name}."
        if hasattr(game, '_inventory'):
            game._inventory.append(game_object)
        scene = game.whichSceneAmIIn()
        if scene and hasattr(scene, 'remove_object'):
            scene.remove_object(game_object)
        return f"You pick up the {game_object.name} and put it in your bag."
    
    def need_more_info(self):
        return False

class DropItStrategy(InteractionStrategy):
    def do_it(self, game_object, game, options):
        if hasattr(game, '_inventory') and game_object in game._inventory:
            game._inventory.remove(game_object)
        scene = game.whichSceneAmIIn()
        if scene and hasattr(scene, 'add_object'):
            scene.add_object(game_object)
        return f"You drop the {game_object.name} on the ground."
    
    def need_more_info(self):
        return False
