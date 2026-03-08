class InteractionController:

    def __init__(self, game):
        self._game = game
        self._selectedObject = None
        self._selectedStrategy = None
        self._options = {}

    def pickGameObject(self, objectName):
        scene = self._game.whichSceneAmIIn()
        obj = scene.get_object(objectName)
        if obj is None:
            print(f"Hittade inget objekt som heter '{objectName}'.")
            return False
        self._selectedObject = obj
        print(f"Du valde: {obj.name}")
        return True

    def chooseInteraction(self, interactionType):
        if self._selectedObject is None:
            print("Du måste välja ett objekt först!")
            return False
        tillgangliga = self._selectedObject.get_available_strategies()
        if interactionType not in tillgangliga:
            print(f"'{interactionType}' går inte att göra med '{self._selectedObject.name}'.")
            return False
        self._selectedStrategy = interactionType
        print(f"Du valde interaktion: {interactionType}")
        return True

    def provideOptions(self, options):
        self._options = options

    def performInteraction(self):
        if self._selectedObject is None:
            return None
        if self._selectedStrategy is None:
            return None
        self._selectedObject.set_interaction_strategy(self._selectedStrategy, self._game)
        result = self._selectedObject.execute_interaction(self._options)
        self._selectedStrategy = None
        self._options = {}
        return result

    def cancelInteraction(self):
        self._selectedObject = None
        self._selectedStrategy = None
        self._options = {}