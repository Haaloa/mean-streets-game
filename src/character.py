class CharacterResponse:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class ConversationRecord:
    def __init__(self, char_id, stage_id):
        self.character_id = char_id
        self.stage_id = stage_id


class Character:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.responses = {}
        self.default_msg = f"{self.name} looks at you blankly."
        self.gift = None

    def add_response(self, keyword, reply):
        keyword = keyword.lower()
        if keyword not in self.responses:
            self.responses[keyword] = []
        self.responses[keyword].append(reply)

    def set_gift_object(self, obj):
        self.gift = obj

    def handle_query(self, query, stage):
        query = query.lower()
        for keyword, replies in self.responses.items():
            if keyword in query:
                return CharacterResponse(replies[0])
        return CharacterResponse(self.default_msg)

    def end_conversation(self, stage):
        return ConversationRecord(self.name, stage.stage_id)

    def create_game_object(self, stage):
        return self.gift


class CharacterInterface:
    def __init__(self):
        self.char = None

    def connect(self, character):
        self.char = character

    def disconnect(self):
        self.char = None

    def send_query(self, query, stage):
        if self.char is None:
            return CharacterResponse("No one to talk to.")
        return self.char.handle_query(query, stage)

    @property
    def is_connected(self):
        return self.char is not None

    @property
    def active_character(self):
        return self.char



# from src.game_object import GameObject


# class CharacterResponse:
#     def __init__(self, text):
#         self.text = text

#     def __str__(self):
#         return self.text


# class ConversationRecord:
#     def __init__(self, char_id, stage_id):
#         self.character_id = char_id
#         self.stage_id = stage_id


# class Character:
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description
#         self.responses = {}
#         self.default_msg = f"{self.name} looks at you blankly."
#         self.gift = None

#     def add_response(self, keyword, reply):
#         kw = keyword.lower()
#         if kw not in self.responses:
#             self.responses[kw] = []
#         self.responses[kw].append(reply)

#     def set_gift_object(self, obj):
#         self.gift = obj

#     def handle_query(self, query, stage):
#         q = query.lower()
#         for kw, replies in self.responses.items():
#             if kw in q:
#                 return CharacterResponse(replies[0])
#         return CharacterResponse(self.default_msg)

#     def end_conversation(self, stage):
#         return ConversationRecord(self.name, stage.stage_id)

#     def create_game_object(self, stage):
#         return self.gift


# class CharacterInterface:
#     def __init__(self):
#         self.char = None

#     def connect(self, character):
#         self.char = character

#     def disconnect(self):
#         self.char = None

#     def send_query(self, query, stage):
#         if self.char is None:
#             return CharacterResponse("No one to talk to.")
#         return self.char.handle_query(query, stage)

#     @property
#     def is_connected(self):
#         return self.char is not None

#     @property
#     def active_character(self):
#         return self.char
