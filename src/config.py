from __future__ import annotations
from pathlib import Path
import yaml


def load_config(config_path: str = "config/default.yaml") -> dict:
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)