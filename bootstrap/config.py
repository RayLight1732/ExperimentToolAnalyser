from ast import List
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Set,List
import yaml
from domain.value.condition import Condition,Position,CoolingMode
from domain.value.condition import Condition,Position,CoolingMode

@dataclass(frozen=True)
class Config:
    working_dir: str
    save_dir: str
    required_conditions: Set[Condition]

def _load_required_conditions(raw_conditions:List[Any])->Set[Condition]:
    conditions: Set[Condition] = set()

    for i, item in enumerate(raw_conditions):
        if not isinstance(item, dict):
            raise ValueError(f"Condition #{i} must be a mapping")

        try:
            mode = CoolingMode[item["mode"]]
        except KeyError as e:
            raise ValueError(f"Invalid or missing mode in condition #{i}") from e

        position = None
        if "position" in item:
            try:
                position = Position[item["position"]]
            except KeyError as e:
                raise ValueError(
                    f"Invalid position in condition #{i}: {item['position']}"
                ) from e

        try:
            conditions.add(Condition(mode=mode, position=position))
        except ValueError as e:
            raise ValueError(f"Invalid condition #{i}: {e}") from e
    return conditions

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
        save_dir = data["save_dir"]

        raw_conditions = data["required_conditions"]
        if not isinstance(raw_conditions, list):
            raise ValueError("'required' must be a list")
        required_conditions = _load_required_conditions(raw_conditions)
        
        return Config(working_dir=working_dir, save_dir=save_dir,required_conditions=required_conditions)

        raw_conditions = data["required_conditions"]
        if not isinstance(raw_conditions, list):
            raise ValueError("'required' must be a list")
        required_conditions = _load_required_conditions(raw_conditions)
        
        return Config(working_dir=working_dir, save_dir=save_dir,required_conditions=required_conditions)
    except KeyError as e:
        raise ValueError(f"Missing required config key: {e}") from e
