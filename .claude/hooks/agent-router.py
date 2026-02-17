#!/usr/bin/env python3
"""
UserPromptSubmit hook: Route to appropriate agent based on user intent.

Analyzes user prompts and suggests the most appropriate agent
(Codex for design/debug, Gemini for research/multimodal).

Multimodal file detection is highest priority — when PDF, video, audio,
or image files are referenced, Gemini is ALWAYS suggested.
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

# Triggers for Codex (design, debugging, deep reasoning)
CODEX_TRIGGERS = {
    "ja": [
        "設計", "どう設計", "アーキテクチャ",
        "なぜ動かない", "エラー", "バグ", "デバッグ",
        "どちらがいい", "比較して", "トレードオフ",
        "実装方法", "どう実装",
        "リファクタリング", "リファクタ",
        "レビュー", "見て",
        "考えて", "分析して", "深く",
    ],
    "en": [
        "design", "architecture", "architect",
        "debug", "error", "bug", "not working", "fails",
        "compare", "trade-off", "tradeoff", "which is better",
        "how to implement", "implementation",
        "refactor", "simplify",
        "review", "check this",
        "think", "analyze", "deeply",
    ],
}

# Triggers for Gemini (research, multimodal, large context)
GEMINI_TRIGGERS = {
    "ja": [
        "調べて", "リサーチ", "調査",
        "PDF", "動画", "音声", "画像",
        "コードベース全体", "リポジトリ全体",
        "最新", "ドキュメント",
        "ライブラリ", "パッケージ",
    ],
    "en": [
        "research", "investigate", "look up", "find out",
        "pdf", "video", "audio", "image",
        "entire codebase", "whole repository",
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

    # HIGHEST PRIORITY: Multimodal file detection
    multimodal_file = detect_multimodal_files(prompt)
    if multimodal_file:
        return "gemini-multimodal", multimodal_file, True

    # Check Codex triggers
    for triggers in CODEX_TRIGGERS.values():
        for trigger in triggers:
            if trigger in prompt_lower:
                return "codex", trigger, False

    # Check Gemini triggers
    for triggers in GEMINI_TRIGGERS.values():
        for trigger in triggers:
            if trigger in prompt_lower:
                return "gemini", trigger, False

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
                        f"[Agent Routing] Detected '{trigger}' - this task may benefit from "
                        "Codex CLI's deep reasoning capabilities. Consider: "
                        "`codex exec --model gpt-5.3-codex --sandbox read-only --full-auto "
                        '"{task description}"` for design decisions, debugging, or complex analysis.'
                    )
                }
            }
            print(json.dumps(output))

        elif agent == "gemini":
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Agent Routing] Detected '{trigger}' - this task may benefit from "
                        "Gemini CLI's research capabilities. Consider: "
                        '`gemini -p "Research: {topic}" 2>/dev/null` '
                        "for documentation, library research, or multimodal content."
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
