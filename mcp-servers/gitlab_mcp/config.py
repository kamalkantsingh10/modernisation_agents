import os
import yaml
from pathlib import Path


def _find_project_root() -> Path:
    if root := os.environ.get("BMAD_PROJECT_ROOT"):
        return Path(root)
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / "config.yaml").exists():
            return parent
    raise RuntimeError(
        "config.yaml not found. Set BMAD_PROJECT_ROOT env var or run from project directory."
    )


def load_config() -> dict:
    config_path = _find_project_root() / "config.yaml"
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise RuntimeError(f"config.yaml is malformed: {e}") from e
