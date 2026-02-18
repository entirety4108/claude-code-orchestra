#!/usr/bin/env python3
"""
UserPromptSubmit hook: Route to appropriate agent based on user intent.

Routing rules:
- Multimodal files (PDF/video/audio/image) → Gemini CLI (HIGHEST PRIORITY)
- Planning, design, complex code → Codex CLI
- External research → Subagent with WebSearch/WebFetch
"""

import json
import re
import sys

# Multimodal file extensions that MUST be processed by Gemini
MULTIMODAL_EXTENSIONS = [
    # PDF
    ".pdf",
    # Video
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    # Audio
    ".mp3", ".wav", ".m4a", ".flac", ".ogg",
    # Image (for detailed analysis — screenshots can be read by Claude directly)
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
]

# Pattern to detect file paths with multimodal extensions
MULTIMODAL_PATTERN = re.compile(
    r'[\w./\\~-]+\.(?:' +
    '|'.join(ext.lstrip('.') for ext in MULTIMODAL_EXTENSIONS) +
    r')(?:\s|$|["\']|,)',
    re.IGNORECASE,
)

# Triggers for Codex (planning, design, debugging, complex implementation)
CODEX_TRIGGERS = {
    "ja": [
        "設計", "どう設計", "アーキテクチャ",
        "計画", "計画を立てて",
        "なぜ動かない", "エラー", "バグ", "デバッグ",
        "どちらがいい", "比較して", "トレードオフ",
        "実装方法", "どう実装",
        "リファクタリング", "リファクタ",
        "レビュー",
        "考えて", "分析して", "深く",
        "最適化",
    ],
    "en": [
        "design", "architecture", "architect",
        "plan", "planning",
        "debug", "error", "bug", "not working", "fails",
        "compare", "trade-off", "tradeoff", "which is better",
        "how to implement", "implementation", "complex",
        "refactor", "simplify",
        "review", "check this",
        "think", "analyze", "deeply",
        "optimize", "performance",
    ],
}

# Triggers for external research (handled by subagent, NOT Gemini)
RESEARCH_TRIGGERS = {
    "ja": [
        "調べて", "リサーチ", "調査",
        "最新", "ドキュメント",
        "ライブラリ", "パッケージ",
    ],
    "en": [
        "research", "investigate", "look up", "find out",
        "latest", "documentation", "docs",
        "library", "package", "framework",
    ],
}


def detect_multimodal_files(prompt: str) -> str | None:
    """Detect multimodal file references in the prompt. Returns matched file path or None."""
    match = MULTIMODAL_PATTERN.search(prompt)
    if match:
        return match.group(0).strip().rstrip('"\',')
    return None


def detect_agent(prompt: str) -> tuple[str | None, str, bool]:
    """Detect which agent should handle this prompt.

    Returns (agent, trigger, is_multimodal).
    """
    prompt_lower = prompt.lower()

    # HIGHEST PRIORITY: Multimodal file detection → Gemini
    multimodal_file = detect_multimodal_files(prompt)
    if multimodal_file:
        return "gemini-multimodal", multimodal_file, True

    # Codex triggers (planning, design, debug, complex code)
    for triggers in CODEX_TRIGGERS.values():
        for trigger in triggers:
            if trigger in prompt_lower:
                return "codex", trigger, False

    # Research triggers → subagent (NOT Gemini)
    for triggers in RESEARCH_TRIGGERS.values():
        for trigger in triggers:
            if trigger in prompt_lower:
                return "research-subagent", trigger, False

    return None, "", False


def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        # Skip short prompts
        if len(prompt) < 10:
            sys.exit(0)

        agent, trigger, is_multimodal = detect_agent(prompt)

        if is_multimodal:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Multimodal File Detected] Found '{trigger}' in prompt. "
                        "**MUST** use Gemini CLI to process this file. "
                        "Pass the file to Gemini with specific extraction instructions: "
                        f'`gemini -p "Extract: {{what to extract}}" < {trigger} 2>/dev/null` '
                        "Do NOT attempt to read this file directly — use Gemini for content extraction."
                    )
                }
            }
            print(json.dumps(output))

        elif agent == "codex":
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Agent Routing] Detected '{trigger}' — this task may benefit from "
                        "Codex CLI for planning, design, or complex implementation. Consider: "
                        "`codex exec --model gpt-5.3-codex --sandbox read-only --full-auto "
                        '"{task description}"` for design decisions, planning, debugging, '
                        "or complex analysis."
                    )
                }
            }
            print(json.dumps(output))

        elif agent == "research-subagent":
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Research Detected] Detected '{trigger}' — use a subagent "
                        "(Task tool with subagent_type='general-purpose') with "
                        "WebSearch/WebFetch for external research. "
                        "Do NOT use Gemini for research — Gemini is multimodal file reading only. "
                        "Save results to .claude/docs/research/."
                    )
                }
            }
            print(json.dumps(output))

        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
