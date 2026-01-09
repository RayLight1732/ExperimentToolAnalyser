from dataclasses import dataclass
from application.model.processing_category import ProcessingCategory

@dataclass(frozen=True)
class ProgressPhase:
    name:str
    category:ProcessingCategory

    def __str__(self) -> str:
        return f"{self.category}:{self.name}"