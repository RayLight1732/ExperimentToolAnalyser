from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Set
import yaml


@dataclass(frozen=True)
class Config:
    working_dir: str


def load_config(path: Optional[str] = None) -> Config:
    path = path or ".config.yml"
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        data: Dict[str, Any] = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("Invalid config format")

    try:
        working_dir = data["working_dir"]
        return Config(working_dir=working_dir)
    except KeyError as e:
        raise ValueError(f"Missing required config key: {e}") from e
