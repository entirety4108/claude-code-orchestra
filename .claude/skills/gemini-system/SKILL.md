---
name: gemini-system
description: |
  Gemini CLI is EXCLUSIVELY for multimodal file reading. MUST use when PDF,
  video, audio, or image files need content extraction — pass the file to
  Gemini with specific extraction instructions. Gemini does NOT do external
  research, library investigation, or codebase analysis.
  Auto-triggers: file extensions .pdf, .mp4, .mov, .mp3, .wav, .m4a.
  External research → use subagent with WebSearch/WebFetch instead.
metadata:
  short-description: Gemini CLI — multimodal file reading only
---

# Gemini System — Multimodal File Reading Only

**Gemini CLI はマルチモーダルファイル読取専用。それ以外には使わない。**

> **詳細ルール**: `.claude/rules/gemini-delegation.md`

## Gemini の唯一の役割

**PDF、動画、音声、画像ファイルの内容抽出。**

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

## Auto-Trigger（自動発動）

マルチモーダルファイルがタスクに登場した時点で、ユーザー指示を待たず自動で Gemini に渡す。

## Gemini を使わないこと

| タスク | 正しい担当 |
|--------|-----------|
| 外部情報取得・リサーチ | **サブエージェント**（WebSearch/WebFetch） |
| ライブラリ調査 | **サブエージェント**（WebSearch/WebFetch） |
| コードベース分析 | **Claude 直接**（1M context） |
| 設計・計画 | **Codex** |
| デバッグ | **Codex** |
| コード実装 | **Claude / サブエージェント** |

## How to Use

### Direct Call

```bash
# PDF
gemini -p "Extract: {what to extract}" < /path/to/file.pdf 2>/dev/null

# Video
gemini -p "Summarize: key concepts, timestamps" < /path/to/video.mp4 2>/dev/null

# Audio
gemini -p "Transcribe and summarize: decisions, action items" < /path/to/audio.mp3 2>/dev/null

# Image (diagrams, charts)
gemini -p "Analyze: components, relationships, data flow" < /path/to/diagram.png 2>/dev/null
```

### Subagent Pattern (出力が大きい場合)

```
Task tool parameters:
- subagent_type: "general-purpose"
- prompt: |
    Process this file with Gemini: {file_path}
    Extract: {what information to extract}

    gemini -p "{extraction prompt}" < {file_path} 2>/dev/null

    Return CONCISE summary (5-7 bullet points).
```

## Language Protocol

1. Ask Gemini in **English**
2. Receive response in **English**
3. Report to user in **Japanese**
