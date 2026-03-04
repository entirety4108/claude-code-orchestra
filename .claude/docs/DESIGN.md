# Project Design Document

> This document tracks design decisions made during conversations.
> Updated automatically by the `design-tracker` skill.

## Overview

Claude Code Orchestra is a multi-agent collaboration framework. Claude Code (200K context) is the orchestrator, with Codex CLI for planning/design/complex code, Gemini CLI (1M context) for codebase analysis, research, and multimodal reading, and subagents (Opus) for code implementation and Codex delegation.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Claude Code Lead (Opus 4.6 — 200K context)                      │
│  Role: Orchestration, user interaction, task management           │
│                                                                   │
│  ┌──────────────────────┐  ┌──────────────────────┐             │
│  │ Agent Teams (Opus)    │  │ Subagents (Opus)      │             │
│  │ (parallel + comms)    │  │ (isolated + results)  │             │
│  │                       │  │                       │             │
│  │ Researcher ←→ Archit. │  │ Code implementation   │             │
│  │ Implementer A/B/C     │  │ Codex consultation    │             │
│  │ Security/Quality Rev. │  │ Gemini consultation   │             │
│  └──────────────────────┘  └──────────────────────┘             │
│                                                                   │
│  External CLIs:                                                   │
│  ├── Codex CLI (gpt-5.3-codex) — planning, design, complex code  │
│  └── Gemini CLI (1M context) — codebase analysis, research,      │
│       multimodal reading                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Role | Responsibilities |
|-------|------|------------------|
| Claude Code（メイン） | 全体統括 | ユーザー対話、タスク管理、簡潔なコード編集 |
| general-purpose（Opus） | 実装・Codex委譲 | コード実装、Codex委譲、ファイル操作 |
| gemini-explore（Opus） | 大規模分析・調査 | コードベース理解、外部リサーチ、マルチモーダル読取 |
| Codex CLI | 計画・難実装 | アーキテクチャ設計、実装計画、複雑なコード、デバッグ |
| Gemini CLI（1M context） | 分析・調査・読取 | コードベース分析、外部リサーチ、マルチモーダル読取 |

## Implementation Plan

### Patterns & Approaches

| Pattern | Purpose | Notes |
|---------|---------|-------|
| Agent Teams | Parallel work with inter-agent communication | /startproject, /team-implement, /team-review |
| Subagents | Isolated tasks returning results | External research, Codex consultation, implementation |
| Skill Pipeline | `/startproject` → `/team-implement` → `/team-review` | Separation of concerns across skills |

### Libraries & Roles

| Library | Role | Version | Notes |
|---------|------|---------|-------|
| Codex CLI | Planning, design, complex code | gpt-5.3-codex | Architecture, planning, debug, complex implementation |
| Gemini CLI | Multimodal file reading | gemini-3-pro | PDF/video/audio/image extraction ONLY |

### Key Decisions

| Decision | Rationale | Alternatives Considered | Date |
|----------|-----------|------------------------|------|
| Add `gh-issue-close` skill for reproducible issue comments + close workflow | Standardize post-implementation issue closure with reproducible evidence (files, commands, verification, commit info) and reduce manual variance | Close issues with ad-hoc short comments that are hard to reproduce | 2026-03-04 |
| Require escalated execution for all `gh` commands in `gh-issue` skill | `gh` commands depend on network/auth and can fail under sandbox restrictions; making escalation explicit improves reliability and operator consistency | Retry with escalation only after a failure (less predictable and slower) | 2026-03-03 |
| Convert `.codex/prompts/gh-issue-implement.md` into reusable `gh-issue` skill | Reuse the GitHub issue implementation workflow through skill invocation while preserving existing safety constraints | Keep slash-prompt-only usage without a reusable skill | 2026-03-03 |
| Add `gh-issue-implement` slash command in `.codex/prompts` | Standardize issue-driven implementation workflow via GitHub CLI with explicit safety constraints | Ad-hoc issue handling each time without reusable command template | 2026-03-03 |
| Add git-commit-push skill for end-of-task Git delivery | Standardize safe commit/push workflow with branch/upstream checks and non-destructive defaults | Ad-hoc manual Git flow per task (inconsistent and error-prone) | 2026-02-28 |
| Gemini role expanded to codebase analysis + research + multimodal | Gemini CLI has native 1M context; Claude Code is 200K; delegate large-context tasks to Gemini | Keep Claude for codebase analysis (requires 1M Beta) | 2026-02-19 |
| All subagents default to Opus | 200K context makes quality of reasoning more important than context size; Opus provides better output | Sonnet (cheaper but 200K same as Opus, weaker reasoning) | 2026-02-19 |
| Agent Teams default model changed to Opus | Consistent with subagent model selection; better reasoning for parallel tasks | Sonnet (cheaper) | 2026-02-19 |
| Claude Code context corrected to 200K | 1M is Beta/pay-as-you-go only; most users have 200K; design must work for common case | Assume 1M (only works for Tier 4+ users) | 2026-02-19 |
| Subagent delegation threshold lowered to ~20 lines | 200K context requires more aggressive context management | 50 lines (was based on 1M assumption) | 2026-02-19 |
| Codex role unchanged (planning + complex code) | Codex excels at deep reasoning for both design and implementation | Keep Codex advisory-only | 2026-02-17 |
| /startproject split into 3 skills | Separation of Plan/Implement/Review gives user control gates | Single monolithic skill | 2026-02-08 |
| Agent Teams for Research ↔ Design | Bidirectional communication enables iterative refinement | Sequential subagents (old approach) | 2026-02-08 |
| Agent Teams for parallel implementation | Module-based ownership avoids file conflicts | Single-agent sequential implementation | 2026-02-08 |

## TODO

- [ ] Test Agent Teams workflow end-to-end with a real project
- [ ] Update hooks for Agent Teams quality gates
- [ ] Evaluate optimal team size for /team-implement

## Open Questions

- [ ] Optimal team size for /team-implement (2-3 vs 4-5 teammates)?
- [ ] Should /team-review be mandatory or optional?
- [ ] How to handle Compaction in long Agent Teams sessions?

## Changelog

| Date | Changes |
|------|---------|
| 2026-03-04 | Added `gh-issue-close` skill to post reproducible implementation comments and close GitHub issues safely |
| 2026-03-03 | Updated `gh-issue` skill: require escalated execution for all `gh` commands with explicit justification |
| 2026-03-03 | Added `gh-issue` skill under `.codex/skills` based on `.codex/prompts/gh-issue-implement.md` |
| 2026-03-03 | Added `/gh-issue-implement` custom slash command template under `.codex/prompts` |
| 2026-02-28 | Added git-commit-push skill to standardize safe commit/push execution |
| 2026-02-19 | Context-aware redesign: Claude=200K, Gemini=1M (codebase+research+multimodal), all subagents/teams→Opus |
| 2026-02-17 | Role clarification: Gemini → multimodal only, Codex → planning + complex code, Subagents → external research |
| 2026-02-08 | Major redesign for Opus 4.6: 1M context, Agent Teams, skill pipeline |
| | Initial |
