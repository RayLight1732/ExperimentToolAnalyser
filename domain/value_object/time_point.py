from enum import Enum, auto

class TimePoint(Enum):
    BEFORE = ("before")
    AFTER = ("after")

    def __init__(self,display_name:str):
        super().__init__()
        self.display_name = display_name