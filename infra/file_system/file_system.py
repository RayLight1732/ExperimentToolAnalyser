from abc import ABC, abstractmethod
from typing import List,Generator
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