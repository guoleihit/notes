import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    base_url: str
    api_key: str
    model: str


def _load_env_file(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip()
    return result


def load_config(project_root: Path) -> Config:
    env = _load_env_file(project_root / ".env")
    env = {**env, **os.environ}
    return Config(
        base_url=env.get("KB_LLM_BASE_URL", ""),
        api_key=env.get("KB_LLM_API_KEY", ""),
        model=env.get("KB_LLM_MODEL", "glm-5.2"),
    )
