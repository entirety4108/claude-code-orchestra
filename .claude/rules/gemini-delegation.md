# Gemini Delegation Rule

**Gemini CLI はマルチモーダルファイル読取専用ツール。それ以外には使わない。**

## Gemini の唯一の役割: マルチモーダルファイル読取

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

---

## Gemini を使わないこと

以下は Gemini ではなく、適切なエージェントが担当する:

| タスク | 担当 |
|--------|------|
| 外部情報取得・リサーチ | **サブエージェント**（WebSearch/WebFetch） |
| ライブラリ調査 | **サブエージェント**（WebSearch/WebFetch） |
| コードベース分析 | **Claude 直接**（1M context） |
| 設計・計画 | **Codex** |
| デバッグ | **Codex** |
| コード実装 | **Claude / サブエージェント** |

## Auto-Trigger（ユーザー指示なしで自動発動）

- タスク内で PDF/動画/音声ファイルが参照されている
- ユーザーがファイルパスを提示し、拡張子がマルチモーダル対象

## How to Consult

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

### Direct Call (短い抽出の場合)

```bash
gemini -p "{what to extract}" < /path/to/file 2>/dev/null
```

## Language Protocol

1. Ask Gemini in **English**
2. Receive response in **English**
3. Report to user in **Japanese**
