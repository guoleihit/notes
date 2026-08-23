import json
import re
from pathlib import Path

from .changes import scan_notes


def load_archive(archive_path: Path) -> dict:
    if archive_path.exists():
        try:
            return json.loads(archive_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_archive(archive_path: Path, archive: dict):
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_text(
        json.dumps(archive, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def extract_features(text: str, filename: str) -> set[str]:
    feats: set[str] = set()
    stem = Path(filename).stem
    for part in re.split(r"[-_\s]+", stem):
        if part:
            feats.add(part.lower())
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            t = re.sub(r"^#+\s*", "", s).strip()
            if t:
                feats.add(t.lower())
    for m in re.findall(r"[a-zA-Z][a-zA-Z0-9]{1,}", text):
        feats.add(m.lower())
    return feats


def linked_targets(text: str) -> set[str]:
    return {m.lower() for m in re.findall(r"\[\[([^\]]+)\]\]", text)}


def run_lint(notes_dir: Path, archive_path: Path, threshold: int = 2) -> dict:
    archive = load_archive(archive_path)
    disk = scan_notes(notes_dir)

    deleted = [p for p in archive if p not in disk]
    for p in deleted:
        archive.pop(p, None)

    docs: dict[str, dict] = {}
    for p, h in disk.items():
        text = (notes_dir / p).read_text(encoding="utf-8")
        docs[p] = {
            "hash": h,
            "features": extract_features(text, p),
            "linked": linked_targets(text),
        }

    changed = [p for p, h in disk.items() if archive.get(p, {}).get("hash") != h]

    suggestions: list[tuple[str, list[tuple[str, int]]]] = []
    orphans: list[str] = []
    for p in changed:
        feats = docs[p]["features"]
        linked = docs[p]["linked"]
        linked_stems = {Path(t).stem.lower() for t in linked}
        related: list[tuple[str, int]] = []
        for q, doc in docs.items():
            if q == p:
                continue
            q_stem = Path(q).stem.lower()
            if q_stem in linked_stems:
                continue
            overlap = feats & doc["features"]
            if len(overlap) >= threshold:
                related.append((q, len(overlap)))
        related.sort(key=lambda x: (-x[1], x[0]))
        archive[p] = {"hash": disk[p], "related": [r[0] for r in related]}
        if related:
            suggestions.append((p, related))
        else:
            orphans.append(p)

    save_archive(archive_path, archive)
    return {
        "changed": changed,
        "deleted": deleted,
        "suggestions": suggestions,
        "orphans": orphans,
    }
