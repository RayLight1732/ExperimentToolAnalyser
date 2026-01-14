from enum import Enum


class GraphType(Enum):
    """グラフの種類を定義"""

    SPAGHETTI = "spaghetti"

    def __str__(self):
        return self.value
