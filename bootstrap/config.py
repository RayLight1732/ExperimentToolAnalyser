from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Set
from usecase.service.operation_contract import (
    ValidOperations,
    ValueType,
    CalculationType,
)
import yaml


@dataclass(frozen=True)
class Config:
    working_dir: str
    valid_operations: ValidOperations = ValidOperations({})


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
        valid_operations = _get_valid_operations(data["valid_operations"])
        return Config(working_dir=working_dir, valid_operations=valid_operations)
    except KeyError as e:
        raise ValueError(f"Missing required config key: {e}") from e


def _get_valid_operations(data: Any) -> ValidOperations:
    if not isinstance(data, dict):
        raise ValueError("Invalid valid_operations format")

    value: Dict[ValueType, Set[CalculationType]] = {}
    for key, calc_list in data.items():
        try:
            value_type = ValueType(key)
            calculations = {CalculationType(calc) for calc in calc_list}
            value[value_type] = calculations
        except ValueError as e:
            raise ValueError(f"Invalid value type or calculation type: {e}") from e

    return ValidOperations(value)
