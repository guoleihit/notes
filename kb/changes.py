import hashlib
from pathlib import Path


def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scan_notes(notes_dir: Path) -> dict[str, str]:
    """返回 notes/ 下所有 Markdown 的相对路径 -> 内容 hash。"""
    result: dict[str, str] = {}
    if not notes_dir.exists():
        return result
    for path in sorted(notes_dir.rglob("*.md")):
        rel = path.relative_to(notes_dir).as_posix()
        result[rel] = content_hash(path)
    return result
