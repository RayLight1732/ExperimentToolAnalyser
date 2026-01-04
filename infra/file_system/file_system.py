from abc import ABC, abstractmethod
from typing import List, Generator
import os
import csv


class FileSystem(ABC):
    @abstractmethod
    def listdir(self, path: str) -> List[str]:
        pass

    @abstractmethod
    def isdir(self, path: str) -> bool:
        pass

    @abstractmethod
    def load_csv(self, path: str) -> Generator[List[str], None, None]:
        pass

    @abstractmethod
    def save_csv(self, path: str, data: Generator[List[str], None, None]):
        pass


class OSFileSystem(FileSystem):
    def listdir(self, path: str) -> list[str]:
        return os.listdir(path)

    def isdir(self, path: str) -> bool:
        return os.path.isdir(path)

    def load_csv(self, path: str) -> Generator[List[str], None, None]:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                yield row

    def save_csv(self, path: str, data: Generator[List[str], None, None]):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)
