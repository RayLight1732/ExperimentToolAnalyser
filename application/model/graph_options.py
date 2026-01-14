from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True)
class GraphOptions:
    """グラフの共通オプション設定"""

    width: int = 800
    height: int = 600
    color_theme: str = "default"
    custom_options: Dict[str, Any] = field(default_factory=dict)
