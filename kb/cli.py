import argparse
import re
import sys
from pathlib import Path

from openai import APIConnectionError, AuthenticationError, OpenAIError

from .config import load_config
from .grep import search
from .lint import run_lint
from .llm import LLM


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _extract_keywords(question: str) -> list[str]:
    parts = re.split(r"[\s,，。.?？!！、;；:：]+", question)
    seen: list[str] = []
    for p in parts:
        if len(p) >= 2 and p not in seen:
            seen.append(p)
    return seen


def cmd_grep(args, notes_dir: Path) -> int:
    results = search(notes_dir, args.keywords)
    if not results:
        print("没有找到匹配的笔记。")
        return 0
    for r in results:
        print(f"\n{r['path']}  (命中 {len(r['matched'])} 词, {r['total_hits']} 次)")
        for line_no, line in r["snippets"][:5]:
            print(f"  {line_no}: {line[:120]}")
    return 0


def cmd_ask(args, notes_dir: Path, llm: LLM) -> int:
    keywords = args.keywords if args.keywords else _extract_keywords(args.question)
    if not keywords:
        print("未能从问题中提取关键词，请用 -k 指定关键词。", file=sys.stderr)
        return 1
    results = search(notes_dir, keywords)
    if not results:
        print("没有找到相关笔记，无法基于笔记回答。")
        return 0
    top = results[: args.top]
    context_parts = []
    for r in top:
        text = (notes_dir / r["path"]).read_text(encoding="utf-8")
        context_parts.append(f"【{r['path']}】\n{text}")
    context = "\n\n".join(context_parts)
    try:
        answer = llm.answer(args.question, context)
    except AuthenticationError:
        print("API key 无效，请检查 .env 中的 KB_LLM_API_KEY。", file=sys.stderr)
        return 1
    except APIConnectionError:
        print("无法连接大模型服务，请检查 .env 中的 KB_LLM_BASE_URL。", file=sys.stderr)
        return 1
    except OpenAIError as e:
        print(f"问答失败：{e}", file=sys.stderr)
        return 1
    print(answer)
    return 0


def cmd_lint(args, notes_dir: Path, cache_dir: Path) -> int:
    report = run_lint(notes_dir, cache_dir / "lint.json", threshold=args.threshold)
    print(f"变更 {len(report['changed'])} 篇, 删除 {len(report['deleted'])} 篇")
    if report["suggestions"]:
        print("\n关联建议：")
        for p, related in report["suggestions"]:
            print(f"\n  {p} 可能相关：")
            for q, n in related[: args.top]:
                print(f"    - {q} (重叠 {n})")
    else:
        print("\n无新的关联建议。")
    if report["orphans"]:
        print("\n孤立笔记：")
        for p in report["orphans"]:
            print(f"  - {p}")
    return 0


def cmd_publish(args, root: Path) -> int:
    drafts_dir = root / "drafts"
    notes_dir = root / "notes"
    name = args.name if args.name.endswith(".md") else args.name + ".md"
    src = drafts_dir / name
    if not src.exists():
        print(f"草稿不存在：{src.relative_to(root)}", file=sys.stderr)
        return 1
    target_dir = notes_dir / args.to if args.to else notes_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    dst = target_dir / src.name
    if dst.exists():
        print(f"目标已存在，未覆盖：{dst.relative_to(root)}", file=sys.stderr)
        return 1
    src.rename(dst)
    print(f"已发布：{src.name} → {dst.relative_to(root)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(prog="kb", description="个人学习知识库")
    sub = parser.add_subparsers(dest="command", required=True)

    g = sub.add_parser("grep", help="关键词检索笔记")
    g.add_argument("keywords", nargs="+", help="一个或多个关键词")

    a = sub.add_parser("ask", help="检索命中笔记后交给大模型回答")
    a.add_argument("question", help="要问的问题")
    a.add_argument("-k", "--keywords", nargs="*", default=None, help="检索关键词（缺省时从问题中提取）")
    a.add_argument("-n", "--top", type=int, default=3, help="喂给大模型的笔记篇数")

    l = sub.add_parser("lint", help="按需整理知识库（关联建议与孤立笔记）")
    l.add_argument("--threshold", type=int, default=2, help="判定相关的特征重叠数")
    l.add_argument("-n", "--top", type=int, default=5, help="每篇笔记显示的关联条数")

    p = sub.add_parser("publish", help="把草稿从 drafts/ 发布到 notes/")
    p.add_argument("name", help="草稿文件名（可省略 .md）")
    p.add_argument("-t", "--to", default=None, help="发布到 notes/ 下的子目录")

    args = parser.parse_args(argv)
    root = project_root()
    notes_dir = root / "notes"
    cache_dir = root / ".kb_cache"

    if args.command == "grep":
        return cmd_grep(args, notes_dir)
    if args.command == "ask":
        config = load_config(root)
        if not config.api_key or not config.base_url:
            print("缺少 LLM 配置：请创建 .env 设置 KB_LLM_API_KEY 与 KB_LLM_BASE_URL。",
                  file=sys.stderr)
            return 1
        return cmd_ask(args, notes_dir, LLM(config))
    if args.command == "lint":
        return cmd_lint(args, notes_dir, cache_dir)
    if args.command == "publish":
        return cmd_publish(args, root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
