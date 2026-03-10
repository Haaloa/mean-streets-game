class GameStage:
    def __init__(self, stage_id, description):
        self.stage_id = stage_id
        self.description = description


class GamePlot:
    def __init__(self):
        self._current_stage = GameStage(1, "Investigate the murder at Stortorget")
        self._conversation_records = []

    def get_current_stage(self):
        return self._current_stage

    def add_conversation_record(self, record):
        self._conversation_records.append(record)




# class GameStage:
#     def __init__(self, stage_id, description):
#         self.stage_id = stage_id
#         self.description = description


# class GamePlot:
#     def __init__(self):
#         self._current_stage = GameStage(1, "Investigate the murder at Stortorget")
#         self._conversation_records = []

#     def get_current_stage(self):
#         return self._current_stage

#     def add_conversation_record(self, record):
#         self._conversation_records.append(record)
