from enum import Enum


class GraphType(Enum):
    """グラフの種類を定義"""

    SPAGHETTI = "spaghetti"
    BOX_PLOT = "box_plot"
    ERROR_BAR ="error_bar"

    def __str__(self):
        return self.value
