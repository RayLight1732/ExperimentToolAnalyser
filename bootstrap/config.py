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
    iqr_factor:float
    sensored:List[str]

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
        iqr_factor = float(data["IQR_factor"])
        sensored = data.get("sensored",[])
        
        return Config(working_dir=working_dir, save_dir=save_dir,iqr_factor=iqr_factor,sensored=sensored)
    
    except KeyError as e:
        raise ValueError(f"Missing required config key: {e}") from e
