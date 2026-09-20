# my-kb User Guide

A personal learning knowledge base: notes are plain-text Markdown, and **keyword search + LLM Q&A** replace heavy-handed categorization.

## The Idea in One Sentence

Just drop your notes into the `notes/` directory, organized however you like. Everything else (search, Q&A, finding connections) is handled by the `kb` command. No embeddings, no vector database, no extra API costs.

## Core Workflow: grep to Find, LLM to Answer

```
① Take notes          ② Search              ③ Ask / Organize
   │                     │                     │
   ▼                     ▼                     ▼
Write Markdown        kb grep "keyword"     kb ask "question"
under notes/,         (grep keyword hits)   (hit docs → GLM → answer)
organized by folder                         kb lint (find links/orphans)
```

**Why not "semantic search"?** Semantic search requires embeddings (extra API cost + a powerful local machine). Keyword matching via grep is free, explainable, and real-time. The trade-off is missing results when wording differs, which is offset by **good folder organization + clear naming**.

## One-Time Setup

1. Install Python 3.11+ and the dependencies:

   ```
   pip install -e .
   ```

2. Create a `.env` file in the project root (edit it if it already exists) and fill in your **OpenCode Go** API key (get one at [opencode.ai/auth](https://opencode.ai/auth)):

   ```
   KB_LLM_BASE_URL=https://opencode.ai/zen/go/v1
   KB_LLM_API_KEY=your Go key
   KB_LLM_MODEL=glm-5.2
   ```

   This reuses your existing Go subscription (the GLM chat model) at zero extra cost. To switch to another OpenAI-compatible service, just change these three lines (Zhipu, local Ollama, etc.).

## Daily Usage

### Taking Notes

Write Markdown under `notes/`, organized by folder (Obsidian is recommended — open the `notes/` directory as a vault). **Give files and titles clear names** — they are the key to grep search.

### Drafts and Publishing

Jot down ideas in `drafts/` first (excluded from grep/ask/lint), then publish when they're ready:

```
kb publish "temporary idea"           # move to notes/
kb publish "temporary idea" -t TopicA # move to notes/TopicA/
```

- The `.md` extension can be omitted from draft filenames
- Publishing refuses to overwrite a file with the same name at the destination
- The drafts folder lives in the same Obsidian vault as notes, so dragging and dropping works too

### Search: kb grep

```
kb grep vector search
```

Ranks by keyword hits and shows the matching notes and snippets:

```
vector-search.md  (2 words hit, 10 times)
  1: # Vector Search
  5: Convert text into high-dimensional vectors……
```

Notes matching more keywords rank higher; if nothing matches, it says so explicitly.

### Q&A: kb ask

```
kb ask "What is vector search and how does it differ from keyword search" -k vector search
```

Workflow: use the `-k` keywords to grep matching notes → feed the matched notes plus your question to GLM → return the answer.

- `-k` is optional; when omitted, words are extracted from the question automatically.
- `-n 3` controls how many notes are fed to the model (default 3).
- When no relevant notes are found, it says so instead of making things up.

### Organizing: kb lint

```
kb lint
```

Organizes the knowledge base on demand, outputting:

- **Link suggestions**: pairs of notes that are related in content but not yet linked (suggesting you add a `[[wiki link]]`)
- **Orphan notes**: notes that connect to nothing else

It is **incremental**: results are stored in `.kb_cache/lint.json`, and only new/changed notes are processed next time.

- `--threshold 2` sets the number of overlapping features required to count as related (default 2; lower is more sensitive and may produce more false positives).
- `-n 5` sets how many links are shown per note (default 5).

## Command Reference

| Command | Purpose |
|------|------|
| `kb grep "word1" "word2"` | Keyword search; lists matching documents and snippets |
| `kb ask "question" -k word1 word2` | Search hits → LLM answer |
| `kb lint` | Find link suggestions + orphan notes (incremental) |
| `kb publish "draft" -t subdir` | Publish a draft from drafts/ to notes/ |

## Project Structure

```
my-kb/
├── notes/        ← Official notes (plain Markdown; included in search/Q&A/lint; git-managed)
├── drafts/       ← Draft area (quick ideas; excluded from search; moves to notes/ once published)
├── kb/           ← Python code for search/Q&A/organizing/publishing
├── .kb_cache/    ← Cache (lint archive; safe to delete, rebuilt automatically)
├── .env          ← LLM config (contains keys; gitignored)
└── openspec/     ← Change management (can be ignored)
```

## FAQ

**Will I lose my notes?** No. Notes are plain-text Markdown under `notes/`, versioned with git. Deleting `.kb_cache/` does not affect notes; `kb lint` will rebuild the archive.

**What's the relationship between `kb grep` and `kb ask`?** `grep` is pure search (no LLM, free); `ask` is search + answer (uses Go's GLM, called on demand). When unsure about keywords, use `grep` first to scout.

**Want to switch LLMs?** Change the three lines in `.env`, e.g. to switch to local Ollama: `KB_LLM_BASE_URL=http://localhost:11434/v1` + the corresponding model name.

**Not accurate enough on connections?** Start with the zero-cost `kb lint`; if you need more accurate semantic connections later, embeddings can be introduced (the upgrade path is open).
