from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True)
class GraphOption:
    """グラフのオプション設定"""

    width: int = 800
    height: int = 600
    x_label: str = ""
    y_label: str = ""
    color_theme: str = "default"
    custom_options: Dict[str, Any] = field(default_factory=dict)
