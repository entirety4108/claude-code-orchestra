# claude-code-orchestra

![Claude Code Orchestra](./summary.png)

Multi-Agent AI Development Environment

```
Claude Code (Orchestrator, 200K) ─┬─ Codex CLI (Planning & Complex Code)
                                   ├─ Gemini CLI (1M context: Analysis, Research, Multimodal)
                                   └─ Subagents/Opus (Implementation, Codex Delegation)
```

## Quick Start

既存プロジェクトのルートで実行:

```bash
git clone --depth 1 https://github.com/DeL-TaiseiOzaki/claude-code-orchestra.git .starter && cp -r .starter/.claude .starter/.codex .starter/.gemini .starter/CLAUDE.md . && rm -rf .starter && claude
```

## Prerequisites

### Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude login
```

### Codex CLI

```bash
npm install -g @openai/codex
codex login
```

### Gemini CLI

```bash
npm install -g @google/gemini-cli
gemini login
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           Claude Code (Orchestrator — 200K context)          │
│           → コンテキスト節約が最優先                         │
│           → ユーザー対話・調整・簡潔な編集を担当             │
│                      ↓                                      │
│  ┌──────────────────────┐  ┌──────────────────────────┐    │
│  │  Subagent (Opus)      │  │  gemini-explore (Opus)    │    │
│  │  general-purpose      │  │  → Gemini CLI 1M context  │    │
│  │  → コード実装         │  │  → コードベース分析       │    │
│  │  → Codex委譲          │  │  → 外部リサーチ           │    │
│  │                       │  │  → マルチモーダル読取     │    │
│  │  ┌──────────────┐    │  │                            │    │
│  │  │  Codex CLI   │    │  │  ┌──────────────┐          │    │
│  │  │  設計・推論  │    │  │  │  Gemini CLI  │          │    │
│  │  │  デバッグ    │    │  │  │  1M context  │          │    │
│  │  └──────────────┘    │  │  └──────────────┘          │    │
│  └──────────────────────┘  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### コンテキスト管理（重要）

メインオーケストレーター（200K context）を節約するため、大規模タスクは適切なエージェントに委譲します。

| 状況 | 推奨方法 |
|------|----------|
| コードベース全体分析 | **Gemini 経由**（1M context） |
| 外部リサーチ・サーベイ | **Gemini 経由**（Google Search grounding） |
| マルチモーダルファイル | **Gemini 経由** |
| コード実装 | サブエージェント（Opus）経由 |
| 設計・計画相談 | サブエージェント → Codex |
| 短い質問・短い回答 | 直接呼び出しOK |
| 詳細な分析が必要 | サブエージェント経由 → ファイル保存 |

## Directory Structure

```
.
├── CLAUDE.md                    # メインシステムドキュメント
├── README.md
├── pyproject.toml               # Python プロジェクト設定
├── uv.lock                      # 依存関係ロックファイル
│
├── .claude/
│   ├── agents/
│   │   ├── general-purpose.md   # 実装・Codex委譲エージェント (Opus)
│   │   ├── codex-debugger.md    # エラー分析エージェント (Opus)
│   │   └── gemini-explore.md    # 大規模分析・調査エージェント (Opus)
│   │
│   ├── skills/                  # 再利用可能なワークフロー
│   │   ├── startproject/        # プロジェクト開始
│   │   ├── plan/                # 実装計画作成
│   │   ├── tdd/                 # テスト駆動開発
│   │   ├── checkpointing/       # セッション永続化
│   │   ├── codex-system/        # Codex CLI連携
│   │   ├── gemini-system/       # Gemini CLI連携
│   │   └── ...
│   │
│   ├── hooks/                   # 自動化フック
│   │   ├── agent-router.py      # エージェントルーティング
│   │   ├── lint-on-save.py      # 保存時自動lint
│   │   └── ...
│   │
│   ├── rules/                   # 開発ガイドライン
│   │   ├── coding-principles.md
│   │   ├── testing.md
│   │   └── ...
│   │
│   ├── docs/
│   │   ├── DESIGN.md            # 設計決定記録
│   │   ├── research/            # 調査結果（Gemini/サブエージェント）
│   │   └── libraries/           # ライブラリ制約
│   │
│   └── logs/
│       └── cli-tools.jsonl      # Codex/Gemini入出力ログ
│
├── .codex/                      # Codex CLI設定
│   ├── AGENTS.md
│   └── config.toml
│
└── .gemini/                     # Gemini CLI設定
    ├── GEMINI.md
    └── settings.json
```

