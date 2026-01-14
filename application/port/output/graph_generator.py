from abc import ABC, abstractmethod
from typing import Type, Optional
from domain.value.grouped_value import GroupedValue
from application.model.graph_type import GraphType
from application.model.graph_options import GraphOptions


# TODO 暗黙的にpngを想定している
class GraphGenerator(ABC):
    """グラフ生成の抽象インターフェース"""

    @abstractmethod
    def generate(
        self,
        title: str,
        data: GroupedValue,
        option: GraphOptions,
    ) -> bytes:
        """
        Returns:
            生成されたグラフの画像データ
        """
        pass

    @abstractmethod
    def supported_type(self) -> GraphType:
        """サポートするグラフタイプを返す"""
        pass
