# Claude Code Orchestra

**マルチエージェント協調フレームワーク（Opus 4.6 + Agent Teams 対応）**

Claude Code が全体統括し、Codex CLI（計画・難実装）と Gemini CLI（マルチモーダル読取）を使い分ける。

---

## Agent Roles — 役割分担

| Agent | Model | Role | Use For |
|-------|-------|------|---------|
| **Claude Code（メイン）** | Opus 4.6 | 全体統括 | ユーザー対話、コードベース分析（1M context）、タスク管理 |
| **general-purpose（サブエージェント）** | **Sonnet**（1M context） | 調査・実装の実行部隊 | 外部情報取得、調査整理、コード実装、Codex委譲 |
| **codex-debugger（サブエージェント）** | **Opus** | エラー解析 | Codex CLI でエラーの根本原因分析・修正提案 |
| **gemini-explore（サブエージェント）** | **Opus** | マルチモーダル読取 | PDF・動画・音声・画像 → Gemini CLI で内容抽出 |
| **Agent Teams チームメイト** | **Sonnet**（デフォルト） | 並列協調 | /startproject, /team-implement, /team-review |
| **Codex CLI** | gpt-5.3-codex | 計画・難しい実装 | アーキテクチャ設計、実装計画、複雑なコード実装 |
| **Gemini CLI** | gemini-3-pro | マルチモーダル読取専用 | ファイルの内容抽出のみ |

### 判断フロー

```
タスク受信
  ├── マルチモーダルファイル（PDF/動画/音声/画像）がある？
  │     → YES: Gemini にファイルを渡して内容抽出
  │
  ├── 計画・設計・難しいコードが必要？
  │     → YES: Codex に相談 or 実装させる
  │
  ├── 外部情報・リサーチが必要？
  │     → YES: サブエージェント（WebSearch/WebFetch）
  │
  └── 通常のコード実装？
        → メインが直接 or サブエージェントに委託
```

---

## Quick Reference

### Codex を使う時

- **計画・設計**（「どう実装？」「アーキテクチャ」「計画を立てて」）
- **難しいコード実装**（複雑なアルゴリズム、最適化、マルチステップ実装）
- **デバッグ**（「なぜ動かない？」「エラーの原因は？」）
- **比較検討**（「AとBどちらがいい？」「トレードオフは？」）

→ 詳細: `.claude/rules/codex-delegation.md`

### Gemini を使う時

- **マルチモーダルファイルの読取のみ（必須・自動委譲）**
  - PDF、動画、音声、画像ファイルが登場したら、ユーザー指示を待たず自動で Gemini に渡す
  ```bash
  gemini -p "{抽出したい情報}" < /path/to/file 2>/dev/null
  ```

> **Gemini は外部リサーチには使わない**。外部情報の取得はサブエージェントが WebSearch/WebFetch で行う。
> スクリーンショットの単純確認は Claude の Read ツールで直接可能。

→ 詳細: `.claude/rules/gemini-delegation.md`

### サブエージェントを使う時

- **外部情報取得**（最新ドキュメント、ライブラリ調査）→ WebSearch/WebFetch
- **調査結果の整理** → `.claude/docs/research/` に保存
- **コード実装**（メインのコンテキストを節約したい場合）

---

## Context Management

Claude Code (Opus 4.6) のコンテキストは **1M トークン**（実質 **350-500k**、ツール定義等で縮小）。

**Compaction 機能**により、長時間セッションでもサーバーサイドで自動要約される。

### モデル選択方針

| エージェント | モデル | 理由 |
|------------|--------|------|
| general-purpose | **Sonnet** | 1M context で大量のコード・調査結果を処理。/startproject の Researcher/Architect にも最適 |
| codex-debugger | **Opus** | エラー解析には高い推論能力が必要。Codex への的確な質問生成に強い |
| gemini-explore | **Opus** | マルチモーダル内容の正確な解釈・要約に高い推論能力が必要 |
| Agent Teams | **Sonnet**（デフォルト） | `CLAUDE_CODE_SUBAGENT_MODEL` で設定。1M context で並列作業に対応 |

### 呼び出し基準

| 出力サイズ | 方法 | 理由 |
|-----------|------|------|
| 短い（〜50行） | 直接呼び出しOK | 1Mコンテキストで十分吸収可能 |
| 大きい（50行以上） | サブエージェント経由を推奨 | コンテキスト効率化 |
| 分析レポート | サブエージェント → ファイル保存 | 詳細は `.claude/docs/` に永続化 |

### 並列処理の選択

| 目的 | 方法 | 適用場面 |
|------|------|----------|
| 結果を取得するだけ | サブエージェント | Codex相談、調査、実装 |
| 相互通信が必要 | **Agent Teams** | 並列実装、並列レビュー |

---

## Workflow

```
/startproject <機能名>     Phase 1-3: 理解 → 調査&設計 → 計画
    ↓ 承認後
/team-implement            Phase 4: Agent Teams で並列実装
    ↓ 完了後
/team-review               Phase 5: Agent Teams で並列レビュー
```

1. Claude がコードベースを直接読み（1Mコンテキスト）、ユーザーと要件ヒアリング
2. サブエージェントで外部調査 + Codex で設計・計画（並列可）
3. Claude が調査と設計を統合し、計画をユーザーに提示
4. 承認後、`/team-implement` で並列実装
5. `/team-review` で並列レビュー

→ 詳細: `/startproject`, `/team-implement`, `/team-review` skills

---

## Tech Stack

- **Python** / **uv** (pip禁止)
- **ruff** (lint/format) / **ty** (type check) / **pytest**
- `poe lint` / `poe test` / `poe all`

→ 詳細: `.claude/rules/dev-environment.md`

---

## Documentation

| Location | Content |
|----------|---------|
| `.claude/rules/` | コーディング・セキュリティ・言語ルール |
| `.claude/docs/DESIGN.md` | 設計決定の記録 |
| `.claude/docs/research/` | 調査結果（サブエージェント / レビュー） |
| `.claude/docs/libraries/` | ライブラリ制約ドキュメント |
| `.claude/logs/cli-tools.jsonl` | Codex/Gemini入出力ログ |

---

## Language Protocol

- **思考・コード**: 英語
- **ユーザー対話**: 日本語
