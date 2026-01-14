from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
from .graph_type import GraphType


@dataclass
class GraphData(ABC):
    """グラフデータの基底クラス"""

    id: str
    type: GraphType
    title: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換（永続化用）"""
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
        }
