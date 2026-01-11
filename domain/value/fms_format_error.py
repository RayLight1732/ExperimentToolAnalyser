class FMSFormatError(Exception):
    def __init__(self):
        super().__init__(f"FMS format is invaid")