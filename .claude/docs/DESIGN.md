# Project Design Document

> This document tracks design decisions made during conversations.
> Updated automatically by the `design-tracker` skill.

## Overview

Claude Code Orchestra is a multi-agent collaboration framework. Claude Code (1M context) is the orchestrator, with Codex CLI for planning/design/complex code, Gemini CLI for reading/analysis/research (leveraging 1M context + Google Search + multimodal), and subagents for routine implementation.

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
│  └── Gemini CLI — reading, analysis & research (1M context)        │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Role | Responsibilities |
|-------|------|------------------|
| Claude Code（メイン） | 全体統括 | ユーザー対話、タスク管理、簡潔なコード編集 |
| general-purpose（Opus） | 実装・Codex委譲 | コード実装、Codex委譲、ファイル操作 |
| gemini-explore（Opus） | 大規模分析・調査 | コードベース理解、外部リサーチ、マルチモーダル読取 |
| Codex CLI | 計画・難実装 | アーキテクチャ設計、実装計画、複雑なコード、デバッグ |
| Gemini CLI | 読取・分析・リサーチ | マルチモーダル読取、コードベース分析（1M context）、外部リサーチ（Google Search） |

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
| Gemini CLI | Reading, analysis & research | gemini-3-pro-preview | Multimodal reading, codebase analysis (1M context), external research (Google Search) |

### Key Decisions

| Decision | Rationale | Alternatives Considered | Date |
|----------|-----------|------------------------|------|
| Claude handles codebase analysis directly | Opus 4.6 has 1M context, no need to delegate | Keep Gemini for codebase analysis | 2026-02-08 |
| Gemini role narrowed to multimodal ONLY | External research done better by WebSearch/WebFetch in subagents; Gemini's unique value is file reading | Keep Gemini for research | 2026-02-17 |
| Gemini role expanded to reading + analysis + research | Gemini's 1M context is ideal for large codebase analysis; Google Search integration enables research; multimodal remains core | Keep multimodal only | 2026-02-19 |
| Codex role expanded to planning + complex code | Codex excels at deep reasoning for both design and implementation | Keep Codex advisory-only | 2026-02-17 |
| Subagents handle external research | WebSearch/WebFetch tools are available to subagents; no need for Gemini CLI | Use Gemini for research | 2026-02-17 |
| Gemini handles research via Google Search | Gemini's native Google Search integration is more comprehensive; subagents still useful for quick lookups | Keep subagents only for research | 2026-02-19 |
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
| 2026-02-19 | Gemini role expanded: multimodal + codebase analysis (1M context) + external research (Google Search). Model name standardized to gemini-3-pro-preview |
| 2026-02-17 | Role clarification: Gemini → multimodal only, Codex → planning + complex code, Subagents → external research |
| 2026-02-08 | Major redesign for Opus 4.6: 1M context, Agent Teams, skill pipeline |
| | Initial |
