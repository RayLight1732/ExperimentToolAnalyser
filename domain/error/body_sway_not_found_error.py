class BodySwayNotFoundError(Exception):
    def __init__(self, path: str):
        super().__init__(f"BodySway not found or empty: {path}")
        self.path = path
