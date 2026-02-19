# Gemini Delegation Rule

**Gemini CLI は読取・分析・リサーチエージェント。1M トークンコンテキストを活用する。**

## Gemini の3つの役割

### 1. マルチモーダルファイル読取（必須・自動委譲）

### 1. コードベース・リポジトリ理解（Codebase Analysis）

- プロジェクト全体の構造分析
- 主要モジュール・責務の把握
- 既存パターン・規約の理解
- 依存関係の分析

> Claude Code のコンテキストは **200K トークン**（実質 140-150K）。
> 大規模コードベースの全体分析は Gemini の **1M context** に委譲する。

### 2. 外部リサーチ・サーベイ（Research & Survey）

- 最新ドキュメント・API仕様の調査
- ライブラリの比較検討・ベストプラクティス
- 技術的なサーベイ・トレンド調査
- 既知の問題・制約の調査

> Gemini CLI は Google Search grounding を内蔵しており、外部情報の取得に最適。

### 3. マルチモーダルファイル読取（Multimodal Reading）

- PDF、動画、音声、画像ファイルの内容抽出
- 図表・ダイアグラムの詳細分析
- 動画の要約・タイムスタンプ抽出
- 音声の文字起こし・要約

## When to Use Gemini

| 状況 | 例 |
|------|------|
| **コードベース分析** | 「プロジェクト全体を理解して」「構造を分析して」 |
| **外部リサーチ** | 「調べて」「リサーチして」「最新のドキュメント」 |
| **ライブラリ調査** | 「ライブラリを比較して」「ベストプラクティスは？」 |
| **マルチモーダル** | PDF/動画/音声/画像ファイルが登場した場合（自動委譲） |

### Trigger Phrases (User Input)

| Japanese | English |
|----------|---------|
| 「コードベースを理解して」「全体構造を見て」 | "Understand the codebase" "Analyze structure" |
| 「調べて」「リサーチして」「サーベイして」 | "Research" "Investigate" "Survey" |
| 「ライブラリを比較」「ベストプラクティス」 | "Compare libraries" "Best practices" |
| 「このPDF/動画/画像を見て」 | "Read this PDF/video/image" |

## When NOT to Use Gemini

- 単純なファイル読み取り（Claude の Read ツールで十分）
- スクリーンショットの単純確認（Claude の Read ツールで直接可能）
- 計画・設計・アーキテクチャ → **Codex** が担当
- デバッグ・エラー解析 → **Codex** が担当
- コード実装 → **Claude / サブエージェント** が担当

## 対象ファイル拡張子（マルチモーダル）

| カテゴリ | 拡張子 |
|----------|--------|
| PDF | `.pdf` |
| 動画 | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` |
| 音声 | `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` |
| 画像（高度な分析） | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg` |

## How to Use

### 2. コードベース分析（1M コンテキスト活用）

Gemini の 1M トークンコンテキストを活かして、大規模なコードベース分析を行う。

- リポジトリ全体のアーキテクチャ分析
- モジュール間のデータフロー追跡
- コード移行の影響範囲評価
- クロスファイル依存関係の分析
- コードベース全体のパターン識別

### 3. 外部リサーチ（Google Search 活用）

Gemini の Google Search 連携を活かして、ドキュメント・ライブラリ・ベストプラクティスを調査する。

- ライブラリ調査・比較
- 最新ドキュメントの参照
- ベストプラクティスの調査
- 既知の問題のトラブルシューティング

| 状況 | 推奨方法 |
|------|----------|
| 短い抽出・回答（〜30行） | 直接呼び出しOK |
| 詳細な分析レポート | サブエージェント経由 |
| リサーチ結果 | サブエージェント経由 → ファイル保存 |

### Subagent Pattern（出力が大きい場合）

```
Task tool parameters:
- subagent_type: "gemini-explore"
- run_in_background: true (for parallel work)
- prompt: |
    {task description}

| タスク | 担当 |
|--------|------|
| 設計・計画 | **Codex** |
| デバッグ（根本原因分析） | **Codex** |
| コード実装 | **Claude / サブエージェント** |
| 単純なファイル編集 | **Claude 直接** |
| Git 操作 | **Claude 直接** |

## When to Consult Gemini

| 状況 | 例 |
|------|------|
| **マルチモーダルファイル** | PDF、動画、音声、画像が登場 |
| **大規模コード分析** | 「リポジトリ全体の構造は？」「データフローを追って」 |
| **ライブラリ調査** | 「このライブラリについて調べて」「比較して」 |
| **ドキュメント参照** | 「最新のドキュメントを確認して」 |
| **移行分析** | 「v2 への移行で影響は？」 |

### Trigger Phrases (User Input)

| Japanese | English |
|----------|---------|
| 「調べて」「リサーチ」「調査して」 | "Research" "Investigate" "Look up" |
| 「ライブラリ」「パッケージ」「比較して」 | "Library" "Package" "Compare" |
| 「ドキュメント」「最新」 | "Documentation" "Latest" |
| 「コードベースを分析」「全体構造」 | "Analyze codebase" "Overall structure" |

## Auto-Trigger（ユーザー指示なしで自動発動）

- タスク内で PDF/動画/音声ファイルが参照されている
- ユーザーがファイルパスを提示し、拡張子がマルチモーダル対象

## How to Consult

### 実行方法

```bash
# マルチモーダルファイル読取
gemini -p "Extract: {what information to extract}" < /path/to/file.pdf 2>/dev/null

# コードベース分析
gemini -p "Analyze: {analysis question}" 2>/dev/null

# 外部リサーチ
gemini -p "Research: {research question}" 2>/dev/null

# ライブラリ調査
gemini -p "Research the library '{name}': features, constraints, best practices" 2>/dev/null
```

### Subagent Pattern (出力が大きい場合)

```
Task tool parameters:
- subagent_type: "gemini-explore"
- prompt: |
    {task description}

    gemini -p "{prompt}" < {file_path if applicable} 2>/dev/null

    Return CONCISE summary (5-7 bullet points).
```

### Direct Call (短い質問の場合)

```bash
gemini -p "{question}" 2>/dev/null
```

## Context Management

| 状況 | 推奨方法 |
|------|----------|
| 短い抽出・質問（〜50行） | 直接呼び出しOK |
| 大規模分析・リサーチ | サブエージェント経由 |
| リサーチ結果の永続化 | サブエージェント → `.claude/docs/research/` に保存 |
| ライブラリ調査 | サブエージェント → `.claude/docs/libraries/` に保存 |

## Language Protocol

1. Ask Gemini in **English**
2. Receive response in **English**
3. Execute based on findings
4. Report to user in **Japanese**
