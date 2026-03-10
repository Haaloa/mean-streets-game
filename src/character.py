class CharacterResponse:
    """A response from a character."""

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class ConversationRecord:
    """Records that a conversation took place (used by GamePlot)."""

    def __init__(self, char_id, stage_id):
        self.character_id = char_id
        self.stage_id = stage_id


class Character:
    """
    A character in the game that the player can talk to.
    Responds to keywords and can give the player an item.
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self._responses = {}
        self._default_msg = f"{self.name} looks at you without saying a word."
        self._gift = None

    def add_response(self, keyword, reply):
        """Register a response for a given keyword."""
        keyword = keyword.lower()
        if keyword not in self._responses:
            self._responses[keyword] = []
        self._responses[keyword].append(reply)

    def set_gift_object(self, obj):
        """Set the item this character can give to the player."""
        self._gift = obj

    def handle_query(self, query, stage):
        """Answer the player's query based on keywords."""
        query = query.lower()
        for keyword, replies in self._responses.items():
            if keyword in query:
                return CharacterResponse(replies[0])
        return CharacterResponse(self._default_msg)

    def end_conversation(self, stage):
        return ConversationRecord(self.name, stage.stage_id)

    def create_game_object(self, stage):
        """Give the player the registered gift item."""
        return self._gift


class CharacterInterface:
    """
    Manages the connection between CharacterInteractionController and an active Character.
    """

    def __init__(self):
        self._char = None

    def connect(self, character):
        self._char = character

    def disconnect(self):
        self._char = None

    def send_query(self, query, stage):
        if self._char is None:
            return CharacterResponse("There is no one to talk to.")
        return self._char.handle_query(query, stage)

    @property
    def is_connected(self):
        return self._char is not None

    @property
    def active_character(self):
        return self._char
