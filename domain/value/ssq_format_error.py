class SSQFormatError(Exception):
    def __init__(self):
        super().__init__(f"SSQ format is invaid")