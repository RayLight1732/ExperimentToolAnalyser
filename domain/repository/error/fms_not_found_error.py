class FMSNotFoundError(Exception):
    def __init__(self, path: str):
        super().__init__(f"FMS not found or empty: {path}")
        self.path = path