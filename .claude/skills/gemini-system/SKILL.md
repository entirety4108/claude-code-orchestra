---
name: gemini-system
description: |
  PROACTIVELY consult Gemini CLI for multimodal file processing and external
  web research. MUST use Gemini when PDF, video, audio, or image files need
  analysis — pass the file to Gemini with specific extraction instructions.
  Also use for: Google Search grounding, latest docs, library research.
  NOTE: Codebase analysis is handled by Claude directly (1M context).
  Auto-triggers: file extensions .pdf, .mp4, .mov, .mp3, .wav, .m4a.
  Explicit triggers: "research", "investigate", "analyze", "latest docs".
metadata:
  short-description: Claude Code ↔ Gemini CLI collaboration (multimodal & external research)
---

# Gemini System — Multimodal File Processing & External Research

**Gemini CLI is your specialist for multimodal file processing and external information.**

> **詳細ルール**: `.claude/rules/gemini-delegation.md`

## Two Use Cases

### 1. マルチモーダルファイル処理（MUST — 自動委譲）

**PDF、動画、音声、画像ファイルの内容理解が必要な場合、必ず Gemini にファイルを渡す。**

```bash
gemini -p "{抽出したい情報を具体的に指示}" < /path/to/file 2>/dev/null
```

| 対象 | 拡張子 |
|------|--------|
| PDF | `.pdf` |
| 動画 | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` |
| 音声 | `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` |
| 画像（高度分析） | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg` |

> スクリーンショットの単純確認は Claude の Read ツールで直接可能。
> 図表・ダイアグラムの詳細分析が必要な場合に Gemini を使う。

### 2. 外部情報の取得（状況に応じて）

```bash
gemini -p "{research question}" 2>/dev/null
```

## Role (Opus 4.6)

| Task | Agent |
|------|-------|
| **コードベース分析** | **Claude 直接** (1M context) |
| **マルチモーダル (PDF/動画/音声/画像)** | **Gemini（必須）** |
| **外部ライブラリ調査** | Gemini (Google Search) |
| **最新ドキュメント検索** | Gemini (Google Search) |
| **設計判断** | Codex |
| **デバッグ** | Codex |

## When to Consult

### MUST（自動委譲 — ユーザー指示不要）

- **マルチモーダルファイル処理** — PDF, 動画, 音声, 画像（高度分析）がタスクに関わる場合

### SHOULD（状況に応じて）

| Situation | Trigger Examples |
|-----------|------------------|
| **External research** | 「調べて」「リサーチ」 / "Research" "Investigate" |
| **Library docs** | 「ライブラリ」「ドキュメント」 / "Library" "Docs" |
| **Latest information** | 「最新の〜」「2026年の〜」 / "Latest" "Current" |

## When NOT to Consult

- **コードベース分析** → Claude が 1M コンテキストで直接読む
- **スクリーンショットの単純確認** → Claude の Read ツールで直接可能
- Design decisions → Codex
- Debugging → Codex
- Code implementation → Claude

## How to Consult

### In Agent Teams (Preferred for /startproject)

Researcher Teammate が Gemini を直接呼び出し、Architect Teammate と双方向通信する。

```
/startproject 内の Phase 2 で、Researcher Teammate として Gemini を活用:
- 外部情報の収集 → Gemini に調査依頼
- Architect からの追加調査依頼に対応
- 調査結果を .claude/docs/research/ に保存
```

### Subagent Pattern (Standalone research)

```
Task tool parameters:
- subagent_type: "general-purpose"
- run_in_background: true (optional, for parallel work)
- prompt: |
    Research: {topic}

    gemini -p "{research question}" 2>/dev/null

    Save full output to: .claude/docs/research/{topic}.md
    Return CONCISE summary (5-7 bullet points).
```

### Direct Call (Short Questions Only)

```bash
gemini -p "Brief question" 2>/dev/null
```

### CLI Options Reference

```bash
# External research (primary use case)
gemini -p "{question}" 2>/dev/null

# Multimodal (PDF/video/audio)
gemini -p "{prompt}" < /path/to/file.pdf 2>/dev/null

# JSON output
gemini -p "{question}" --output-format json 2>/dev/null
```

> **Note**: `--include-directories .` is no longer needed for codebase analysis — Claude handles this directly with 1M context.

## Language Protocol

1. Ask Gemini in **English**
2. Receive response in **English**
3. Synthesize and apply findings
4. Report to user in **Japanese**

## Output Location

Save Gemini research results to:
```
.claude/docs/research/{topic}.md
.claude/docs/libraries/{library}.md
```

This allows Claude and Codex to reference the research later.

## Task Templates

### Library Research

```bash
gemini -p "Research best practices for {library} in Python 2026.
Include:
- Installation and setup
- Common patterns and anti-patterns
- Known limitations and constraints
- Performance considerations
- Security concerns
- Code examples" 2>/dev/null
```

### Latest Documentation Lookup

```bash
gemini -p "Find the latest documentation for {library/API}.
Include:
- Current stable version
- Breaking changes from previous version
- New features
- Migration guide if applicable" 2>/dev/null
```

### Multimodal Analysis

```bash
# Video
gemini -p "Analyze video: main concepts, key points, timestamps" < tutorial.mp4 2>/dev/null

# PDF
gemini -p "Extract: API specs, examples, constraints" < api-docs.pdf 2>/dev/null

# Audio
gemini -p "Transcribe and summarize: decisions, action items" < meeting.mp3 2>/dev/null
```

See also: `references/lib-research-task.md`

## Integration with Codex

| Workflow | Steps |
|----------|-------|
| **New feature** | Gemini research → Codex design review |
| **Library choice** | Gemini comparison → Codex decision |
| **/startproject** | Agent Teams: Researcher (Gemini) ↔ Architect (Codex) |

## Why Gemini?

- **Google Search**: Latest information, official docs, best practices
- **Multimodal**: Native PDF/video/audio processing
- **Web grounding**: Verified facts with source URLs
- **Shared context**: Results saved for Claude/Codex to reference
