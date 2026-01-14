from application.port.output.graph_storage_output_port import GraphStorageOutputPort
from pathlib import Path


class FileGraphStorage(GraphStorageOutputPort):
    def __init__(self, working_dir) -> None:
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, data: bytes):
        """
        Parameters
        ----------
        name : str
            ファイル名（拡張子なし or あり どちらでもOK）
        data : bytes
            PNGなどのバイナリデータ

        Returns
        -------
        Path
            保存されたファイルのパス
        """

        # 拡張子が無ければ .png を付ける
        if not name.lower().endswith(".png"):
            name = f"{name}.png"

        path = self.working_dir / name

        # バイナリとして安全に書き込み
        with open(path, "wb") as f:
            f.write(data)
