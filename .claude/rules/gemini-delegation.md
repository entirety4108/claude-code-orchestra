# Gemini Delegation Rule

**Gemini CLI is your external information and multimodal specialist.**

## Two Use Cases — これだけ覚えればOK

### Use Case 1: マルチモーダルファイル処理（MUST — 自動委譲）

**PDF、動画、画像、音声ファイルの内容を理解する必要がある場合、必ず Gemini に渡す。**

> Claude はテキストファイルとスクリーンショットは読めるが、PDF の中身の構造的読解、動画、音声は処理できない。
> これらのファイルが登場した時点で、Gemini への委譲は**必須**であり、ユーザーの指示を待つ必要はない。

**対象ファイル拡張子**:

| カテゴリ | 拡張子 |
|----------|--------|
| PDF | `.pdf` |
| 動画 | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` |
| 音声 | `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` |
| 画像（高度な分析） | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg` |

> **画像の補足**: スクリーンショットの単純な確認は Claude の Read ツールで直接可能。
> 図表・設計図・ダイアグラムの詳細分析や、画像内テキストの構造的抽出が必要な場合に Gemini を使う。

**実行方法**:

```bash
# PDF — 構造・内容の抽出
gemini -p "Extract: {what information to extract}" < /path/to/file.pdf 2>/dev/null

# 動画 — 要約・キーポイント・タイムスタンプ
gemini -p "Summarize: key concepts, decisions, timestamps" < /path/to/video.mp4 2>/dev/null

# 音声 — 文字起こし・要約
gemini -p "Transcribe and summarize: decisions, action items" < /path/to/audio.mp3 2>/dev/null

# 画像 — 図表・ダイアグラムの詳細分析
gemini -p "Analyze this diagram: components, relationships, data flow" < /path/to/diagram.png 2>/dev/null
```

**重要**: `-p` の後に「何を抽出してほしいか」を具体的に指示すること。ファイルを渡すだけでは不十分。

### Use Case 2: 外部情報の取得（状況に応じて）

**最新ドキュメント、ライブラリ調査、Web上の情報が必要な場合に Gemini を使う。**

```bash
gemini -p "{research question}" 2>/dev/null
```

---

## Role (Opus 4.6)

> Claude 自身が 1M トークンのコンテキストを持つため、コードベース分析は Claude が直接行う。
> Gemini の役割は「マルチモーダルファイル処理」と「外部情報取得」の2つに限定される。

| Task | Agent |
|------|-------|
| コードベース分析 | **Claude 直接** |
| マルチモーダル (PDF/動画/音声/画像) | **Gemini（必須）** |
| ライブラリ調査・最新ドキュメント | Gemini |
| 設計判断 | Codex |

## Context Management

| 状況 | 推奨方法 |
|------|----------|
| 短い質問・短い回答 | 直接呼び出しOK |
| マルチモーダル処理 | サブエージェント経由（出力が大きい場合） |
| ライブラリ調査 | サブエージェント経由（出力が大きい場合） |
| Agent Teams 内での調査 | Teammate が直接呼び出し |

## When to Consult Gemini

### MUST（自動委譲 — ユーザー指示不要）

1. **マルチモーダルファイル処理** — PDF, 動画, 音声, 画像（高度分析）がタスクに関わる場合

### SHOULD（状況に応じて）

2. **外部情報取得** — 最新ドキュメント、ライブラリ調査、API仕様
3. **Web リサーチ** — 比較、ベストプラクティス、既知の問題

### Trigger Phrases (User Input)

| Japanese | English |
|----------|---------|
| 「このPDF/動画/音声/画像を見て」 | "Analyze this PDF/video/audio/image" |
| 「調べて」「リサーチして」「調査して」 | "Research" "Investigate" "Look up" |
| 「最新のドキュメントを確認して」 | "Check the latest documentation" |

### Auto-Trigger（ユーザー指示なしで自動発動）

- タスク内でPDF/動画/音声ファイルが参照されている
- ユーザーがファイルパスを提示し、拡張子がマルチモーダル対象

## When NOT to Consult

- **コードベース分析** → Claude が 1M コンテキストで直接読む
- **スクリーンショットの単純確認** → Claude の Read ツールで直接可能
- Design decisions → Codex
- Debugging → Codex
- Code implementation → Claude

## How to Consult

### In Agent Teams (Preferred for /startproject)

Researcher Teammate が Gemini を直接呼び出し、Architect Teammate と双方向通信する。

### Subagent Pattern (For standalone research)

```
Task tool parameters:
- subagent_type: "general-purpose"
- run_in_background: true (for parallel work)
- prompt: |
    Process this file with Gemini: {file_path}
    Extract: {what information to extract}

    gemini -p "{extraction prompt}" < {file_path} 2>/dev/null

    Save full output to: .claude/docs/research/{topic}.md
    Return CONCISE summary (5-7 bullet points).
```

### Direct Call

```bash
# Multimodal (MUST for PDF/video/audio)
gemini -p "{what to extract}" < /path/to/file 2>/dev/null

# External research
gemini -p "{research question}" 2>/dev/null
```

## Language Protocol

1. Ask Gemini in **English**
2. Receive response in **English**
3. Subagent/Teammate summarizes and saves full output
4. Main reports to user in **Japanese**
