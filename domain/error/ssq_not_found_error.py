class SSQNotFoundError(Exception):
    def __init__(self, path: str):
        super().__init__(f"SSQ not found or empty: {path}")
        self.path = path