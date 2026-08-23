from pathlib import Path


def search(notes_dir: Path, keywords: list[str]) -> list[dict]:
    """按关键词在 notes/ 下检索，返回按相关度排序的命中文档列表。"""
    kws = [k.lower() for k in keywords if k.strip()]
    results: list[dict] = []
    if not notes_dir.exists() or not kws:
        return results
    for path in sorted(notes_dir.rglob("*.md")):
        rel = path.relative_to(notes_dir).as_posix()
        text = path.read_text(encoding="utf-8")
        low = text.lower()
        matched = [k for k in kws if k in low]
        if not matched:
            continue
        snippets: list[tuple[int, str]] = []
        for line_no, line in enumerate(text.splitlines(), 1):
            ll = line.lower()
            if any(k in ll for k in kws):
                snippets.append((line_no, line.strip()))
        total_hits = sum(low.count(k) for k in kws)
        results.append(
            {
                "path": rel,
                "matched": matched,
                "total_hits": total_hits,
                "snippets": snippets,
            }
        )
    results.sort(key=lambda r: (-len(r["matched"]), -r["total_hits"], r["path"]))
    return results
