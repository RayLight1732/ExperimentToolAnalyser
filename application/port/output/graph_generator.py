from abc import ABC, abstractmethod
from typing import Type
from application.model.graph_data import GraphData
from application.model.graph_type import GraphType
from application.model.graph_options import GraphOptions


class GraphGenerator(ABC):
    """グラフ生成の抽象インターフェース"""

    @abstractmethod
    def generate(self, data: GraphData, option: GraphOptions) -> bytes:
        """
        グラフを生成してバイナリデータを返す

        Args:
            data: グラフデータ（具体的な型は各実装で異なる）

        Returns:
            生成されたグラフの画像データ
        """
        pass

    @abstractmethod
    def supported_type(self) -> GraphType:
        """サポートするグラフタイプを返す"""
        pass

    @abstractmethod
    def expected_data_type(self) -> Type[GraphData]:
        """期待するデータ型を返す"""
        pass