## Skills

### `/startproject` — プロジェクト開始

マルチエージェント協調でプロジェクトを開始します。

```
/startproject ユーザー認証機能
```

**ワークフロー:**
1. **Gemini** → コードベース分析・事前調査（1M context）
2. **Claude** → ユーザーと要件ヒアリング
3. **Agent Teams** → Researcher（Gemini）↔ Architect（Codex）で並列調査・設計
4. **Claude** → 計画統合・ユーザー承認

### `/plan` — 実装計画

要件を具体的なステップに分解します。

```
/plan APIエンドポイントの追加
```

**出力:**
- 実装ステップ（ファイル・変更内容・検証方法）
- 依存関係・リスク
- 検証基準

### `/tdd` — テスト駆動開発

Red-Green-Refactorサイクルで実装します。

```
/tdd ユーザー登録機能
```

**ワークフロー:**
1. テストケース設計
2. 失敗するテスト作成（Red）
3. 最小限の実装（Green）
4. リファクタリング（Refactor）

### `/checkpointing` — セッション永続化

セッションの状態を保存します。

```bash
/checkpointing              # 基本: 履歴ログ
/checkpointing --full       # 完全: git履歴・ファイル変更含む
/checkpointing --analyze    # 分析: 再利用可能なスキルパターン発見
```

### `/codex-system` — Codex CLI連携

設計判断・デバッグ・トレードオフ分析に使用します。

**トリガー例:**
- 「どう設計すべき？」「どう実装する？」
- 「なぜ動かない？」「エラーが出る」
- 「どちらがいい？」「比較して」

### `/gemini-system` — Gemini CLI連携

Gemini の 1M context を活用した大規模分析・リサーチ・マルチモーダル処理。

**トリガー例:**
- 「コードベースを理解して」「全体構造を分析して」
- 「調べて」「リサーチして」「サーベイして」
- 「このPDF/動画を見て」

### `/simplify` — コードリファクタリング

コードを簡潔化・可読性向上させます。

### `/design-tracker` — 設計決定追跡

アーキテクチャ・実装決定を自動記録します。

## Development

### Tech Stack

| ツール | 用途 |
|--------|------|
| **uv** | パッケージ管理（pip禁止） |
| **ruff** | リント・フォーマット |
| **ty** | 型チェック |
| **pytest** | テスト |
| **poethepoet** | タスクランナー |

### Commands

```bash
# 依存関係
uv add <package>           # パッケージ追加
uv add --dev <package>     # 開発依存追加
uv sync                    # 依存関係同期

# 品質チェック
poe lint                   # ruff check + format
poe typecheck              # ty
poe test                   # pytest
poe all                    # 全チェック実行

# 直接実行
uv run pytest -v
uv run ruff check .
```

## Hooks

自動化フックにより、適切なタイミングでエージェント連携を提案します。

| フック | トリガー | 動作 |
|--------|----------|------|
| `agent-router.py` | ユーザー入力 | Codex/Geminiへのルーティング提案 |
| `lint-on-save.py` | ファイル保存 | 自動lint実行 |
| `check-codex-before-write.py` | ファイル書き込み前 | Codex相談提案 |
| `log-cli-tools.py` | Codex/Gemini実行 | 入出力ログ記録 |

## Language Rules

- **コード・思考・推論**: 英語
- **ユーザーへの応答**: 日本語
- **技術ドキュメント**: 英語
- **README等**: 日本語可
