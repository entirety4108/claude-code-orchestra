#!/usr/bin/env python
"""
PreToolUse hook: Redirect WebSearch to Gemini CLI, suggest Gemini for WebFetch research.

WebSearch → ALWAYS redirect to Gemini CLI (Google Search grounding is built-in).
WebFetch  → Suggest Gemini for research-heavy fetches.
"""

import json
import sys

# Keywords that suggest WebFetch would benefit from Gemini
WEBFETCH_RESEARCH_INDICATORS = [
    "documentation",
    "best practice",
    "comparison",
    "library",
    "framework",
    "tutorial",
    "guide",
    "example",
    "pattern",
    "architecture",
    "migration",
    "upgrade",
    "breaking change",
    "api reference",
    "specification",
]

# WebFetch lookups that don't need Gemini
WEBFETCH_SIMPLE_PATTERNS = [
    "error message",
    "stack trace",
    "release notes",
    "changelog",
]


def should_suggest_gemini_for_fetch(url: str, prompt: str) -> tuple[bool, str]:
    """Determine if Gemini should be suggested for a WebFetch."""
    combined = f"{url.lower()} {prompt.lower()}"

    for pattern in WEBFETCH_SIMPLE_PATTERNS:
        if pattern in combined:
            return False, ""

    for indicator in WEBFETCH_RESEARCH_INDICATORS:
        if indicator in combined:
            return True, f"Fetch involves '{indicator}'"

    if len(prompt) > 80:
        return True, "Complex fetch prompt detected"

    return False, ""


def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if tool_name == "WebSearch":
            # Always redirect WebSearch to Gemini CLI
            query = tool_input.get("query", "")
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": (
                        "[Gemini Required] Do NOT use WebSearch. "
                        "Use Gemini CLI instead — it has Google Search grounding built-in "
                        "and 1M context to synthesize results. "
                        f'Run: `gemini -p "Search and summarize: {query}" 2>/dev/null` '
                        "Or delegate to gemini-explore subagent: "
                        "Task(subagent_type='gemini-explore', "
                        f"prompt='Research: {query}. Save findings to .claude/docs/research/')"
                    ),
                }
            }
            print(json.dumps(output))

        elif tool_name == "WebFetch":
            url = tool_input.get("url", "")
            prompt = tool_input.get("prompt", "")
            should_suggest, reason = should_suggest_gemini_for_fetch(url, prompt)

            if should_suggest:
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "additionalContext": (
                            f"[Gemini Research Suggestion] {reason}. "
                            "Consider using Gemini CLI (1M context + Google Search grounding): "
                            f'`gemini -p "{prompt}" 2>/dev/null` '
                            "or delegate to gemini-explore subagent to preserve main context. "
                            "Save results to .claude/docs/research/."
                        ),
                    }
                }
                print(json.dumps(output))

        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
